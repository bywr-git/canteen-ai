function HealthyScoreCard({ health }) {

    if (!health) {
        return (
            <div className="bg-white rounded-xl shadow-md p-6">
                Loading...
            </div>
        );
    }

    const score = health.healthy_score;

    let color = "text-red-500";
    let message = health.message;

    if (score >= 80) {
        color = "text-green-600";
    } else if (score >= 60) {
        color = "text-yellow-500";
    }

    return (
        <div className="bg-white rounded-xl shadow-md p-6">

            <h2 className="text-xl font-bold mb-4">
                🥗 Healthy Eating Score
            </h2>

            <p className={`text-5xl font-bold ${color}`}>
                {score}%
            </p>

            <p className="mt-4 text-gray-600">
                {message}
            </p>

            <div className="mt-6 space-y-2">

                <p>
                    <strong>Healthy:</strong> {health.healthy_items}
                </p>

                <p>
                    <strong>Junk:</strong> {health.junk_items}
                </p>

                <p>
                    <strong>Neutral:</strong> {health.neutral_items}
                </p>

            </div>

        </div>
    );
}

export default HealthyScoreCard;