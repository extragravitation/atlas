# Audit part B: term classification brief (plan v2 §3.2)

`/home/claude/audit_xcop/partB/terms/term_scan.csv` lists every occurrence of a fixed term list in the built pages of a public science website, the Atlas of Extra Gravitation. Each occurrence comes with its page and context. The site's standard is to describe observations and never assume a cause of the acceleration discrepancy, and to take no side between the competing accounts.

**Classify each occurrence** as `allowed` or `finding`.

It is **allowed** only if it is one of these:
- quoting a source;
- naming an account in the confrontations section;
- the single note on the conventional term "mass discrepancy";
- naming a source's own fitting function as the source's method.

Any other use is a **finding**. Where the context is too short to decide, open the page under `/home/claude/audit_xcop/partB/site/` and read the surrounding text.

**Isolation:** read only `/home/claude/audit_xcop/partB/site/` and `/home/claude/audit_xcop/partB/terms/term_scan.csv`, and write only to `/home/claude/audit_xcop/partB/terms/`. Do not open `/home/claude/atlas` or any other folder.

**Output:** `terms/classified.csv`, with the header `page,term,match,context,classification,rule,reason`. The `rule` column names which allowed rule applies, or which part of the standard the occurrence breaks. Reply with the counts.
