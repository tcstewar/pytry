import os
import random
import time
import uuid


class Params(object):
    pass


class Trial(object):
    def __init__(self):
        self.param_defaults = {}
        self.param_descriptions = {}
        self.system_params = []

        self._create_base_params()
        self.params()

    def _create_base_params(self):
        self.param('data directory', data_dir='data', system=True)
        self.param('display figures', show_figs=False, system=True)
        self.param('save figures', save_figs=False, system=True)
        self.param('hide overlay on figures', hide_overlay=False, system=True)
        self.param('filename for data', data_filename=None, system=True)
        self.param('print progress information', verbose=True, system=True)
        self.param('random number seed', seed=1)

    def param(self, description, system=False, **kwarg):
        if len(kwarg) != 1:
            raise ValueException('Must specify exactly one parameter')
        k, v = list(kwarg.items())[0]
        if k in self.param_defaults:
            raise ValueException('Cannot redefine parameter "%s"' % k)
        self.param_defaults[k] = v
        self.param_descriptions[k] = description
        if system:
            self.system_params.append(k)

    def _create_parameters(self, **kwargs):
        p = Params()
        for k, v in self.param_defaults.items():
            setattr(p, k, v)
        for k, v in kwargs.items():
            if k not in self.param_defaults:
                raise AttributeError('Unknown parameter: "%s"' % k)
            setattr(p, k, v)
        if p.data_filename is None:
            uid = uuid.uuid4().fields[0]
            name = self.__class__.__name__
            p.data_filename = '%s#%s-%s' % (name,
                                            time.strftime('%Y%m%d-%H%M%S'),
                                            '%08x' % uid)
        return p

    def run(self, **kwargs):
        p = self._create_parameters(**kwargs)

        if p.verbose:
            print('running %s' % p.data_filename)

        try:
            import numpy
            numpy.random.seed(p.seed)
        except ImportError:
            pass
        random.seed(p.seed)

        if p.save_figs or p.show_figs:
            import matplotlib.pyplot
            plt = matplotlib.pyplot
            plt.figure()
        else:
            plt = None

        result = self.execute_trial(p, plt)

        if result is None:
            print('No results to record')
            return

        text = []
        for k, v in sorted(result.items()):
            if k in self.param_defaults:
                raise AttributeError('"%s" cannot be both a parameter and '
                                     'a result value' % k)
            text.append('%s = %r' % (k, v))

        args_text = []
        for k in self.param_defaults.keys():
            if k not in self.system_params:
                args_text.append('%s = %r' % (k, getattr(p, k)))

        if plt is not None and not p.hide_overlay:
            plt.suptitle(p.data_filename + '\n' + '\n'.join(text), fontsize=8)
            plt.figtext(0.13, 0.12, '\n'.join(args_text))

        text = args_text + text
        text = '\n'.join(text)

        if not os.path.exists(p.data_dir):
            os.mkdir(p.data_dir)
        fn = os.path.join(p.data_dir, p.data_filename)
        if p.save_figs:
            plt.savefig(fn + '.png', dpi=300)

        with open(fn + '.txt', 'w') as f:
            f.write(text)
        if p.verbose:
            print(text)

        if p.show_figs:
            plt.show()

        return result

    def execute_trial(self, p, plt):
        return self.evaluate(p, plt)

    def params(self):
        raise NotImplementedError

    def evaluate(self, p, plt):
        raise NotImplementedError
