"""A6 strong lensing: apply the frozen precedence rule (docs/methods/A6S_PRECEDENCE.md,
D-065, sections 2 and 3) to source METADATA only.

Input:  a6s_options.csv  (one row per source option: survey, scope, record, side, year,
        number of lenses, original/re-model, model class, re-use, sigma prior,
        IMF, band count, per-object fit, aperture, membership). No measured value.
        a6s_records.csv, arxiv_licences.csv (for the inventory table).
Output: precedence_result.csv and inventory_tables.md (written next to this file).

Run:    python -I rank_a6s.py

Rules coded (quoted from A6S_PRECEDENCE.md):
  §2.1 originals first; §2.2 a full model over the image-separation estimate;
  §2.3 among a survey's own models the most recent, unless a later paper only
       re-uses the earlier one.
  §3.3 excluded as default: priors using the lens's own sigma; lensing or dynamical
       masses (and, by D-063 item 1, IMF-free fits); then more photometric bands;
       then a per-object population fit before a fixed-age scaling; then the most recent.
  §3.1 / §3.2 are reported as flags (profile integration needed; single-IMF range).
Nothing is decided where the metadata cannot decide: such cases are flagged.
"""
import csv
import os
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))


def read(name):
    with open(os.path.join(HERE, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def usable(r):
    return r["usable"].strip().startswith("Y")


def year(r):
    return int(r["year"])


def nint(s):
    s = (s or "").strip()
    return int(s) if s else None


# ---------- §2 observed side ----------
FULL = {"full"}


def rank_observed(rows):
    flags = []
    pool = [r for r in rows if usable(r)]
    if not pool:
        return None, [], ["no usable observed-side source"]
    orig = [r for r in pool if r["original"] == "Y"]
    stage = orig if orig else pool                       # §2.1
    if not orig:
        flags.append("no original-survey model: default taken from re-models")
    full = [r for r in stage if r["model_class"] in FULL]  # §2.2
    if full:
        stage = full
    else:
        other_full = [r for r in pool if r["model_class"] in FULL]
        if other_full:
            flags.append("CONFLICT: originals give only an image-separation/ring estimate while a "
                         "re-model is a full model (§2.1 vs §2.2 and D-063 item 2): returns to JvH")
        flags.append("default is not a full lens model (" + stage[0]["model_class"] + ")")
    own = [r for r in stage if r["reuses_earlier_model"] != "Y"]  # §2.3
    if own:
        stage = own
    stage = sorted(stage, key=year, reverse=True)
    if len(stage) > 1 and year(stage[0]) == year(stage[1]):
        flags.append("tie on year between " + stage[0]["record"] + " and " + stage[1]["record"])
    d = stage[0]
    if d["membership"] != "listed":
        flags.append("conditional: membership of this system in " + d["record"] + " not checked")
    alts = [r for r in pool if r is not d]
    return d, alts, flags


# ---------- §3 stellar mass ----------
PER_OBJECT = {"Y": 2, "partial": 1, "disputed": 1, "N": 0, "unverified": 1}


def excluded_reason(r):
    if not usable(r):
        return "not usable: " + r["usable"]
    if r["sigma_prior"] == "Y":
        return "prior uses the lens's own sigma (§3.3; D-063 item 3)"
    if r["lensing_or_dynamical"] == "Y":
        return "lensing or dynamical mass (§3.3)"
    imf = r["imf"].lower()
    if imf.startswith("fitted"):
        return "IMF fitted, not a fixed named IMF (D-063 item 1)"
    if imf.startswith("unverified"):
        return "IMF not verified at source"
    return ""


def _cmp(x, y):
    return (x > y) - (x < y)


def _later(a, b):
    """Criteria after band count: per-object fit, then most recent.
    Returns (+1 if a wins, -1 if b wins, 0 tie, soft) where soft is True when the
    per-object step decides on a partial or disputed reading against the year order."""
    pa, pb = PER_OBJECT.get(a["per_object_fit"], 1), PER_OBJECT.get(b["per_object_fit"], 1)
    if pa != pb:
        res = 1 if pa > pb else -1
        soft = bool({"partial", "disputed", "unverified"} & {a["per_object_fit"], b["per_object_fit"]})
        return res, soft and _cmp(year(a), year(b)) != res
    return _cmp(year(a), year(b)), False


def better(a, b, flags):
    """True if a outranks b under §3.3 (after exclusions).
    Band counts are [min, max] ranges; the order is evaluated at both extremes
    (a at min vs b at max, a at max vs b at min). If the extremes disagree the
    result is flagged as undetermined and the min-vs-min order is used provisionally."""
    amin, amax = nint(a["n_bands_min"]), nint(a["n_bands_max"])
    bmin, bmax = nint(b["n_bands_min"]), nint(b["n_bands_max"])
    if None in (amin, amax, bmin, bmax):
        flags.append("band count not read for %s or %s: order provisional" % (a["record"], b["record"]))
        scen = [0]
        prov = 0
    else:
        scen = [_cmp(amin, bmax), _cmp(amax, bmin)]
        prov = _cmp(amin, bmin)
    results, soft_any = [], False
    for bo in scen:
        if bo != 0:
            results.append(bo)
        else:
            o, soft = _later(a, b)
            soft_any = soft_any or soft
            results.append(o)
    if len(set(results)) > 1:
        flags.append("band count order undetermined between %s and %s (outcome depends on per-system band counts): provisional" % (a["record"], b["record"]))
        outcome = prov if prov != 0 else _later(a, b)[0]
    else:
        outcome = results[0]
    if soft_any:
        flags.append("per-object criterion decided on a partial or disputed reading (%s vs %s)" % (a["record"], b["record"]))
    if outcome == 0:
        flags.append("full tie between %s and %s" % (a["record"], b["record"]))
    return outcome > 0


def rank_stellar(rows):
    flags, excluded = [], []
    elig = []
    for r in rows:
        why = excluded_reason(r)
        if why:
            excluded.append((r, why))
        else:
            elig.append(r)
    if not elig:
        return None, [r for r, _ in excluded], ["no eligible default stellar mass"] + \
            ["%s excluded: %s" % (r["record"], w) for r, w in excluded]
    best = elig[0]
    for r in elig[1:]:
        if better(r, best, flags):
            best = r
    # flags from §3.1 / §3.2
    ap = best["aperture"]
    if ap.startswith("total") or ap.startswith("profile"):
        flags.append("mstar_in_RE_from_profile needed (default prints %s)" % ap)
    elif ap.startswith("disputed"):
        flags.append("aperture disputed between readers: read at source before packaging")
    elif ap not in ("inside R_E (printed)", "inside R_E (luminosity × M/L)", "inside R_E (fraction × R60 M_E)"):
        flags.append("aperture is '%s': check it matches the default R_E" % ap)
    if best["imf"].lower().startswith("single"):
        flags.append("single IMF printed: range from the model paper's Chabrier-to-Salpeter ratio (§3.2)")
    if best["membership"] != "listed":
        flags.append("conditional: membership of this system in " + best["record"] + " not checked")
    for r, w in excluded:
        flags.append("%s excluded as default: %s" % (r["record"], w))
    alts = [r for r in rows if r is not best and usable(r)]
    return best, alts, flags


def main():
    opts = read("a6s_options.csv")
    groups = OrderedDict()
    for r in opts:
        groups.setdefault((r["survey"], r["scope"]), []).append(r)

    out_rows = []
    for (survey, scope), rows in groups.items():
        od, oalts, oflags = rank_observed([r for r in rows if r["side"] == "observed"])
        st_rows = [r for r in rows if r["side"] == "stellar"]
        sd, salts, sflags = rank_stellar(st_rows) if st_rows else (None, [], ["no stellar-mass source"])
        zrows = [r for r in rows if r["side"] == "redshift" and usable(r)]
        n_both = ""
        if od and sd:
            ns = [int(od["n_lenses"]), int(sd["n_lenses"])] + [int(z["n_lenses"]) for z in zrows]
            n_both = str(min(ns))
        else:
            n_both = "0"
        out_rows.append(OrderedDict([
            ("survey", survey), ("scope", scope),
            ("observed_default", od["record"] if od else ""),
            ("observed_alternatives", "; ".join(sorted({r["record"] for r in oalts}))),
            ("observed_flags", " | ".join(oflags)),
            ("stellar_default", sd["record"] if sd else ""),
            ("stellar_alternatives", "; ".join(sorted({r["record"] for r in salts}))),
            ("stellar_flags", " | ".join(sflags)),
            ("redshift_from", "; ".join(z["record"] for z in zrows)),
            ("n_both_upper_bound", n_both),
        ]))

    with open(os.path.join(HERE, "precedence_result.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    # ---------- markdown fragments ----------
    lic = {r["arxiv"]: r["arxiv_licence"] for r in read("arxiv_licences.csv")}
    recs = read("a6s_records.csv")
    md = []
    md.append("### Per-record inventory (generated from `a6s_records.csv`)\n")
    md.append("| # | Code | Citation | arXiv (licence at arXiv) | Survey | Side(s) supplied | N lenses | Lens z as read | Evidence tier and data location | Licence at the data location | Fetchable from this workspace |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in recs:
        ax = []
        for a in [x.strip() for x in r["arxiv"].split(";") if x.strip() and x.strip() != "—"]:
            ax.append("%s (%s)" % (a, lic.get(a, "not read")))
        cells = [r["record"], r["code"], r["citation"], "; ".join(ax) or "—", r["survey"], r["sides"],
                 r["n_lenses"], r["lens_z_as_read"], r["tier_and_location"], r["licence_at_location"],
                 r["fetch_from_workspace"]]
        md.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |")
    md.append("")
    md.append("### Precedence result (generated from `a6s_options.csv`)\n")
    md.append("| Survey | Scope | Observed default | Observed alternatives | Stellar-mass default | Stellar-mass alternatives | Redshifts from | N with both (upper bound) | Flags |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for o in out_rows:
        fl = [x for x in (o["observed_flags"].split(" | ") + o["stellar_flags"].split(" | ")) if x]
        md.append("| " + " | ".join([o["survey"], o["scope"], o["observed_default"] or "none",
                                      o["observed_alternatives"] or "—", o["stellar_default"] or "none",
                                      o["stellar_alternatives"] or "—", o["redshift_from"] or "(with the observed side)",
                                      o["n_both_upper_bound"], "<br>".join(fl) or "—"]) + " |")
    with open(os.path.join(HERE, "inventory_tables.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    for o in out_rows:
        print("%-18s %-28s obs=%-5s stellar=%-5s both<=%s" % (o["survey"], o["scope"], o["observed_default"] or "none",
                                                           o["stellar_default"] or "none", o["n_both_upper_bound"]))


if __name__ == "__main__":
    main()
