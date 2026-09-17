export default function CareerResultsPanel({ result }) {
  if (!result) {
    return (
      <div className="results-panel results-empty">
        <p className="eyebrow">Awaiting input</p>
        <h3>Your recommendation shows up here</h3>
        <p>Fill in the form and run it to see your top-fit career tracks.</p>
      </div>
    );
  }

  const top = result.alternatives[0];
  const rest = result.alternatives.slice(1);

  return (
    <div className="results-panel">
      <span className="eyebrow">Top recommendation</span>
      <h2 className="career-title">{top.career}</h2>
      <div className="confidence-bar-row">
        <div className="confidence-bar-track">
          <div className="confidence-bar-fill" style={{ width: `${Math.round(top.confidence * 100)}%` }} />
        </div>
        <span className="numeric confidence-pct">{Math.round(top.confidence * 100)}%</span>
      </div>

      {rest.length > 0 && (
        <div className="results-block">
          <span className="eyebrow">Also worth considering</span>
          <div className="alt-career-list">
            {rest.map((alt) => (
              <div className="alt-career-row" key={alt.career}>
                <span>{alt.career}</span>
                <div className="confidence-bar-row">
                  <div className="confidence-bar-track confidence-bar-track-sm">
                    <div className="confidence-bar-fill confidence-bar-fill-muted" style={{ width: `${Math.round(alt.confidence * 100)}%` }} />
                  </div>
                  <span className="numeric confidence-pct-sm">{Math.round(alt.confidence * 100)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
