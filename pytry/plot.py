import os
import warnings

from . import trial


class PlotTrial(trial.Trial):
    def _create_base_params(self):
        super(PlotTrial, self)._create_base_params()
        self.param('display plot', plt=False, system=True)
        self.param('save plot', plt_save=False, system=True)
        self.param('show overlay on plot', plt_overlay=False, system=True)

        self.param('display figures', show_figs=False, system=True, hidden=True)
        self.param('save figures', save_figs=False, system=True, hidden=True)
        self.param('hide overlay on figures', hide_overlay=False, system=True, hidden=True)

    def execute_trial(self, p):
        if p.show_figs:
            warnings.warn('show_figs has been deprecated; use plt instead')
            p.plt = p.show_figs
        if p.save_figs:
            warnings.warn('save_figs has been deprecated; use plt_save instead')
            p.plt_save = p.save_figs
        if p.plt_overlay:
            warnings.warn('plt_overlay has been deprecated; use hide_overlay instead')

        if p.plt or p.plt_save:
            if isinstance(p.plt, bool):
                import matplotlib.pyplot
                self.plt = matplotlib.pyplot
                self.plt.figure()
            else:
                self.plt = p.plt
        else:
            self.plt = None

        result = super(PlotTrial, self).execute_trial(p)

        title = p.data_filename

        if self.plt is not None:
            if p.plt_overlay:
                param_text = self.generate_param_text(p)
                if result is not None:
                    result_text = self.generate_result_text(result)
                    title = '%s\n%s' % (title, result_text)

                self.plt.figtext(0.13, 0.12, param_text)
            self.plt.suptitle(title, fontsize=8)

        if p.plt_save:
            fn = os.path.join(p.data_dir, p.data_filename)
            self.plt.savefig(fn + '.png', dpi=300)

        if p.plt is True:
            self.plt.show()

        return result

    def do_evaluate(self, p):
        return self.evaluate(p, self.plt)
