# Site

The static website. Hosting: Cloudflare Workers, static assets only, with a preview for every pull request (decision D-007, amended).

For now `public/` holds a single "in preparation" page so the domain serves something real. Cloudflare serves it via `wrangler.jsonc` at the repository root (assets directory `site/public`); no build command. The full site is built after the data packages (backlog milestone 4), at which point the build settings change.
