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
  name: 'range',
  title: 'Range',
  type: 'string'
}),

defineField({
  name: 'chargingSpeed',
  title: 'Charging Speed',
  type: 'string'
}),

defineField({
  name: 'bodyType',
  title: 'Body Type',
  type: 'string'
}),

defineField({
  name: 'inventoryStatus',
  title: 'Inventory Status',
  type: 'string',
  options: {
    list: [
      { title: 'In Stock', value: 'in-stock' },
      { title: 'Low Inventory', value: 'low' },
      { title: 'Preorder', value: 'preorder' }
    ]
  }
}),

defineField({
  name: 'highlights',
  title: 'Highlights',
  type: 'array',
  of: [{ type: 'string' }]
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

    defineField({
      name: 'showLeadForm',
      title: 'Show Lead Form',
      type: 'boolean',
      initialValue: true,
    }),

    defineField({
      name: 'leadHeadline',
      title: 'Lead Form Headline',
      type: 'string',     
    }),
    
  ],
})