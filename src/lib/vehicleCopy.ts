/** Temporary correction until the original Sanity heroText is updated.
 * Only the known Ioniq 5 placeholder is affected; future CMS edits pass through.
 */
export function normalizeVehicleCopy<T extends { slug?: string; heroText?: string | null }>(vehicle: T): T {
  if (vehicle.slug === 'ioniq-5' && vehicle.heroText === 'Lease smarter, dummy.') {
    return { ...vehicle, heroText: 'Lease smarter.' };
  }
  return vehicle;
}
