async function parseError(res) {
  const text = await res.text()
  try {
    const err = JSON.parse(text)
    const detail = err.detail
    if (Array.isArray(detail)) {
      return detail.map((d) => d.msg || JSON.stringify(d)).join(', ')
    }
    if (detail) return detail
  } catch {
    /* not JSON */
  }
  return text.trim() || `Request failed (${res.status})`
}

export async function requestActivation(payload) {
  const res = await fetch('/licensing/activation/request', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(await parseError(res))
  return res.json()
}

export async function verifyActivationOtp(payload) {
  const res = await fetch('/licensing/activation/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(await parseError(res))
  return res.json()
}
