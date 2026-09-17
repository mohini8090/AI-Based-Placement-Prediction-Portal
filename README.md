# Trajectory — Smart Placement Prediction Portal (all 9 modules)

Frontend: React.js · Backend: FastAPI · Database: MongoDB · ML: scikit-learn

All nine modules, complete and wired together:

1. User Registration & Login
2. Student Dashboard
3. Resume Upload & Parsing
4. Resume Analysis
5. Placement Prediction
6. Career Recommendation
7. Skill Gap Analysis
8. Learning Roadmap
9. Admin Dashboard

## Project structure

```
placement-portal-full/
├── backend/
│   ├── app/
│   │   ├── main.py            FastAPI entrypoint, registers all 9 routers
│   │   ├── database.py        Motor (async MongoDB) client, collections, indexes
│   │   ├── schemas.py         Every request/response shape, module by module
│   │   ├── utils.py           Converts Mongo's _id -> a plain "id" string
│   │   ├── core/
│   │   │   ├── config.py      Settings from .env
│   │   │   ├── security.py    Password hashing + JWT
│   │   │   └── deps.py        get_current_user, require_admin
│   │   ├── ml/
│   │   │   ├── skills_taxonomy.py   Skill keywords, career requirements, learning resources
│   │   │   ├── resume_parser.py     Text extraction + ATS-style scoring (modules 3 & 4)
│   │   │   ├── dataset.py           Synthetic training data generator
│   │   │   ├── train_model.py       Trains placement + career models
│   │   │   ├── predictor.py         Placement inference (module 5)
│   │   │   ├── career_predictor.py  Career recommendation inference (module 6)
│   │   │   └── skill_gap.py         Skill gap + roadmap generation (modules 7 & 8)
│   │   └── routers/
│   │       ├── auth.py         Module 1
│   │       ├── users.py        (supporting) GET /api/users/me
│   │       ├── dashboard.py    Module 2
│   │       ├── resumes.py      Modules 3 & 4
│   │       ├── prediction.py   Module 5
│   │       ├── career.py       Module 6
│   │       ├── skills.py       Modules 7 & 8
│   │       └── admin.py        Module 9
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    └── src/
        ├── pages/
        │   Login.jsx, Register.jsx, Dashboard.jsx, ResumeUpload.jsx, Predict.jsx,
        │   CareerRecommendation.jsx, SkillGapAnalysis.jsx, LearningRoadmap.jsx, AdminDashboard.jsx
        ├── components/
        │   Navbar.jsx, ProtectedRoute.jsx, AdminRoute.jsx, AuthVisual.jsx,
        │   PredictionForm.jsx, ProbabilityGauge.jsx, ResultsPanel.jsx, CareerResultsPanel.jsx
        ├── context/AuthContext.jsx
        ├── services/api.js
        └── styles/tokens.css, app.css
```

## 1. Install MongoDB

Pick one:
- **MongoDB Community Server** (local) — download from mongodb.com/try/download/community.
- **MongoDB Compass** (GUI, optional but recommended) — mongodb.com/products/compass, connect to `mongodb://localhost:27017`.
- **Docker**: `docker run -d -p 27017:27017 --name placement-mongo mongo`
- **MongoDB Atlas** (cloud) — create a free cluster, use its connection string as `MONGO_URI` below.

No schema to run — collections are created automatically on first insert.

## 2. Set up the backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` — for a local MongoDB install, the defaults already work:
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=placement_portal
```

Run it:
```bash
uvicorn app.main:app --reload --port 8000
```
(If Windows blocks `uvicorn.exe` with an Application Control error, run
`python -m uvicorn app.main:app --reload --port 8000` instead — same
effect, routed through `python.exe`.)

## 3. Train the ML models (modules 5 & 6)

```bash
python -m app.ml.train_model
```

Generates a synthetic dataset and trains a placement classifier, a
package regressor, and a career classifier, saving all three to
`app/ml/artifacts/`. Takes under a minute; re-run any time.

## 4. Set up the frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173, register an account, and walk through the
modules from the navbar: Resume → Predict → Career → Skill Gap →
Roadmap. Each feeds into the next — resume skills feed skill gap
analysis, which feeds the roadmap.

## 5. Test the Admin Dashboard (module 9)

Admin access is gated by a `role` field on the user document, which
defaults to `"student"` on registration. To test it, promote your
account manually in MongoDB Compass (or `mongosh`):

```js
use placement_portal
db.users.updateOne(
  { email: "you@example.com" },
  { $set: { role: "admin" } }
)
```

Log out and back in (so the JWT/session picks up the change), and an
**Admin** link appears in the navbar. It shows aggregated stats —
placement rate, branch breakdown, top recommended careers — and a table
of every student. Non-admin users are redirected away from `/admin`
automatically if they try the URL directly.

## What's stateless vs. stored

- **Skill Gap Analysis** and **Learning Roadmap** are computed on the
  fly from `skills_taxonomy.py` — nothing is saved per run, since the
  input (your latest resume's skills + a chosen career) is already
  stored elsewhere.
- **Placement Prediction** and **Career Recommendation** save every run
  to MongoDB, which is what powers both the Dashboard's "latest" cards
  and the Admin Dashboard's aggregates.

## Troubleshooting

- **"ServerSelectionTimeoutError" on startup** — MongoDB isn't running.
- **503 on /api/predict/ or /api/career/recommend** — models aren't
  trained yet; run `python -m app.ml.train_model`.
- **403 on /api/admin/\*** — your account's `role` is still `"student"`;
  see step 5.
- **CORS error in the browser** — check `FRONTEND_ORIGIN` in `.env`
  matches `http://localhost:5173`.

