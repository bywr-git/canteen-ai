import React, { createContext, useContext, useState } from 'react'
import { saveAuth, clearAuth, getCurrentUser, login as apiLogin, register as apiRegister } from '../services/auth'
import { useNavigate } from 'react-router-dom'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(getCurrentUser())
  const navigate = useNavigate()

  const login = async (email, password) => {
    const res = await apiLogin({ email, password })
    saveAuth(res.access_token, res.user)
    setUser(res.user)
    return res
  }

  const register = async (payload) => {
    const res = await apiRegister(payload)
    return res
  }

  const logout = () => {
    clearAuth()
    setUser(null)
    navigate('/login')
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}

export function RequireAuth({ children }) {
  const { user } = useAuth()
  if (!user) {
    window.location.href = '/login'
    return null
  }
  return children
}
