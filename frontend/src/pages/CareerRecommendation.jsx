import { useState } from "react";
import PredictionForm from "../components/PredictionForm";
import CareerResultsPanel from "../components/CareerResultsPanel";
import { recommendCareer } from "../services/api";

export default function CareerRecommendation() {
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(payload) {
    setSubmitting(true);
    setError("");
    try {
      const data = await recommendCareer(payload);
      setResult(data);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Couldn't generate a recommendation. Make sure the career model is trained."
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="dash-section">
      <div className="container">
        
        <h1 className="section-title">Career recommendation</h1>
        <p className="section-sub">
          Same academic and skill signals as the placement predictor, run through a
          separate model trained to match profiles to the career tracks they fit best.
        </p>

        {error && <p className="form-error">{error}</p>}

        <div className="predict-grid">
          <PredictionForm onSubmit={handleSubmit} submitting={submitting} />
          <CareerResultsPanel result={result} />
        </div>
      </div>
    </section>
  );
}
