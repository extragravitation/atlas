# Audit part B: neutrality reader brief (plan v2 §3.3)

You are one of two independent readers of a public science website: the Atlas of Extra Gravitation. It compares the observed gravitational acceleration (g_obs) with the acceleration expected from detected ordinary matter under Newtonian gravity (g_bar). The site's own standard is to describe the observations and never assume a cause. It must take no side between the competing accounts (for example dark matter, modified gravity, or others). Accounts may be named only in a quotation from a source, in a separate "confrontations" section, in a single note on the conventional term "mass discrepancy", or as the name of a source's own fitting function used as that source's method.

**Pages:** the built pages listed in `/home/claude/audit_xcop/partB/pages.txt`, relative to `/home/claude/audit_xcop/partB/site/`. Read each page's visible text, headings, labels, tooltips, alt text and any chart labels or legends in the HTML. Where a page's chart data is in a linked JSON or JS file under `site/`, you may read it for labels.

**Checklist for each page:**
1. Does any sentence, label or visual assume a cause of the acceleration discrepancy?
2. Does any favour one account over another, by wording, ordering, colour or emphasis?
3. Does any label or category name carry a result (for example, a class named by its g_obs/g_bar value or by an interpretation)?
4. Is a continuous property binned or thresholded where the data do not require it?
5. Are the plain and expert versions both present and saying the same thing?
6. Is any number shown without a visible route to its source?

**Isolation:** read only `/home/claude/audit_xcop/partB/site/`, `pages.txt` and this brief. Write only to your own folder, `/home/claude/audit_xcop/partB/<READER>/`. Do not open `/home/claude/atlas`, any other reader's folder, `/home/claude/audit_v2/readers`, or the live site.

**Output:** `<READER>/findings.csv`, with the header `page,checklist_item,text,finding,severity`:
- one row per finding;
- quote the text exactly;
- severity is `must fix` or `should fix`.

Also write `<READER>/pages_reviewed.csv`, with the header `page,reviewed,notes`, covering every page.

Reply with the number of findings per checklist item and the paths of your files.
