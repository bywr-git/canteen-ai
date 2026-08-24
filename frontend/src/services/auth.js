import api from './api'

const TOKEN_KEY = 'canteen_ai_token'
const USER_KEY = 'canteen_ai_user'

export function saveAuth(token, user) {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getCurrentUser() {
  const raw = localStorage.getItem(USER_KEY)
  return raw ? JSON.parse(raw) : null
}

export async function register(payload) {
  const r = await api.post('/auth/register', payload)
  return r.data
}

export async function login(payload) {
  const r = await api.post('/auth/login', payload)
  return r.data
}

export function authHeader() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}
