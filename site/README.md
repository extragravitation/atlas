# Site

The static website. Hosting: Cloudflare Workers, static assets only, with a preview for every pull request (decision D-007, amended).

For now `public/` holds a single "in preparation" page so the domain serves something real. Cloudflare serves it via `wrangler.jsonc` at the repository root (assets directory `site/public`); no build command. The full site is built after the data packages (backlog milestone 4), at which point the build settings change.

**Preview quirk (2026-10-28):** Cloudflare's preview builds (open beta) do not apply `not_found_handling`, so unknown addresses on a preview show Cloudflare's plain "Not found" text. Production applies it correctly and serves `404.html`. Judge 404 behaviour on the live site, not on previews.
