"""REPRODUCTION.md test 2: King (1966) reproduces McLaughlin & van der Marel (2005) King fits.

Run from the package directory after `python -m aeg.fetch .`:
    python reproduction/test2_king_fits.py
Writes checks/test2_king_fits.csv (one row per King fit) and prints the outcome.
The test is as frozen: every Mod = K row within 0.02 of Conc and 0.02 dex of Rc and Rh.
"""

import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "pipeline"))

from aeg.king66 import King66  # noqa: E402
from sources_io import read_votable  # noqa: E402

TOL = 0.02


def main() -> int:
    rows = [r for r in read_votable(HERE / "source/mvdm05/J_ApJS_161_304_models.vot") if r["Mod"] == "K"]
    out = []
    for r in rows:
        m = King66(float(r["W0/gamma"]), float(r["r0pc"]))
        d_conc = m.concentration - float(r["Conc"])
        d_rc = math.log10(m.half_power_radius()) - float(r["Rc"])
        d_rh = math.log10(m.half_light_radius()) - float(r["Rh"])
        ok = max(abs(d_conc), abs(d_rc), abs(d_rh)) <= TOL
        # diagnostic only: the table's own angular scale radius times its distance, in pc
        r0_from_arcsec = float(r["r0"]) * float(r["Dist"]) * 1000.0 / 206264.806
        out.append({"cluster": r["Cluster"], "W0": r["W0/gamma"], "r0pc": r["r0pc"], "Conc": r["Conc"], "Rc": r["Rc"],
                    "Rh": r["Rh"], "d_conc": f"{d_conc:+.4f}", "d_logRc": f"{d_rc:+.4f}", "d_logRh": f"{d_rh:+.4f}",
                    "within_tolerance": ok,
                    "diag_log_r0pc_vs_r0arcsec_x_dist": f"{math.log10(float(r['r0pc']) / r0_from_arcsec):+.4f}"})
    (HERE / "checks").mkdir(exist_ok=True)
    with (HERE / "checks/test2_king_fits.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader(); w.writerows(out)
    n_bad = sum(not x["within_tolerance"] for x in out)
    print(f"test 2: {len(out) - n_bad} of {len(out)} King fits within tolerance -> {'PASS' if n_bad == 0 else 'FAIL'}")
    for x in out:
        if not x["within_tolerance"]:
            print("  outside:", x["cluster"], x["d_conc"], x["d_logRc"], x["d_logRh"])
    return 0 if n_bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
