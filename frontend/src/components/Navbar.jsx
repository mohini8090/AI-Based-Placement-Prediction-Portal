import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="navbar">
      <div className="container navbar-inner">
        <Link to="/" className="brand">
          <span className="brand-mark" aria-hidden="true" />
          Trajectory
        </Link>

        <nav className="navlinks">
          {user ? (
            <>
              <Link to="/dashboard">Dashboard</Link>
              <Link to="/resume">Resume</Link>
              <Link to="/predict">Predict</Link>
              <Link to="/career">Career</Link>
              <Link to="/skills">Skill Gap</Link>
              <Link to="/roadmap">Roadmap</Link>
              {user.role === "admin" && <Link to="/admin">Admin</Link>}
              <span className="navlinks-user numeric">{user.full_name}</span>
              <button
                className="btn btn-ghost"
                onClick={() => {
                  logout();
                  navigate("/login");
                }}
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Log in</Link>
              <Link to="/register" className="btn btn-brass">
                Get started
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
