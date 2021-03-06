# Generated by Django 2.1.4 on 2018-12-19 18:42

from django.db import migrations, models
import photoslib.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('file', models.ImageField(unique=True, upload_to=photoslib.models.get_photo_upload_to, verbose_name='File')),
                ('hash', models.CharField(max_length=32, unique=True, verbose_name='Hash')),
                ('ref_count', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Count of references')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
                'ordering': ('-created',),
            },
            bases=(models.Model,),
        ),
    ]
