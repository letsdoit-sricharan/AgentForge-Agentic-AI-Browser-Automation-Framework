# PROJECT_GUIDE.md

# AgentForge

Version: 1.0

---

# 1. Project Overview

AgentForge is a production-grade Agentic AI Automation Framework capable of understanding natural language, planning complex workflows, and autonomously interacting with websites through browser automation.

The framework is designed to be reusable.

BookMyShow is only the first plugin.

Future plugins include:

- Amazon
- Flipkart
- Swiggy
- Zomato
- Gmail
- Google Calendar
- LinkedIn

The core framework must never depend on a specific website.

---

# 2. Vision Statement

Our objective is not to build a movie booking bot.

Our objective is to build a reusable AI Automation Platform.

Every website integration should be implemented as an independent plugin.

---

# 3. Engineering Philosophy

The project should resemble a production software product rather than a college assignment.

Architecture always comes before implementation.

Every module should have one responsibility.

Modules should communicate through interfaces rather than direct dependencies.

The framework must remain independent of any website.

The browser is considered a tool, not part of the AI.

The AI is considered a decision maker, not a browser automation script.

---

# 4. Design Principles

Always follow:

Single Responsibility Principle

Open Closed Principle

Dependency Injection

Loose Coupling

High Cohesion

Interface Driven Design

Composition over Inheritance

Clean Architecture

Domain Driven Design where appropriate

---

# 5. High-Level Architecture

User

↓

Frontend

↓

Backend API

↓

Agent Orchestrator

↓

LangGraph Workflow

↓

Browser Engine

↓

Plugin

↓

Website

---

# 6. Core Components

Frontend

Backend

Agent Core

Memory

Planner

Execution

Verification

Recovery

Browser Engine

Plugin SDK

Plugins

Shared Utilities

---

# 7. AI Agents

The framework currently contains:

Intent Agent

Planning Agent

Execution Agent

Verification Agent

Recovery Agent

Memory Agent

Each agent should have a clearly defined responsibility.

No agent should perform multiple unrelated tasks.

---

# 8. Browser Engine

Browser automation must be abstracted.

The rest of the system should never communicate directly with Playwright.

Browser Engine is responsible for:

Browser lifecycle

Navigation

Click

Type

Scroll

Wait

Downloads

Screenshots

Cookies

Session persistence

---

# 9. Plugin SDK

Plugins are independent modules.

Every plugin should implement a common interface.

Plugins should never modify the framework.

The framework loads plugins dynamically.

---

# 10. Technology Stack

Frontend

Next.js

React

TypeScript

Tailwind

Backend

FastAPI

Python

Database

PostgreSQL

ORM

SQLAlchemy

Browser

Playwright

AI

LangGraph

LLM

OpenAI initially

Ollama support later

Deployment

Docker

Railway

Vercel

---

# 11. Folder Structure

(To be maintained as the project evolves.)

---

# 12. Coding Standards

Python:

PEP8

Type hints required

Docstrings for public methods

No global variables

Avoid hardcoded values

Meaningful variable names

Use logging instead of print()

Frontend:

Functional components

TypeScript only

Reusable components

Avoid duplicate code

Environment variables only for secrets

---

# 13. API Standards

RESTful naming

Version APIs

Consistent JSON responses

Proper HTTP status codes

Centralized exception handling

---

# 14. Database Standards

UUID primary keys

Foreign key constraints

Indexes where required

Soft delete when appropriate

Audit timestamps

---

# 15. Testing Strategy

Unit Tests

Integration Tests

Plugin Tests

Browser Tests

End-to-End Tests

Every major module should be independently testable.

---

# 16. Deployment

Dockerized services

Separate frontend/backend deployments

Environment-specific configurations

CI/CD through GitHub Actions

---

# 17. Future Roadmap

Support multiple plugins.

Support multiple LLM providers.

Support local LLMs.

Voice interaction.

Mobile application.

Distributed agent execution.

Cloud deployment.

---

# 18. AI Assistant Instructions

If an AI assistant contributes to this project, it must follow these rules:

Never redesign the architecture unless explicitly requested.

Never create tightly coupled modules.

Never bypass the Browser Engine.

Never bypass the Plugin SDK.

Never hardcode website-specific logic into the framework.

Prefer modular, reusable, and testable code.

Do not generate code for unrelated modules.

Explain architectural decisions before implementation.

Follow this document as the source of truth.