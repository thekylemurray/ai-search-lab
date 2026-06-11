import {createClient} from '@sanity/client'

export const sanityClient = createClient({
  projectId: '8utqo9sg',
  dataset: 'production',
  apiVersion: '2026-06-10',
  useCdn: true,
})