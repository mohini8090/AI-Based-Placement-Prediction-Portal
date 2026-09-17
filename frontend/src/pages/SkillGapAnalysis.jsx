import { useEffect, useState } from "react";
import { fetchCareerOptions, analyzeSkillGap } from "../services/api";

export default function SkillGapAnalysis() {
  const [careers, setCareers] = useState([]);
  const [targetCareer, setTargetCareer] = useState("");
  const [useLatestResume, setUseLatestResume] = useState(true);
  const [result, setResult] = useState(null);
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

  async function runAnalysis(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await analyzeSkillGap({ targetCareer, useLatestResume });
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Couldn't run the analysis.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="dash-section">
      <div className="container">
        
        <h1 className="section-title">Skill gap analysis</h1>
        <p className="section-sub">
          Pick a target career and we'll compare its required skills against the ones
          detected on your latest resume, weighted by how important each one is.
        </p>

        <form onSubmit={runAnalysis} className="skillgap-controls">
          <label className="field">
            <span>Target career</span>
            <select value={targetCareer} onChange={(e) => setTargetCareer(e.target.value)}>
              {careers.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </label>

          <label className="checkbox-field">
            <input
              type="checkbox"
              checked={useLatestResume}
              onChange={(e) => setUseLatestResume(e.target.checked)}
            />
            <span>Use skills from my latest uploaded resume</span>
          </label>

          <button type="submit" className="btn btn-brass" disabled={loading || !targetCareer}>
            {loading ? "Analyzing…" : "Analyze gap"}
          </button>
        </form>

        {error && <p className="form-error">{error}</p>}

        {result && (
          <div className="skillgap-results">
            <div className="readiness-block">
              <span className="eyebrow">Readiness for {result.target_career}</span>
              <div className="readiness-bar-track">
                <div
                  className="readiness-bar-fill"
                  style={{ width: `${result.readiness_percent}%` }}
                />
              </div>
              <span className="numeric readiness-pct">{result.readiness_percent}%</span>
            </div>

            <div className="skillgap-columns">
              <div>
                <span className="eyebrow">Skills you have ({result.matched_skills.length})</span>
                <div className="chip-row">
                  {result.matched_skills.length > 0
                    ? result.matched_skills.map((s) => <span className="chip chip-teal" key={s.skill}>{s.skill}</span>)
                    : <p className="stat-card-sub">No overlap yet — see the gaps on the right.</p>}
                </div>
              </div>
              <div>
                <span className="eyebrow">Gaps to close ({result.missing_skills.length})</span>
                <div className="chip-row">
                  {result.missing_skills.map((s) => (
                    <span className={`chip ${s.weight >= 3 ? "" : "chip-muted"}`} key={s.skill}>
                      {s.skill}{s.weight >= 3 ? " ●" : ""}
                    </span>
                  ))}
                </div>
                {result.missing_skills.some((s) => s.weight >= 3) && (
                  <p className="stat-card-sub" style={{ marginTop: "0.6rem" }}>● = high priority for this role</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
