import ProbabilityGauge from "./ProbabilityGauge";

export default function ResultsPanel({ result }) {
  if (!result) {
    return (
      <div className="results-panel results-empty">
        <p className="eyebrow">Awaiting input</p>
        <h3>Your dashboard shows up here</h3>
        <p>Fill in the form and run a prediction to see your placement odds.</p>
      </div>
    );
  }

  return (
    <div className="results-panel">
      <div className="results-top">
        <ProbabilityGauge probability={result.placement_probability} status={result.placement_status} />
        <div className="results-package">
          
          
        </div>
      </div>

      {result.top_skill_gaps?.length > 0 && (
        <div className="results-block">
          <span className="eyebrow">Focus areas</span>
          <div className="chip-row">
            {result.top_skill_gaps.map((gap) => <span className="chip" key={gap}>{gap}</span>)}
          </div>
        </div>
      )}
    </div>
  );
}
