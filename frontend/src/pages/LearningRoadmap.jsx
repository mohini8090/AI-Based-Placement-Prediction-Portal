import { useEffect, useState } from "react";
import { fetchCareerOptions, fetchRoadmap } from "../services/api";

const PRIORITY_CLASS = { High: "priority-high", Medium: "priority-medium", Low: "priority-low" };

export default function LearningRoadmap() {
  const [careers, setCareers] = useState([]);
  const [targetCareer, setTargetCareer] = useState("");
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchCareerOptions()
      .then((list) => {
        setCareers(list);
        if (list.length > 0) setTargetCareer(list[0]);
      })
      .catch(() => setError("Couldn't load career options."));
  }, []);

  async function runRoadmap(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await fetchRoadmap({ targetCareer });
      setRoadmap(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Couldn't generate a roadmap.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="dash-section">
      <div className="container">
      
        <h1 className="section-title">Learning roadmap</h1>
        <p className="section-sub">
          The highest-priority missing skills for your
          target career, turned into an ordered set of topics to study.
        </p>

        <form onSubmit={runRoadmap} className="skillgap-controls">
          <label className="field">
            <span>Target career</span>
            <select value={targetCareer} onChange={(e) => setTargetCareer(e.target.value)}>
              {careers.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </label>
          <button type="submit" className="btn btn-brass" disabled={loading || !targetCareer}>
            {loading ? "Building roadmap…" : "Build roadmap"}
          </button>
        </form>

        {error && <p className="form-error">{error}</p>}

        {roadmap && (
          roadmap.stages.length === 0 ? (
            <div className="skillgap-results">
              <p className="stat-card-sub">
                No major gaps found for {roadmap.target_career} — your resume already covers the top required skills.
              </p>
            </div>
          ) : (
            <ol className="roadmap-list">
              {roadmap.stages.map((stage) => (
                <li className="roadmap-stage" key={stage.stage}>
                  <div className="roadmap-stage-num numeric">{String(stage.stage).padStart(2, "0")}</div>
                  <div className="roadmap-stage-body">
                    <div className="roadmap-stage-head">
                      <h3>{stage.skill}</h3>
                      <span className={`priority-badge ${PRIORITY_CLASS[stage.priority]}`}>{stage.priority} priority</span>
                    </div>
                    <ul className="roadmap-topics">
                      {stage.topics.map((topic, i) => <li key={i}>{topic}</li>)}
                    </ul>
                  </div>
                </li>
              ))}
            </ol>
          )
        )}
      </div>
    </section>
  );
}
