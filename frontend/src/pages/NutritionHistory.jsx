import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'

export default function NutritionHistory() {
  const [scans, setScans] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let active = true
    const loadHistory = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await api.get('/food-scans')
        const data = Array.isArray(response.data) ? response.data : []
        if (active) setScans(data)
      } catch (requestError) {
        if (active) {
          setError(requestError.response?.status === 401
            ? 'Your session has expired. Please log in again.'
            : 'Unable to load nutrition history.')
        }
      } finally {
        if (active) setLoading(false)
      }
    }
    loadHistory()
    return () => { active = false }
  }, [])

  return <main className="min-h-screen bg-slate-950 px-4 py-8 text-slate-900 sm:px-8">
    <div className="mx-auto max-w-4xl">
      <header className="mb-8 flex flex-wrap items-center justify-between gap-4 text-white">
        <div><p className="text-sm font-semibold uppercase tracking-widest text-emerald-300">Canteen AI</p><h1 className="text-4xl font-bold">Nutrition History</h1></div>
        <div className="flex gap-3"><Link to="/food-scanner" className="rounded-lg bg-emerald-600 px-4 py-2">New Scan</Link><Link to="/dashboard" className="rounded-lg border border-slate-600 px-4 py-2">Dashboard</Link></div>
      </header>
      {loading && <section className="rounded-2xl bg-white p-6 shadow-xl">Loading nutrition history...</section>}
      {!loading && error && <section className="rounded-2xl bg-red-50 p-6 text-red-700 shadow-xl">{error}</section>}
      {!loading && !error && !scans.length && <section className="rounded-2xl bg-white p-6 shadow-xl"><h2 className="text-xl font-semibold">No scans yet</h2><p className="mt-2 text-slate-600">Your confirmed food scans will appear here.</p></section>}
      {!loading && !error && scans.length > 0 && <section className="space-y-4">{scans.map((scan) => <article key={scan.scan_id} className="rounded-2xl bg-white p-6 shadow-xl"><div className="flex flex-wrap justify-between gap-3"><h2 className="text-xl font-semibold">{scan.detected_food_name || 'Food not recognized'}</h2><span className="rounded-full bg-slate-100 px-3 py-1 text-sm">{scan.status?.replace('_', ' ') || 'saved'}</span></div><div className="mt-4 grid grid-cols-2 gap-3 text-sm sm:grid-cols-4"><p>Calories<br /><strong>{scan.estimated_calories ?? 'Not available'}</strong></p><p>Protein<br /><strong>{scan.estimated_protein ?? 'Not available'} g</strong></p><p>Carbohydrates<br /><strong>{scan.estimated_carbohydrates ?? 'Not available'} g</strong></p><p>Fat<br /><strong>{scan.estimated_fat ?? 'Not available'} g</strong></p></div>{scan.estimated_fiber != null && <p className="mt-3 text-sm">Fiber: <strong>{scan.estimated_fiber} g</strong></p>}{scan.analysis_notes && <p className="mt-3 text-sm text-slate-600">{scan.analysis_notes}</p>}</article>)}</section>}
    </div>
  </main>
}
