/**
 * Safe inline formatting for JPbot chat bubbles.
 * Supports **bold**, *italic*, and {{accent}} (brand-colored emphasis).
 */
export function formatChatMessage(text) {
  if (!text) return ''

  const escaped = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  return escaped
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\{\{(.+?)\}\}/g, '<span class="msg-accent">$1</span>')
    .replace(/\n/g, '<br>')
}
