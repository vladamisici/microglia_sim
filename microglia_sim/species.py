"""
Defines species indices and reaction kinetics.
"""
from typing import Dict, Tuple

SPECIES = ['ATP','ADP','AMP','ADO']
Index = dict(ATP=0, ADP=1, AMP=2, ADO=3)

def ectonucleotidase_rates(conc: Tuple[float,float,float,float], ecto) -> Tuple[float,float,float,float]:
    """Compute net production/consumption rates via Michaelis-Menten."""
    atp, adp, amp, ado = conc
    r1 = ecto.Vmax_ATP_ADP * atp/(ecto.Km_ATP_ADP + atp) * ecto.CD39_level
    r2 = ecto.Vmax_ADP_AMP * adp/(ecto.Km_ADP_AMP + adp) * ecto.CD39_level
    r3 = ecto.Vmax_AMP_ADO * amp/(ecto.Km_AMP_ADO + amp) * ecto.CD73_level
    # net changes: ATP→ADP, ADP→AMP, AMP→ADO
    return (-r1, r1 - r2, r2 - r3, r3)