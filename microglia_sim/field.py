"""
Reaction–diffusion field solver with Strang splitting and Crank–Nicolson.
"""
import numpy as np
import logging
from scipy.sparse import diags, eye, kron
from scipy.sparse.linalg import spsolve
from .species import Index, ectonucleotidase_rates

logger = logging.getLogger(__name__)
def build_CN_matrices(nx, ny, dx, dt, D, lam):
    # 1D Laplacian operator
    main = -2.0 * np.ones(nx)
    off  =  np.ones(nx - 1)
    Lx1d = diags([off, main, off], [-1, 0, 1]) / (dx*dx)
    Iy   = eye(ny)
    Ix   = eye(nx)
    L2d  = kron(Lx1d, Iy) + kron(Iy, Lx1d)
    # include decay
    L = D * L2d - lam * eye(nx*ny)
    A = eye(nx*ny) - 0.5 * dt * L
    B = eye(nx*ny) + 0.5 * dt * L
    return A.tocsr(), B.tocsr()


class Field:
    def __init__(self, config):
        self.cfg = config
        nx, ny = config.grid_size
        self.nx, self.ny = nx, ny
        S = len(Index)
        # grid shape (species, nx*ny) for linear solvers
        self.grid = np.zeros((S, nx*ny), dtype=np.float64)
        # constant ATP source
        x0, y0 = config.source_position
        idx0 = x0 * ny + y0
        self.grid[Index['ATP'], idx0] = 100.0

        # Pre-build CN matrices for each species
        self.A = {}
        self.B = {}
        for sp in ['ATP','ADP','AMP','ADO']:
            D = config.solver.diffusion[sp]
            lam = config.solver.decay[sp]
            A_mat, B_mat = build_CN_matrices(nx, ny,
                                             config.solver.dx,
                                             config.solver.dt,
                                             D, lam)
            self.A[sp] = A_mat
            self.B[sp] = B_mat

    def _reaction_half(self, dt_half):
        # Strang half-step reaction: c += dt/2 * R(c)
        S, N = self.grid.shape
        new = np.empty_like(self.grid)
        for i in range(N):
            conc = tuple(self.grid[k, i] for k in range(S))
            dr = ectonucleotidase_rates(conc, self.cfg.ecto)
            for k in range(S):
                new[k, i] = self.grid[k, i] + dt_half * dr[k]
        self.grid = new

    def step(self):
        cfg = self.cfg
        dt = cfg.solver.dt
        logger.debug(f"Field.step(): reaction half-step with dt={dt}")
        # 1) Reaction half-step
        self._reaction_half(0.5 * dt)
        # 2) Diffusion full-step via CN
        for sp in ['ATP','ADP','AMP','ADO']:
            vec = self.grid[Index[sp], :]
            logger.debug(f"Diffusing species {sp}: max before={np.max(vec):.3f}")
            Bv  = self.B[sp].dot(vec)
            sol = spsolve(self.A[sp], Bv)
            self.grid[Index[sp], :] = sol
            logger.debug(f"Species {sp}: max after={np.max(sol):.3f}")
        # reapply constant ATP source
        idx0 = cfg.source_position[0] * self.ny + cfg.source_position[1]
        self.grid[Index['ATP'], idx0] = 100.0
        # 3) Reaction half-step
        self._reaction_half(0.5 * dt)

    def get_concentration(self, pos, species_name: str) -> float:
        # convert 2D index to flat
        i = int(pos[0]); j = int(pos[1])
        i = max(0, min(i, self.nx-1))
        j = max(0, min(j, self.ny-1))
        idx = i * self.ny + j
        conc = float(self.grid[Index[species_name], idx])
        logger.debug(f"get_concentration({species_name}) at ({i},{j}) = {conc}")
        return conc