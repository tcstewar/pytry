import os

from . import trial


class PlotTrial(trial.Trial):
    def _create_base_params(self):
        super(PlotTrial, self)._create_base_params()
        self.param('display figures', show_figs=False, system=True)
        self.param('save figures', save_figs=False, system=True)
        self.param('hide overlay on figures', hide_overlay=False, system=True)

    def execute_trial(self, p):
        if p.save_figs or p.show_figs:
            import matplotlib.pyplot
            self.plt = matplotlib.pyplot
            self.plt.figure()
        else:
            self.plt = None

        result = super(PlotTrial, self).execute_trial(p)

        param_text = self.generate_param_text(p)
        result_text = self.generate_result_text(result)

        if self.plt is not None and not p.hide_overlay:
            self.plt.suptitle(p.data_filename + '\n' + result_text, fontsize=8)
            self.plt.figtext(0.13, 0.12, param_text)

        if p.save_figs:
            fn = os.path.join(p.data_dir, p.data_filename)
            self.plt.savefig(fn + '.png', dpi=300)

        if p.show_figs:
            self.plt.show()

        return result

    def do_evaluate(self, p):
        return self.evaluate(p, self.plt)
