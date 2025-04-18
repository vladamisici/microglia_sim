"""
Orchestrates simulation: initializes field and agents, runs time steps, records data.
"""
import yaml
import pickle
import os, sys
import numpy as np
import logging
from .config import SimulationConfig
from .field import Field
from .agent import Agent
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
class Simulation:
    def __init__(self, cfg: SimulationConfig):
        self.cfg = cfg
        self.field = Field(cfg)
        self.agents = [Agent(pos, cfg) for pos in cfg.initial_tips]
        self.history = {'time': [], 'positions': [], 'Ca': []}

    def run(self, outpath):
        total_steps = int(self.cfg.total_time / self.cfg.solver.dt)
        rec = self.cfg.record_every
        logger.info(f"Running simulation for {self.cfg.total_time}s ({total_steps} steps), record every {rec} steps")
        for step in range(total_steps):
            self.field.step()
            for agent in self.agents:
                agent.step(self.field)
            if step % rec == 0:
                logger.debug(f"At step {step}/{total_steps}")
                t = step * self.cfg.solver.dt
                self.history['time'].append(t)
                self.history['positions'].append([a.pos.copy() for a in self.agents])
                self.history['Ca'].append([a.Ca for a in self.agents])
        # Save results
        os.makedirs(outpath, exist_ok=True)
        fname = os.path.join(outpath, 'results.pkl')
        with open(fname, 'wb') as f:
            pickle.dump(self.history, f)
        logger.info(f"Simulation complete, results saved to {fname}")