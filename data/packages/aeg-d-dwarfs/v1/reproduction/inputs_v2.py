"""A5 conversion inputs, version 2 -> reading/conversion_inputs.csv.

Version 2 differs from version 1 (reproduction/inputs.py, frozen) only for Leo II: its distance
original, Monelli et al. 2025 (A&A 700, A201; version of record from JvH, sha256 6cf940d5...),
has now been read twice (reading/residual_reading_{1,2}_leo2.csv). D-052 item 3 applies: the
headline distance modulus (else distance); both readings must agree on it. Run
reproduction/inputs_d062.py afterwards, as before. Frozen before it was run.

Version 1 docstring follows.

A5 conversion inputs: one row per plotted-candidate system -> reading/conversion_inputs.csv.

Frozen before it was run, and before any g_obs or g_bar was computed.
Usage (from the package directory): python reproduction/inputs.py

Assembles, for every system with a plotted dispersion (reading/sigma_selection_v3.csv), the
inputs REPRODUCTION.md names, from the selections and rulings already on record:

  sigma        sigma_selection_v3 (D-038, D-051, D-055); upper limits at the stated level.
  structure    structure_selection.csv (D-052, D-054), except:
                 bootes_3   Moskowitz 2020 standard 1-Plummer fit (D-061 item 1);
                 tucana_1   Saviane 1996 via the D-053 resolution (mcc_resolution.csv): Re is a
                            physical "effective geometric radius" (circularised) at Saviane's
                            own distance modulus 24.69; it is turned back into an angle at that
                            distance (the same exact rescaling as D-058).
  R_h          circularised: a sqrt(1 - e) for semi-major values (D-048 item 2), r_h as printed
               for circularised values.
  distance     structure_selection.csv (D-052), except:
                 leo_1      Stetson 2014 midpoint 22.155 (-0.175/+0.165) (D-061 item 4);
                 leo_4/5    Medina 2018 151.4 +- 4.4 / 169.0 +- 4.4 kpc (residual reading);
                 segue_2    Boettcher 2013 BHB 34.4 +- 2.6 kpc (D-055 item 8);
                 tucana_1   Bernard 2009 24.74 +- 0.12 (D-053 resolution);
                 leo_2      Monelli 2025 not yet read: no distance, not plotted.
  m_V,0        structure_selection.csv (D-052 item 4), else rebuilt as M_V + the paper's modulus:
                 Munoz 2018 systems: 5 log10(D_Table1 / 10 pc) (D-061 item 3);
                 andromeda_06/07: McConnachie 2005 moduli 24.47 / 24.41 (cited by McConnachie 2006);
                 phoenix_1: van de Rydt 1991 M_V -9.9 +- 0.4 with 23.1 +- 0.1 (D-061 item 5);
                 leo_t: de Jong 2008 M_V -8.0 with 23.1 +- 0.2 (D-061 item 6);
                 tucana_5: Simon 2020 M_V -1.1 (+0.5/-0.6) with 55 kpc (D-061 item 7);
                 tucana_1: Saviane 1996 M_V -9.55 +- 0.27 with its own 24.69;
                 bootes_3: Correnti 2009 M_V -5.8 +- 0.5, distance-independent (D-061 item 2).
  L_V          10^(-0.4 (m_V,0 - mu - 4.85)); M_V,sun = 4.85 (McLaughlin & van der Marel 2005,
               sec. 4, the Upsilon_V source). For bootes_3, 10^(-0.4 (M_V - 4.85)).
  Upsilon_V    reading/upsilon_v.csv (D-059, D-060).
  gas          reproduction/gas.py on reading/gas_values.csv at the package distance (D-058).
Errors are carried as printed (minus/plus); a modulus error maps to the distance by
D = 10^(mu/5 + 1) pc at mu -+ err. Nothing here computes g_obs or g_bar.
"""

from __future__ import annotations

import csv
import math
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
R = PKG / "reading"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gas import gas_for_system  # noqa: E402

MV_SUN = 4.85


def num(x) -> float | None:
    if x is None:
        return None
    t = str(x).strip().replace("−", "-").replace("–", "-").lstrip("~≃ ")
    m = re.match(r"^[-+]?\d+(\.\d+)?", t)
    return float(m.group(0)) if m else None


def errs(s: str) -> tuple[float | None, float | None]:
    if not s or "/" not in s:
        return None, None
    a, b = s.split("/", 1)
    return num(a), num(b)


def mu_of_kpc(d: float) -> float:
    return 5.0 * math.log10(d * 100.0)


def kpc_of_mu(mu: float) -> float:
    return 10 ** (mu / 5.0 + 1.0) / 1000.0


MUNOZ = "Munoz2018ApJ...860...66M"
DIST_OVERRIDE = {  # key: (kind, value, err_minus, err_plus, source, flag)
    "leo_1": ("mu", 22.155, 0.175, 0.165, "Stetson 2014, midpoint of 22.06 +- 0.08 to 22.25 +- 0.07", "distance_range_midpoint"),
    "leo_4": ("kpc", 151.4, 4.4, 4.4, "Medina 2018, RR Lyrae mean", ""),
    "leo_5": ("kpc", 169.0, 4.4, 4.4, "Medina 2018, RR Lyrae mean", ""),
    "segue_2": ("kpc", 34.4, 2.6, 2.6, "Boettcher 2013, BHB stars (D-055 item 8)", ""),
    "tucana_1": ("mu", 24.74, 0.12, 0.12, "Bernard 2009, RR Lyrae, reddening-corrected (D-053)", ""),
}
MAG_OVERRIDE = {  # key: (M_V, e_minus, e_plus, modulus or None, mod_err, source, flag)
    "andromeda_06": (-11.5, 0.2, 0.2, 24.47, 0.07, "McConnachie 2006 M_V + McConnachie 2005 modulus", ""),
    "andromeda_07": (-13.3, 0.3, 0.3, 24.41, 0.10, "McConnachie 2006 M_V + McConnachie 2005 modulus", ""),
    "phoenix_1": (-9.9, 0.4, 0.4, 23.1, 0.1, "van de Rydt 1991 M_V + adopted modulus (D-061 item 5)", "mv_modulus_assumed"),
    "leo_t": (-8.0, None, None, 23.1, 0.2, "de Jong 2008 M_V + red-clump modulus (D-061 item 6)", "mv_modulus_assumed"),
    "tucana_5": (-1.1, 0.6, 0.5, mu_of_kpc(55.0), None, "Simon 2020 M_V + Table 6 distance 55 kpc (D-061 item 7)", "mv_modulus_assumed"),
    "tucana_1": (-9.55, 0.27, 0.27, 24.69, 0.16, "Saviane 1996 M_V + its own TRGB modulus (D-053)", ""),
    "bootes_3": (-5.8, 0.5, 0.5, None, None, "Correnti 2009 M_V, distance-independent (D-061 item 2)", "mv_distance_independent"),
}


def main() -> int:
    sel = [r for r in csv.DictReader(open(R / "sigma_selection_v3.csv", encoding="utf-8")) if r["sigma"].strip() or r["limit"].strip()]
    st = {r["key"]: r for r in csv.DictReader(open(R / "structure_selection.csv", encoding="utf-8"))}
    ups = {r["key"]: r for r in csv.DictReader(open(R / "upsilon_v.csv", encoding="utf-8"))}
    gasv = {r["key"]: r for r in csv.DictReader(open(R / "gas_values.csv", encoding="utf-8"))}
    munoz_d = {r["key"]: num(r["value"]) for r in csv.DictReader(open(R / "residual_reading_1.csv", encoding="utf-8"))
               if r["paper"] == MUNOZ and r["quantity"] == "distance" and r["value"].strip()}
    munoz_d2 = {r["key"]: num(r["value"]) for r in csv.DictReader(open(R / "residual_reading_2.csv", encoding="utf-8"))
                if r["paper"] == MUNOZ and r["quantity"] == "distance" and r["value"].strip()}
    if munoz_d != munoz_d2:
        raise SystemExit("Munoz Table 1 readings differ")
    sv = list(csv.DictReader(open(R / "structure_values_all.csv", encoding="utf-8")))
    out = []
    for s in sel:
        k = s["key"]
        t = st[k]
        flags, notes = [], []
        # sigma
        row = {"key": k, "sigma_paper": s["default_paper"], "sigma": s["sigma"], "sigma_err_minus": s["err_minus"],
               "sigma_err_plus": s["err_plus"], "sigma_limit": s["limit"], "sigma_limit_level": s["limit_level"]}
        # structure
        rh, rh_unit, conv, e = num(t["r_h"]), t["r_h_unit"], t["rh_convention"], num(t["ellipticity"]) or 0.0
        rh_src = t["r_h_loc"]
        if k == "bootes_3":
            pick = {r["quantity"]: r for r in sv if r["key"] == k and r["role"] == "structure"
                    and "1-Plummer" in r["variant"] and r["quantity"] in ("r_h", "ellipticity")}
            rh, rh_unit, conv, e = num(pick["r_h"]["value"]), "arcmin", "circularised", num(pick["ellipticity"]["value"])
            rh_src = f"{pick['r_h']['paper']} {pick['r_h']['location']} (1-Plummer, D-061 item 1)"
        if k == "tucana_1":
            rh_pc = 205.0
            rh = rh_pc / (kpc_of_mu(24.69) * 1000.0) * (180.0 / math.pi) * 60.0
            rh_unit, conv, e = "arcmin", "circularised", 0.48
            rh_src = "Saviane 1996 Re = 205 +- 32 pc at (m-M)0 = 24.69, as an angle (D-053; D-058 rescaling)"
            flags.append("rh_from_physical_at_source_distance")
        if rh is None or rh_unit not in ("arcmin", "arcsec"):
            row.update(status="not plotted", reason="no angular half-light radius")
            out.append(row)
            continue
        rh_arcmin = rh / 60.0 if rh_unit == "arcsec" else rh
        if conv.startswith("semi-major"):
            R_arcmin = rh_arcmin * math.sqrt(1.0 - e)
            if "assumed" in conv:
                flags.append("rh_semimajor_assumed")
        else:
            R_arcmin = rh_arcmin
        row.update(rh_printed=f"{rh:.6g}", rh_unit=rh_unit, rh_convention=conv, ellipticity=f"{e:g}",
                   R_h_arcmin=f"{R_arcmin:.6g}", rh_source=rh_src)
        # distance
        if k in DIST_OVERRIDE:
            kind, v, em, ep, src, fl = DIST_OVERRIDE[k]
            if fl:
                flags.append(fl)
        elif k == "leo_2":
            heads = []
            for i in (1, 2):
                hs = {}
                for x in csv.DictReader(open(R / f"residual_reading_{i}_leo2.csv", encoding="utf-8")):
                    if x["variant"].strip().lower().startswith("headline") and x["value"].strip() \
                            and x["quantity"] in ("distance_modulus", "distance"):
                        hs.setdefault(x["quantity"], set()).add((num(x["value"]), num(x["err_minus"]), num(x["err_plus"])))
                q = "distance_modulus" if "distance_modulus" in hs else "distance"
                heads.append((q, hs.get(q, set())))
            if heads[0] != heads[1] or len(heads[0][1]) != 1:
                row.update(status="not plotted", reason="Leo II distance: readings differ or no single headline (for JvH)",
                           flags=" ".join(flags))
                out.append(row)
                continue
            q, (v, em, ep) = heads[0][0], next(iter(heads[0][1]))
            kind = "mu" if q == "distance_modulus" else "kpc"
            src = "Monelli2025A&A...700A.201M (headline; version of record)"
        else:
            v = num(t["distance"])
            em, ep = errs(t["distance_err"])
            kind = "mu" if t["distance_quantity"] == "distance_modulus" else "kpc"
            src = t["distance_loc"]
            if v is None:
                row.update(status="not plotted", reason="no distance", flags=" ".join(flags))
                out.append(row)
                continue
        if kind == "mu":
            mu, d = v, kpc_of_mu(v)
            d_lo = d - kpc_of_mu(v - em) if em is not None else None
            d_hi = kpc_of_mu(v + ep) - d if ep is not None else None
        else:
            d, mu = v, mu_of_kpc(v)
            d_lo, d_hi = em, ep
        row.update(distance_kpc=f"{d:.6g}", distance_err_minus="" if d_lo is None else f"{d_lo:.4g}",
                   distance_err_plus="" if d_hi is None else f"{d_hi:.4g}", mu=f"{mu:.4f}", distance_source=src)
        # magnitude
        m0, m_lo, m_hi, msrc, L = None, None, None, "", None
        if k in MAG_OVERRIDE:
            MV, em_, ep_, mod, mod_e, msrc, fl = MAG_OVERRIDE[k]
            if fl:
                flags.append(fl)
            if mod is None:
                L = 10 ** (-0.4 * (MV - MV_SUN))
                m_lo, m_hi = em_, ep_
            else:
                m0 = MV + mod
                m_lo = math.hypot(em_ or 0.0, mod_e or 0.0) or None
                m_hi = math.hypot(ep_ or 0.0, mod_e or 0.0) or None
        elif t["m_V0"].strip():
            m0 = num(t["m_V0"])
            msrc = t["m_V0_route"]
            if t["M_V"].strip() and not t["m_V0_route"].startswith("printed"):
                m_lo, m_hi = errs(t["M_V_err"])
        elif k in munoz_d and MUNOZ in t["M_V_loc"]:
            MV = num(t["M_V"])
            m0 = MV + mu_of_kpc(munoz_d[k])
            m_lo, m_hi = errs(t["M_V_err"])
            msrc = f"Munoz 2018 M_V + 5 log10(D/10 pc), D = {munoz_d[k]:g} kpc (Table 1; D-061 item 3)"
            flags.append("mv_distance_from_table1")
        if L is None and m0 is None:
            row.update(status="not plotted", reason="no extinction-corrected magnitude", flags=" ".join(flags))
            out.append(row)
            continue
        if L is None:
            L = 10 ** (-0.4 * (m0 - mu - MV_SUN))
        row.update(m_V0="" if m0 is None else f"{m0:.4f}", mag_err_minus="" if m_lo is None else f"{m_lo:.4g}",
                   mag_err_plus="" if m_hi is None else f"{m_hi:.4g}", mag_source=msrc, L_V=f"{L:.6g}")
        # Upsilon_V
        u = ups.get(k, {})
        if not u.get("upsilon_v"):
            row.update(status="not plotted", reason="no Upsilon_V (no metallicity, D-059)", flags=" ".join(flags + u.get("flags", "").split()))
            out.append(row)
            continue
        row.update(upsilon_v=u["upsilon_v"], upsilon_v_low=u["upsilon_v_low"], upsilon_v_high=u["upsilon_v_high"], feh=u["feh"])
        flags += u["flags"].split()
        # gas
        g = gas_for_system(gasv.get(k), d)
        row.update(gas_status=g["gas_status"], m_gas_rh=f"{g['m_gas_rh']:.6g}",
                   m_hi_pkg="" if "m_hi_pkg" not in g else f"{g['m_hi_pkg']:.6g}",
                   d_putman_kpc=str(g.get("d_putman_kpc", "")))
        flags += g["flags"].split()
        row.update(status="plotted", reason="", flags=" ".join(dict.fromkeys(f for f in flags if f)))
        out.append(row)
    names = list(dict.fromkeys(c for r in out for c in r))
    with open(R / "conversion_inputs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, restval="")
        w.writeheader()
        w.writerows(out)
    n = sum(1 for r in out if r.get("status") == "plotted")
    print(f"{len(out)} systems; plotted {n}; not plotted {len(out) - n}: "
          + "; ".join(f"{r['key']} ({r['reason']})" for r in out if r.get("status") != "plotted"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
