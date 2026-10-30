"""D-037 reproduction check on the Baumgardt line-of-sight bins of type "RV" (aeg.repro_bins, D-045 item 5).

Writes checks/d037_rv_bins.csv (one row per bin) and checks/d037_rv_clusters.csv (one row per cluster).
Every result is labelled "reconstructed binning". Reported whatever the outcome; never plotted.
"""

import csv
import html
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "pipeline"))
from aeg.repro_bins import LABEL, PublishedBin, RVStar, check_profile  # noqa: E402
from sources_io import norm_name, read_rv, read_veldis  # noqa: E402


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def main() -> int:
    src = HERE / "source"
    a = (src / "appendix.html").read_text(encoding="latin1")
    files = {norm_name(html.unescape(re.sub(r"<[^>]+>", "", n)).strip()): f
             for n, f in re.findall(r'<td[^>]*>(.*?)</td>\s*<td[^>]*>\s*<a href="([^"]+\.txt)"', a, re.S | re.I)}
    prof: dict[str, list] = {}
    names = {}
    for r in read_veldis(src / "veldis.html"):
        if r["type"] == "RV":
            k = norm_name(r["cluster"])
            names[k] = r["cluster"]
            prof.setdefault(k, []).append(PublishedBin(float(r["r_arcsec"]), int(r["n_star"]), float(r["sigma"]),
                                                       float(r["err_lo"]), float(r["err_hi"])))
    bins_out, cl_out = [], []
    for k in sorted(prof):
        if k not in files:
            cl_out.append({"cluster": names[k], "outcome": "not_testable", "reason": "no RV file in the release",
                           "n_bins": len(prof[k]), "n_pass": 0, "n_fail": 0, "n_not_testable": len(prof[k]),
                           "n_selected": "", "n_published": sum(b.n_star for b in prof[k]), "label": LABEL})
            continue
        stars = [RVStar(num(s["DCEN"]), num(s["RV"]), num(s["E_RV"]), num(s["PMEM_RV"]), num(s["P_Single"]))
                 for s in read_rv(src / "rv" / files[k])]
        res = check_profile(stars, prof[k])
        cnt = Counter(b.result.outcome for b in res.bins)
        for b in res.bins:
            rc = b.result.recomputed
            bins_out.append({"cluster": names[k], "r_mean_published_arcsec": b.published.r_mean,
                             "r_mean_rebuilt_arcsec": f"{b.r_mean_rebuilt:.2f}" if b.r_mean_rebuilt is not None else "",
                             "n_star": b.published.n_star, "sigma_published": b.published.sigma,
                             "err_lo_published": b.published.lo, "err_hi_published": b.published.hi,
                             "sigma_recomputed": f"{rc.sigma:.3f}" if rc else "",
                             "interval_recomputed": f"[{rc.lo:.3f}, {rc.hi:.3f}]" if rc else "",
                             "outcome": b.result.outcome, "reason": b.result.reason, "label": LABEL})
        overall = ("not_testable" if cnt["not_testable"] == len(res.bins) else
                   "fail" if cnt["fail"] else "pass")
        cl_out.append({"cluster": names[k], "outcome": overall, "reason": res.reason, "n_bins": len(res.bins),
                       "n_pass": cnt["pass"], "n_fail": cnt["fail"], "n_not_testable": cnt["not_testable"],
                       "n_selected": res.n_selected, "n_published": res.n_published, "label": LABEL})
    (HERE / "checks").mkdir(exist_ok=True)
    for name, rows in (("d037_rv_bins.csv", bins_out), ("d037_rv_clusters.csv", cl_out)):
        with (HERE / "checks" / name).open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
    bc = Counter(b["outcome"] for b in bins_out)
    cc = Counter(c["outcome"] for c in cl_out)
    print(f"D-037 ({LABEL}): clusters {dict(cc)}; bins {dict(bc)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
