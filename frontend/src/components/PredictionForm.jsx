import { useState } from "react";

const BRANCHES = ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil", "AI/ML"];

const INITIAL = {
  cgpa: "7.5", tenth_percentage: "80", twelfth_percentage: "78", backlogs: "0",
  internships: "1", projects: "2", certifications: "1",
  aptitude_score: "65", technical_score: "65", communication_score: "70", coding_score: "60",
  branch: "CSE",
};

const SCORE_FIELDS = [
  ["aptitude_score", "Aptitude score"],
  ["technical_score", "Technical knowledge"],
  ["communication_score", "Communication skills"],
  ["coding_score", "Coding proficiency"],
];

export default function PredictionForm({ onSubmit, submitting }) {
  const [values, setValues] = useState(INITIAL);

  function update(field, value) {
    setValues((v) => ({ ...v, [field]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit({
      cgpa: parseFloat(values.cgpa),
      tenth_percentage: parseFloat(values.tenth_percentage),
      twelfth_percentage: parseFloat(values.twelfth_percentage),
      backlogs: parseInt(values.backlogs, 10),
      internships: parseInt(values.internships, 10),
      projects: parseInt(values.projects, 10),
      certifications: parseInt(values.certifications, 10),
      aptitude_score: parseFloat(values.aptitude_score),
      technical_score: parseFloat(values.technical_score),
      communication_score: parseFloat(values.communication_score),
      coding_score: parseFloat(values.coding_score),
      branch: values.branch,
    });
  }

  return (
    <form onSubmit={handleSubmit} className="predict-form">
      <div className="form-group">
        <h3>Academics</h3>
        <div className="form-row">
          <label className="field">
            <span>CGPA (0–10)</span>
            <input type="number" step="0.01" min="0" max="10" required
              value={values.cgpa} onChange={(e) => update("cgpa", e.target.value)} />
          </label>
          <label className="field">
            <span>10th %</span>
            <input type="number" step="0.1" min="0" max="100" required
              value={values.tenth_percentage} onChange={(e) => update("tenth_percentage", e.target.value)} />
          </label>
          <label className="field">
            <span>12th %</span>
            <input type="number" step="0.1" min="0" max="100" required
              value={values.twelfth_percentage} onChange={(e) => update("twelfth_percentage", e.target.value)} />
          </label>
        </div>
        <div className="form-row">
          <label className="field">
            <span>Active backlogs</span>
            <input type="number" min="0" required
              value={values.backlogs} onChange={(e) => update("backlogs", e.target.value)} />
          </label>
          <label className="field">
            <span>Branch</span>
            <select value={values.branch} onChange={(e) => update("branch", e.target.value)}>
              {BRANCHES.map((b) => <option key={b} value={b}>{b}</option>)}
            </select>
          </label>
        </div>
      </div>

      <div className="form-group">
        <h3>Experience</h3>
        <div className="form-row">
          <label className="field">
            <span>Internships</span>
            <input type="number" min="0" required
              value={values.internships} onChange={(e) => update("internships", e.target.value)} />
          </label>
          <label className="field">
            <span>Projects</span>
            <input type="number" min="0" required
              value={values.projects} onChange={(e) => update("projects", e.target.value)} />
          </label>
          <label className="field">
            <span>Certifications</span>
            <input type="number" min="0" required
              value={values.certifications} onChange={(e) => update("certifications", e.target.value)} />
          </label>
        </div>
      </div>

      <div className="form-group">
        <h3>Skill scores (0–100)</h3>
        <div className="form-row">
          {SCORE_FIELDS.map(([key, label]) => (
            <label className="field" key={key}>
              <span>{label}</span>
              <input type="number" min="0" max="100" required
                value={values[key]} onChange={(e) => update(key, e.target.value)} />
            </label>
          ))}
        </div>
      </div>

      <button type="submit" className="btn btn-brass btn-lg" disabled={submitting}>
        {submitting ? "Scoring your profile…" : "Run prediction"}
      </button>
    </form>
  );
}
