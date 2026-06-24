(function () {
  var link = document.querySelector('link[rel="preload"][as="style"][href*="/assets/index-"]')
  if (!link || link.rel === 'stylesheet') return

  function activate() {
    link.rel = 'stylesheet'
  }

  link.addEventListener('load', activate, { once: true })

  var entries = performance.getEntriesByName(link.href)
  if (entries.length && entries[entries.length - 1].responseEnd > 0) {
    activate()
  }
})()
