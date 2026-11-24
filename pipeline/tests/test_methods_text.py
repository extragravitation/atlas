"""The written methods (docs/methods/datasets/*.md, D-113 item 2) reproduce every row.

Each test recomputes g_obs and g_bar for every default row of a v3 package from
the inputs the row names in the observables table, following only the steps the
dataset's methods page states, and compares with the published row. It checks
that the text is complete and right; it does not re-read the sources (the audit
does that). Where a step needs a numerical model the text specifies (the King
1966 projection), the Atlas's implementation of that specification is used.
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
