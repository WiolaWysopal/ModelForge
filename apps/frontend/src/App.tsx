import "./App.css";

function App() {
  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">MLOps Platform</p>

        <h1>ModelForge</h1>

        <p className="description">
          Train, track, deploy, and monitor machine learning models.
        </p>

        <div className="status">
          <span className="status-dot" />
          Frontend is running
        </div>
      </section>
    </main>
  );
}

export default App;