"""Compare the two independent A6 input readings (written before either reading was opened).

Usage: python compare_readings.py <reading_a.csv> <reading_b.csv> <out.csv>

Rows are keyed by (scope, normalised system_id, record, quantity, imf-or-note-free).
Numeric values are compared as printed: equal if their decimal values are equal
(so "0.80" equals "0.8"), with the same form (linear or log10) and limit.
Text quantities (methods, kinds, models) are listed side by side, not scored.
Every key present in only one reading is listed. Nothing is changed in either reading.
"""
import csv
import re
import sys
from decimal import Decimal, InvalidOperation

NUMERIC = {"z_l", "z_s", "theta_E", "M_E", "H0", "Om", "mstar", "R_e", "sersic_n", "component_share"}


def norm_id(s):
    return re.sub(r"[\s_\-−–]", "", (s or "")).upper().replace("SDSSJ", "J")


def num(s):
    try:
        return Decimal((s or "").strip().replace("−", "-"))
    except InvalidOperation:
        return None


def load(p):
    rows = {}
    with open(p, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            k = (r["scope"].strip(), norm_id(r["system_id"]), r["record"].strip(), r["quantity"].strip(),
                 (r.get("note") or "").strip().lower() if r["quantity"].strip() == "mstar" else "")
            rows.setdefault(k, []).append(r)
    return rows


def main(a, b, out):
    A, B = load(a), load(b)
    keys = sorted(set(A) | set(B))
    n_num = n_agree = 0
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["scope", "system", "record", "quantity", "variant", "value_a", "value_b", "err_a", "err_b", "form_a", "form_b", "status"])
        for k in keys:
            ra, rb = A.get(k, [{}])[0], B.get(k, [{}])[0]
            va, vb = ra.get("value", ""), rb.get("value", "")
            if k not in A or k not in B:
                status = "only_a" if k in A else "only_b"
            elif k[3] in NUMERIC:
                n_num += 1
                same = (num(va) is not None and num(va) == num(vb)
                        and num(ra.get("err_minus")) == num(rb.get("err_minus"))
                        and num(ra.get("err_plus")) == num(rb.get("err_plus"))
                        and (ra.get("form") or "") == (rb.get("form") or "")
                        and (ra.get("limit") or "") == (rb.get("limit") or ""))
                n_agree += same
                status = "agree" if same else "differ"
            else:
                status = "text"
            w.writerow([*k[:4], k[4], va, vb, f"{ra.get('err_minus','')}/{ra.get('err_plus','')}",
                        f"{rb.get('err_minus','')}/{rb.get('err_plus','')}", ra.get("form", ""), rb.get("form", ""), status])
    print(f"numeric keys in both: {n_num}; agree: {n_agree}; only in A or B: {sum(1 for k in keys if (k in A) != (k in B))}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
