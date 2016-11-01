import os


def read(path):
    data = []
    if os.path.exists(path):
        for fn in os.listdir(path):
            fn = os.path.join(path, fn)
            try:
                if fn.endswith('.txt'):
                    data.append(text(fn))
                elif fn.endswith('.npz'):
                    data.append(npz(fn))
            except:
                print('Error reading file "%s"' % fn)
    return data


def text(fn):
    with open(fn) as f:
        text = f.read()
    d = {}
    try:
        import numpy
        d['array'] = numpy.array
        d['nan'] = numpy.nan
    except ImportError:
        numpy = None
    exec(text, d)
    del d['__builtins__']
    if numpy is not None:
        if d['array'] is numpy.array:
            del d['array']
    return d


def npz(fn):
    import numpy as np
    d = {}
    f = np.load(fn)
    for k in f.files:
        d[k] = f[k]
    return d
