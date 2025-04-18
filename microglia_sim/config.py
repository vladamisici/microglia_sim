"""
Simulation configuration and biological parameters.
Units: length in micrometers, time in seconds, concentration in micromolar.
"""
from dataclasses import dataclass, field
from typing import Dict, Tuple

@dataclass
class EctoParameters:
    CD39_level: float = 1.0    # unitless relative expression
    CD73_level: float = 1.0
    Km_ATP_ADP: float = 12.0    # μM
    Vmax_ATP_ADP: float = 0.5   # μM/s
    Km_ADP_AMP: float = 10.0
    Vmax_ADP_AMP: float = 0.4
    Km_AMP_ADO: float = 5.0
    Vmax_AMP_ADO: float = 0.3

@dataclass
class ProcessParameters:
    chemotactic_coeff: float = 2.0     # dimensionless
    ado_sensitivity: float = 1.0       # 1/(μM)
    adp_sensitivity: float = 10.0      # 1/(μM)
    extension_rate: float = 0.1        # μm/s per unit force
    retraction_rate: float = 0.05      # μm/s
    Ca_on: float = 0.1                 # s^-1·μM^-1
    Ca_off: float = 0.05               # s^-1

@dataclass
class SolverParameters:
    dx: float = 1.0        # μm grid spacing
    dt: float = 0.01       # s time step
    max_steps: int = 60000 # for 600 s at dt=0.01
    diffusion: Dict[str, float] = field(default_factory=lambda: {
        'ATP': 300.0,       # μm^2/s
        'ADP': 200.0,
        'AMP': 100.0,
        'ADO': 150.0,
    })
    decay: Dict[str, float] = field(default_factory=lambda: {
        'ATP': 0.3,         # s^-1
        'ADP': 0.2,
        'AMP': 0.1,
        'ADO': 0.05,
    })
    refine_threshold: float = 1e-6

@dataclass
class SimulationConfig:
    grid_size: Tuple[int, int] = (200, 200)          # μm
    source_position: Tuple[int, int] = (100, 100)    # μm
    record_every: int = 1000                         # steps
    total_time: float = 600.0                        # s
    initial_tips: Tuple[Tuple[float, float], ...] = (
        (50.0,50.0), (150.0,50.0), (50.0,150.0), (150.0,150.0)
    )
    ecto: EctoParameters = field(default_factory=EctoParameters)
    process: ProcessParameters = field(default_factory=ProcessParameters)
    solver: SolverParameters = field(default_factory=SolverParameters)