import countries from '@/data/countries.json'
import { BLOCKED_COUNTRY_CODES } from '@/data/blockedCountries.js'

export const CountryService = {
  getCountries() {
    const allowed = countries.filter((country) => !BLOCKED_COUNTRY_CODES.has(country.code))
    return Promise.resolve(allowed)
  },
}
