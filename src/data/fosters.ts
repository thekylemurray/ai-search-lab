export const currentFoster = {
  name: 'Linus',
  listingUrl: 'https://bfpa.org/adopt/dogs/adoptable-dogs/#action_0=pet&animalID_0=21082121&petIndex_0=6',
  portrait: '/images/fosters/linus-adopt-me.webp',
};

export const previousFosters: Array<{
  name: string;
  status: string;
  timeline: string;
  story: string[];
  remembrance?: string;
  image: string;
  imageAlt: string;
  width: number;
  height: number;
  gallery?: Array<{ image: string; alt: string; width: number; height: number }>;
}> = [
  {
    name: 'Milo',
    status: 'Adopted by me · In loving memory',
    timeline: 'Fostered February–May 2017 · Adopted May 2017',
    story: [
      'Milo came to me as a foster in February 2017. By May, I’d adopted him. A happy-go-lucky boy who loved people and sleeping on the couch, he became part of the family.',
      'Whenever an emergency vehicle went by, Milo would howl after it. My dad’s nickname for him was “MiloooOOOOooooOOO.” You can probably hear it.',
      'We didn’t know his birthday, so I gave him one in his adoption month: Cinco de Milo.',
    ],
    remembrance: 'Milo passed away at home on April 9, 2026, with me and my parents at his side.',
    image: '/images/fosters/milo-portrait.webp',
    imageAlt: 'Milo looking up at the camera with his mouth open and tongue out',
    width: 360,
    height: 480,
    gallery: [
      { image: '/images/fosters/milo-group.webp', alt: 'Milo wearing a purple shirt in front of a group wearing matching purple shirts', width: 525, height: 525 },
      { image: '/images/fosters/milo-hug.webp', alt: 'Milo being hugged by a person sitting on the floor', width: 720, height: 960 },
    ],
  },
];
