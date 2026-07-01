# AGENT_RUNTIME.md

Version: 1.0

---

# Agent Runtime

## Purpose

The Agent Runtime is the heart of AgentForge.

It is responsible for converting a natural language request into an executable workflow.

The runtime is independent of any specific website and delegates website-specific behavior to plugins.

The runtime should never directly interact with browser automation libraries or website-specific code.

---

# Runtime Goals

The Agent Runtime must:

- Understand user intent
- Build execution plans
- Execute tasks
- Monitor execution
- Handle failures
- Maintain memory
- Request human approval when required
- Emit events
- Support multiple plugins
- Support future AI models

---

# Runtime Architecture

                        User
                          │
                          ▼
                 Agent Runtime
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
  Intent Agent      Planning Agent      Memory Manager
        │
        ▼
 Task Scheduler
        │
        ▼
 Task Executor
        │
        ▼
 Verification Agent
        │
        ▼
 Recovery Agent
        │
        ▼
 Tool Manager
        │
        ▼
 Browser Engine
        │
        ▼
 Website Plugin

---

# Runtime Lifecycle

User Request

↓

Intent Detection

↓

Memory Retrieval

↓

Task Planning

↓

Plan Validation

↓

Task Scheduling

↓

Task Execution

↓

Verification

↓

Recovery (if required)

↓

Completion

↓

Memory Update

↓

Event Publication

---

# Shared Runtime State

Every component operates on a shared immutable state object.

Example

AgentState

Request ID

Session ID

User ID

Conversation

Intent

Entities

Execution Plan

Current Step

Completed Steps

Failed Steps

Browser State

Plugin State

Memory Context

Current Tool

Current Plugin

Events

Logs

Errors

Result

Every state transition creates a new state.

No component should mutate state directly.

---

# Components

## Intent Agent

Purpose

Understand the user's request.

Input

Natural language.

Output

Structured intent.

Example

Input

Book two tickets for Superman tomorrow.

Output

Movie

Superman

Tickets

2

Date

Tomorrow

Time

Evening

---

Responsibilities

Intent Classification

Entity Extraction

Confidence Scoring

Validation

Clarification Requests

Must NOT

Open browsers.

Call plugins.

---

# Memory Manager

Responsibilities

Load user profile.

Load previous conversations.

Load booking history.

Load preferences.

Persist new memories.

Memory Types

Short-Term

Current conversation.

Long-Term

User preferences.

Working Memory

Current execution.

---

# Planning Agent

Purpose

Convert intent into executable tasks.

Example

Open Browser

↓

Navigate Website

↓

Search Movie

↓

Select Date

↓

Choose Theatre

↓

Select Seats

↓

Proceed Payment

↓

Download Ticket

Planner never executes.

Planner only builds plans.

---

# Plan Validator

Responsibilities

Validate generated plan.

Ensure dependencies.

Ensure tool availability.

Reject impossible plans.

---

# Task Scheduler

Responsibilities

Determine execution order.

Support sequential tasks.

Support future parallel execution.

Manage retries.

Pause execution.

Resume execution.

---

# Task Executor

Purpose

Execute one task at a time.

Responsibilities

Execute planned tasks.

Call Tool Manager.

Receive responses.

Update runtime state.

Publish events.

Task Executor never decides.

Task Executor only executes.

---

# Verification Agent

Purpose

Verify task completion.

Examples

Movie exists.

Seats selected.

Payment initiated.

Ticket downloaded.

Verification determines

Success

Retry

Failure

Human approval

---

# Recovery Agent

Purpose

Recover from failures.

Recovery Options

Retry

Alternative seat

Alternative timing

Alternative theatre

Request clarification

Abort execution

Log incident

---

# Tool Manager

Purpose

Provide tools to the runtime.

Examples

Browser Tool

PDF Tool

Email Tool

Calendar Tool

Database Tool

Filesystem Tool

OCR Tool

Future tools should require no runtime modifications.

---

# Event Manager

Every important action generates events.

Examples

AGENT_STARTED

INTENT_DETECTED

PLAN_CREATED

PLAN_VALIDATED

EXECUTION_STARTED

TASK_STARTED

TASK_COMPLETED

TASK_FAILED

RECOVERY_STARTED

RECOVERY_COMPLETED

BOOKING_SUCCESS

BOOKING_FAILED

AGENT_COMPLETED

---

# Human Approval

Some actions require approval.

Examples

Payments

Deleting data

Purchases

Sending emails

Approval Flow

Pause execution

↓

Notify frontend

↓

Receive approval

↓

Resume execution

---

# Retry Strategy

Recoverable Errors

Network timeout

Browser crash

Slow loading

Retry three times.

Exponential backoff.

Non-Recoverable Errors

Movie unavailable

Invalid plugin

Authentication failure

Unsupported request

Stop execution.

---

# Runtime States

CREATED

INITIALIZED

PLANNING

WAITING

EXECUTING

VERIFYING

RECOVERING

COMPLETED

FAILED

CANCELLED

Only valid transitions are allowed.

---

# Plugin Invocation

Runtime

↓

Tool Manager

↓

Browser Engine

↓

Plugin

↓

Website

The runtime never communicates directly with plugins.

---

# Browser Interaction

The runtime never uses Playwright.

Only Browser Engine knows Playwright.

---

# Memory Updates

Memory updates occur

Before planning.

After execution.

After completion.

After failures.

---

# Logging

Every component must generate logs.

Include

Timestamp

Agent Run ID

Request ID

Component

Execution Time

Current State

Result

---

# Performance Goals

Intent Detection

< 2 seconds

Planning

< 3 seconds

Task Scheduling

< 1 second

Browser Launch

< 5 seconds

Execution

Depends on website.

---

# Security

No secrets in runtime.

No credentials in prompts.

No payment information stored.

Environment variables only.

JWT authentication.

Encrypted memory.

---

# Extensibility

Future runtimes may support

Voice

Desktop Automation

API Automation

Mobile Automation

Robot Control

The runtime must remain unchanged.

Only tools should change.

---

# Engineering Rules

The runtime is the brain.

The planner thinks.

The scheduler organizes.

The executor executes.

The verifier checks.

The recovery agent heals.

The Tool Manager provides capabilities.

The Browser Engine controls browsers.

Plugins understand websites.

No component should violate another component's responsibility.

Every dependency must point downward.

No circular dependencies.

Implementation must always follow this document.