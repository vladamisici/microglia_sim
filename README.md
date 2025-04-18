# Microglia Chemotaxis Simulation

A Python package for agent-based modeling of microglial process chemotaxis, coupling extracellular purinergic reaction–diffusion with intracellular Ca²⁺ feedback.

---

## Currently Implemented

### 1. Reaction–Diffusion Field Solver
- **Species:** ATP, ADP, AMP, ADO  
- **Numerical Methods:** Strang splitting with Crank–Nicolson for diffusion and decay  
- **Enzymatic Kinetics:** Michaelis–Menten ectonucleotidase rates (CD39: ATP→ADP→AMP; CD73: AMP→ADO)  
- **Constant Source:** Fixed ATP release at designated grid location  

### 2. Agent-Based Tip Dynamics
- **Agents:** Point-tips initialized at configurable positions  
- **Ligand Sensing:** ADP concentration gradient from the field  
- **Intracellular Ca²⁺:** First-order ODE (dCa/dt = k_on·[ADP] − k_off·Ca) stepped by Euler integration  
- **Movement:** Balance of chemotactic extension (proportional to Ca²⁺) and retraction, with boundary clamping  

### 3. Configurability
- Dataclasses for parameters:  
  - `EctoParameters` (CD39/CD73 levels, Km/Vmax values)  
  - `ProcessParameters` (chemotactic coefficients, sensitivity, rates)  
  - `SolverParameters` (dx, dt, diffusion, decay)  
  - `SimulationConfig` (grid size, source position, time, recording intervals, initial tips)  

### 4. Utilities
- **Example Script:** `examples/run_parameter_sweep.py` for parallel sweeps and plotting  
- **Visualization:** `pkl_viewer.py` to inspect simulation outputs (trajectories, Ca traces)  
- **Test Suite:** Unit tests for `agent`, `field`, and `simulation` modules  

---

## Installation

```bash
pip install .
# or
pip install -r requirements.txt
```

## Usage
```python
from microglia_sim import Simulation, SimulationConfig

cfg = SimulationConfig(
    total_time=600.0,
    grid_size=(200,200),
    source_position=(100,100),
)
sim = Simulation(cfg)
sim.run(outpath="results/")
```
or use the example
```bash
python -m examples.run_parameter_sweep --jobs 4
```

## Roadmap & TODO

### Biological Model Enhancements
- **Receptor Kinetics:** Implement explicit P2Y/P2X binding/unbinding, desensitization, second‑messenger cascades (IP₃‑mediated Ca²⁺ release)  
- **Adenosine Sensing:** Include ADO gradient sensing via A₁/A₂ receptors and dual‑ligand chemotaxis  
- **Complex Ca²⁺ Dynamics:** Model ER store release, buffering, spatial gradients, and stochastic channel gating  
- **Branching Morphology:** Represent full microglial arborization with branching/retraction rules  
- **Stochasticity:** Add noise to diffusion, receptor states, and movement (Brownian fluctuations)  
- **Multiple Cues:** Integrate additional chemokines (e.g., CCL2, CX3CL1) and repellent signals  
- **Dynamic Regulation:** Allow CD39/CD73 expression to vary with activation state or feedback  
- **Validation & Calibration:** Fit model parameters against experimental data; perform sensitivity analyses  
