// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://ai-search-lab.pages.dev',
  trailingSlash: 'always',
  integrations: [sitemap({
    // The confirmation page is not a search landing page.
    filter: (page) => new URL(page).pathname !== '/thank-you/',
  })],
});
