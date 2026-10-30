"""REPRODUCTION.md test 4 (pre-registered decision): how Harris r_c is read.

(a) median |log10(r_c,Harris / r0,MvdM)|, (b) median |log10(r_c,Harris / R_c,MvdM)|, both in pc at the
Harris distance (r0 and R_c rescaled from McLaughlin & van der Marel's Dist). (a) <= (b): Harris r_c is read
as r0 (D-045). Also the median and scatter of c_Harris - Conc. Writes checks/test4_harris_rc.csv.
"""

import csv
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from sources_io import norm_name, read_harris, read_votable  # noqa: E402

ARCSEC_PER_RAD = 206264.806


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def main() -> int:
    harris = {norm_name(k): v for k, v in read_harris(HERE / "source/mwgc.dat").items()}
    rows = []
    for r in read_votable(HERE / "source/mvdm05/J_ApJS_161_304_models.vot"):
        if not (r["Cluster"].startswith("MW-") and r["Mod"] == "K"):
            continue
        h = harris.get(norm_name(r["Cluster"]))
        if not h or num(h.get("III:c")) is None or num(h.get("III:r_c")) is None or num(h.get("I:R_Sun")) is None:
            continue
        dh, dm = float(h["I:R_Sun"]), float(r["Dist"])
        rc_h = float(h["III:r_c"]) * 60.0 / ARCSEC_PER_RAD * dh * 1000.0
        r0 = float(r["r0pc"]) * dh / dm
        rc_m = 10 ** float(r["Rc"]) * dh / dm
        rows.append({"cluster": r["Cluster"], "harris_c": h["III:c"], "harris_flag": h.get("III:flags", ""),
                     "harris_rc_arcmin": h["III:r_c"], "mvdm_conc": r["Conc"], "mvdm_r0pc": r["r0pc"], "mvdm_Rc": r["Rc"],
                     "a_abs_log_rc_over_r0": abs(math.log10(rc_h / r0)), "b_abs_log_rc_over_Rc": abs(math.log10(rc_h / rc_m)),
                     "c_harris_minus_conc": float(h["III:c"]) - float(r["Conc"])})
    a = statistics.median(x["a_abs_log_rc_over_r0"] for x in rows)
    b = statistics.median(x["b_abs_log_rc_over_Rc"] for x in rows)
    dc = [x["c_harris_minus_conc"] for x in rows]
    (HERE / "checks").mkdir(exist_ok=True)
    with (HERE / "checks/test4_harris_rc.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for x in rows:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in x.items()})
    print(f"test 4: n = {len(rows)}; (a) median |log rc_H/r0| = {a:.4f}; (b) median |log rc_H/R_c| = {b:.4f}")
    print(f"        c_Harris - Conc: median {statistics.median(dc):+.3f}, scatter (st. dev.) {statistics.pstdev(dc):.3f}")
    print("        decision:", "Harris r_c read as r0 (D-045 reading kept)" if a <= b else
          "D-045 reading rejected: Harris-only clusters recorded, not plotted; returns to JvH")
    return 0 if a <= b else 1


if __name__ == "__main__":
    sys.exit(main())
