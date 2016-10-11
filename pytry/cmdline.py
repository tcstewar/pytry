import argparse
import sys

import pytry


def run():
    parser = argparse.ArgumentParser(
        description='pytry: Run Trials with parameters')
    parser.add_argument('filename', metavar='FILE', type=str, nargs=1,
                        help='.py file containing Trial object')

    if len(sys.argv) < 2:
        parser.parse_args()   # this will fail with an error message
    filename = sys.argv[1]

    with open(filename) as f:
        code = f.read()
    objs = dict()
    compiled = compile(code, filename, 'exec')
    exec(compiled, objs)

    trials = []
    for x in objs.values():
        if isinstance(x, type):
            if issubclass(x, pytry.Trial):
                trials.append(x)

    if len(trials) == 0:
        print 'Error: no pytry.Trial class found in %s' % filename
    elif len(trials) > 1:
        print 'Error: more than one pytry.Trial class found'
    else:
        trial = trials[0]()
        run_trial(trial, parser)


def str2bool(text):
    return text.lower() in ("yes", "true", "t", "1")


def run_trial(trial, parser):
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

    args = parser.parse_args()
    params = vars(args)
    del params['filename']

    trial.run(**params)
