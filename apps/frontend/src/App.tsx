import { useEffect, useState } from "react";

import { getHealthStatus } from "./api/health";
import type { HealthResponse } from "./types/health";

import "./App.css";

type ApiStatus = "loading" | "online" | "offline";

function App() {
  const [apiStatus, setApiStatus] = useState<ApiStatus>("loading");
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);

  useEffect(() => {
    async function checkApiHealth() {
      try {
        const data = await getHealthStatus();

        setHealthData(data);
        setApiStatus("online");
      } catch (error) {
        console.error("Failed to connect to the backend:", error);
        setApiStatus("offline");
      }
    }

    void checkApiHealth();
  }, []);

  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">MLOps Platform</p>

        <h1>ModelForge</h1>

        <p className="description">
          Train, track, deploy, and monitor machine learning models.
        </p>

        <div className={`status status--${apiStatus}`}>
          <span className="status-dot" />

          {apiStatus === "loading" && "Checking backend connection..."}

          {apiStatus === "online" &&
            `${healthData?.service ?? "Backend"} is online`}

          {apiStatus === "offline" && "Backend is offline"}
        </div>
      </section>
    </main>
  );
}

export default App;