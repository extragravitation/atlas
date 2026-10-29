// Static build of the Atlas site. Every page is generated from the repository's data packages.
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://extragravitation.org',
  output: 'static',
  trailingSlash: 'ignore',
  build: { format: 'directory' },
  devToolbar: { enabled: false },
  vite: { server: { fs: { allow: ['..'] } } },
});
