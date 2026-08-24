import React, { useState } from 'react'
import { useAuth } from '../hooks/AuthProvider'

export default function Register(){
  const { register } = useAuth()
  const [form, setForm] = useState({ name: '', email: '', password: '', department: '', year: '' })
  const [error, setError] = useState(null)

  const submit = async (e) => {
    e.preventDefault()
    try{
      await register(form)
      window.location.href = '/login'
    }catch(err){
      setError('Registration failed')
    }
  }

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Register</h2>
      <form onSubmit={submit} className="space-y-2">
        <input placeholder="Name" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} className="w-full p-2 border" />
        <input placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} className="w-full p-2 border" />
        <input type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} className="w-full p-2 border" />
        <input placeholder="Department" value={form.department} onChange={e=>setForm({...form, department:e.target.value})} className="w-full p-2 border" />
        <input placeholder="Year" value={form.year} onChange={e=>setForm({...form, year:Number(e.target.value)})} className="w-full p-2 border" />
        {error && <div className="text-red-600">{error}</div>}
        <button className="px-4 py-2 bg-green-600 text-white rounded">Register</button>
      </form>
    </div>
  )
}
