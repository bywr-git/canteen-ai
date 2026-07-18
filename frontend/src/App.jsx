import { useEffect, useState } from "react";
import api from "./services/api";

function App() {

  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {

    api.get("/dashboard/1")
      .then((response) => {
        setDashboard(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

  }, []);

  return (
    <div style={{ padding: "40px" }}>
      <h1>Canteen Budget Tracker</h1>

      {dashboard ? (
        <pre>
          {JSON.stringify(dashboard, null, 2)}
        </pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;