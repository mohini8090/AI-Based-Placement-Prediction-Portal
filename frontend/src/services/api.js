import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = axios.create({ baseURL: API_BASE_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("tpp_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function registerUser({ fullName, email, password }) {
  const { data } = await api.post("/api/auth/register", {
    full_name: fullName,
    email,
    password,
  });
  return data;
}

export async function loginUser({ email, password }) {
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);
  const { data } = await api.post("/api/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data;
}

export async function fetchCurrentUser() {
  const { data } = await api.get("/api/users/me");
  return data;
}

export async function fetchDashboard() {
  const { data } = await api.get("/api/dashboard/");
  return data;
}

export async function uploadResume(file) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/api/resumes/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function fetchLatestResume() {
  const { data } = await api.get("/api/resumes/latest");
  return data;
}

export async function submitPrediction(studentInput) {
  const { data } = await api.post("/api/predict/", studentInput);
  return data;
}

export async function fetchPredictionHistory() {
  const { data } = await api.get("/api/predict/history");
  return data;
}

export async function recommendCareer(studentInput) {
  const { data } = await api.post("/api/career/recommend", studentInput);
  return data;
}

export async function fetchLatestCareer() {
  const { data } = await api.get("/api/career/latest");
  return data;
}

export async function fetchCareerOptions() {
  const { data } = await api.get("/api/skills/careers");
  return data.careers;
}

export async function analyzeSkillGap({ targetCareer, knownSkills = [], useLatestResume = true }) {
  const { data } = await api.post("/api/skills/gap-analysis", {
    target_career: targetCareer,
    known_skills: knownSkills,
    use_latest_resume: useLatestResume,
  });
  return data;
}

export async function fetchRoadmap({ targetCareer, knownSkills = [], useLatestResume = true }) {
  const { data } = await api.post("/api/skills/roadmap", {
    target_career: targetCareer,
    known_skills: knownSkills,
    use_latest_resume: useLatestResume,
  });
  return data;
}

export async function fetchAdminStats() {
  const { data } = await api.get("/api/admin/stats");
  return data;
}

export async function fetchAdminStudents() {
  const { data } = await api.get("/api/admin/students");
  return data;
}
