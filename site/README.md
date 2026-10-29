# Site

The static website, built with [Astro](https://astro.build) from the data packages in `data/packages/` and the assumption registry `data/assumptions.json`. Nothing on the site is typed in by hand: tables, payloads and downloads are generated from the packages at build time.

## Build

```
cd site
npm ci
npm run build      # writes site/dist
npm test           # unit tests for the build libraries
cd .. && python -m aeg.site_check site/dist   # values, downloads, links, reading layers
```

`npm run dev` serves a live preview. Set `AEG_OFFLINE=1` to build without reading the Known issues from GitHub (the page then lists them from the package files and says so).

## Hosting

Cloudflare Workers, static assets only (decision D-007, amended), configured in `wrangler.jsonc` at the repository root (assets directory `site/dist`). The build command is set in the Cloudflare dashboard (Workers Builds): `cd site && npm ci && npm run build`. Node version: `.node-version` at the root.

**Preview quirk (2026-10-28):** Cloudflare's preview builds (open beta) do not apply `not_found_handling`, so unknown addresses on a preview show Cloudflare's plain "Not found" text. Production serves `404.html`.

## Structure

| Path | Contents |
|---|---|
| `src/lib/` | Build-time readers: ECSV parser, package loader, labels for both reading layers, Markdown, known issues |
| `src/formula.mjs` | The assumption-formula evaluator, twin of `pipeline/aeg/formula.py` (checked to agree by `aeg.formula_check`) |
| `src/pages/` | Map, scale strip, system pages, dataset pages, known issues, methods, about, data, payload and download endpoints |
| `src/scripts/` | Browser code: shared state (in the page address), model (applies assumptions), map, strip, pull budget, sliders |
| `src/components/` | `L` and `Layer` (both reading layers required; the build fails otherwise), `Slider` |
| `tests/` | Node unit tests |

## Rendering

Charts are drawn with Canvas 2D for now. The charter asks for GPU rendering; the renderer is isolated in `src/scripts/draw.js` and the per-chart drawing functions so it can be replaced if Canvas 2D is not fast enough on phones.
