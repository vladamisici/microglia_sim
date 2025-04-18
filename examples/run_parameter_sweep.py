"""
Example script to perform a parameter sweep over chemotactic and sensitivity parameters,
run simulations in parallel, and generate analysis plots for each condition.
"""
import sys

import sys, os, itertools
from concurrent.futures import ProcessPoolExecutor, as_completed

# ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from microglia_sim.config    import SimulationConfig
from microglia_sim.simulation import Simulation
from microglia_sim.analysis   import Analyzer

# Parameter ranges to sweep
chemotactic_coeffs = [1.0, 2.0, 4.0]
ado_sensitivities   = [0.5, 1.0, 2.0]
adp_sensitivities   = [5.0, 10.0, 20.0]

# Output directory
results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sweep_results'))
os.makedirs(results_dir, exist_ok=True)

# Function to run one parameter set
def run_task(params):
    cc, ado, adp = params
    # configure simulation
    cfg = SimulationConfig()
    # cheap test mode for speed
    cfg.grid_size      = (100, 100)
    cfg.total_time     = 1200.0    # seconds
    cfg.solver.dt      = 0.05    # seconds
    cfg.record_every   = 20      # steps
    # ensure source and initial tips are within the new grid bounds
    mid_x = cfg.grid_size[0] // 2
    mid_y = cfg.grid_size[1] // 2
    cfg.source_position = (mid_x, mid_y)
    cfg.initial_tips = (
        (mid_x-10, mid_y-10),
        (mid_x+10, mid_y-10),
        (mid_x-10, mid_y+10),
        (mid_x+10, mid_y+10),
    )
    # set parameters
    cfg.process.chemotactic_coeff = cc
    cfg.process.ado_sensitivity   = ado
    cfg.process.adp_sensitivity   = adp

    label   = f'cc{cc}_ado{ado}_adp{adp}'
    outpath = os.path.join(results_dir, label)
    os.makedirs(outpath, exist_ok=True)

    # run simulation
    sim = Simulation(cfg)
    sim.run(outpath)

    # analyze and save
    result_file = os.path.join(outpath, 'results.pkl')
    analyzer   = Analyzer(result_file)
    analyzer.plot_trajectories(savepath=os.path.join(outpath, 'trajectories.png'))
    analyzer.plot_Ca_traces   (savepath=os.path.join(outpath, 'Ca_traces.png'))
    return label

# Build task list
tasks = list(itertools.product(chemotactic_coeffs, ado_sensitivities, adp_sensitivities))

# Run in parallel
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parallel parameter sweep')
    parser.add_argument('-j', '--jobs', type=int, default=2, help='number of parallel workers')
    args = parser.parse_args()

    print(f"Starting sweep with {args.jobs} workers...")
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(run_task, t): t for t in tasks}
        for fut in as_completed(futures):
            try:
                label = fut.result()
                print(f'[✔] Completed {label}')
            except Exception as e:
                params = futures[fut]
                print(f'[✖] Failed {params}: {e}')
