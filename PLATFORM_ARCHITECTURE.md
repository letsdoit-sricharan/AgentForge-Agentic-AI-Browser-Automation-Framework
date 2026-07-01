# PLATFORM_ARCHITECTURE.md

# AgentForge Platform Architecture

Version: 1.0

---

# Platform Overview

AgentForge is a modular AI Automation Platform designed to execute complex digital workflows using natural language.

Rather than building a single-purpose automation bot, AgentForge provides a reusable execution platform capable of interacting with websites through standardized plugins.

The platform separates intelligence, execution, browser automation, and website-specific logic into independent components.

BookMyShow is the first plugin built on top of the platform and serves as a demonstration of the framework's capabilities.

The architecture is intentionally designed to support future integrations without modifying the platform itself.

---

# Vision

Our goal is not to automate one website.

Our goal is to build a reusable AI Automation Platform capable of executing browser-based workflows across multiple domains.

The platform should allow developers to integrate new websites simply by creating plugins.

The intelligence layer should remain unchanged regardless of which website is automated.

---

# Core Philosophy

AgentForge follows four fundamental principles.

## Intelligence should be reusable.

The AI should never know how BookMyShow works.

It should only know how to solve problems.

---

## Websites are plugins.

Every website should exist as an independent plugin.

The framework should never contain website-specific code.

---

## Browser automation is infrastructure.

Browser automation is treated as a reusable infrastructure service.

The AI should never communicate directly with Playwright.

---

## Execution is independent from reasoning.

Planning is different from execution.

The AI decides what should happen.

The execution engine performs the work.

---

# Platform Layers

AgentForge consists of multiple independent layers.

User Experience Layer

↓

Application Layer

↓

Agent Runtime

↓

Execution Layer

↓

Tool Layer

↓

Browser Layer

↓

Plugin Layer

↓

Target Website

Every layer has a clearly defined responsibility.

Each layer communicates only with adjacent layers.

---

# Layer Responsibilities

## User Experience Layer

Responsibilities

- Chat Interface
- Dashboard
- Authentication
- Booking History
- Notifications
- Ticket Viewer

The UI never performs AI reasoning.

---

## Application Layer

Responsibilities

- REST API
- Authentication
- User Sessions
- Database Access
- Agent Invocation
- WebSocket Communication

The application layer manages users and requests.

It does not perform automation.

---

## Agent Runtime

Responsibilities

- Understand requests
- Build execution plans
- Maintain execution state
- Coordinate tools
- Handle recovery
- Manage memory

The runtime is the decision-making engine.

---

## Execution Layer

Responsibilities

- Execute plans
- Schedule tasks
- Monitor execution
- Publish events
- Handle retries

Execution should not make decisions.

---

## Tool Layer

Responsibilities

Provide reusable capabilities.

Examples

Browser

PDF

Email

Calendar

Filesystem

REST API

Database

OCR

Future tools should integrate without changing the runtime.

---

## Browser Layer

Responsibilities

Abstract browser automation.

Provide

Navigation

Typing

Clicking

Downloads

Cookies

Sessions

Screenshots

Browser lifecycle

The Browser Layer should never understand websites.

---

## Plugin Layer

Responsibilities

Translate generic runtime requests into website-specific actions.

Each plugin owns

Selectors

Navigation logic

Validation

Website recovery

Business rules

---

## Target Website

Examples

BookMyShow

Amazon

Flipkart

Swiggy

LinkedIn

Gmail

Google Calendar

The platform treats every website equally.

---

# Platform Independence

The following components must never depend on websites.

Agent Runtime

Execution Engine

Memory

Browser Engine

Tool Manager

API

Frontend

Database

Only plugins may contain website-specific knowledge.

---

# Component Relationships

Frontend

↓

Backend

↓

Agent Runtime

↓

Execution Engine

↓

Tool Manager

↓

Browser Engine

↓

Plugin

↓

Website

Dependencies must always point downward.

No circular dependencies are allowed.

---

# Why Plugins?

Without plugins

AI

↓

Browser

↓

BookMyShow

Adding Amazon would require modifying the AI.

Adding Swiggy would require modifying the browser logic.

This leads to tightly coupled software.

With plugins

AI

↓

Browser

↓

Plugin

↓

Website

The runtime never changes.

Only plugins evolve.

---

# Why Browser Abstraction?

Browser automation libraries change.

Playwright today.

Something else tomorrow.

The rest of the platform should never notice.

Only the Browser Layer should know the underlying automation technology.

---

# Why Separate Planning and Execution?

Planning answers

"What should happen?"

Execution answers

"How do we make it happen?"

Keeping these responsibilities separate improves

Maintainability

Testing

Scalability

Debugging

Future parallel execution

---

# Scalability Strategy

The platform should support

Multiple users

Multiple browsers

Multiple AI providers

Multiple plugins

Cloud execution

Distributed execution

Local execution

Future mobile agents

Voice agents

API-based agents

Desktop automation

The architecture should not require redesign for these features.

---

# Engineering Principles

Every component has one responsibility.

Every dependency points downward.

No business logic inside infrastructure.

No browser logic inside AI.

No website logic inside runtime.

Plugins own website knowledge.

Tools own capabilities.

Runtime owns reasoning.

Execution owns execution.

---

# Long-Term Vision

AgentForge should eventually become a general-purpose AI Automation Platform capable of orchestrating browser, API, desktop, and cloud workflows through a unified execution engine.

BookMyShow is simply the first demonstration plugin.

The platform itself is the product.

Plugins are examples of its capabilities.

---

# Design Statement

The architecture prioritizes modularity, extensibility, maintainability, and clean separation of responsibilities.

Every future feature should integrate into the existing platform rather than requiring architectural redesign.

Implementation must always preserve these principles.