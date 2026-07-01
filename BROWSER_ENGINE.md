# BROWSER_ENGINE.md

# Browser Engine Design

Version: 1.0

---

# Purpose

The Browser Engine is the browser abstraction layer of AgentForge.

Its responsibility is to provide a unified interface for browser automation while hiding the implementation details of the underlying automation framework.

The Browser Engine is independent of:

- Websites
- Plugins
- AI Models
- Runtime Logic
- Business Rules

It should only know how to control browsers.

---

# Mission Statement

The Browser Engine provides reliable, reusable and secure browser automation capabilities to the Agent Runtime.

It acts as the bridge between the runtime and browser automation technologies.

The Browser Engine must never contain website-specific logic.

---

# Design Goals

The Browser Engine should be

- Reusable
- Modular
- Stateless where possible
- Asynchronous
- Replaceable
- Testable
- Observable

---

# High Level Architecture

Agent Runtime

↓

Task Executor

↓

Browser Engine

↓

Browser Adapter

↓

Browser Instance

↓

Website Plugin

↓

Target Website

---

# Responsibilities

The Browser Engine is responsible for

- Browser lifecycle
- Browser contexts
- Tabs
- Navigation
- Mouse interaction
- Keyboard interaction
- Downloads
- Screenshots
- Cookies
- Local Storage
- Session persistence
- Waiting strategies
- Browser events
- Error reporting

---

# Non Responsibilities

The Browser Engine must NEVER

Understand websites

Understand CSS selectors

Know BookMyShow

Know Amazon

Perform AI reasoning

Plan tasks

Validate business rules

Choose seats

Decide what to click

These belong elsewhere.

---

# Core Components

Browser Manager

↓

Session Manager

↓

Context Manager

↓

Page Manager

↓

Navigation Controller

↓

Interaction Controller

↓

Download Manager

↓

Cookie Manager

↓

Storage Manager

↓

Screenshot Manager

↓

Event Publisher

↓

Browser Adapter

---

# Browser Manager

Responsibilities

Launch browser

Close browser

Restart browser

Manage browser pool

Browser configuration

---

# Session Manager

Responsibilities

Create sessions

Resume sessions

Destroy sessions

Store session metadata

Handle session timeout

---

# Context Manager

Responsibilities

Create browser context

Destroy context

Load cookies

Save cookies

Incognito mode

User profile isolation

---

# Page Manager

Responsibilities

Open tabs

Close tabs

Switch tabs

Reload

Refresh

Navigate back

Navigate forward

---

# Navigation Controller

Responsibilities

Open URL

Wait for page

Reload

Redirect handling

Timeout handling

Network idle detection

---

# Interaction Controller

Responsibilities

Click

Double click

Right click

Hover

Type

Press keys

Scroll

Drag

Drop

Select dropdown

Checkbox

Radio buttons

---

# Download Manager

Responsibilities

Monitor downloads

Rename downloads

Move downloads

Track download status

Return file path

---

# Screenshot Manager

Responsibilities

Take screenshots

Capture full page

Capture elements

Store screenshots

Return screenshot paths

---

# Cookie Manager

Responsibilities

Save cookies

Load cookies

Delete cookies

Export cookies

Import cookies

---

# Storage Manager

Responsibilities

Local Storage

Session Storage

IndexedDB

Cache Storage

---

# Event Publisher

Responsibilities

Publish browser events.

Examples

Browser Started

Browser Closed

Page Loaded

Download Started

Download Completed

Navigation Failed

Interaction Failed

Screenshot Captured

---

# Browser Adapter

Purpose

Provide an abstraction over browser automation libraries.

Current Implementation

Playwright Adapter

Future

Selenium Adapter

CDP Adapter

Remote Browser Adapter

Cloud Browser Adapter

---

# Browser Lifecycle

Initialize

↓

Launch Browser

↓

Create Context

↓

Open Page

↓

Perform Actions

↓

Download Files

↓

Save Session

↓

Close Context

↓

Close Browser

---

# Browser State

Created

↓

Launching

↓

Ready

↓

Busy

↓

Waiting

↓

Downloading

↓

Error

↓

Closed

---

# Waiting Strategy

Never use fixed sleep calls.

Preferred

Wait for element

Wait for network idle

Wait for page load

Wait for response

Wait for download

Timeout only as fallback.

---

# Error Handling

Recoverable

Slow network

Popup interruption

Element delayed

Temporary browser crash

Retry with exponential backoff.

---

Non Recoverable

Browser executable missing

Corrupted profile

Plugin incompatibility

Security block

Abort execution.

---

# Logging

Every browser operation must log

Timestamp

Session ID

Browser ID

Context ID

Page ID

Operation

Duration

Status

Error

---

# Security

Cookies encrypted

Downloads validated

No credentials logged

Secure session storage

Sandbox enabled

HTTPS preferred

---

# Performance

Reuse browser contexts

Avoid unnecessary browser launches

Lazy page creation

Close unused tabs

Minimize memory consumption

---

# Future Expansion

Support

Remote browsers

Headless browsers

Mobile emulation

Proxy rotation

Multiple browsers

Cloud browsers

Browser clustering

---

# Engineering Principles

Browser Engine controls browsers.

Plugins understand websites.

Runtime makes decisions.

Execution performs work.

Browser Adapter hides automation libraries.

No website logic belongs inside the Browser Engine.

Implementation must follow this document.