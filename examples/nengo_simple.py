import nengo
import pytry
import numpy as np

class NengoSimple(pytry.NengoTrial):
    def params(self):
        self.param('number of neurons', N=100)
        self.param('number of dimensions', D=2)

    def model(self, p):
        model = nengo.Network()
        with model:
            stim = nengo.Node([0]*p.D)
            ens = nengo.Ensemble(n_neurons=p.N, dimensions=p.D)
            nengo.Connection(stim, ens)
            self.probe = nengo.Probe(ens, synapse=0.01)
        return model

    def evaluate(self, p, sim, plt):
        sim.run(1)

        if plt is not None:
            plt.plot(sim.trange(), sim.data[self.probe])

        rmse = np.sqrt(np.mean((sim.data[self.probe])**2))
        return dict(rmse=rmse)
        
