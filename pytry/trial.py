import os
import random
import time
import uuid

from . import write
from . import parser


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
        self.param('filename for data', data_filename=None, system=True)
        self.param('data file format [txt,npz]',
                   data_format='txt', system=True)
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

    def generate_param_text(self, p):
        args_text = []
        for k in self.param_defaults.keys():
            if k not in self.system_params:
                args_text.append('%s = %r' % (k, getattr(p, k)))
        return '\n'.join(args_text)

    def generate_result_text(self, result):
        text = []
        for k, v in sorted(result.items()):
            text.append('%s = %r' % (k, v))
        return '\n'.join(text)

    def run(self, **kwargs):
        p = self._create_parameters(**kwargs)

        if p.verbose:
            print('running %s' % p.data_filename)

        if not os.path.exists(p.data_dir):
            os.mkdir(p.data_dir)

        try:
            import numpy
            numpy.random.seed(p.seed)
        except ImportError:
            pass
        random.seed(p.seed)

        result = self.execute_trial(p)

        if result is None:
            print('No results to record')
            return

        for k in result.keys():
            if k in self.param_defaults:
                raise AttributeError('"%s" cannot be both a parameter and '
                                     'a result value' % k)

        fn = os.path.join(p.data_dir, p.data_filename)
        write.write(self, fn, p, result)

        if p.verbose:
            print(self.generate_param_text(p))
            print(self.generate_result_text(result))

        return result

    def do_evaluate(self, p):
        return self.evaluate(p)

    def execute_trial(self, p):
        return self.do_evaluate(p)

    def parse_args(self, args=None):
        return parser.parse_args(self, args)

    def params(self):
        raise NotImplementedError

    def evaluate(self, p, plt):
        raise NotImplementedError
