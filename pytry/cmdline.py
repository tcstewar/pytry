import argparse
import sys

from . import parser
from . import trial


def get_trial_class(filename):
    with open(filename) as f:
        code = f.read()
    objs = dict(__file__=filename, __name__='__pytry__')
    compiled = compile(code, filename, 'exec')
    exec(compiled, objs)

    trials = []
    for x in objs.values():
        if isinstance(x, type):
            if issubclass(x, trial.Trial):
                trials.append(x)

    if len(trials) == 0:
        print('Error: no pytry.Trial class found in %s' % filename)
    elif len(trials) > 1:
        print('Error: more than one pytry.Trial class found')
    else:
        return trials[0]


def run():
    parser1 = argparse.ArgumentParser(
        description='pytry: Run Trials with parameters')
    parser1.add_argument('_trial_filename', metavar='FILE', type=str, nargs=1,
                         help='.py file containing Trial object')

    if len(sys.argv) < 2 or sys.argv[1].startswith('-'):
        parser1.parse_args()   # this will fail with an error message
    filename = sys.argv[1]

    trial = get_trial_class(filename)

    if trial is not None:
        t = trial()
        args = parser.parse_args(t, args=None, allow_filename=True)
        t.run(**args)
