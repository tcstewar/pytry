from __future__ import absolute_import

import importlib
import logging
import sys

from . import plot


class NengoTrial(plot.PlotTrial):
    def _create_base_params(self):
        super(NengoTrial, self)._create_base_params()
        self.param('nengo backend to use', backend='nengo')
        self.param('nengo timestep', dt=0.001)
        self.param('run in nengo GUI', gui=False, system=True)
        self.param('enable debug messages', debug=False, system=True)

    def execute_trial(self, p):
        if p.debug:
            logging.basicConfig(level=logging.DEBUG)

        model = self.model(p)
        import nengo
        if not isinstance(model, nengo.Network):
            raise ValueError('model() must return a nengo.Network')

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
            if ':' in p.backend:
                backend, clsname = p.backend.split(':', 1)
            else:
                backend = p.backend
                clsname = 'Simulator'
            module = importlib.import_module(backend)
            Simulator = getattr(module, clsname)

            self.sim = Simulator(model, dt=p.dt)
            with self.sim:
                return super(NengoTrial, self).execute_trial(p)

    def do_evaluate(self, p):
        return self.evaluate(p, self.sim, self.plt)

    def make_model(self, **kwargs):
        p = self._create_parameters(**kwargs)
        return self.model(p)

    def model(self, p):
        raise NotImplementedError
