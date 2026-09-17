import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser, fetchCurrentUser } from "../services/api";
import { useAuth } from "../context/AuthContext";
import AuthVisual from "../components/AuthVisual";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const data = await loginUser({ email, password });
      localStorage.setItem("tpp_token", data.access_token);
      const me = await fetchCurrentUser();
      login(data.access_token, me);
      navigate("/dashboard");
    } catch (err) {
      setError(err?.response?.data?.detail || "Couldn't log in. Check your details and try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-shell">
      <AuthVisual
        eyebrow="Placement intelligence"
        quote={<>See the placement you're <span>on track for</span>, before the interview does.</>}
      />

      <div className="auth-form-side">
        <div className="auth-form-card">
          <p className="eyebrow">Welcome back</p>
          <h1>Log in</h1>

          <form onSubmit={handleSubmit} className="form">
            <label className="field">
              <span>Email</span>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@college.edu"
              />
            </label>

            <label className="field">
              <span>Password</span>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
              />
            </label>

            {error && <p className="form-error">{error}</p>}

            <button type="submit" className="btn btn-brass btn-lg" disabled={submitting}>
              {submitting ? "Logging in…" : "Log in"}
            </button>
          </form>

          <p className="auth-switch">
            New here? <Link to="/register">Create an account</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
