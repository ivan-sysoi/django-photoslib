import datetime
import os
import time

from django.conf import settings
from django.core.management import BaseCommand
from django.db import connection
from django.db.models import ForeignKey
from django.db.transaction import atomic
from django.utils import timezone

from photoslib.fields import PhotoField, ManyPhotosField, SortableManyPhotosField
from photoslib.models import Photo
from photoslib.utils import get_photo_relations


def update_photos_refcount(model_column_list):
    photo_rel_sql = []
    for model_cls, field in model_column_list:
        if isinstance(field, PhotoField):
            col = field.column
            table = model_cls._meta.db_table
        elif isinstance(field, (ManyPhotosField, SortableManyPhotosField)):
            col = tuple(filter(lambda f: isinstance(f, ForeignKey) and f.target_field.model == Photo,
                               field.remote_field.through._meta.get_fields()))
            assert len(col) == 1
            col = col[0].column
            table = field.remote_field.through._meta.db_table

        photo_rel_sql.append("SELECT {col} as photo_id FROM {table}".format(col=col, table=table))

    select_ref_count_sql = """
        SELECT {photos_table}.id as photo_id, COALESCE(ct.photo_count, 0) AS photo_count
        FROM {photos_table}
        LEFT JOIN (
            SELECT photo_id, count(*) AS photo_count
            FROM (
                {photo_rel_sql}
            ) p_rel
            GROUP  BY 1
        ) ct on {photos_table}.id = ct.photo_id
    """.format(
        photos_table=Photo._meta.db_table,
        photo_rel_sql=' UNION ALL '.join(photo_rel_sql)
    )

    update_sql = """
        UPDATE {table} SET (ref_count) = (
            SELECT photo_count from (
                {select_ref_count_sql}
            ) q where {table}.id = q.photo_id
        )            
    """.format(
        table=Photo._meta.db_table,
        select_ref_count_sql=select_ref_count_sql
    )

    with connection.cursor() as cursor:
        cursor.execute(update_sql)


def get_photo_files(photo):
    files = [photo.file.path]
    for size in settings.PHOTOSLIB_PHOTO_SIZES.keys():
        files.append(getattr(photo, size).path)
    return files


class RollbackException(Exception):
    pass


class Command(BaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--dry-run", action="store_true", default=False)

    def handle(self, *args, **options):
        start_time = time.time()

        verbose = options['verbosity'] > 0
        dry_run = options['dry_run']

        models_with_photos = get_photo_relations()

        if verbose:
            self.stdout.write('Found relations:')
            for model_cls, field in models_with_photos:
                self.stdout.write('* {}: {}'.format(model_cls._meta.db_table, field.name))
        try:
            with atomic():
                update_photos_refcount(models_with_photos)

                total_deleted = 0
                old_photos_qs = Photo.objects.filter(
                    ref_count=0,
                    created__lte=timezone.now() - settings.PHOTOSLIB_UNBOUND_PHOTO_LIFETIME
                )
                for photo in old_photos_qs:
                    if verbose:
                        self.stdout.write('Delete photo #{}'.format(photo.id))

                    for file_path in get_photo_files(photo):
                        if os.path.exists(file_path):
                            if not dry_run:
                                os.remove(file_path)
                            if verbose:
                                self.stdout.write('* deleted: {}'.format(file_path))

                    photo.delete()
                    total_deleted += 1

                if verbose:
                    self.stdout.write('Total deleted: {}'.format(total_deleted))

                if dry_run:
                    raise RollbackException

        except RollbackException:
            pass

        if verbose:
            self.stdout.write('Executed in {} sec'.format(time.time() - start_time))
