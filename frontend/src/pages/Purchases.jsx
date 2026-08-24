import { useEffect, useState } from 'react'
import api from '../services/api'
import { Link } from 'react-router-dom'

export default function Purchases() {
  const [purchases, setPurchases] = useState([])
  const [category, setCategory] = useState('')
  const [error, setError] = useState(null)
  const load = () => api.get('/purchases', { params: { category: category || undefined } }).then((r) => setPurchases(r.data)).catch(() => setError('Unable to load purchases.'))
  useEffect(() => { load() }, [category])
  const remove = async (id) => { if (!window.confirm('Delete this purchase?')) return; try { await api.delete(`/purchases/${id}`); load() } catch { setError('Unable to delete purchase.') } }
  return <main className="min-h-screen bg-gray-100 p-8"><div className="flex justify-between mb-8"><h1 className="text-3xl font-bold">Purchase history</h1><Link to="/dashboard">Dashboard</Link></div>
    <input value={category} onChange={(e) => setCategory(e.target.value)} placeholder="Filter by category" className="p-2 border bg-white mb-6" />
    {error && <p className="bg-red-100 text-red-700 p-3 mb-4">{error}</p>}
    <section className="bg-white rounded-xl shadow p-5">{purchases.length ? purchases.map((purchase) => <div key={purchase.purchase_id} className="flex flex-wrap justify-between gap-3 border-b py-3"><span>Item #{purchase.item_id} x {purchase.quantity}</span><span>₹{(purchase.total_price ?? purchase.amount ?? 0).toFixed(2)}</span><button onClick={() => remove(purchase.purchase_id)} className="text-red-600">Delete</button></div>) : <p>No purchases yet.</p>}</section>
  </main>
}
