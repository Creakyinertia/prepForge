# PrepForge

PrepForge is an Interview Preparation SaaS built to help software engineers prepare for technical interviews through structured learning, roadmap-based progression, topic tracking, revision scheduling, and future AI-assisted coaching.

This project is being developed as a production-oriented full-stack application with a strong focus on scalable backend architecture, clean code practices, and real-world engineering patterns.

---

## Vision

Most interview preparation platforms focus on content delivery.

PrepForge focuses on:

* Structured learning paths
* Topic-centric progress tracking
* Revision and retention
* Personalized interview preparation
* Future AI-assisted coaching

The goal is to help engineers not only learn concepts but also retain them and prepare effectively for interviews.

---

## Current Features

### Authentication

* User Registration
* User Login
* JWT Access Tokens
* Refresh Tokens
* Refresh Token Rotation
* Logout
* Current User Endpoint (`/auth/me`)

### Roadmaps

* Create Roadmap
* List Roadmaps
* Get Roadmap by ID

### Topics

* Create Topic
* List Topics
* Get Topic by ID

### Roadmap Topic Mapping

* Attach Topics to Roadmaps
* Ordered Roadmap Structure
* Many-to-Many Relationship Support

### Progress Tracking

* Track Topic Progress
* Update Progress Status
* Status Types:

  * NOT_STARTED
  * IN_PROGRESS
  * COMPLETED

---

## Planned Features

### Revision Scheduler

* Spaced Repetition
* Due Revision Tracking
* Revision History

### Notes

* Topic-specific Notes
* Personal Knowledge Base

### Resources

* Curated Learning Resources
* External References

### Question Bank

* Interview Questions
* Categorized by Topic

### AI Coach

* Interview Guidance
* Personalized Recommendations
* Learning Assistance

### Mock Interviews

* Technical Mock Sessions
* Feedback Generation

### Community Features

* Shared Learning Paths
* Collaboration
* Discussion

---

## Architecture

### Backend

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic

### Authentication

* JWT Access Tokens
* Refresh Tokens
* Token Rotation Strategy
* Password Hashing with pwdlib (Argon2)

### Architecture Style

Feature-Based Architecture with Service Layer.

```text
backend/

├── core/
├── dependencies/
├── models/
│
├── features/
│   ├── auth/
│   ├── roadmaps/
│   ├── topics/
│   └── progress/
│
├── migrations/
└── main.py
```

### Design Principles

* Separation of Concerns
* Service Layer Pattern
* Scalable Domain Modeling
* UUID Primary Keys
* PostgreSQL First
* Future AI Integration Ready

---

## Current Domain Model

```text
User
│
├── Progress
│
Roadmap
│
├── RoadmapTopic
│
Topic
```

### Roadmap Structure

```text
Roadmap
    ↕
RoadmapTopic
    ↕
Topic
```

A Topic can belong to multiple Roadmaps without duplication.

---

## Progress Tracking

```text
User
    ↕
TopicProgress
    ↕
Topic
```

Each user has a unique progress state for every topic.

---

## Development Goals

This project is intentionally designed to demonstrate:

* Backend Engineering
* System Design
* API Design
* Database Design
* Scalable Architecture
* Full-Stack Development

The focus is on building software using patterns commonly found in production systems rather than tutorial-style CRUD applications.

---

## Status

🚧 Active Development

Current Phase:

* Authentication ✅
* Roadmaps ✅
* Topics ✅
* Progress Tracking ✅
* Revision Scheduler 🚧
* Notes ⏳
* AI Coach ⏳

---

## Author

Built as a long-term engineering portfolio project focused on modern full-stack architecture and interview preparation tooling.
