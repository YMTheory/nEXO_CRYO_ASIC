import numpy as np
import matplotlib.pyplot as plt
from scripts.CryoAsicAnalysis import CryoAsicAnalysis


class comparison:
    def __init__(self) -> None:
        self.analysers          = {}
        self.nevent_dict        = {}
        self.nsampling_dict     = {}

        self.viewers            = {}
        
        self.noise_dfs          = {}    
    
    
    ## adder
    
    def _add_viewer(self, label, viewer):
        self.viewers[label] = viewer
    
    def _add_analyser(self, label, ana):
        self.analysers[label]       = ana
        self.nevent_dict[label]     = ana.nevents_total 
        self.nsampling_dict[label]  = ana.nsamples
        

    ## getter        
    def _get_analyser(self, label):
        return self.analysers[label]
    
    def _get_viewer(self, label):
        return self.viewers[label]

    def _get_waveforms_oneEvent(self, ana, evtid):
        return ana.df['Data'].iloc[evtid]


    def _get_waveform_oneChannel_oneEvent(self, ana, evtid, chid):
        return ana.df['Data'].iloc[evtid][chid]

    def _get_std_oneChannel_oneSet(self, lb, chid):
        return self.noise_dfs[lb]['STD'].iloc[chid]


    def _get_std_oneSet(self, lb):
        return self.noise_dfs[lb]['STD'].to_numpy()
    
    


    ## noise analysis
    def calculate_noise(self):
        for lb, ana in self.analysers.items():
            ana.calculate_avg_psds() # We must calculate PSD before stds in this script...
            ana.calculate_stds()
            self.noise_dfs[lb] = ana.noise_df


    ## plotter
    
    def _plot_oneChannel_oneEvent(self, evtid, chid):
        
        fig, ax = plt.subplots(figsize=(12, 8))
        for lb, ana in self.analysers.items():
            time = ana.times
            ax.plot(time, self._get_waveform_oneChannel_oneEvent(ana, evtid, chid), label=lb)
        
        ax.set_xlabel('time [us]', fontsize=13)
        ax.set_ylabel('ADC', fontsize=13)
        ax.tick_params(axis='both', which='major', labelsize=13)
        ax.legend(fontsize=13)
        
        plt.tight_layout()
        return fig    


    def _plot_std(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        for lb, _ in self.analysers.items():
            stds = self._get_std_oneSet(lb)
            ax.plot(stds, 'o-', label=lb)
        ax.set_xlabel('Channel ID', fontsize=13)
        ax.set_ylabel('STD', fontsize=13)
        ax.tick_params(axis='both', which='major', labelsize=13)
        ax.legend(fontsize=13)
        
        plt.tight_layout()
        return fig    





