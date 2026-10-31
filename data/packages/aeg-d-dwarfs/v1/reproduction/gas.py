"""Gas mass inside r_half from Putman et al. 2021 Table 1 (D-034, D-035 d, D-058; REPRODUCTION.md "Gas").

Frozen before the conversion ran. convert.py calls gas_for_system() once per system with the
row from reading/gas_values.csv and the package distance (D-052, with D-055 item 8).

Rules:
- Not in Putman 2021: status "not addressed" (or "absent (literature limit for the kind)" only
  where a cited statement covers the system; none is coded here), no mass.
- l_MHI == "<": a 5 sigma upper limit -> status "absent (measured limit)" (D-035 d); the limit is
  rescaled and recorded, never added to g_bar.
- Otherwise a detection -> status "measured":
    M_HI,pkg = M_HI * (D_package / D_Putman)^2               (D-058; Putman M_HI = 2.36e5 S D^2)
    M_gas    = helium_factor * M_HI,pkg                       (D-034; register default 1.33)
    M_gas(<r_half) = 0.5 * M_gas, flag "gas_half_total"       (Table 1 gives totals only)
  The asymmetric errors e_MHI (minus) and E_MHI (plus, blank = symmetric) scale the same way.
"""

from __future__ import annotations

HELIUM_FACTOR = 1.33  # data/assumptions.json helium_factor (Lelli et al. 2016, read at source)


def _f(x: str) -> float | None:
    t = (x or "").strip()
    return float(t) if t else None


def gas_for_system(row: dict | None, d_package_kpc: float) -> dict:
    if not row or row.get("status", "").startswith("not in"):
        return {"gas_status": "not addressed", "m_gas_rh": 0.0, "flags": ""}
    d_put = float(row["Dist"])
    k = (d_package_kpc / d_put) ** 2
    m = float(row["MHI"]) * k
    em = (_f(row.get("e_MHI", "")) or 0.0) * k
    ep_raw = _f(row.get("E_MHI", ""))
    ep = ep_raw * k if ep_raw is not None else em
    out = {"d_putman_kpc": d_put, "d_package_kpc": d_package_kpc, "distance_factor": k,
           "m_hi_pkg": m, "m_hi_err_minus": em, "m_hi_err_plus": ep, "helium_factor": HELIUM_FACTOR}
    if row.get("l_MHI", "").strip() == "<":
        return {**out, "gas_status": "absent (measured limit)", "m_gas_rh": 0.0, "flags": "hi_upper_limit_5sigma"}
    return {**out, "gas_status": "measured", "m_gas_rh": 0.5 * HELIUM_FACTOR * m,
            "m_gas_rh_err_minus": 0.5 * HELIUM_FACTOR * em, "m_gas_rh_err_plus": 0.5 * HELIUM_FACTOR * ep,
            "flags": "gas_half_total"}
