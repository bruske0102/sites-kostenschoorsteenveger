/**
 * Semrush NL city/intent research for Schoorsteenveger (2026-10-04).
 * Volumes from phrase_these database=nl. Do not invent numbers.
 * A-plus threshold = local vol ≥200.
 */
import { listingCount } from "./nl-count";

export type CityIntentFlags = {
  volume: number;
  kd?: number;
  primaryPhrase: string;
};

/** Keyed by plaats slug. */
export const CITY_INTENTS: Record<string, CityIntentFlags> = {
  "den-haag": { volume: 590, kd: 28, primaryPhrase: "schoorsteenveger den haag" },
  "eindhoven": { volume: 590, kd: 11, primaryPhrase: "schoorsteenveger eindhoven" },
  "amsterdam": { volume: 480, kd: 21, primaryPhrase: "schoorsteenveger amsterdam" },
  "arnhem": { volume: 480, kd: 9, primaryPhrase: "schoorsteenveger arnhem" },
  "enschede": { volume: 480, kd: 8, primaryPhrase: "schoorsteenveger enschede" },
  "groningen": { volume: 480, kd: 16, primaryPhrase: "schoorsteenveger groningen" },
  "groningen-gemeente": { volume: 480, kd: 16, primaryPhrase: "schoorsteenveger groningen" },
  "haarlem": { volume: 480, kd: 11, primaryPhrase: "schoorsteenveger haarlem" },
  "tilburg": { volume: 480, kd: 15, primaryPhrase: "schoorsteenveger tilburg" },
  "utrecht": { volume: 480, kd: 23, primaryPhrase: "schoorsteenveger utrecht" },
  "utrecht-gemeente": { volume: 480, kd: 23, primaryPhrase: "schoorsteenveger utrecht" },
  "ede": { volume: 390, kd: 14, primaryPhrase: "schoorsteenveger ede" },
  "rotterdam": { volume: 390, kd: 16, primaryPhrase: "schoorsteenveger rotterdam" },
  "den-bosch": { volume: 320, kd: 23, primaryPhrase: "schoorsteenveger den bosch" },
  "s-hertogenbosch": { volume: 320, kd: 23, primaryPhrase: "schoorsteenveger den bosch" },
};

export const INTENT_BLOG_LINKS = {
  kosten: { href: "/blog/", label: "Kosten schoorsteenveger" },
  onderhoud: { href: "/zoeken/", label: "Veegbedrijf zoeken" },
  kiezen: { href: "/zoeken/", label: "Schoorsteenveger zoeken" },
} as const;

export function cityIntent(plaatsSlug: string): CityIntentFlags | undefined {
  return CITY_INTENTS[plaatsSlug];
}

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
  const { stad, plaatsSlug, n } = opts;
  const intent = CITY_INTENTS[plaatsSlug];
  if (n <= 0) return `Schoorsteenveger ${stad}`;
  if (intent && intent.volume >= 200) {
    return `Schoorsteenveger ${stad}: tarieven, tip & adressen`;
  }
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
  return `Vergelijk ${listingCount(n)} in ${stad} (${provincieNaam}): adres, telefoon en openingstijden.`;
}
