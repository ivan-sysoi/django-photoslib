import xxhash

__all__ = ('get_hash',)


def get_hash(input):
    h = xxhash.xxh32()
    h.update(input)
    return h.hexdigest()
