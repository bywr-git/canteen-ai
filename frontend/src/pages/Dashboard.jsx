import { useEffect, useState } from "react";
import api from "../services/api";
import BudgetCard from "../components/BudgetCard";
import HealthyScoreCard from "../components/HealthyScoreCard";

function Dashboard() {

    const [dashboard, setDashboard] = useState(null);

    useEffect(() => {

        api.get("/dashboard/1")
            .then((response) => {
                setDashboard(response.data);
            })
            .catch((error) => {
                console.log(error);
            });

    }, []);

    return (

        <div className="min-h-screen bg-gray-100 p-8">

            <h1 className="text-4xl font-bold mb-8">
                🍽️ Canteen Budget & Habit Tracker
            </h1>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                <BudgetCard
                    budget={dashboard?.budget}
                />

                <HealthyScoreCard
                    health={dashboard?.healthy_score}
                />

            </div>

        </div>

    );

}

export default Dashboard;