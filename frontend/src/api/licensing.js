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

export async function fetchExistingActivation(appFingerprint, appName, options = {}) {
  const params = new URLSearchParams({
    appfingerprint: appFingerprint.trim(),
    appname: appName.trim(),
  })
  if (options.licenseCode) params.set('licensecode', options.licenseCode.trim())
  if (options.activationDate) params.set('activationdate', options.activationDate.trim())
  const res = await fetch(`/licensing/activation/existing?${params}`)
  if (res.status === 404) return null
  if (!res.ok) throw new Error(await parseError(res))
  return res.json()
}

export async function checkRecoverableLicense(email, appName) {
  const params = new URLSearchParams({
    email: email.trim().toLowerCase(),
    appname: appName.trim(),
  })
  const res = await fetch(`/licensing/activation/recover/check?${params}`)
  if (!res.ok) throw new Error(await parseError(res))
  return res.json()
}

export async function requestLicenseRecovery(payload) {
  const res = await fetch('/licensing/activation/recover/request', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(await parseError(res))
  return res.json()
}

export async function verifyLicenseRecovery(payload) {
  const res = await fetch('/licensing/activation/recover/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(await parseError(res))
  return res.json()
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
