/**
 * ISO 3166-1 alpha-2 codes excluded from license activation country selection.
 *
 * Aligns with US OFAC restrictions relevant to software licensing and exports.
 * Review periodically — programs change (e.g. Syria comprehensive sanctions ended July 2025).
 *
 * @see https://ofac.treasury.gov/sanctions-programs-and-country-information
 */
export const BLOCKED_COUNTRY_CODES = new Set([
  // Comprehensive or near-comprehensive OFAC programs
  'CU', // Cuba
  'IR', // Iran
  'KP', // North Korea (DPRK)
  'RU', // Russia
  'BY', // Belarus

  // Broad sectoral sanctions — high compliance risk for US-origin services
  'VE', // Venezuela
  'MM', // Myanmar (Burma)

  // Additional OFAC country-based programs with significant commercial restrictions
  'AF', // Afghanistan
  'CF', // Central African Republic
  'CD', // Democratic Republic of the Congo
  'HT', // Haiti
  'LY', // Libya
  'ML', // Mali
  'NI', // Nicaragua
  'SD', // Sudan
  'SO', // Somalia
  'SS', // South Sudan
  'YE', // Yemen
])
