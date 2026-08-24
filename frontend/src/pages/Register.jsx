import React, { useState } from 'react'
import { useAuth } from '../hooks/AuthProvider'
import { Link } from 'react-router-dom'

export default function Register(){
  const { register } = useAuth()
  const [form, setForm] = useState({ name: '', email: '', password: '', department: '', year: '' })
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try{
      await register(form)
      window.location.href = '/login'
    }catch(err){
      const detail = err.response?.data?.detail
      const validation = Array.isArray(detail) ? detail[0]?.msg : detail
      setError(validation || 'Registration failed. Please check your details and try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Register</h2>
      <form onSubmit={submit} className="space-y-2">
        <input required placeholder="Name" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} className="w-full p-2 border" />
        <input required type="email" placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} className="w-full p-2 border" />
        <input required minLength={8} type="password" placeholder="Password (8+ characters)" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} className="w-full p-2 border" />
        <input placeholder="Department (optional)" value={form.department} onChange={e=>setForm({...form, department:e.target.value})} className="w-full p-2 border" />
        <input min="1" max="5" type="number" placeholder="Year (optional)" value={form.year} onChange={e=>setForm({...form, year:e.target.value ? Number(e.target.value) : null})} className="w-full p-2 border" />
        {error && <div className="text-red-600">{error}</div>}
        <button disabled={submitting} className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-60">{submitting ? 'Registering...' : 'Register'}</button>
        <p className="text-sm text-gray-600">Already have an account? <Link to="/login" className="text-blue-600 underline">Login</Link></p>
      </form>
    </div>
  )
}
