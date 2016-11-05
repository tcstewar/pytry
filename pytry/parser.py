import argparse


def str2bool(text):
    if text.lower() in ("yes", "true", "t", "1"):
        return True
    elif text.lower() in ("no", "false", "f", "0"):
        return False
    else:
        raise ValueError("invalid boolean value: '%s'" % text)


def parse_args(trial, args, allow_filename=False):
    parser = argparse.ArgumentParser(
        description='pytry: Run Trials with parameters')

    if allow_filename:
        parser.add_argument('filename', metavar='FILE', type=str, nargs=1,
                            help='.py file containing Trial object')

    keys = list(trial.param_defaults.keys())

    for k in sorted(keys, key=lambda x: (x in trial.system_params, x)):
        v = trial.param_defaults[k]
        desc = '%s (default=%r)' % (trial.param_descriptions[k], v)

        if v is False:
            parser.add_argument('--%s' % k, default=v,
                                action='store_true',
                                help=desc)
        elif v is True:
            parser.add_argument('--%s' % k, default=v,
                                metavar='<X>',
                                type=str2bool,
                                action='store',
                                help=desc)
        else:
            parser.add_argument('--%s' % k, type=type(v), default=v,
                                metavar='<X>', action='store',
                                help=desc)

    args = parser.parse_args(args)
    params = vars(args)
    if allow_filename:
        del params['filename']
    return params
