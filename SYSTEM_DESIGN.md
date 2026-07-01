# SYSTEM_DESIGN.md

# AgentForge System Design

Version: 1.0

---

# Purpose

This document describes the overall system design of AgentForge.

It explains how every component communicates, what responsibilities each module has, and how a user request flows through the system.

This document intentionally avoids implementation details.

Implementation belongs in the respective module documentation.

---

# 1. System Overview

AgentForge is a modular Agentic AI Automation Platform.

The framework allows users to interact with websites using natural language.

The framework itself is independent of any website.

Website-specific behavior is implemented through plugins.

Current Plugin:

- BookMyShow

Future Plugins:

- Amazon
- Flipkart
- Swiggy
- Gmail
- Google Calendar
- LinkedIn

---

# 2. Design Goals

The architecture should satisfy the following goals.

## Scalability

Support additional plugins without modifying the framework.

---

## Modularity

Every module should have a single responsibility.

---

## Reusability

Browser automation should be reusable across plugins.

---

## Extensibility

Adding a new website should require only a new plugin.

---

## Reliability

Agent execution should survive recoverable failures.

---

## Observability

Every important action should generate events and logs.

---

## Testability

Every module should be independently testable.

---

# 3. High Level Architecture

                       User
                         │
                         ▼
                Frontend (Next.js)
                         │
                  REST/WebSockets
                         │
                         ▼
                Backend API (FastAPI)
                         │
                         ▼
                Agent Orchestrator
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
    Memory Service   Tool Registry    Event Bus
                         │
                         ▼
                 LangGraph Workflow
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
     Intent        Planner         Executor
         │
         ▼
   Verification
         │
         ▼
     Recovery
         │
         ▼
   Browser Engine
         │
         ▼
     Plugin SDK
         │
         ▼
BookMyShow Plugin

---

# 4. Component Responsibilities

## Frontend

Responsibilities

- User authentication
- Chat interface
- Dashboard
- Booking history
- Ticket viewer
- Real-time progress

Must NOT

- Perform AI reasoning
- Perform browser automation
- Access plugins directly

---

## Backend API

Responsibilities

- Authentication
- Authorization
- API endpoints
- Session management
- Database access
- Invoke Agent Orchestrator

Must NOT

- Execute browser logic
- Contain website-specific logic

---

## Agent Orchestrator

Responsibilities

- Start workflows
- Maintain execution state
- Route tasks
- Invoke LangGraph
- Handle retries
- Monitor execution

Must NOT

- Click buttons
- Parse HTML
- Know website layouts

---

## Memory Service

Responsibilities

- User preferences
- Agent memory
- Context
- Previous conversations
- Session state

---

## Tool Registry

Responsibilities

Maintain available tools.

Examples

Browser Tool

PDF Tool

Email Tool

Calendar Tool

Future Tools

OCR

Filesystem

REST API

Database

---

## Event Bus

Responsibilities

Broadcast events.

Examples

AGENT_STARTED

MOVIE_FOUND

SEAT_SELECTED

PAYMENT_PENDING

BOOKING_COMPLETED

BOOKING_FAILED

---

## Browser Engine

Responsibilities

Browser lifecycle

Tabs

Navigation

Typing

Mouse

Keyboard

Downloads

Cookies

Screenshots

Session persistence

Must never know BookMyShow.

---

## Plugin SDK

Responsibilities

Define plugin interface.

Load plugins.

Validate plugins.

Lifecycle management.

---

## Plugins

Responsibilities

Implement website-specific behavior.

Examples

BookMyShow

Amazon

Flipkart

---

# 5. End-to-End Request Flow

Step 1

User submits

Book two tickets for Superman tomorrow.

↓

Frontend sends request.

↓

Backend authenticates user.

↓

Backend starts Agent Orchestrator.

↓

Memory loads user preferences.

↓

Intent Agent extracts meaning.

↓

Planner creates workflow.

↓

Executor starts execution.

↓

Browser Engine opens browser.

↓

BookMyShow Plugin performs actions.

↓

Verification checks results.

↓

Recovery handles failures if required.

↓

Ticket downloaded.

↓

Database updated.

↓

Frontend receives completion event.

↓

User downloads ticket.

---

# 6. Agent Lifecycle

User Request

↓

Intent

↓

Planning

↓

Execution

↓

Verification

↓

Recovery (if needed)

↓

Completion

---

# 7. Browser Lifecycle

Initialize Browser

↓

Create Context

↓

Load Cookies

↓

Open Website

↓

Execute Tasks

↓

Download Files

↓

Close Browser

---

# 8. Plugin Lifecycle

Load Plugin

↓

Initialize

↓

Validate Configuration

↓

Execute Task

↓

Handle Errors

↓

Cleanup

---

# 9. Event Flow

Every module publishes events.

Example

Agent Started

↓

Planning Started

↓

Planning Finished

↓

Execution Started

↓

Browser Opened

↓

Movie Found

↓

Seats Selected

↓

Payment Waiting

↓

Payment Confirmed

↓

Ticket Downloaded

↓

Completed

---

# 10. Failure Handling

Possible Failures

Movie unavailable

Seats unavailable

Browser crash

Website changed

Network failure

Plugin failure

Payment timeout

Recovery Strategy

Retry

Alternative path

Ask user

Abort

Log error

---

# 11. State Management

Agent State

Planning State

Browser State

Plugin State

Session State

User State

All state transitions should be deterministic.

---

# 12. Logging

Every module must generate structured logs.

Every request should have

Request ID

Session ID

Agent Run ID

User ID

Timestamp

Duration

---

# 13. Security

JWT Authentication

HTTPS

Encrypted secrets

Environment variables

No hardcoded credentials

Least privilege access

Audit logs

---

# 14. Scalability

Support

Multiple users

Multiple browsers

Multiple plugins

Multiple LLMs

Horizontal scaling

Distributed workers

---

# 15. Future Expansion

The architecture should support

Voice agents

Desktop agent

Mobile application

Cloud execution

Local execution

API integrations

Autonomous scheduling

---

# Design Principles

The framework must remain independent of websites.

The browser is a tool.

Plugins own website knowledge.

Agents own decision making.

Every module has one responsibility.

Every dependency should point inward.

Implementation must always follow this document.