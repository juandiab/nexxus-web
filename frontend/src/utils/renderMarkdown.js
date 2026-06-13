/**
 * Line-based Markdown renderer for blog posts.
 * Handles fenced code blocks safely (won't break on Python """ strings).
 */

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

function inlineMarkdown(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`([^`\n]+)`/g, '<code>$1</code>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
}

function parseTableRow(line) {
  return line
    .split('|')
    .slice(1, -1)
    .map((cell) => cell.trim())
}

function renderTable(lines) {
  const header = parseTableRow(lines[0])
  const rows = lines.slice(2).map(parseTableRow)
  const thead =
    '<thead><tr>' +
    header.map((h) => `<th>${inlineMarkdown(h)}</th>`).join('') +
    '</tr></thead>'
  const tbody =
    '<tbody>' +
    rows
      .map(
        (cells) =>
          '<tr>' + cells.map((c) => `<td>${inlineMarkdown(c)}</td>`).join('') + '</tr>'
      )
      .join('') +
    '</tbody>'
  return `<table class="md-table">${thead}${tbody}</table>`
}

function isTableSeparator(line) {
  return /^\|[\s\-:|]+\|$/.test(line.trim())
}

function titlesMatch(a, b) {
  return a.trim().toLowerCase() === b.trim().toLowerCase()
}

/**
 * @param {string} md
 * @param {{ skipTitle?: string }} [options]
 */
export function renderMarkdown(md, options = {}) {
  if (!md) return ''

  const lines = md.replace(/\r\n/g, '\n').split('\n')
  const htmlParts = []
  let index = 0

  while (index < lines.length) {
    const line = lines[index]

    if (!line.trim()) {
      index += 1
      continue
    }

    const fenceOpen = line.match(/^```([\w-]*)\s*$/)
    if (fenceOpen) {
      const lang = fenceOpen[1] || ''
      index += 1
      const codeLines = []
      let depth = 1

      while (index < lines.length && depth > 0) {
        const nestedFence = lines[index].match(/^```([\w-]*)\s*$/)
        if (nestedFence) {
          if (nestedFence[1]) {
            depth += 1
            codeLines.push(lines[index])
          } else {
            depth -= 1
            if (depth > 0) codeLines.push(lines[index])
          }
          index += 1
          continue
        }
        if (depth > 0) codeLines.push(lines[index])
        index += 1
      }

      const langClass = lang ? ` class="language-${lang}"` : ''
      const langLabel = lang
        ? `<div class="code-block-header"><span class="code-lang">${lang}</span></div>`
        : ''
      htmlParts.push(
        `<div class="code-block">${langLabel}<pre><code${langClass}>${escapeHtml(codeLines.join('\n'))}</code></pre></div>`
      )
      continue
    }

    if (line.includes('|') && index + 1 < lines.length && isTableSeparator(lines[index + 1])) {
      const tableLines = [lines[index], lines[index + 1]]
      index += 2
      while (index < lines.length && lines[index].includes('|')) {
        tableLines.push(lines[index])
        index += 1
      }
      htmlParts.push(renderTable(tableLines))
      continue
    }

    if (line.startsWith('### ')) {
      htmlParts.push(`<h3>${inlineMarkdown(line.slice(4))}</h3>`)
      index += 1
      continue
    }
    if (line.startsWith('## ')) {
      htmlParts.push(`<h2>${inlineMarkdown(line.slice(3))}</h2>`)
      index += 1
      continue
    }
    if (line.startsWith('# ')) {
      const title = line.slice(2)
      if (!options.skipTitle || !titlesMatch(title, options.skipTitle)) {
        htmlParts.push(`<h1>${inlineMarkdown(title)}</h1>`)
      }
      index += 1
      continue
    }

    if (line.startsWith('> ')) {
      const quoteLines = []
      while (index < lines.length && lines[index].startsWith('> ')) {
        quoteLines.push(lines[index].slice(2))
        index += 1
      }
      htmlParts.push(`<blockquote>${inlineMarkdown(quoteLines.join(' '))}</blockquote>`)
      continue
    }

    if (/^[-*] /.test(line)) {
      const items = []
      while (index < lines.length && /^[-*] /.test(lines[index])) {
        items.push(lines[index].replace(/^[-*] /, ''))
        index += 1
      }
      htmlParts.push(
        `<ul>${items.map((item) => `<li>${inlineMarkdown(item)}</li>`).join('')}</ul>`
      )
      continue
    }

    const paragraphLines = []
    while (
      index < lines.length &&
      lines[index].trim() &&
      !lines[index].startsWith('#') &&
      !lines[index].startsWith('> ') &&
      !/^```/.test(lines[index]) &&
      !/^[-*] /.test(lines[index]) &&
      !(lines[index].includes('|') && index + 1 < lines.length && isTableSeparator(lines[index + 1]))
    ) {
      paragraphLines.push(lines[index])
      index += 1
    }
    htmlParts.push(`<p>${inlineMarkdown(paragraphLines.join(' '))}</p>`)
  }

  return htmlParts.join('\n')
}
