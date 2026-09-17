import { useEffect, useState } from "react";
import { uploadResume, fetchLatestResume } from "../services/api";

export default function ResumeUpload() {
  const [analysis, setAnalysis] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [dragOver, setDragOver] = useState(false);

  useEffect(() => {
    fetchLatestResume()
      .then(setAnalysis)
      .catch(() => {}); // no resume yet — fine, just show the upload state
  }, []);

  async function handleFile(file) {
    if (!file) return;
    setError("");
    setUploading(true);
    try {
      const data = await uploadResume(file);
      setAnalysis(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Couldn't process that file. Try a PDF, DOCX, or TXT resume.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <section className="dash-section">
      <div className="container">
        
        <h1 className="section-title">Resume upload &amp; analysis</h1>
        <p className="section-sub">
          Upload a PDF, DOCX, or TXT resume. We'll pull out your skills, check for the
          sections recruiters look for, and score it against common ATS screening signals.
        </p>

        <div className="resume-grid">
          <div
            className={`dropzone ${dragOver ? "is-dragover" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              handleFile(e.dataTransfer.files?.[0]);
            }}
          >
            <p className="dropzone-title">{uploading ? "Analyzing your resume…" : "Drop your resume here"}</p>
            <p className="dropzone-sub">PDF, DOCX, or TXT — up to 5 MB</p>
            <label className="btn btn-brass">
              Choose a file
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                style={{ display: "none" }}
                onChange={(e) => handleFile(e.target.files?.[0])}
                disabled={uploading}
              />
            </label>
            {error && <p className="form-error" style={{ marginTop: "1rem" }}>{error}</p>}
          </div>

          {analysis ? (
            <div className="resume-analysis">
              <div className="resume-analysis-top">
                <div>
                  <span className="eyebrow">Analyzed file</span>
                  <p className="resume-filename">{analysis.filename}</p>
                </div>
                <div className="ats-score">
                  <span className="ats-score-value numeric">{Math.round(analysis.ats_score)}</span>
                  <span className="ats-score-label">ATS score</span>
                </div>
              </div>

              <div className="resume-block">
                <span className="eyebrow">Skills detected ({analysis.skills.length})</span>
                <div className="chip-row">
                  {analysis.skills.length > 0
                    ? analysis.skills.map((s) => <span className="chip" key={s}>{s}</span>)
                    : <p className="stat-card-sub">No recognizable skill keywords found.</p>}
                </div>
              </div>

              <div className="resume-block">
                <span className="eyebrow">Sections found</span>
                <div className="chip-row">
                  {analysis.sections_found.map((s) => (
                    <span className="chip chip-teal" key={s}>{s}</span>
                  ))}
                </div>
              </div>

              {analysis.suggestions.length > 0 && (
                <div className="resume-block">
                  <span className="eyebrow">Suggestions</span>
                  <ul className="suggestion-list">
                    {analysis.suggestions.map((s, i) => <li key={i}>{s}</li>)}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="resume-analysis resume-analysis-empty">
              <p className="eyebrow">No resume yet</p>
              <h3>Your analysis will show up here</h3>
              <p>Upload a resume on the left to see your ATS score, detected skills, and suggestions.</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
