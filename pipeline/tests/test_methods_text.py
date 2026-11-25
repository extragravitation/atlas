"""Arithmetic and selection checks of the written methods (docs/methods/datasets/*.md, D-113 item 2).

What these tests show: following only the steps the methods pages state, the inputs each row names
(read from the Atlas's own observables table and, where noted, its stored intermediate columns) give
the published g_obs and g_bar, for default and alternative rows; and, where cheap, that the stated
selection rules pick the rows the package uses.

What they do not show:
- that the inputs were read correctly from the sources (the audit does that);
- that the text is complete for a reader who does not know the code. They were written by the
  author of the text, who does know it. Only a blind reading can test completeness.
Steps not re-derived here, because their inputs are not in the tables, are listed per test.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest
from astropy.table import Table

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))

G = 6.67430e-11
MSUN = 1.98840987e30
PC = 3.0856775814913673e16
REL = 1e-9


def tables(ds: str):
    p = ROOT / "data/packages" / ds / "v3/tables"
    m = Table.read(p / "measurements.ecsv", format="ascii.ecsv")
    o = Table.read(p / "observables.ecsv", format="ascii.ecsv")
    return m, {r["observable_id"]: r for r in o}


def ids(s) -> list[str]:
    return [x for x in str(s or "").split(";") if x and x != "--"]


def defaults(m):
    return [r for r in m if str(r["role"]) in ("", "default", "--")]


def close(a: float, b: float, rel: float = REL) -> bool:
    return abs(a - b) <= rel * max(abs(a), abs(b))


# --------------------------------------------------------------------------- globular clusters

def test_gc_text_reproduces_every_default_row():
    from aeg.king66 import King66
    m, ob = tables("aeg-d-gc-baumgardt")
    rows = defaults(m)
    assert len(rows) == 62
    for r in rows:
        obs = [ob[i] for i in ids(r["observed_from"])]
        bar = [ob[i] for i in ids(r["baryonic_from"])]
        par = {str(o["x_gc_baumgardt_parameter"]): float(o["value"]) for o in bar}
        bins = sorted((float(o["x_gc_baumgardt_r_arcsec"]), float(o["value"])) for o in obs if o["quantity"] == "sigma_los")
        assert {str(o["x_gc_baumgardt_dataset"]) for o in obs} == {str(r["x_gc_baumgardt_dataset"])}
        # §4 step 1-2: King (1966) model from W0, r0 (arcsec)
        k = King66(par["McLaughlin & van der Marel 2005 King fit: W0/gamma"], par["McLaughlin & van der Marel 2005 King fit: r0"])
        rad = [b[0] for b in bins]
        # step 3: edges
        edges = [0.0] + [0.5 * (rad[i] + rad[i + 1]) for i in range(len(rad) - 1)] + [rad[-1] + 0.5 * (rad[-1] - rad[-2])]
        # step 4-5
        w = [k.cumulative_fraction(edges[i + 1]) - k.cumulative_fraction(edges[i]) for i in range(len(bins))]
        sig = math.sqrt(sum(wi * s * s for wi, (_, s) in zip(w, bins)) / sum(w))
        assert sum(w) >= 0.80 and len(bins) >= 2
        # step 6-9
        rh = 10 ** par["McLaughlin & van der Marel 2005 King fit: Rh"] * par["R_Sun (horizontal branch)"] / par["McLaughlin & van der Marel 2005 King fit: Dist"]
        r_half = 4.0 / 3.0 * rh * PC
        lv = 10 ** (-0.4 * (par["M_V,t"] - 4.85))
        g_obs = 3.0 * (sig * 1e3) ** 2 / r_half
        g_bar = G * 0.5 * lv * par["BC03 + Chabrier disk IMF"] * MSUN / r_half ** 2
        assert close(g_obs, float(r["g_obs"]), 1e-6), (r["measurement_id"], g_obs, float(r["g_obs"]))
        assert close(g_bar, float(r["g_bar"]), 1e-9), (r["measurement_id"], g_bar, float(r["g_bar"]))


# --------------------------------------------------------------------------- dwarf galaxies

def test_dwarfs_text_reproduces_every_default_row():
    m, ob = tables("aeg-d-dwarfs")
    rows = defaults(m)
    assert len(rows) == 64
    for r in rows:
        q = {}
        for i in ids(r["observed_from"]) + ids(r["baryonic_from"]):
            q.setdefault(str(ob[i]["quantity"]), ob[i])
        sig = float(q["sigma_los"]["value"])
        d_kpc = float(q["distance"]["value"])
        rh = float(q["half_light_radius"]["value"])
        rh = rh / 60.0 if str(q["half_light_radius"]["unit"]) == "arcsec" else rh
        conv = str(q["half_light_radius"]["x_dwarfs_parameter"])
        eps = float(q["structural_param"]["value"])
        R_arcmin = rh * math.sqrt(1.0 - eps) if "semi-major" in conv else rh           # §3 step 2
        R_pc = R_arcmin / 60.0 * math.pi / 180.0 * d_kpc * 1000.0                       # §3 step 7
        r_half = 4.0 / 3.0 * R_pc * PC
        if "apparent_magnitude" in q:                                                   # §3 step 4
            mu = 5.0 * math.log10(d_kpc * 1000.0 / 10.0)
            lv = 10 ** (-0.4 * (float(q["apparent_magnitude"]["value"]) - mu - 4.85))
        else:
            lv = float(q["luminosity"]["value"])  # Boötes III: from M_V, distance-independent
        ups = float(q["stellar_ml_population"]["value"])
        m_gas = 0.0                                                                     # §3 step 6
        if "mass_hi" in q:
            m_gas = 0.5 * 1.33 * float(q["mass_hi"]["value"])  # value is already rescaled to D (parameter text)
        g_obs = 3.0 * (sig * 1e3) ** 2 / r_half
        g_bar = G * (0.5 * lv * ups + m_gas) * MSUN / r_half ** 2
        # the Atlas rounds its stored inputs (§3, rounding): agreement to 1e-4 relative, about 4e-5 dex
        assert close(g_obs, float(r["g_obs"]), 1e-4), (r["measurement_id"], g_obs, float(r["g_obs"]))
        assert close(g_bar, float(r["g_bar"]), 1e-4), (r["measurement_id"], g_bar, float(r["g_bar"]))


# --------------------------------------------------------------------------- SPARC, KiDS-1000, X-COP

def test_sparc_text_reproduces_every_row():
    m, ob = tables("aeg-d-sparc")
    C = 1e6 / (PC * 1e3)  # (km/s)^2 / kpc -> m/s^2
    assert close(C, 3.2407792894443656e-14, 1e-15)
    rows = defaults(m)
    assert len(rows) == 3391
    for r in rows:
        R = float(r["r_kpc"])
        vo, vg, vd, vb = (float(r[c]) for c in ("x_sparc_v_obs", "x_sparc_v_gas", "x_sparc_v_disk", "x_sparc_v_bul"))
        g_obs = vo * vo / R * C
        g_bar = (0.5 * vd * abs(vd) + 0.7 * vb * abs(vb) + vg * abs(vg)) / R * C
        assert close(g_obs, float(r["g_obs"])) and close(g_bar, float(r["g_bar"]), 1e-9), r["measurement_id"]


def test_kids_text_reproduces_every_row():
    m, ob = tables("aeg-d-kids1000-rar")
    F = 4 * G * MSUN / PC ** 2
    rows = defaults(m)
    assert len(rows) == 30
    for r in rows:
        g_obs = F * float(r["x_kids1000_rar_esd_t"]) / float(r["x_kids1000_rar_bias"])
        gb = ob[ids(r["baryonic_from"])[0]]
        assert close(g_obs, float(r["g_obs"]), 1e-9), r["measurement_id"]
        assert float(gb["value"]) == float(r["g_bar"])
        k = int(str(r["source_ref"]).rsplit("data row ", 1)[1])
        sample = str(r["x_kids1000_rar_sample"])
        assert (str(r["plotted"]) == "false") == (sample == "kids_bright" and k <= 8), r["measurement_id"]


def test_xcop_text_reproduces_every_row():
    # Trivial by construction: the source releases g_obs and g_bar; this only shows the Atlas converts nothing.
    m, ob = tables("aeg-d-xcop")
    rows = defaults(m)
    assert len(rows) == 109
    for r in rows:
        o = ob[ids(r["observed_from"])[0]]
        b = ob[ids(r["baryonic_from"])[0]]
        assert float(o["value"]) == float(r["g_obs"]) and float(b["value"]) == float(r["g_bar"]), r["measurement_id"]
        assert str(r["plotted"]) == "true"


# --------------------------------------------------------------------------- strong lenses

def test_lenses_text_reproduces_every_default_row():
    from aeg import lensing as Lz
    m, ob = tables("aeg-d-strong-lensing")
    X = "x_strong_lensing_"
    f = lambda r, c: None if str(r[X + c]) == "--" else float(r[X + c])
    rows = defaults(m)
    assert len(rows) == 94
    for r in rows:
        th, zl, zs, h0, om = f(r, "theta_e_arcsec"), f(r, "z_l"), f(r, "z_s"), f(r, "h0"), f(r, "om")
        # §2 steps 2-3
        if str(r[X + "r_e_source"]) == "printed":
            r_e = float(r["r_kpc"])
        else:
            r_e = th * Lz.ARCSEC * Lz.angular_diameter_distance(zl, h0, om) / Lz.KPC
        if str(r[X + "m_e_source"]) == "computed":
            ds, dl = Lz.angular_diameter_distance(zs, h0, om), Lz.angular_diameter_distance(zl, h0, om)
            dls = (Lz.comoving_distance(zs, h0, om) - Lz.comoving_distance(zl, h0, om)) / (1 + zs)
            m_e = (th * Lz.ARCSEC) ** 2 * Lz.C ** 2 * ds * dl / (4 * Lz.G * dls) / Lz.M_SUN
        else:
            m_e = f(r, "m_e_msun")
        # step 4
        route = str(r[X + "mstar_route"])
        if route == "profile":
            n = f(r, "sersic_n")
            frac = Lz._gammainc_lower_reg(2 * n, Lz.sersic_b(n) * (th / f(r, "r_eff_arcsec")) ** (1 / n))
            ms = f(r, "mstar_msun") * frac
        elif route == "L_times_ML":
            ms = f(r, "l_aperture_lsun") * f(r, "ml")
        else:
            ms = f(r, "mstar_msun")
        # steps 5-6
        gas = (0.0012 + 0.0) * ms
        R = r_e * Lz.KPC
        g_obs = G * m_e * MSUN / R ** 2
        g_bar = G * (ms + gas) * MSUN / R ** 2
        assert close(g_obs, float(r["g_obs"]), 1e-9), (r["measurement_id"], route, g_obs, float(r["g_obs"]))
        assert close(g_bar, float(r["g_bar"]), 1e-9), (r["measurement_id"], route, g_bar, float(r["g_bar"]))


def test_dwarf_input_table_is_current():
    """The per-system input table on the dwarf methods page equals what the generator writes now."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("mit", ROOT / "docs/methods/datasets/make_input_tables.py")
    mit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mit)
    page = (ROOT / "docs/methods/datasets/aeg-d-dwarfs.md").read_text(encoding="utf-8")
    assert page.split(mit.MARK, 1)[1].strip() == mit.dwarfs().strip()


# --------------------------------------------------------------------------- stronger checks (added on review)

def test_gc_selection_rules_pick_the_bins_used():
    """§3 and §5 of the globular-cluster page: line-of-sight Types only; >= 2 bins and coverage >= 0.80;
    RV first, then more stars, then the later year; M54's bins beyond 200 arcsec dropped. Applied to every
    sigma_los observable of each system, the rules must select exactly the Type and bins each default row uses."""
    import collections
    from aeg.king66 import King66
    m, ob = tables("aeg-d-gc-baumgardt")
    year = {"RV": 0, "F13": 2013, "L13": 2013, "L15": 2015, "K18": 2018, "D21": 2021, "C22": 2022, "G22": 2022}
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for o in ob.values():
        if str(o["quantity"]) == "sigma_los":
            by[o["system_id"]][str(o["x_gc_baumgardt_dataset"])].append(o)
    m54 = "aeg-s-000295"
    for r in defaults(m):
        sid = r["system_id"]
        par = {str(ob[i]["x_gc_baumgardt_parameter"]): float(ob[i]["value"]) for i in ids(r["baryonic_from"])}
        k = King66(par["McLaughlin & van der Marel 2005 King fit: W0/gamma"], par["McLaughlin & van der Marel 2005 King fit: r0"])
        ok = []
        for typ, bins in by[sid].items():
            assert typ in year
            keep = [b for b in bins if not (sid == m54 and typ == "RV" and float(b["x_gc_baumgardt_r_arcsec"]) > 200)]
            rad = sorted(float(b["x_gc_baumgardt_r_arcsec"]) for b in keep)
            if len(rad) < 2:
                continue
            if k.cumulative_fraction(rad[-1] + 0.5 * (rad[-1] - rad[-2])) >= 0.80:
                n_star = sum(0 if str(b["x_gc_baumgardt_n_star"]) == "--" else int(b["x_gc_baumgardt_n_star"]) for b in bins)
                ok.append(((typ != "RV", -n_star, -year[typ]), typ, {b["observable_id"] for b in keep}))
        assert ok, r["measurement_id"]
        _, typ, chosen = sorted(ok, key=lambda x: x[0])[0]
        used = {i for i in ids(r["observed_from"]) if str(ob[i]["quantity"]) == "sigma_los"}
        assert used == chosen, r["measurement_id"]


def test_dwarf_luminosity_and_gas_from_the_stated_routes():
    """§3 steps 4 and 6 of the dwarf page, from the printed inputs: L_V from m_V,0 and the package
    distance's modulus; gas from Putman Table 1 (values as transcribed in v1/reading/gas_values.csv)
    rescaled to the package distance, times 1.33, halved. Not re-derived here: Υ_V (needs the
    McLaughlin & van der Marel table, not in the repository) and Boötes III's distance-independent L_V."""
    import csv
    import json
    m, ob = tables("aeg-d-dwarfs")
    sysrows = {r["system_id"]: r for r in Table.read(ROOT / "data/packages/aeg-d-dwarfs/v3/tables/systems.ecsv", format="ascii.ecsv")}
    gas = {r["key"]: r for r in csv.DictReader(open(ROOT / "data/packages/aeg-d-dwarfs/v1/reading/gas_values.csv", encoding="utf-8"))}
    n_l = n_g = 0
    for r in defaults(m):
        q = {}
        for i in ids(r["baryonic_from"]):
            q.setdefault(str(ob[i]["quantity"]), ob[i])
        d = float(q["distance"]["value"])
        if "apparent_magnitude" in q:
            mu = 5.0 * math.log10(d * 1000.0 / 10.0)
            lv = 10 ** (-0.4 * (float(q["apparent_magnitude"]["value"]) - mu - 4.85))
            assert close(lv, float(r["x_dwarfs_l_v"]), 1e-4), r["measurement_id"]
            n_l += 1
        key = json.loads(str(sysrows[r["system_id"]]["properties"]))["lvdb_key"]
        g = gas.get(key)
        if str(r["x_dwarfs_gas_status"]) == "measured":
            mg = 0.5 * 1.33 * float(g["MHI"]) * (d / float(g["Dist"])) ** 2
            assert close(mg, float(r["x_dwarfs_m_gas_rh"]), 1e-5), r["measurement_id"]
            n_g += 1
        else:
            assert float(r["x_dwarfs_m_gas_rh"]) == 0.0
    assert n_l == 63 and n_g == 2


def test_lenses_independent_implementation_all_rows():
    """The lens page's formulas implemented again without the Atlas's lensing module (scipy quadrature,
    gamma function and root finder), on default and alternative rows."""
    from scipy.integrate import quad
    from scipy.optimize import brentq
    from scipy.special import gammainc
    m, ob = tables("aeg-d-strong-lensing")
    X = "x_strong_lensing_"
    f = lambda r, k: None if str(r[X + k]) == "--" else float(r[X + k])
    c, arcsec = 299792458.0, math.pi / 180 / 3600

    def dc(z, h0, om):
        return c / (h0 * 1e3 / (PC * 1e6)) * quad(lambda x: 1 / math.sqrt(om * (1 + x) ** 3 + 1 - om), 0, z, epsrel=1e-12)[0]
    for r in m:
        th, zl, zs, h0, om = f(r, "theta_e_arcsec"), f(r, "z_l"), f(r, "z_s"), f(r, "h0"), f(r, "om")
        re_ = float(r["r_kpc"]) * 1e3 * PC if str(r[X + "r_e_source"]) == "printed" else th * arcsec * dc(zl, h0, om) / (1 + zl)
        if str(r[X + "m_e_source"]) == "computed":
            dl, ds = dc(zl, h0, om) / (1 + zl), dc(zs, h0, om) / (1 + zs)
            dls = (dc(zs, h0, om) - dc(zl, h0, om)) / (1 + zs)
            me = (th * arcsec) ** 2 * c * c * ds * dl / (4 * G * dls) / MSUN
        else:
            me = f(r, "m_e_msun")
        route = str(r[X + "mstar_route"])
        if route == "profile":
            n = f(r, "sersic_n")
            b = brentq(lambda x: gammainc(2 * n, x) - 0.5, 1e-6, 50)
            ms = f(r, "mstar_msun") * gammainc(2 * n, b * (th / f(r, "r_eff_arcsec")) ** (1 / n))
        elif route == "L_times_ML":
            ms = f(r, "l_aperture_lsun") * f(r, "ml")
        else:
            ms = f(r, "mstar_msun")
        gb = G * ms * (1 + f(r, "gas_hot_frac") + f(r, "gas_cold_frac")) * MSUN / re_ ** 2
        assert close(G * me * MSUN / re_ ** 2, float(r["g_obs"]), 1e-9), r["measurement_id"]
        assert close(gb, float(r["g_bar"]), 1e-9), r["measurement_id"]


def test_stated_identifier_mappings():
    """The identifier-to-row mappings the methods pages state (added after the pilot, D-118)."""
    m, _ = tables("aeg-d-sparc")
    for r in m:
        assert int(str(r["measurement_id"])[-6:]) == int(str(r["source_ref"]).split("data row ")[1].split(",")[0])
    m, _ = tables("aeg-d-kids1000-rar")
    order = ["kids_bright", "kids_bright_hotgas", "gama"]
    for r in m:
        n = int(str(r["measurement_id"])[-6:])
        assert str(r["x_kids1000_rar_sample"]) == order[(n - 1) // 15]
        assert int(str(r["source_ref"]).rsplit("data row ", 1)[1]) == (n - 1) % 15 + 1
    m, _ = tables("aeg-d-xcop")
    counts = [("A644", 19), ("A1795", 21), ("A2029", 22), ("A2142", 20), ("A2319", 27)]
    expect = [(c, k) for c, n in counts for k in range(1, n + 1)]
    for r in m:
        n = int(str(r["measurement_id"])[-6:])
        c, k = expect[n - 1]
        assert str(r["source_ref"]) == f"data_E22.tar.gz:{c}/gbar_gobs_{c}.fits:row {k}"
