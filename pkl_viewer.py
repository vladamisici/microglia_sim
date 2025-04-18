import argparse
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np


def load_history(pkl_path):
    """
    Load the simulation history dictionary from a pickle file.
    Expected keys: 'time', 'positions', 'Ca'.
    Returns: dict with numpy arrays.
    """
    with open(pkl_path, 'rb') as f:
        hist = pickle.load(f)
    # Convert lists to arrays
    hist['time'] = np.array(hist['time'])
    hist['positions'] = np.array(hist['positions'])  # shape (T, N, 2)
    hist['Ca'] = np.array(hist['Ca'])               # shape (T, N)
    return hist


def plot_trajectories(hist, show=True, save=None):
    """
    Plot X-Y trajectories of all agents.
    """
    pos = hist['positions']  # (T, N, 2)
    T, N, _ = pos.shape
    plt.figure()
    for i in range(N):
        xs = pos[:, i, 0]
        ys = pos[:, i, 1]
        plt.plot(xs, ys, label=f'Agent {i}')
    plt.xlabel('X (μm)')
    plt.ylabel('Y (μm)')
    plt.title('Trajectories')
    plt.legend()
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    plt.close()


def plot_ca_traces(hist, show=True, save=None):
    """
    Plot intracellular Ca2+ over time for each agent.
    """
    times = hist['time']
    Ca = hist['Ca']  # (T, N)
    plt.figure()
    for i in range(Ca.shape[1]):
        plt.plot(times, Ca[:, i], label=f'Agent {i}')
    plt.xlabel('Time (s)')
    plt.ylabel('[Ca2+] (μM)')
    plt.title('Intracellular Ca2+ Traces')
    plt.legend()
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='View simulation results from a results.pkl file')
    parser.add_argument('pkl', help='Path to results.pkl')
    parser.add_argument('--no-show', action='store_true', help="Do not display interactive plots")
    parser.add_argument('--save-dir', default=None, help='Directory to save generated figures')
    parser.add_argument('--plot', choices=['all', 'trajectories', 'ca'], default='all',
                        help='Which plot to generate')
    args = parser.parse_args()

    hist = load_history(args.pkl)
    show = not args.no_show
    savedir = args.save_dir
    if savedir and not os.path.exists(savedir):
        os.makedirs(savedir)

    if args.plot in ('all', 'trajectories'):
        save_path = os.path.join(savedir, 'trajectories.png') if savedir else None
        plot_trajectories(hist, show=show, save=save_path)
    if args.plot in ('all', 'ca'):
        save_path = os.path.join(savedir, 'Ca_traces.png') if savedir else None
        plot_ca_traces(hist, show=show, save=save_path)

if __name__ == '__main__':
    main()
