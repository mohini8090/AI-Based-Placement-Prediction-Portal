import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchDashboard } from "../services/api";

function initials(name) {
  return name.split(" ").map((p) => p[0]).slice(0, 2).join("").toUpperCase();
}

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDashboard()
      .then(setData)
      .catch(() => setError("Couldn't load your dashboard. Try refreshing."));
  }, []);

  if (error) {
    return <section className="dash-section"><div className="container"><p className="form-error">{error}</p></div></section>;
  }
  if (!data) {
    return <section className="dash-section"><div className="container page-loading">Loading your dashboard…</div></section>;
  }

  const memberSince = new Date(data.member_since).toLocaleDateString(undefined, { month: "long", year: "numeric" });

  return (
    <section className="dash-section">
      <div className="container">
        <div className="dash-header">
          <div className="dash-avatar">{initials(data.full_name)}</div>
          <div>
            <h1>Welcome, {data.full_name.split(" ")[0]}</h1>
            <span className="dash-role-badge">{data.role}</span>
          </div>
        </div>

        <div className="dash-grid">
          <div>
            <div className="stat-card">
              <span className="eyebrow">Member since</span>
              <p className="stat-card-value">{memberSince}</p>
              <p className="stat-card-sub">{data.email}</p>
            </div>

            <div className="stat-card">
              <span className="eyebrow">Resume</span>
              {data.has_resume ? (
                <>
                  <p className="stat-card-value numeric">{Math.round(data.latest_resume_score)}<span style={{ color: "var(--text-low)", fontSize: "0.5em" }}> / 100</span></p>
                  <p className="stat-card-sub">Latest ATS score — <Link to="/resume" style={{ color: "var(--brass-bright)" }}>view analysis</Link></p>
                </>
              ) : (
                <>
                  <p className="stat-card-value" style={{ color: "var(--text-low)" }}>Not uploaded</p>
                  <p className="stat-card-sub"><Link to="/resume" style={{ color: "var(--brass-bright)" }}>Upload your resume</Link> to get an ATS score.</p>
                </>
              )}
            </div>

            <div className="stat-card">
              <span className="eyebrow">Placement prediction</span>
              {data.latest_prediction ? (
                <>
                  <p className="stat-card-value numeric">{Math.round(data.latest_prediction.placement_probability * 100)}%</p>
                  <p className="stat-card-sub">{data.latest_prediction.placement_status} — {data.total_predictions} prediction{data.total_predictions !== 1 ? "s" : ""} run</p>
                </>
              ) : (
                <>
                  <p className="stat-card-value" style={{ color: "var(--text-low)" }}>No predictions yet</p>
                  <p className="stat-card-sub"><Link to="/predict" style={{ color: "var(--brass-bright)" }}>Run your first prediction</Link></p>
                </>
              )}
            </div>

            <div className="stat-card">
              <span className="eyebrow">Career recommendation</span>
              {data.latest_career ? (
                <>
                  <p className="stat-card-value" style={{ fontSize: "var(--step-1)" }}>{data.latest_career}</p>
                  <p className="stat-card-sub"><Link to="/career" style={{ color: "var(--brass-bright)" }}>Run again</Link>, <Link to="/skills" style={{ color: "var(--brass-bright)" }}>check your skill gap</Link>, or <Link to="/roadmap" style={{ color: "var(--brass-bright)" }}>see a learning roadmap</Link></p>
                </>
              ) : (
                <>
                  <p className="stat-card-value" style={{ color: "var(--text-low)" }}>Not run yet</p>
                  <p className="stat-card-sub"><Link to="/career" style={{ color: "var(--brass-bright)" }}>Get a career recommendation</Link></p>
                </>
              )}
            </div>
          </div>

          {/* <div className="module-panel">
            <h2>Your roadmap</h2>
            <ul className="module-list">
              {data.modules_unlocked.map((m) => (
                <li className="module-item is-unlocked" key={m}><span className="module-dot">✓</span>{m}</li>
              ))}
              {data.modules_upcoming.map((m) => (
                <li className="module-item is-upcoming" key={m}><span className="module-dot">•</span>{m}</li>
              ))}
            </ul>
          </div> */}
        </div>
      </div>
    </section>
  );
}
