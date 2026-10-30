"""Stellar M/L_V for dwarf galaxies by metallicity (D-039 item 1b; aeg-d-dwarfs REPRODUCTION.md).

Frozen with the package's REPRODUCTION.md, before any dwarf value is opened.

Input: a published model table of (metallicity, M/L, error) for old populations at
one age (first case: McLaughlin & van der Marel 2005, BC03 + Chabrier disk IMF,
(M/L)_1 against [Fe/H] for Milky Way globular clusters, all at log age 10.11).
Output for a given [Fe/H]: the piecewise-linear interpolation through the tabulated
points, ordered by metallicity, for both value and error. Outside the tabulated
range the nearest end value is returned with the flag `beyond_source_range`:
never extrapolated. Duplicate metallicities with different values are refused
(the table must be a function of metallicity). Standard library only.
"""

from __future__ import annotations

import math
from bisect import bisect_left
from dataclasses import dataclass
from typing import Sequence

SPEC_VERSION = "1.0.0"
BEYOND = "beyond_source_range"


@dataclass(frozen=True)
class MLValue:
    ml: float
    err: float | None
    flag: str  # "" or BEYOND


class MLTable:
    def __init__(self, feh: Sequence[float], ml: Sequence[float], err: Sequence[float | None] | None = None):
        if not feh or len(feh) != len(ml) or (err is not None and len(err) != len(ml)):
            raise ValueError("empty table or columns of different length")
        rows = sorted(zip(feh, ml, err if err is not None else [None] * len(ml)), key=lambda r: r[0])
        for (f1, m1, _), (f2, m2, _) in zip(rows, rows[1:]):
            if f1 == f2 and m1 != m2:
                raise ValueError(f"two different M/L values at [Fe/H] = {f1}")
        uniq = []
        for r in rows:
            if not uniq or r[0] != uniq[-1][0]:
                uniq.append(r)
        if any(not (math.isfinite(f) and math.isfinite(m) and m > 0) for f, m, _ in uniq):
            raise ValueError("non-finite metallicity or non-positive M/L")
        self.feh = [r[0] for r in uniq]
        self.ml = [r[1] for r in uniq]
        self.err = [r[2] for r in uniq]

    def __call__(self, feh: float) -> MLValue:
        if not math.isfinite(feh):
            raise ValueError("non-finite metallicity")
        f = self.feh
        if feh <= f[0]:
            return MLValue(self.ml[0], self.err[0], "" if feh == f[0] else BEYOND)
        if feh >= f[-1]:
            return MLValue(self.ml[-1], self.err[-1], "" if feh == f[-1] else BEYOND)
        j = bisect_left(f, feh)
        if f[j] == feh:
            return MLValue(self.ml[j], self.err[j], "")
        i = j - 1
        t = (feh - f[i]) / (f[j] - f[i])
        e = None if self.err[i] is None or self.err[j] is None else self.err[i] + t * (self.err[j] - self.err[i])
        return MLValue(self.ml[i] + t * (self.ml[j] - self.ml[i]), e, "")
