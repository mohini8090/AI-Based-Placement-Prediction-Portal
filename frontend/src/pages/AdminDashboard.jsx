import { useEffect, useState } from "react";
import { fetchAdminStats, fetchAdminStudents } from "../services/api";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [students, setStudents] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([fetchAdminStats(), fetchAdminStudents()])
      .then(([statsData, studentsData]) => {
        setStats(statsData);
        setStudents(studentsData);
      })
      .catch(() => setError("Couldn't load admin data."));
  }, []);

  if (error) {
    return <section className="dash-section"><div className="container"><p className="form-error">{error}</p></div></section>;
  }
  if (!stats) {
    return <section className="dash-section"><div className="container page-loading">Loading admin dashboard…</div></section>;
  }

  return (
    <section className="dash-section">
      <div className="container">
        <p className="eyebrow">Module 9 — Admin only</p>
        <h1 className="section-title">Admin dashboard</h1>
        <p className="section-sub">Aggregated view across every student who has used the portal.</p>

        <div className="admin-stats-grid">
          <div className="stat-card">
            <span className="eyebrow">Students</span>
            <p className="stat-card-value numeric">{stats.total_students}</p>
          </div>
          <div className="stat-card">
            <span className="eyebrow">Predictions run</span>
            <p className="stat-card-value numeric">{stats.total_predictions}</p>
          </div>
          <div className="stat-card">
            <span className="eyebrow">Placement rate</span>
            <p className="stat-card-value numeric">{stats.placement_rate_percent}%</p>
          </div>
          <div className="stat-card">
            <span className="eyebrow">Avg. predicted package</span>
            <p className="stat-card-value numeric">
              {stats.average_predicted_package ? `₹${stats.average_predicted_package} LPA` : "—"}
            </p>
          </div>
        </div>

        <div className="admin-breakdown-grid">
          <div className="module-panel">
            <h2>Predictions by branch</h2>
            {Object.keys(stats.branch_breakdown).length === 0 ? (
              <p className="stat-card-sub">No predictions yet.</p>
            ) : (
              <ul className="breakdown-list">
                {Object.entries(stats.branch_breakdown).map(([branch, count]) => (
                  <li key={branch}>
                    <span>{branch}</span>
                    <span className="numeric">{count}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="module-panel">
            <h2>Top recommended careers</h2>
            {Object.keys(stats.top_recommended_careers).length === 0 ? (
              <p className="stat-card-sub">No career recommendations yet.</p>
            ) : (
              <ul className="breakdown-list">
                {Object.entries(stats.top_recommended_careers).map(([career, count]) => (
                  <li key={career}>
                    <span>{career}</span>
                    <span className="numeric">{count}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className="table-wrap">
          <h2 style={{ margin: "0 0 1rem" }}>Students</h2>
          <table className="admin-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Resume</th>
                <th>Predictions</th>
                <th>Latest status</th>
                <th>Latest career</th>
              </tr>
            </thead>
            <tbody>
              {students.map((s) => (
                <tr key={s.id}>
                  <td>{s.full_name}</td>
                  <td>{s.email}</td>
                  <td>{s.has_resume ? "✓" : "—"}</td>
                  <td className="numeric">{s.total_predictions}</td>
                  <td>
                    {s.latest_placement_status ? (
                      <span className={`tag ${s.latest_probability >= 0.5 ? "tag-positive" : "tag-warning"}`}>
                        {s.latest_placement_status}
                      </span>
                    ) : "—"}
                  </td>
                  <td>{s.latest_career || "—"}</td>
                </tr>
              ))}
              {students.length === 0 && (
                <tr><td colSpan={6} className="stat-card-sub">No students yet.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
