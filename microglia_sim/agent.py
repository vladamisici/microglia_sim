"""
Microglia tip-agent with intracellular Ca2+ dynamics and chemotactic movement.
"""
import numpy as np
import logging
from .species import Index

logger = logging.getLogger(__name__)

def clamp(val, lo, hi):
    return max(lo, min(val, hi))

class Agent:
    def __init__(self, position, config):
        self.config = config
        self.pos = np.array(position, dtype=np.float64)
        self.Ca = 0.0

    def _compute_gradient(self, field, species='ADP'):
        """Central finite difference for concentration gradient."""
        dx = 1.0
        grad = np.zeros(2, dtype=np.float64)
        for dim in (0,1):
            forward = self.pos.copy()
            forward[dim] += 1
            backward = self.pos.copy()
            backward[dim] -= 1
            c_f = field.get_concentration(forward, species)
            c_b = field.get_concentration(backward, species)
            grad[dim] = (c_f - c_b) / (2.0 * dx)
        return grad

    def step(self, field):
        cfg = self.config
        dt = cfg.solver.dt
        proc = cfg.process

        # 1. Update intracellular Ca2+ (simple Euler)
        ligand = field.get_concentration(self.pos, 'ADP')
        logger.debug(f"Agent at {self.pos}: [ADP]={ligand:.3f}, Ca before={self.Ca:.3f}")
        dCa = proc.Ca_on * ligand - proc.Ca_off * self.Ca
        self.Ca += dt * dCa
        logger.debug(f"Agent Ca after update={self.Ca:.3f}")

        # 2. Compute chemotactic force from gradient of ADP
        grad = self._compute_gradient(field, species='ADP')
        norm = np.linalg.norm(grad)
        logger.debug(f"Gradient={grad}, norm={norm:.3f}")
        if norm > 0:
            unit_grad = grad / norm
            force_mag = proc.chemotactic_coeff * norm
            force = unit_grad * force_mag
        else:
            force = np.zeros(2)

        # 3. Compute movement: extension vs retraction
        ext = proc.extension_rate * (1.0 + self.Ca)
        movement = force * ext * dt
        # retraction opposes movement direction
        if np.linalg.norm(movement) < 1e-12:
            movement = -proc.retraction_rate * movement / (np.linalg.norm(movement) + 1e-12) * dt

        # 4. Update position with boundary clamp
        new_pos = self.pos + movement
        nx, ny = cfg.grid_size
        new_pos[0] = clamp(new_pos[0], 0, nx-1)
        new_pos[1] = clamp(new_pos[1], 0, ny-1)
        logger.debug(f"Agent moving by {movement}, new pos={new_pos}")
        self.pos = new_pos