/**
 * Semrush NL city/intent research for Kostenschoorsteenveger.nl.
 * Volumes TBD — do not invent numbers.
 */
import { listingCount } from "./nl-count";

export type CityIntentFlags = {
  volume: number;
  kd?: number;
  primaryPhrase: string;
};

export const CITY_INTENTS: Record<string, CityIntentFlags> = {};

export function isHighTrafficCity(plaatsSlug: string): boolean {
  const row = CITY_INTENTS[plaatsSlug];
  return Boolean(row && row.volume >= 200);
}

export function cityPageTitle(opts: {
  stad: string;
  plaatsSlug: string;
  n: number;
  aPlus?: boolean;
}): string {
  const { stad, n } = opts;
  if (n <= 0) return `Schoorsteenveger ${stad}`;
  return `Schoorsteenveger ${stad}: ${listingCount(n)} met adres`;
}

export function cityPageDescription(opts: {
  stad: string;
  plaatsSlug: string;
  n: number;
  provincieNaam: string;
  aPlus?: boolean;
}): string {
  const { stad, n, provincieNaam } = opts;
  return `Vergelijk ${listingCount(n)} in ${stad} (${provincieNaam}) — met adres en telefoon.`;
}
