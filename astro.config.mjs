// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://ai-search-lab.pages.dev',
  trailingSlash: 'always',
  integrations: [sitemap({
    // The root duplicates /vehicles/; the confirmation page is not a search landing page.
    filter: (page) => !['/', '/thank-you/'].includes(new URL(page).pathname),
  })],
});
