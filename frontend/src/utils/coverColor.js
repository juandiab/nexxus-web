const COVER_CLASS_BY_HEX = {
  '#007ba7': 'cover-007BA7',
  '#00a8e0': 'cover-00A8E0',
  '#005f7f': 'cover-005F7F',
  '#38383d': 'cover-38383D',
  '#4db8e0': 'cover-4DB8E0',
  '#6b5ce7': 'cover-6B5CE7',
  '#5b4fe8': 'cover-5B4FE8',
  '#1dd4b4': 'cover-1DD4B4',
  '#0c3a6b': 'cover-0C3A6B',
  '#1a2340': 'cover-1A2340',
}

/** Map blog cover_color hex values to static CSS classes for strict CSP. */
export function coverColorClass(color) {
  return COVER_CLASS_BY_HEX[String(color || '').trim().toLowerCase()] || 'cover-007BA7'
}
