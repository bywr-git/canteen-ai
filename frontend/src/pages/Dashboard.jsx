import { useEffect, useState } from "react";
import api from "../services/api";
import BudgetCard from "../components/BudgetCard";
import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/AuthProvider'

function Dashboard() {
    const { user, logout } = useAuth()
    const [dashboard, setDashboard] = useState(null);
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const loadDashboard = async () => {
            setLoading(true)
            setError(null)
            try {
                const response = await api.get("/dashboard")
                setDashboard(response.data);
            } catch {
                setError('Unable to load your dashboard.')
            } finally {
                setLoading(false)
            }
        }
        loadDashboard()

    }, []);

    return (

        <div className="min-h-screen bg-gray-100 p-8">
            <nav className="flex flex-wrap gap-4 mb-8 items-center">
                <Link to="/dashboard" className="font-semibold">Dashboard</Link>
                <Link to="/food">Food</Link>
                <Link to="/purchases">Purchases</Link>
                <Link to="/budget">Budget</Link>
                <span className="ml-auto">{user?.name}</span>
                <button onClick={logout} className="px-3 py-1 bg-gray-800 text-white rounded">Log out</button>
            </nav>

            <h1 className="text-4xl font-bold mb-8">
                🍽️ Canteen Budget & Habit Tracker
            </h1>

            {error && <p className="bg-red-100 text-red-700 p-4 mb-6">{error}</p>}
            {loading && <p className="bg-white p-6">Loading dashboard...</p>}

            {dashboard && <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                <BudgetCard
                    budget={dashboard?.budget}
                />

                <section className="bg-white rounded-xl shadow-md p-6">
                    <h2 className="text-xl font-bold mb-4">Spending summary</h2>
                    <p>Total: ₹{dashboard.analytics?.total_spending?.toFixed(2)}</p>
                    <p>This month: ₹{dashboard.analytics?.spending_this_month?.toFixed(2)}</p>
                    <p>Purchases: {dashboard.analytics?.number_of_purchases}</p>
                </section>

                <section className="bg-white rounded-xl shadow-md p-6 md:col-span-2">
                    <h2 className="text-xl font-bold mb-4">Recent purchases</h2>
                    {dashboard.recent_purchases?.length ? dashboard.recent_purchases.map((purchase) => (
                        <div key={purchase.purchase_id} className="flex justify-between border-b py-2">
                            <span>Item #{purchase.item_id} x {purchase.quantity}</span>
                            <span>₹{(purchase.total_price ?? purchase.amount ?? 0).toFixed(2)}</span>
                        </div>
                    )) : <p>No purchases yet. Add your first purchase from the food catalogue.</p>}
                </section>

            </div>}

        </div>

    );

}

export default Dashboard;