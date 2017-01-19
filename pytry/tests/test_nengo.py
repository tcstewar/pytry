import pytest

import nengo

import pytry

class DummyTrial(pytry.NengoTrial):
    def params(self):
        pass
    def model(self, p):
        return nengo.Network()
    def evaluate(self, p, sim, plt):
        self.sim = sim
        return {}

def test_sim_close():
    t = DummyTrial()
    t.run()
    assert t.sim.closed


