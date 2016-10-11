from __future__ import absolute_import

import importlib
import logging
import sys

from . import trial


class NengoTrial(trial.Trial):
    def _create_base_params(self):
        super(NengoTrial, self)._create_base_params()
        self.param('nengo backend to use', backend='nengo')
        self.param('nengo timestep', dt=0.001)
        self.param('run in nengo GUI', gui=False, system=True)
        self.param('enable debug messages', debug=False, system=True)

    def execute_trial(self, p, plt):
        if p.debug:
            logging.basicConfig(level=logging.DEBUG)

        model = self.model(p)
        import nengo
        if not isinstance(model, nengo.Network):
            raise ValueError('model() must return a nengo.Network')

        if p.gui:
            import nengo_gui
            nengo_gui.GUI(model=model,
                          filename=sys.argv[1],
                          locals=dict(model=model),
                          editor=False,
                          ).start()
        else:
            module = importlib.import_module(p.backend)
            Simulator = module.Simulator

            sim = Simulator(model, dt=p.dt)
            return self.evaluate(p, sim, plt)

    def make_model(self, **kwargs):
        p = self._create_parameters(**kwargs)
        return self.model(p)

    def model(self, p):
        raise NotImplementedError
