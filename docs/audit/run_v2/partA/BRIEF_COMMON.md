# Audit reader brief

## The task (fixed text, plan §2.6)

> You are auditing one measurement of a public dataset. From the source given, read the inputs that the written method needs, exactly as printed, with their units and where you found them (page, table, row, column, or file and row). Then compute the observed acceleration g_obs and the baryonic acceleration g_bar, both in m s⁻², with your own code, following only the written method. Use only the constants stated in the method. If the method does not say how to do a step, do not guess: record "method incomplete" and what was missing. If you cannot read a value, record "unreadable" and why. Return one CSV row per measurement with: measurement_id, each input with its unit and locator, g_obs, g_bar, and notes. Do not look for or use any other copy of this dataset.

Do this for every measurement in your packet's `rows.csv`.

## What you have

Your packet (read only): `/home/claude/audit_v2/packets/<STRATUM>/`
- `rows.csv`: the measurements to audit, with the system name and the locator (`source_ref`). A few numbers in locators are replaced by "[value redacted]"; read them from the source yourself.
- `method/`: the dataset's written method. That is the methods page text, plus the package's method file(s), plus `sources.json`, which lists the source files and documents.
- `sources/`: the source files and documents, already downloaded and checked against the hashes in `sources.json`.

If a paper that the method or a locator names is not in `sources/`, you may download its arXiv e-print from arxiv.org, and nothing else. Record the URL and the file's SHA-256 in your notes.

## Isolation (strict)

- Work only in your own output folder, `/home/claude/audit_v2/readers/<READER>/<STRATUM>/`, and read only your packet.
- Do NOT open, list or search:
  - `/home/claude/atlas` or `/home/claude/atlas-a6`, or any `.claude/worktrees` folder;
  - any other folder under `/home/claude/audit_v2/readers/` or `/home/claude/audit_v2/provenance/`;
  - `/tmp` scratch folders that are not yours;
  - extragravitation.org, or the GitHub repository extragravitation/atlas.
- Do not search the web for this dataset's converted values.
- You are one of two independent readers. You must not see the other reader's work, and the other reader must not see yours.

## What to write (exact formats; the comparison script reads them)

`values.csv`, with the header `measurement_id,g_obs,g_bar,status,notes`:
- one row per measurement in `rows.csv`;
- `g_obs` and `g_bar` in m s⁻², as plain decimals or e-notation (for example `1.234e-10`);
- `status` is exactly `ok`, `method incomplete` or `unreadable`:
  - if it is `method incomplete`, say in `notes` which step the method did not specify, and leave `g_obs` or `g_bar` empty where you could not compute it;
  - if the source gives an upper limit rather than a value, compute at the limit, keep `ok`, and write `limit` in `notes`.

`inputs.csv`, with the header `measurement_id,input,value,unit,locator`:
- one row per input you read from a source;
- name each input by the source's own column label or symbol (for example `Vobs`, `M_FORW`, `sigma`);
- give `value` exactly as printed, with the same digits;
- give the locator as file and row, or page, table, row and column.

`code/`: the code you wrote to compute the accelerations. `notes.md`: anything else, including any steps you were unsure of.

Use your own code (Python 3; astropy may be used where the method says it is used). Take constants only from the method text. If the method does not state a constant, that is "method incomplete".

## When you finish

Reply with:
- the number of rows per status;
- the method steps you found incomplete, if any;
- the paths of your files.

Do not paste the computed values into your reply.
