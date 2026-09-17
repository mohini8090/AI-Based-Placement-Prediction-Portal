import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminRoute from "./components/AdminRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ResumeUpload from "./pages/ResumeUpload";
import Predict from "./pages/Predict";
import CareerRecommendation from "./pages/CareerRecommendation";
import SkillGapAnalysis from "./pages/SkillGapAnalysis";
import LearningRoadmap from "./pages/LearningRoadmap";
import AdminDashboard from "./pages/AdminDashboard";

export default function App() {
  return (
    <>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/resume" element={<ProtectedRoute><ResumeUpload /></ProtectedRoute>} />
          <Route path="/predict" element={<ProtectedRoute><Predict /></ProtectedRoute>} />
          <Route path="/career" element={<ProtectedRoute><CareerRecommendation /></ProtectedRoute>} />
          <Route path="/skills" element={<ProtectedRoute><SkillGapAnalysis /></ProtectedRoute>} />
          <Route path="/roadmap" element={<ProtectedRoute><LearningRoadmap /></ProtectedRoute>} />
          <Route path="/admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
        </Routes>
      </main>
      <footer className="footer">
        <div className="container">
          <span>Trajectory — Smart Placement Prediction Portal made by &#10084;Mohini Rajvanshi &#10084;</span>
        </div>
      </footer>
    </>
  );
}
