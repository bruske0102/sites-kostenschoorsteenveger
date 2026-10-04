/**
 * Dutch count + noun agreement.
 * 1 → singular; 0 and 2+ → plural.
 */
export function nlCount(n: number, singular: string, plural: string): string {
  return `${n} ${n === 1 ? singular : plural}`;
}

export const LISTING_NOUN = {
  singular: "schoorsteenveger",
  plural: "schoorsteenvegers",
} as const;

export function listingCount(n: number): string {
  return nlCount(n, LISTING_NOUN.singular, LISTING_NOUN.plural);
}
