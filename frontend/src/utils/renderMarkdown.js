/**
 * Renders blog Markdown with consistent site styling.
 * Uses the same rules as existing posts (GFM-style subset).
 */
function inlineMarkdown(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`([^`\n]+)`/g, '<code>$1</code>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
}

function convertTables(md) {
  return md.replace(
    /^(\|.+\|)\n(\|[\s\-:|]+\|)\n((?:\|.+\|\n?)*)/gm,
    (_, headerLine, _sep, bodyLines) => {
      const parseCells = (line) =>
        line
          .split('|')
          .slice(1, -1)
          .map((c) => c.trim())
      const headers = parseCells(headerLine)
      const rows = bodyLines
        .trim()
        .split('\n')
        .filter(Boolean)
        .map(parseCells)
      const thead =
        '<thead><tr>' +
        headers.map((h) => `<th>${inlineMarkdown(h)}</th>`).join('') +
        '</tr></thead>'
      const tbody =
        '<tbody>' +
        rows
          .map(
            (cells) =>
              '<tr>' +
              cells.map((c) => `<td>${inlineMarkdown(c)}</td>`).join('') +
              '</tr>'
          )
          .join('') +
        '</tbody>'
      return `<table class="md-table">${thead}${tbody}</table>`
    }
  )
}

export function renderMarkdown(md) {
  if (!md) return ''

  let html = convertTables(md)
    .replace(/\r\n/g, '\n')
    // Fenced code blocks (before inline transforms)
    .replace(/```(\w*)\n([\s\S]*?)```/g, (_, _lang, code) => {
      const escaped = code
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
      return `<pre><code>${escaped}</code></pre>`
    })
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>)+/g, (block) => `<ul>${block}</ul>`)

  html = inlineMarkdown(html)

  const blocks = html.split(/\n\n+/)
  html = blocks
    .map((block) => {
      const trimmed = block.trim()
      if (!trimmed) return ''
      if (/^<(h[1-6]|ul|pre|blockquote|table)/.test(trimmed)) return trimmed
      return `<p>${trimmed.replace(/\n/g, '<br>')}</p>`
    })
    .join('\n')

  return html
}
