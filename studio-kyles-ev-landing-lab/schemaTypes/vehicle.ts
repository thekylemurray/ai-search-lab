import {defineField, defineType} from 'sanity'

export const vehicle = defineType({
  name: 'vehicle',
  title: 'Vehicle',
  type: 'document',

  fields: [
    defineField({
      name: 'title',
      title: 'Title',
      type: 'string',
    }),

    defineField({
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      options: {
        source: 'title',
        maxLength: 96,
      },
    }),

    defineField({
      name: 'heroText',
      title: 'Hero Text',
      type: 'text',
    }),

    defineField({
  name: 'image',
  title: 'Vehicle Image',
  type: 'image',
}),
    
    defineField({
      name: 'price',
      title: 'Price',
      type: 'string',
    }),

    defineField({
  name: 'ctaText',
  title: 'CTA Text',
  type: 'string',
}),

    defineField({
  name: 'ctaUrl',
  title: 'CTA URL',
  type: 'url',
}),
  ],
})