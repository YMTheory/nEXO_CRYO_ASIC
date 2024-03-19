import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

class ENC_calculator():
    
    def __init__(self, config) -> None:
        
        try:
            self.FEset = config['FEset']
        except:
            self.FEset = '912' # 0.6 us, 1.5X
        
        try:
            self.LSB = config['LSB']
        except:
            self.LSB = 0.000390625
            
        self.C = 1.6e-19 # electron charge

        try:
            self.adc_vrms = config['adc_vrms']
        except:
            # set it as a fixed number, currently
            self.adc_vrms = 4.22e-4  # unit: V
            

        try:
            self.C1 = config['capacitance_1']
            #print(f'The capacitance of 0-32 channels is set as {self.C1} pF.')
        except KeyError:
            print('Error! One must specify at least one capacitance for the board!')
           
        
        try:
            self.C2 = config['capacitance_2']
            #print(f'The capacitance of 32-64 channels is set as {self.C2} pF.')
        except KeyError:
            self.C2 = self.C1
            #print(f'The capacitance of 0-32 channels is set as {self.C2} pF.')
        
        self.infile = ''
        self.noise_df = None


        # Simulation pulse amplitudes under -113 celsius degree
        self.Vo_Ampls = { \
                             '896': 1.5798, \
                             '900': 1.5751, \
                             '904': 1.5785, \
                             '908': 1.5769, \
                             '912': 1.5773, \
                             '916': 1.5731, \
                             '920': 1.5783, \
                             '924': 1.5763, \
                             '928': 1.5706, \
                             '932': 1.5679, \
                             '936': 1.5735, \
                             '940': 1.5741, \
                             '944': 1.5604, \
                             '948': 1.5609, \
                             '952': 1.5659, \
                             '956': 1.5703, \
                             }

        self.Qins = { \
                             '896': 150e-15, \
                             '900': 150e-15, \
                             '904': 150e-15, \
                             '908': 150e-15, \
                             '912': 100e-15, \
                             '916': 100e-15, \
                             '920': 100e-15, \
                             '924': 100e-15, \
                             '928': 50e-15, \
                             '932': 50e-15, \
                             '936': 50e-15, \
                             '940': 50e-15, \
                             '944': 25e-15, \
                             '948': 25e-15, \
                             '952': 25e-15, \
                             '956': 25e-15, \
                             } # unit: fC

        
        
        self.enc_fc = None
        self.enc_fe = None
        
        
    def set_filename(self, filename):
        self.infile = filename 
    
    def load_noise_csv(self):
        # This is implemented for UCSD organized data csv files.
        self.noise_df = pd.read_csv(self.infile)
      
    def load_noise_df(self, std):
        self.noise_df = pd.DataFrame({'Average Noise' : std})
      
    def set_FEset(self, set):
        self.FEset = set
      
      
    def plot_channelwise_noise(self, data, data_err, ylabel='noise'):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.errorbar(range(len(data)), data, yerr=data_err, fmt='o-', lw=2, ms=6)
        ax.set_xlabel('channel No.', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.tick_params(axis='both', labelsize=12)
        plt.tight_layout()
        plt.show()
    
        
    def ENC_FC(self):
        '''
        Calculate ENC from the measured baseline fluctuations.
        ENC_FC = (bl_std * LSB) / (V_ampl) * (Qin / C)
        V_ampl are values from simulation.
        '''
        bl_rms = self.noise_df['Average Noise'].to_numpy()
        Qin = self.Qins[self.FEset] 
        Vorms_FC = bl_rms * self.LSB
        if self.FEset in self.Vo_Ampls.keys():
            Vo_Ampl = self.Vo_Ampls[self.FEset]
        else:
            Vo_Ampl = self.Vo_Ampls['920'] ### temporary
            print(f'No Vo_Ampl defined for current FEset {self.FEset} -> set FEset as 920 now.')
        self.enc_fc = Vorms_FC / Vo_Ampl * Qin / self.C
        
       
   
   
    def ENC_FE(self):
        bl_rms = self.noise_df['Average Noise'].to_numpy()
        Qin = self.Qins[self.FEset]
        Vorms_FC = bl_rms * self.LSB
        Vorms_FE = np.where(Vorms_FC > self.adc_vrms, np.sqrt(Vorms_FC**2 - self.adc_vrms**2), 0 )
        #chas = np.where(Vorms_FC < self.adc_vrms)
        #print('Channel ', chas, 'has FC noise less than the ADC noise.')
        if self.FEset in self.Vo_Ampls.keys():
            Vo_Ampl = self.Vo_Ampls[self.FEset]
        else:
            Vo_Ampl = self.Vo_Ampls['920'] ### temporary
            print(f'No Vo_Ampl defined for current FEset {self.FEset} -> set FEset as 920 now.')
        self.enc_fe = Vorms_FE / Vo_Ampl * Qin / self.C
        

    def ENC_FC_filtered(self):
        '''
        Calculate ENC from the measured baseline fluctuations.
        ENC_FC = (bl_std * LSB) / (V_ampl) * (Qin / C)
        V_ampl are values from simulation.
        '''
        bl_rms = self.noise_df['Average Filtered Noise'].to_numpy()
        Qin = self.Qins[self.FEset] 
        Vorms_FC = bl_rms * self.LSB
        if self.FEset in self.Vo_Ampls.keys():
            Vo_Ampl = self.Vo_Ampls[self.FEset]
        else:
            Vo_Ampl = self.Vo_Ampls['920'] ### temporary
            print(f'No Vo_Ampl defined for current FEset {self.FEset} -> set FEset as 920 now.')
        self.enc_fc = Vorms_FC / Vo_Ampl * Qin / self.C
        
       
   
    def ENC_FE_filtered(self):
        bl_rms = self.noise_df['Average Filtered Noise'].to_numpy()
        Qin = self.Qins[self.FEset]
        Vorms_FC = bl_rms * self.LSB
        #Vorms_FE = np.sqrt(Vorms_FC**2 - self.adc_vrms**2) 
        Vorms_FE = np.where(Vorms_FC > self.adc_vrms, np.sqrt(Vorms_FC**2 - self.adc_vrms**2), 0 )
        #chas = np.where(Vorms_FC < self.adc_vrms)
        #print('Channel ', chas, 'has FC noise less than the ADC noise.')
        if self.FEset in self.Vo_Ampls.keys():
            Vo_Ampl = self.Vo_Ampls[self.FEset]
        else:
            Vo_Ampl = self.Vo_Ampls['920'] ### temporary
            print(f'No Vo_Ampl defined for current FEset {self.FEset} -> set FEset as 920 now.')
        self.enc_fe = Vorms_FE / Vo_Ampl * Qin / self.C
        


