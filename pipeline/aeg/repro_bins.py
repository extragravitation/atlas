"""D-037 reproduction check for binned profiles without published bin edges (D-045 item 5).

Frozen before any velocity file or profile value is opened. Applies the
frozen D-037 check (`aeg.repro_dispersion`, not edited) bin by bin where a
source publishes a binned dispersion profile with each bin's number of stars
but not its radial edges, and releases the per-star velocities (first case:
the Baumgardt globular cluster database, line-of-sight bins of type "RV").

Rule (D-045 item 5):

1. Members: stars whose radial-velocity membership probability is > 0.5.
   A star with no probability is not a member.
2. Binaries: stars whose probability of being single is < 0.5 are excluded;
   a star with no such probability is kept.
3. Stars without a finite velocity, error or radius are not used; their
   number is reported.
4. Count test: the number of selected stars must equal the sum of the
   published bins' star counts. If not, every bin is **not testable**
   ("membership not reproduced"), with both numbers reported.
5. Bins are rebuilt as consecutive groups of the published star counts,
   taking the selected stars in order of projected radius (ties in file
   order), innermost bin first.
6. Each rebuilt bin goes through `aeg.repro_dispersion.reproduce` with the
   published value and its 68% interval: pass, fail or not testable, as
   frozen in D-037.
7. Diagnostic, not part of pass/fail: each rebuilt bin's mean radius is
   reported next to the published mean radius.

Every result is labelled "reconstructed binning": a fail may come from the
binning rather than from the data, and the page says so.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from aeg.repro_dispersion import NOT_TESTABLE, Published, ReproResult, Star, reproduce

SPEC_VERSION = "1.0.0"
LABEL = "reconstructed binning"


@dataclass(frozen=True)
class RVStar:
    r: float | None          # projected radius (any unit, same as the published bins)
    v: float | None          # line-of-sight velocity
    e: float | None          # its error
    p_member: float | None   # radial-velocity membership probability
    p_single: float | None   # probability of being single


@dataclass(frozen=True)
class PublishedBin:
    r_mean: float
    n_star: int
    sigma: float
    lo: float
    hi: float


@dataclass(frozen=True)
class BinResult:
    published: PublishedBin
    result: ReproResult
    r_mean_rebuilt: float | None
    label: str = LABEL


@dataclass(frozen=True)
class ProfileResult:
    bins: tuple[BinResult, ...]
    n_selected: int
    n_published: int
    n_unusable: int
    reason: str = ""
    spec_version: str = SPEC_VERSION


def _finite(*xs) -> bool:
    return all(x is not None and math.isfinite(x) for x in xs)


def select(stars: Sequence[RVStar]) -> tuple[list[RVStar], int]:
    """Members that are not flagged binaries; returns (selected, number unusable)."""
    out, unusable = [], 0
    for s in stars:
        if s.p_member is None or not math.isfinite(s.p_member) or not s.p_member > 0.5:
            continue
        if s.p_single is not None and math.isfinite(s.p_single) and s.p_single < 0.5:
            continue
        if not _finite(s.r, s.v, s.e) or s.e < 0:
            unusable += 1
            continue
        out.append(s)
    return out, unusable


def check_profile(stars: Sequence[RVStar], bins: Sequence[PublishedBin]) -> ProfileResult:
    pub = sorted(bins, key=lambda b: b.r_mean)
    n_pub = sum(b.n_star for b in pub)
    sel, unusable = select(stars)
    if len(sel) != n_pub:
        reason = f"membership not reproduced: {len(sel)} selected stars, {n_pub} in the published bins"
        res = tuple(BinResult(b, ReproResult(NOT_TESTABLE, None, Published(b.sigma, b.lo, b.hi), reason), None)
                    for b in pub)
        return ProfileResult(res, len(sel), n_pub, unusable, reason)
    order = sorted(range(len(sel)), key=lambda i: (sel[i].r, i))
    out, k = [], 0
    for b in pub:
        group = [sel[i] for i in order[k:k + b.n_star]]
        k += b.n_star
        stars_ = [Star(v=s.v, e=s.e, member=True) for s in group]
        r = reproduce(stars_, Published(b.sigma, b.lo, b.hi))
        rm = sum(s.r for s in group) / len(group) if group else None
        out.append(BinResult(b, r, rm))
    return ProfileResult(tuple(out), len(sel), n_pub, unusable)
