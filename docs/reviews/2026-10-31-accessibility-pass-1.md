# Accessibility and performance: first pass (issue #14)

2026-10-31, on `main` at 681744b plus the fixes in this pull request. This is a first pass with automated tools and scripted keyboard checks. It is **not** the full WCAG 2.2 AA audit #14 asks for on the final content: no screen reader was used and no person with a disability has tested the site.

## Method

- **axe-core 4.10.2**, rule tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa` and `best-practice`. 17 pages, both themes, at 1280 px and 390 px (68 runs):
  - home (map), scale strip, about, methods, coverage, tests, known issues, data, for data providers;
  - the dataset index and two dataset pages (dwarfs, KiDS);
  - the systems index and one system page of each kind: SPARC, X-COP, globular cluster, dwarf.
- **Reflow (WCAG 1.4.10)** at 320 px: 75 pages, namely every top-level page, every dataset page, and every seventh system page.
- **Keyboard (WCAG 2.1.1, 2.4.3, 2.4.7):** 70 Tab presses on the map page at 1280 px and 390 px, recording each focused element and whether it shows a focus ring.
- **Non-text contrast (WCAG 1.4.11):** contrast ratios of the canvas colours against the chart background, computed from the theme tokens.
- **Page weight:** byte sizes of the built pages, scripts, fonts and map data, raw and gzip -9.

## Fixed in this pull request

| Check | Finding | Fix |
|---|---|---|
| 2.4.7 Focus visible | The header search box showed no focus indicator (its outline was switched off). | The search field shows the standard focus ring when the input has focus. |
| 2.5.8 Target size | The stacked download links on the Data page were 18 px tall and touching (80 targets). | Those links are at least 24 px tall. |
| 2.1.1 Keyboard | On phones, the Data page's command block scrolled sideways but could not be reached by keyboard. | It is focusable and labelled. |
| 1.4.10 Reflow | At 320 px, five page types widened the page: Data (file paths in the changelog), dwarf system pages (the citation box), and the KiDS and X-COP dataset pages (long links in the source text). | Long paths, links and citations wrap. Now 0 of 75 pages scroll sideways. |

After the fixes, axe reports **0 violations on all 68 runs.** The site's own tests and `aeg.site_check` still pass.

## Found, not fixed: for a ruling or a later pass

1. **Map points cannot be selected by keyboard.** The canvas takes focus and zooms and pans by keyboard (+, −, 0, arrows, P), but Enter does nothing, so the Selected-system card is reachable only by pointer. The same systems are reachable by keyboard through the header search and the Systems index, which is arguably an equivalent path. **Proposed:** add keyboard stepping through the visible systems (for example, N and Shift+N) that opens the card, with a live-region announcement.
2. **Colour ramp ends are faint.** At full opacity, every dataset colour clears 3:1 against the chart background in both themes, except two ends of the "colour by" ramp:
   - dark theme, low end: 2.8:1;
   - light theme, top two steps: 2.6:1 and 1.8:1.
   The highest values of a coloured property are therefore the hardest to see in the light theme. **Proposed:** a thin dark outline on ramp-coloured points in the light theme, or a ramp whose light end stays at 3:1. The order of the steps is unchanged either way.
3. **Dense point clouds are translucent by design.** SPARC and KiDS points use 50% (dark) and 38% (light) opacity so that density shows. A single isolated point is then about 3.3:1 in dark but only about 1.9:1 in light. Overlapping points build up to full contrast. This is a deliberate trade-off between showing density and showing single points. **Proposed:** keep it, but raise the light-theme opacity to about 0.5 if an outside reviewer finds lone points hard to see.
4. **Map data weight.** The map page downloads about 540 kB gzipped of data. SPARC alone is 377 kB, and most of it is repeated text columns (`assumptions`, `source_ref`, `adjustable`, `method`) that the map does not draw. Fonts and scripts add roughly 100 kB more (each woff2 font file is about 33 kB; the map script is 31 kB). That is acceptable on 4G but slow on 3G. **Proposed:** split the map payload into the columns the map draws, and load the record columns when a system is selected. `site_check` would then check both files.
5. **Not tested yet:**
   - screen readers (VoiceOver, NVDA, TalkBack);
   - 200% text zoom on desktop;
   - Windows high-contrast mode;
   - real phones (only emulated widths were used);
   - Lighthouse timing on a throttled connection;
   - the scale strip's and the pull-budget chart's own keyboard handling.

## Not findings

- Text contrast: axe found no failures in either theme.
- Skip link, landmarks, one `main` per page, labelled control groups, `aria-pressed` on toggles, `prefers-reduced-motion`: present.
- The only violations axe reported after the fixes came from `/downloads/`. That URL serves files, not a page; in this run, the local test server returned a directory listing there.
