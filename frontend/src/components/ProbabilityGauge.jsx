const RADIUS = 90;
const CIRCUMFERENCE = Math.PI * RADIUS;

export default function ProbabilityGauge({ probability, status }) {
  const pct = Math.round(probability * 100);
  const offset = CIRCUMFERENCE * (1 - probability);
  const color = probability >= 0.5 ? "var(--teal-bright)" : "var(--coral-bright)";

  return (
    <div className="gauge">
      <svg viewBox="0 0 220 130" className="gauge-svg">
        <path d="M 20 110 A 90 90 0 0 1 200 110" fill="none" stroke="var(--ink-700)" strokeWidth="14" strokeLinecap="round" />
        <path
          d="M 20 110 A 90 90 0 0 1 200 110"
          fill="none" stroke={color} strokeWidth="14" strokeLinecap="round"
          strokeDasharray={CIRCUMFERENCE} strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.8s ease, stroke 0.4s ease" }}
        />
        <text x="110" y="95" textAnchor="middle" className="gauge-value numeric">{pct}%</text>
      </svg>
      <p className={`gauge-status ${probability >= 0.5 ? "is-positive" : "is-warning"}`}>{status}</p>
    </div>
  );
}
