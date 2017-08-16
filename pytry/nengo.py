from __future__ import absolute_import

import inspect
import importlib
import logging
import sys

from . import plot

try:
    basestring         # For Python 2 compatibility
except NameError:
    basestring = str   # For Python 3 compatibility


class NengoTrial(plot.PlotTrial):
    def _create_base_params(self):
        super(NengoTrial, self)._create_base_params()
        self.param('nengo backend to use', backend='nengo')
        self.param('nengo timestep', dt=0.001)
        self.param('run in nengo GUI', gui=False, system=True)
        self.param('enable debug messages', debug=False, system=True)
        self.param('neuron type', neuron_type='default')

    def execute_trial(self, p):
        if p.debug:
            logging.basicConfig(level=logging.DEBUG)

        model = self.model(p)
        import nengo
        if not isinstance(model, nengo.Network):
            raise ValueError('model() must return a nengo.Network')

        if p.neuron_type != 'default':
            if isinstance(p.neuron_type, basestring):
                neuron_type = eval(p.neuron_type)
            else:
                neuron_type = p.neuron_type

            if not isinstance(neuron_type, nengo.neurons.NeuronType):
                raise AttributeError('%s is not a NeuronType' % p.neuron_type)

            for ens in model.all_ensembles:
                ens.neuron_type = neuron_type

        if p.gui:
            locals_dict = getattr(self, 'locals', dict(model=model))
            import nengo_gui
            try:
                nengo_gui.GUI(model=model,
                              filename=sys.argv[1],
                              locals=locals_dict,
                              editor=False,
                              ).start()
            except TypeError:
                # support nengo_gui v0.2.0 and previous
                nengo_gui.GUI(model=model,
                              filename=sys.argv[1],
                              locals=locals_dict,
                              interactive=False,
                              allow_file_change=False,
                              ).start()
        else:
            backend = p.backend

            extra_args = {}
            if backend.endswith(')') and '(' in backend:
                backend, arg_text = backend[:-1].split('(', 1)
                extra_args = eval('dict(%s)' % arg_text)

            if ':' in backend:
                backend, clsname = backend.split(':', 1)
            else:
                clsname = 'Simulator'
            module = importlib.import_module(backend)
            Simulator = getattr(module, clsname)

            args = inspect.getargspec(Simulator.__init__)[0]
            if (not p.verbose and 'progress_bar' in args):
                    self.sim = Simulator(model, dt=p.dt, progress_bar=False,
                                         **extra_args)
            else:
                self.sim = Simulator(model, dt=p.dt, **extra_args)

            with self.sim:
                return super(NengoTrial, self).execute_trial(p)

    def do_evaluate(self, p):
        return self.evaluate(p, self.sim, self.plt)

    def make_model(self, **kwargs):
        p = self._create_parameters(**kwargs)
        return self.model(p)

    def model(self, p):
        raise NotImplementedError
