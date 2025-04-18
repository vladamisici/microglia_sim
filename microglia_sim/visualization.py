"""
Matplotlib routines to visualize field snapshots with agents.
"""
import matplotlib.pyplot as plt
import numpy as np
from .species import Index

def plot_field_and_agents(field, agents, species='ATP', cmap='viridis', savepath=None):
    grid = field.grid[Index[species]]
    plt.imshow(grid.T, origin='lower', cmap=cmap)
    xs=[a.pos[0] for a in agents]
    ys=[a.pos[1] for a in agents]
    plt.scatter(xs, ys, c='r', edgecolor='k')
    plt.title(f'{species} Field with Agent Positions')
    if savepath: plt.savefig(savepath)
    plt.show()