import numpy as np
import matplotlib.pyplot as plt
from scripts.CryoAsicAnalysis import CryoAsicAnalysis


class batch:
    def __init__(self) -> None:
        self.analysers          = {}
        self.nevent_dict        = {}
        self.nsampling_dict     = {}

        self.viewers            = {}
        
        self.noise_dfs          = {}    

        self.coupled_channelId  = None
        self.noncoupled_channelId = None
    
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
    
    
    def _set_coupled_channel(self, chids):
        self.coupled_channelId = chids
        self.noncoupled_channelId = np.array([ i for i in range(64) if i not in chids])

    ## noise analysis
    def calculate_noise(self, calcpsd=False, subtract_baseline=False):
        for lb, ana in self.analysers.items():
            if subtract_baseline:
                ana.baseline_subtract()
            if calcpsd:
                ana.calculate_avg_psds() # We must calculate PSD before stds in this script...
            ana.calculate_stds()
            self.noise_dfs[lb] = ana.noise_df


    ## plotter
    
    def _plot_waveforms_oneChannel_oneEvent(self, lbs, evtid, chid):
        
        fig, ax = plt.subplots(figsize=(12, 8))
        if len(lbs) == 0:
            lbs = self.analysers.keys()
        for lb in lbs:
            ana = self.analysers[lb]
            time = ana.times
            ax.plot(time, self._get_waveform_oneChannel_oneEvent(ana, evtid, chid), label=lb)
        
        ax.set_xlabel('time [us]', fontsize=13)
        ax.set_ylabel('ADC', fontsize=13)
        ax.tick_params(axis='both', which='major', labelsize=13)
        ax.legend(fontsize=13)
        
        plt.tight_layout()
        return fig    


    def _plot_std(self, lbs):
        fig, ax = plt.subplots(figsize=(12, 8))
        if len(lbs) == 0:
            lbs = self.analysers.keys()
        for lb in lbs:
            stds = self._get_std_oneSet(lb)
            ax.plot(stds, 'o-', label=lb)
        ax.set_xlabel('Channel ID', fontsize=13)
        ax.set_ylabel('STD', fontsize=13)
        ax.tick_params(axis='both', which='major', labelsize=13)
        ax.legend(fontsize=13)
        
        plt.tight_layout()
        return fig    


    def _plot_std_separately(self, lbs):
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        print(self.noncoupled_channelId)
        if len(lbs) == 0:
            lbs = self.analysers.keys()
        for lb in lbs:
            stds = self._get_std_oneSet(lb)
            ax[0].plot(self.coupled_channelId, stds[self.coupled_channelId], 'o-', label=lb)
            ax[1].plot(self.noncoupled_channelId, stds[self.noncoupled_channelId], 'o-', label=lb)
        
        for i in range(2):
            ax[i].set_xlabel('Channel ID', fontsize=13)
            ax[i].set_ylabel('STD', fontsize=13)
            ax[i].tick_params(axis='both', which='major', labelsize=13)
            ax[i].legend(fontsize=13)
        
        plt.tight_layout()
        return fig    


    def _plot_waveforms_oneEvent(self, lbs, channels, evtid):

        fig, ax = plt.subplots(figsize=(8, 6))
        
        if len(lbs) == 0:
            lbs = self.analysers.keys()
        for lb in lbs:
            ana = self.analysers[lb]
            for cha in channels:
                time = ana.times
                one_wave = self._get_waveform_oneChannel_oneEvent(ana, evtid, cha)
                ax.plot(time, one_wave, label=f'cha {cha}')
                
        ax.set_xlabel('time [us]', fontsize=13)
        ax.set_ylabel('ADC', fontsize=13)
        ax.tick_params(axis='both', which='major', labelsize=13)
        ax.legend(fontsize=13)
        
        plt.tight_layout()
        return fig

