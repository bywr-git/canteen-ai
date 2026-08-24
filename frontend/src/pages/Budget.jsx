import { useEffect, useState } from 'react'
import api from '../services/api'
import { Link } from 'react-router-dom'

export default function Budget() {
  const [budget, setBudget] = useState(null)
  const [amount, setAmount] = useState('')
  const [error, setError] = useState(null)
  const [message, setMessage] = useState(null)
  const load = () => api.get('/budgets/current').then((r) => { setBudget(r.data.budget === null ? null : r.data); if (r.data.amount) setAmount(r.data.amount) }).catch(() => setError('Unable to load budget.'))
  useEffect(() => { load() }, [])
  const save = async (event) => { event.preventDefault(); try { await api.post('/budgets', { monthly_limit: Number(amount), period: 'monthly' }); setMessage('Budget saved.'); load() } catch { setError('Unable to save budget.') } }
  return <main className="min-h-screen bg-gray-100 p-8"><div className="flex justify-between mb-8"><h1 className="text-3xl font-bold">Monthly budget</h1><Link to="/dashboard">Dashboard</Link></div>
    {error && <p className="bg-red-100 text-red-700 p-3 mb-4">{error}</p>}{message && <p className="bg-green-100 text-green-700 p-3 mb-4">{message}</p>}
    <form onSubmit={save} className="bg-white rounded-xl shadow p-5 max-w-md"><label className="block mb-2">Budget amount<input required min="0.01" type="number" value={amount} onChange={(e) => setAmount(e.target.value)} className="block w-full p-2 border mt-1" /></label><button className="px-4 py-2 bg-blue-600 text-white rounded">Save budget</button></form>
    {budget && <section className="bg-white rounded-xl shadow p-5 max-w-md mt-6"><p>Budget: ₹{budget.amount}</p><p>Spent: ₹{budget.spent}</p><p>Remaining: ₹{budget.remaining}</p><p>Used: {budget.percentage_used.toFixed(1)}%</p></section>}
  </main>
}
