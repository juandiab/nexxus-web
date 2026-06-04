const API_BASE = '/licensing'

export async function submitActivation(payload) {
  const res = await fetch(`${API_BASE}/activation`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    const detail = err.detail
    const message = Array.isArray(detail)
      ? detail.map((d) => d.msg).join(', ')
      : detail || 'Activation failed'
    throw new Error(message)
  }

  return res.json()
}
