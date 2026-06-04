import { startAuthentication, startRegistration } from '@simplewebauthn/browser'
import {
  fetchPasskeyStatus,
  webauthnLoginBegin,
  webauthnLoginFinish,
  webauthnRegisterBegin,
  webauthnRegisterFinish,
} from '@/api/client'

export async function getPasskeyStatus(username) {
  return fetchPasskeyStatus(username)
}

export async function registerPasskey(username, label = '') {
  const cleaned = username.trim().toLowerCase()
  const options = await webauthnRegisterBegin(cleaned)
  const credential = await startRegistration({ optionsJSON: options })
  return webauthnRegisterFinish(cleaned, credential, label)
}

export async function loginWithPasskey(username, { preferCrossDevice = false } = {}) {
  const cleaned = username.trim().toLowerCase()
  const options = await webauthnLoginBegin(cleaned, preferCrossDevice)
  const credential = await startAuthentication({ optionsJSON: options })
  return webauthnLoginFinish(cleaned, credential)
}

export function passkeyErrorMessage(error) {
  if (error?.name === 'NotAllowedError') {
    return 'Passkey request was cancelled or timed out.'
  }
  if (error?.message) return error.message
  return 'Passkey operation failed.'
}
