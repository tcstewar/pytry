import os


def write(trial, fn, p, result):
    if p.data_format == 'txt':
        text(trial, fn, p, result)
    elif p.data_format == 'npz':
        npz(trial, fn, p, result)
    else:
        raise AttributeError('Unknown data_format "%s"' % p.data_format)


def param_items(trial, p):
    for k in trial.param_defaults.keys():
        if k not in trial.system_params:
            yield k, getattr(p, k)


def text(trial, fn, p, result):
    with open(fn + '.txt', 'w') as f:
        for k, v in param_items(trial, p):
            f.write('%s = %r\n' % (k, v))
        f.write('\n')
        for k, v in result.items():
            f.write('%s = %r\n' % (k, v))


def npz(trial, fn, p, result):
    import numpy as np

    data = dict(param_items(trial, p))
    data.update(result)
    np.savez(fn + '.npz', **data)
