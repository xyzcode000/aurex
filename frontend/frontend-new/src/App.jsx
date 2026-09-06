import "./App.css";

function App() {
  return (
    <div className="app">

      <header>
        <h1>🚀 AUREX</h1>
        <p>Project Intelligence & Risk Investigation Engine</p>
      </header>

      <main>
        <h2>Dashboard</h2>

        <section className="project-overview">

          <div className="card">
            <h3>Total Projects</h3>
            <p>12</p>
          </div>

          <div className="card">
            <h3>Active Projects</h3>
            <p>8</p>
          </div>

          <div className="card">
            <h3>High Risk Projects</h3>
            <p>3</p>
          </div>

        </section>

        <section className="recent-projects">
          <h2>Recent Projects</h2>

          <div className="project-card">
            <h3>Project A</h3>
            <p>Status: Active</p>
            <p>Risk: Low</p>
          </div>

          <div className="project-card">
            <h3>Project B</h3>
            <p>Status: Under Review</p>
            <p>Risk: Medium</p>
          </div>

          <div className="project-card">
            <h3>Project C</h3>
            <p>Status: Active</p>
            <p>Risk: High</p>
          </div>

        </section>
      </main>

    </div>
  );
}

export default App;