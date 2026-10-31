# aeg-d-dwarfs/v1: brief for the residual conversion inputs

Written 2026-10-31, before any value listed here was read. Every reader gets this file verbatim. Two readings are made independently, compared by script, and disagreements are resolved against the paper.

**Why.** For 30 plotted systems the D-052 selection left a gap:
- the modulus behind an M_V (D-052 item 4: m_V,0 = M_V + the paper's own modulus), where that modulus is printed only as a distance or in another table;
- or a distance the earlier reading recorded as "not printed".

This reading fills the gaps from the papers already named in the record.

**Sheet** (`residual_sheet.csv`): key, paper, file, task. Tasks:
- **A.** The distance the paper adopted for that system (e.g. a table column "adopted" distance), with its errors and units. Also any sentence that says which distance the paper's M_V uses.
- **B1.** The extinction the paper applies to that system (A_V or E(B−V)), and how its M_V is computed (quote).
- **B2.** The distance modulus the paper prints for that system. Match the system only by a name the paper itself prints; if the paper uses another name and does not say the two are the same, write the row with the paper's name and say so.
- **C.** Every distance or distance modulus printed for the system, the paper's headline first.
- **D.** The distance modulus or distance used to compute the stated M_V. If it is printed, copy it; if the paper only cites another paper for it, say which.

**Output columns:** `key, paper, task, quantity, value, err_minus, err_plus, unit, variant, quote, location, note`.
- `quantity` is one of `distance`, `distance_modulus`, `extinction_AV`, `extinction_EBV`, `M_V`, or `statement` (a sentence with no number).
- Start `variant` with `headline` if the paper presents the value as its result.
- If nothing is printed, write one row with `value` blank and the reason in `note`.

**Rules.**
- Copy, don't judge.
- Compute nothing.
- Use no other source and no memory.
- Do not open any other reader's work.
