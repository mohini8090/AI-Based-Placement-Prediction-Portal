import { useState } from "react";
import PredictionForm from "../components/PredictionForm";
import ResultsPanel from "../components/ResultsPanel";
import { submitPrediction } from "../services/api";

export default function Predict() {
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(payload) {
    setSubmitting(true);
    setError("");
    try {
      const data = await submitPrediction(payload);
      setResult(data);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Couldn't run the prediction. Make sure the backend is running and models are trained."
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="dash-section">
      <div className="container">
       
        <h1 className="section-title">Placement prediction</h1>
        <p className="section-sub">
          These are the same signals a placement cell reviews — academics, hands-on
          experience, and the four skill scores most recruiters test for.
        </p>

        {error && <p className="form-error">{error}</p>}

        <div className="predict-grid">
          <PredictionForm onSubmit={handleSubmit} submitting={submitting} />
          <ResultsPanel result={result} />
        </div>
      </div>
    </section>
  );
}
