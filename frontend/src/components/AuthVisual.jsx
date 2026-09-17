export default function AuthVisual({ eyebrow, quote }) {
  return (
    <div className="auth-visual">
      <span className="eyebrow">{eyebrow}</span>

      <p className="auth-visual-quote">{quote}</p>

      <svg viewBox="0 0 320 120" width="100%" style={{ maxWidth: 280 }} aria-hidden="true">
        <polyline
          points="10,100 60,88 110,70 160,52 210,36 300,10"
          fill="none"
          stroke="var(--teal)"
          strokeWidth="2.5"
          strokeLinecap="round"
        />
        {[
          [10, 100], [60, 88], [110, 70], [160, 52], [210, 36], [300, 10],
        ].map(([x, y], i) => (
          <circle key={i} cx={x} cy={y} r="4.5" fill="var(--ink-950)" stroke="var(--brass-bright)" strokeWidth="2" />
        ))}
      </svg>

      
    </div>
  );
}
