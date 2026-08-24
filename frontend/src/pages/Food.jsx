import { useEffect, useState } from 'react'
import api from '../services/api'
import { Link } from 'react-router-dom'

export default function Food() {
  const [items, setItems] = useState([])
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [error, setError] = useState(null)
  const [quantity, setQuantity] = useState({})
  const [message, setMessage] = useState(null)

  const load = () => api.get('/food-items', { params: { search: search || undefined, category: category || undefined } })
    .then((response) => setItems(response.data))
    .catch(() => setError('Unable to load food items.'))

  useEffect(() => { load() }, [search, category])

  const buy = async (item) => {
    try {
      const count = Number(quantity[item.item_id] || 1)
      await api.post('/purchases', { item_id: item.item_id, quantity: count })
      setMessage(`${item.name} added to purchases.`)
    } catch { setError('Unable to record this purchase.') }
  }

  return <main className="min-h-screen bg-gray-100 p-8">
    <div className="flex justify-between mb-8"><h1 className="text-3xl font-bold">Food catalogue</h1><Link to="/dashboard">Dashboard</Link></div>
    <div className="flex gap-3 mb-6">
      <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search food" className="p-2 border bg-white" />
      <input value={category} onChange={(e) => setCategory(e.target.value)} placeholder="Category" className="p-2 border bg-white" />
    </div>
    {message && <p className="bg-green-100 text-green-700 p-3 mb-4">{message}</p>}
    {error && <p className="bg-red-100 text-red-700 p-3 mb-4">{error}</p>}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {items.map((item) => <article key={item.item_id} className="bg-white rounded-xl shadow p-5">
        <h2 className="text-xl font-semibold">{item.name}</h2><p className="text-gray-600">{item.category}</p>
        <p className="text-2xl font-bold mt-3">₹{item.price}</p>
        <p className="text-sm mt-2">Calories: {item.calories ?? 'Not available'}</p>
        <p className="text-sm">Protein: {item.protein ?? 'Not available'}</p>
        <div className="flex gap-2 mt-4"><input type="number" min="1" value={quantity[item.item_id] || 1} onChange={(e) => setQuantity({ ...quantity, [item.item_id]: e.target.value })} className="w-16 p-2 border" /><button onClick={() => buy(item)} className="px-3 py-2 bg-blue-600 text-white rounded">Add purchase</button></div>
      </article>)}
    </div>
    {!items.length && !error && <p className="bg-white p-6">No available food items match your search.</p>}
  </main>
}
