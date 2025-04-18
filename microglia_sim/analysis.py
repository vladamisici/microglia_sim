"""
Load results and generate trajectory & Ca2+ plots.
"""
import pickle
import matplotlib.pyplot as plt
import numpy as np

class Analyzer:
    def __init__(self, result_file):
        with open(result_file,'rb') as f: self.h=pickle.load(f)
    def plot_trajectories(self, savepath=None):
        times = self.h['time']; pos=np.array(self.h['positions'])
        for idx in range(pos.shape[1]):
            xs=pos[:,idx,0]; ys=pos[:,idx,1]
            plt.plot(xs, ys, label=f'Agent {idx}')
        plt.xlabel('X (μm)'); plt.ylabel('Y (μm)')
        plt.legend(); plt.title('Trajectories')
        if savepath: plt.savefig(savepath)
        plt.show()
    def plot_Ca_traces(self, savepath=None):
        times=self.h['time']; Ca=np.array(self.h['Ca'])
        for idx in range(Ca.shape[1]):
            plt.plot(times, Ca[:,idx], label=f'Agent {idx}')
        plt.xlabel('Time (s)'); plt.ylabel('[Ca2+]')
        plt.legend(); plt.title('Intracellular Ca2+ Traces')
        if savepath: plt.savefig(savepath)
        plt.show()