import { useEffect, useState } from 'react'
import api from '../services/api'
import { Link } from 'react-router-dom'

const MAX_IMAGE_BYTES = 5 * 1024 * 1024
const IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']

const emptyForm = {
  detected_food_name: '', confidence: '', portion_description: '',
  estimated_calories: '', estimated_protein: '', estimated_carbohydrates: '',
  estimated_fat: '', estimated_fiber: '', analysis_notes: '',
}

export default function FoodScanner() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [scan, setScan] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [catalogue, setCatalogue] = useState([])
  const [history, setHistory] = useState([])
  const [loadingHistory, setLoadingHistory] = useState(true)
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState(null)
  const [message, setMessage] = useState(null)
  const [selectedFoodItemId, setSelectedFoodItemId] = useState('')

  useEffect(() => {
    let active = true
    const load = async () => {
      try {
        const [foodResponse, historyResponse] = await Promise.all([
          api.get('/food-items'), api.get('/food-scans'),
        ])
        if (active) {
          setCatalogue(foodResponse.data)
          setHistory(historyResponse.data)
        }
      } catch (requestError) {
        if (active && requestError.response?.status !== 401) setError('Some scanner data could not be loaded.')
      } finally {
        if (active) setLoadingHistory(false)
      }
    }
    load()
    return () => { active = false }
  }, [])

  useEffect(() => () => { if (preview) URL.revokeObjectURL(preview) }, [preview])

  const clearSelection = () => {
    if (preview) URL.revokeObjectURL(preview)
    setFile(null); setPreview(null); setScan(null); setForm(emptyForm)
    setSelectedFoodItemId(''); setStatus('idle'); setError(null); setMessage(null)
  }

  const chooseFile = (event) => {
    const selected = event.target.files?.[0]
    setError(null); setMessage(null)
    if (!selected) return
    if (!IMAGE_TYPES.includes(selected.type)) {
      setError('Choose a JPG, JPEG, PNG, GIF, or WebP image.')
      event.target.value = ''
      return
    }
    if (selected.size > MAX_IMAGE_BYTES) {
      setError('Images must be 5 MB or smaller.')
      event.target.value = ''
      return
    }
    if (preview) URL.revokeObjectURL(preview)
    setFile(selected); setPreview(URL.createObjectURL(selected)); setScan(null); setForm(emptyForm); setStatus('idle')
  }

  const analyze = async () => {
    if (!file) { setError('Select a food photo first.'); return }
    setStatus('analyzing'); setError(null); setMessage(null)
    const body = new FormData(); body.append('image', file)
    try {
      const response = await api.post('/food-scans/analyze', body)
      setScan(response.data)
      setForm({
        detected_food_name: response.data.detected_food_name || '', confidence: response.data.confidence ?? '',
        portion_description: response.data.portion_description || '', estimated_calories: response.data.estimated_calories ?? '',
        estimated_protein: response.data.estimated_protein ?? '', estimated_carbohydrates: response.data.estimated_carbohydrates ?? '',
        estimated_fat: response.data.estimated_fat ?? '', estimated_fiber: response.data.estimated_fiber ?? '',
        analysis_notes: response.data.analysis_notes || '',
      })
      setStatus('review')
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Analysis failed. Please retry.')
      setStatus('idle')
    } finally {
      setStatus((current) => current === 'analyzing' ? 'idle' : current)
    }
  }

  const confirm = async (addToPurchases = false) => {
    if (addToPurchases && !selectedFoodItemId) { setError('Select a catalogue item before adding a purchase.'); return }
    setStatus('confirming'); setError(null); setMessage(null)
    try {
      const response = await api.post(`/food-scans/${scan.scan_id}/confirm`, {
        ...Object.fromEntries(Object.entries(form).map(([key, value]) => [key, value === '' ? null : (key === 'confidence' || key.startsWith('estimated_') ? Number(value) : value)])),
        add_to_purchases: addToPurchases,
        food_item_id: addToPurchases ? Number(selectedFoodItemId) : null,
      })
      setScan(response.data.scan); setHistory((current) => [response.data.scan, ...current.filter((item) => item.scan_id !== scan.scan_id)])
      setStatus('confirmed'); setMessage(addToPurchases ? 'Scan saved and purchase recorded.' : 'Scan saved to Nutrition History.')
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Could not save this scan.'); setStatus('review')
    } finally {
      setStatus((current) => current === 'confirming' ? 'review' : current)
    }
  }

  const edit = (field, value) => setForm((current) => ({ ...current, [field]: value }))
  const confidence = form.confidence === '' || form.confidence == null ? 'Unknown' : `${Math.round(Number(form.confidence) * 100)}%`

  return <main className="min-h-screen bg-slate-950 px-4 py-8 text-slate-900 sm:px-8"><div className="mx-auto max-w-5xl">
    <header className="mb-8 flex flex-wrap items-center justify-between gap-4 text-white"><div><p className="text-sm font-semibold uppercase tracking-widest text-emerald-300">Canteen AI</p><h1 className="text-4xl font-bold">AI Food Scanner</h1></div><div className="flex gap-3"><Link to="/nutrition-history" className="rounded-lg border border-slate-600 px-4 py-2 hover:bg-slate-800">Nutrition History</Link><Link to="/dashboard" className="rounded-lg border border-slate-600 px-4 py-2 hover:bg-slate-800">Back to Dashboard</Link></div></header>
    <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
      <section className="rounded-2xl bg-white p-6 shadow-xl"><p className="mb-6 text-slate-600">Upload a food photo for an image-based estimate. Nutrition values are uncertain and are not medical advice.</p>
        <div className="rounded-xl border-2 border-dashed border-emerald-300 bg-emerald-50 p-6 text-center"><p className="text-lg font-semibold">Start with a food photo</p><p className="mb-5 text-sm text-slate-600">JPG, JPEG, PNG, GIF, or WebP up to 5 MB</p><label className="inline-flex cursor-pointer rounded-lg bg-emerald-600 px-5 py-3 font-semibold text-white hover:bg-emerald-700"><span>Upload Food Photo</span><input type="file" className="sr-only" accept="image/jpeg,image/png,image/gif,image/webp" capture="environment" onChange={chooseFile} /></label>{file && <p className="mt-4 truncate text-sm">Selected: <strong>{file.name}</strong></p>}</div>
        {preview && <div className="mt-6"><div className="mb-3 flex justify-between"><h2 className="text-lg font-semibold">Preview</h2><button onClick={clearSelection} className="font-semibold text-red-600">Replace / cancel</button></div><img src={preview} alt="Selected food preview" className="max-h-80 w-full rounded-xl bg-slate-100 object-contain" /></div>}
        {error && <p className="mt-4 bg-red-100 p-3 text-red-700">{error}</p>}{message && <p className="mt-4 bg-green-100 p-3 text-green-700">{message}</p>}
        {file && !scan && <button disabled={status === 'analyzing'} onClick={analyze} className="mt-5 w-full rounded-lg bg-slate-900 px-4 py-3 font-semibold text-white disabled:cursor-wait disabled:opacity-60">{status === 'analyzing' ? 'Analyzing your food...' : 'Analyze Food'}</button>}{status === 'analyzing' && <p className="mt-3 text-center text-sm text-slate-600">This may take a few seconds.</p>}
        {scan && <div className="mt-8 space-y-3"><h2 className="text-2xl font-semibold">Review your result</h2><p className="text-sm font-medium text-amber-700">Estimated nutrition only. Review and edit before saving.</p><label className="block">Detected food<input value={form.detected_food_name} onChange={(e) => edit('detected_food_name', e.target.value)} className="block w-full rounded border p-2" /></label><label className="block">Serving size<input value={form.portion_description} onChange={(e) => edit('portion_description', e.target.value)} className="block w-full rounded border p-2" /></label><div className="grid grid-cols-2 gap-3">{[['estimated_calories','Calories'],['estimated_protein','Protein (g)'],['estimated_carbohydrates','Carbohydrates (g)'],['estimated_fat','Fat (g)'],['estimated_fiber','Fiber (g)']].map(([field, label]) => <label key={field}>{label}<input type="number" min="0" value={form[field]} onChange={(e) => edit(field, e.target.value)} className="block w-full rounded border p-2" /></label>)}</div><label className="block">AI notes<textarea value={form.analysis_notes} onChange={(e) => edit('analysis_notes', e.target.value)} className="block w-full rounded border p-2" /></label><p>Confidence estimate: <strong>{confidence}</strong></p><label className="block">Catalogue item for optional purchase<select value={selectedFoodItemId} onChange={(e) => setSelectedFoodItemId(e.target.value)} className="block w-full rounded border p-2"><option value="">Select only when adding a purchase</option>{catalogue.map((item) => <option key={item.item_id} value={item.item_id}>{item.name} - ₹{item.price}</option>)}</select></label>{status !== 'confirmed' && <div className="flex flex-wrap gap-3"><button disabled={status === 'confirming'} onClick={() => confirm(false)} className="rounded-lg bg-emerald-600 px-4 py-3 font-semibold text-white disabled:opacity-60">Save to Nutrition History</button><button disabled={status === 'confirming' || !selectedFoodItemId} onClick={() => confirm(true)} className="rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white disabled:opacity-60">Add to Purchase</button></div>}</div>}
      </section>
      <aside className="rounded-2xl bg-slate-900 p-6 text-white shadow-xl"><h2 className="mb-4 text-2xl font-semibold">Recent scans</h2>{loadingHistory ? <p className="text-slate-300">Loading scan history...</p> : history.length ? <div className="space-y-3">{history.slice(0, 6).map((item) => <div key={item.scan_id} className="rounded-lg bg-slate-800 p-3"><p className="font-semibold">{item.detected_food_name || 'Food not recognized'}</p><p className="text-sm text-slate-300">{item.status.replace('_', ' ')}</p></div>)}</div> : <p className="text-slate-300">No scans yet. Saved results will appear here.</p>}</aside>
    </div></div></main>
}
