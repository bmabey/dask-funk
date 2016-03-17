from toolz import curry, identity


# TODO: look into why pytest is not running this docstring after decoration (__doc__ is present!)
@curry
def select_keys(d, keys):
    """

    >>> d = {'foo': 52, 'bar': 12, 'baz': 98}
    >>> select_keys(d, ['foo'])
    {'foo': 52}
    """
    return {k:d[k] for k in keys}

@curry
def split_keys_by_val(f, d):
    pos = set()
    neg = set()
    for k, v in d.items():
        if f(v):
            pos.add(k)
        else:
            neg.add(k)
    return pos, neg

@curry
def map_dict(val_fn, seq, key_fn=identity):
    return {key_fn(v):val_fn(v) for v in seq}
