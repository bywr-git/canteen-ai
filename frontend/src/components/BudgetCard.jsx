function BudgetCard({ budget }) {

    if (!budget) {
        return (
            <div className="bg-white rounded-xl shadow-md p-6">
                Loading...
            </div>
        );
    }

    const percentage =
        (budget.total_spent / budget.monthly_budget) * 100;

    return (
        <div className="bg-white rounded-xl shadow-md p-6">

            <h2 className="text-xl font-bold mb-4">
                💰 Monthly Budget
            </h2>

            <p className="text-3xl font-bold">
                ₹{budget.monthly_budget}
            </p>

            <div className="w-full bg-gray-200 rounded-full h-3 mt-5">

                <div
                    className="bg-blue-500 h-3 rounded-full"
                    style={{
                        width: `${percentage}%`
                    }}
                ></div>

            </div>

            <div className="mt-5">

                <p>
                    <strong>Spent:</strong> ₹{budget.total_spent}
                </p>

                <p>
                    <strong>Remaining:</strong> ₹{budget.remaining}
                </p>

                <p className="font-semibold mt-2">
                    {budget.status}
                </p>

            </div>

        </div>
    );
}

export default BudgetCard;