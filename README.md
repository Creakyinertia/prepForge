# PrepForge

PrepForge is an Interview Preparation SaaS designed to help engineers learn, revise, track progress, and measure interview readiness through structured roadmaps and topic-centric learning.

The project is being built as a production-oriented full-stack application to demonstrate backend architecture, system design, scalable APIs, and frontend engineering practices.

---

## Vision

Most interview preparation platforms focus on content.

PrepForge focuses on **Interview Readiness**.

The goal is not simply to read topics, but to help users:

* Learn concepts
* Track progress
* Revise effectively
* Practice interview questions
* Measure readiness
* Identify weak areas
* Build a personalized preparation workflow

---

## Core Philosophy

PrepForge is built around a **Topic-Centric Architecture**.

Everything revolves around Topics.

Example:

JavaScript
└── Event Loop

React
└── Reconciliation

System Design
└── Load Balancing

A Topic can contain:

* Learning Content
* Resources
* Interview Questions
* Personal Notes
* Progress Tracking
* Revision Tracking
* Readiness Metrics

---

## Tech Stack

### Backend

* FastAPI
* PostgreSQL
* SQLAlchemy 2.0
* Alembic
* JWT Authentication
* Refresh Token Sessions
* Pydantic

### Frontend (Planned)

* Next.js (App Router)
* TypeScript
* Tailwind CSS
* React Query
* Feature-Based Architecture

---

## Architecture

### Backend Structure

```text
features/
├── auth/
├── roadmaps/
├── topics/
├── resources/
├── questions/
├── bookmarks/
├── notes/
├── progress/
├── question_progress/
├── revisions/
├── dashboard/
├── readiness/
├── search/
├── home/
```

### Architectural Principles

* Feature-Based Architecture
* Service Layer Pattern
* Business Logic Separated from Routes
* UUID Primary Keys
* PostgreSQL First Design
* Scalable Domain Modeling
* Production-Oriented API Design

---

## Authentication

Implemented:

* User Registration
* User Login
* Access Tokens
* Refresh Tokens
* Refresh Token Hashing
* Refresh Token Persistence
* JWT Authentication
* Protected Routes
* Admin Authorization

Security decisions:

* Refresh tokens stored hashed in database
* JWT access tokens remain stateless
* Separate refresh token sessions
* Role-based admin access

---

## Content Domain

Content is platform-managed.

Regular users can consume content but cannot create or modify it.

### Roadmaps

Examples:

* JavaScript Roadmap
* React Roadmap
* System Design Roadmap

### Topics

Examples:

* Event Loop
* Closures
* React Reconciliation

Each topic contains:

* Title
* Slug
* Description
* Markdown Content

### Resources

Supported resource types:

* Article
* Documentation
* Video
* Other

### Questions

Interview questions are attached to topics.

Question metadata:

* Title
* Answer
* Difficulty

---

## Learning Domain

### Topic Progress

Tracks learning status per topic.

Statuses:

* Not Started
* In Progress
* Completed

### Question Progress

Tracks interview question mastery.

Statuses:

* Not Attempted
* Attempted
* Mastered

### Notes

Users can maintain personal topic notes.

Relationship:

```text
User
 └── Topic
      └── Note
```

### Bookmarks

Users can save topics for later review.

### Revisions

Spaced repetition inspired revision scheduling.

Current revision flow:

```text
Topic Completed
        ↓
Revision Scheduled
        ↓
Revision Completed
        ↓
Next Revision Scheduled
```

---

## Analytics & Insights

### Dashboard

Aggregated metrics:

* Completed Topics
* Topics In Progress
* Due Revisions
* Notes Count
* Roadmap Activity

### Topic Readiness

Measures readiness at topic level.

Factors:

* Topic Completion
* Question Mastery
* Revision Status

### Roadmap Progress

Tracks completion percentage across roadmap topics.

### Roadmap Readiness

Aggregates readiness across an entire roadmap.

Example:

```json
{
  "roadmap": "JavaScript",
  "readiness_score": 82
}
```

---

## Search

Implemented:

```http
GET /search/topics?q=event
```

Supports topic discovery and navigation.

Future versions may leverage PostgreSQL Full Text Search.

---

## Home Experience

Personalized home dashboard includes:

* Continue Learning
* Due Revisions
* Recent Bookmarks
* Readiness Metrics

---

## Testing

Implemented:

* API Tests
* Service Layer Tests
* Custom Exceptions
* Error Handling

Focus:

* Reliability
* Maintainability
* Production Readiness

---

## Current Status

Completed:

* Authentication
* Refresh Token Sessions
* Roadmaps
* Topics
* Topic Content
* Resources
* Questions
* Notes
* Bookmarks
* Topic Progress
* Question Progress
* Revision Scheduling
* Dashboard APIs
* Topic Readiness
* Roadmap Progress
* Roadmap Readiness
* Search
* Home APIs
* Testing
* Admin Authorization

---

## Planned Features

### Near Term

* Admin Content Management
* Recently Viewed Topics
* Soft Deletes
* Frontend Application

### Future

* AI Coach
* Mock Interviews
* Quiz Generation
* Interview Readiness Recommendations
* Community Features
* Learning Analytics

---

## Project Goal

PrepForge is intentionally designed as a flagship portfolio project demonstrating:

* Backend Architecture
* Domain Modeling
* System Design Thinking
* API Design
* Authentication & Security
* Scalable PostgreSQL Design
* Full-Stack Engineering Practices

The long-term goal is to evolve PrepForge into a complete Interview Readiness Platform rather than a simple content management system.
