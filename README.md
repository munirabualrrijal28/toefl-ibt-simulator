## 🚨🚨🚨🚨very Important Note🚨🚨🚨🚨 the project is under development if you faced any problem just open simulator.html in the browser directly and it will work
# TOEFL iBT Simulator — 2026 Adaptive Edition

A full-stack, multi-stage adaptive TOEFL iBT practice simulator aligned to CEFR band scoring (1.0 – 6.0). The application simulates the real 2026 TOEFL iBT exam format with adaptive difficulty routing, timed sections, and diverse question types across all four language skills.

---

## Tech Stack

| Layer    | Technology                                           |
| -------- | ---------------------------------------------------- |
| Backend  | Python · FastAPI · SQLModel · SQLite                 |
| Frontend | React 19 · TypeScript · Vite · TailwindCSS 4 · Axios |
| Icons    | Lucide React                                         |
| Database | SQLite (file-based, `toefl_simulator.db`)            |

---

## Architecture Overview

```
TOEFL IBT Prep test/
├── backend/                  # FastAPI REST API + data layer
│   ├── main.py               # API endpoints & adaptive routing logic
│   ├── models.py             # SQLModel ORM models (TestSession, SectionState, QuestionItem, UserResponse)
│   ├── database.py           # SQLite engine & session factory
│   ├── seed.py               # Seed script — 63 CEFR-aligned questions
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React SPA
│   ├── src/
│   │   ├── App.tsx            # Main application component (all screens & question renderers)
│   │   ├── components/
│   │   │   └── Shell.tsx      # Dual-pane exam layout with countdown timer
│   │   └── services/
│   │       └── api.ts         # Axios client & session service
│   ├── package.json
│   └── vite.config.ts
├── simulator.html             # Standalone HTML prototype
├── test_no_repeat.py          # Test script to verify no-repeat item selection
└── toefl_simulator.db         # SQLite database file
```

---

## How It Works

### Adaptive Routing Engine

The test uses a **multi-stage adaptive approach** that mirrors the real 2026 TOEFL iBT format:

1. **Routing Stage** — The test begins with a set of routing questions in each adaptive section (Reading, Listening).
2. **Performance Evaluation** — After routing, the engine calculates the student's accuracy. If accuracy ≥ 70%, the student is routed to the **Hard (Academic)** pool; otherwise, they proceed to the **Standard** pool.
3. **Fixed Path** — Writing and Speaking sections follow a fixed (non-adaptive) path with set question pools.

### Difficulty Pools

| Pool       | Description                                          |
| ---------- | ---------------------------------------------------- |
| `ROUTING`  | Initial placement questions (Reading, Listening)     |
| `STANDARD` | Standard difficulty (routed if accuracy < 70%)       |
| `HARD`     | Academic-level difficulty (routed if accuracy ≥ 70%) |
| `FIXED`    | Non-adaptive pool (Writing, Speaking)                |

### Scoring

Each section receives a CEFR-aligned band score. Hard-path students score in the 4.0–6.0 range, while standard-path students score in the 1.0–4.5 range. An overall score is calculated as the average across all sections.

---

## Test Sections & Question Types

### Reading (30 min, Adaptive)

- **READ_DAILY_LIFE** — Comprehension of everyday passages (notices, announcements)
- **COMPLETE_WORDS** — Fill in missing word parts from academic passages
- **ACADEMIC_PASSAGE** — University-level reading comprehension (Hard pool)

### Listening (29 min, Adaptive)

- **LISTEN_AND_RESPONSE** — Short conversation / campus-life comprehension
- **ACADEMIC_TALK** — Academic lecture comprehension (Hard pool)

### Writing (23 min, Fixed)

- **BUILD_SENTENCE** — Arrange scrambled words into grammatically correct sentences
- **WRITE_EMAIL** — Compose formal emails with guided bullet points
- **ACADEMIC_DISCUSSION** — Respond to academic discussion prompts with context

### Speaking (8 min, Fixed)

- **LISTEN_AND_REPEAT** — Repeat academic sentences (uses browser microphone)
- **TAKE_INTERVIEW** — Open-ended spoken responses to interview prompts

---

## Content Bank

The seed script (`backend/seed.py`) populates the database with **63 unique, CEFR-aligned questions** distributed across all four sections and multiple difficulty pools. All content is original and covers diverse academic and daily-life topics.

---

## API Endpoints

| Method | Endpoint                        | Description                        |
| ------ | ------------------------------- | ---------------------------------- |
| POST   | `/session/start`                | Create a new test session          |
| GET    | `/session/{id}/current-state`   | Get the active section state       |
| GET    | `/session/{id}/next-item`       | Fetch the next question (adaptive) |
| POST   | `/session/{id}/submit-response` | Submit an answer                   |
| GET    | `/session/{id}/score`           | Get final scores after completion  |

---

## How to Run

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m backend.seed          # Seed the question database
uvicorn backend.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                     # Starts on http://localhost:5173
```

The frontend expects the backend to be running at `http://localhost:8000`.

---

## Key Features

- **Realistic exam simulation** with section-specific time limits and countdown timer
- **Multi-stage adaptive difficulty** routing based on real-time performance
- **Dual-pane exam UI** with a professional shell layout mirroring the actual TOEFL interface
- **Microphone recording** for the Speaking section (browser MediaRecorder API)
- **Word counter** for writing tasks
- **Results dashboard** with per-section band scores and overall CEFR score
- **No question repeats** — the engine tracks answered items per session to prevent duplicates
- **Glassmorphism landing page** with gradient accents and smooth transitions



----------------------------------------
# toefl-ibt-simulator
A dynamic, multi-stage TOEFL iBT test simulator built with FastAPI. [Work in Progress]

# 🎓 TOEFL iBT Test Simulator [Work in Progress]

## 📝 Overview
A dynamic, multi-stage TOEFL iBT test simulator designed to replicate the official exam environment. Currently focusing on the **Reading Section**, this backend application is built to handle complex, time-sensitive testing logic, asynchronous operations, and dynamic content delivery. 

## 🚀 Tech Stack
* **Backend Framework:** FastAPI (Python)
* **Architecture:** RESTful API design & Modular structure
* **Data Handling:** Pydantic (Data validation) & JSON/Relational Database

## ⚙️ Key Features
* **Asynchronous Performance:** Built utilizing FastAPI's async capabilities for high-performance, non-blocking API requests.
* **Reading Module (Active):** Fully functional reading comprehension engine with real-time logical evaluation.
* **Scalable System Design:** Architected with a clean, modular structure to seamlessly integrate upcoming sections (Listening, Speaking, Writing).
* **Robust Routing:** Efficient endpoint routing to manage multi-stage test states and user sessions.


```
## 🚧 Roadmap
[x] Core Backend Architecture ,
[x] Reading Section Logic & API Endpoints , 
[ ] Listening Section Integration ,
[ ] Database Migration & User Authentication

