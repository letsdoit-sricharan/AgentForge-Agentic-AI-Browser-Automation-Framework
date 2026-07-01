# PLUGIN_SDK.md

# AgentForge Plugin SDK

Version: 1.0

---

# Purpose

The Plugin SDK defines the contract between AgentForge and all website integrations.

Plugins extend the platform without requiring changes to the runtime.

The SDK ensures every plugin behaves consistently regardless of the target website.

---

# Mission Statement

The Plugin SDK enables developers to integrate new websites into AgentForge through standardized interfaces.

The runtime should never contain website-specific knowledge.

Every website should be represented as an independent plugin.

---

# Plugin Philosophy

Plugins own business knowledge.

The Runtime owns reasoning.

The Browser Engine owns browser automation.

The Plugin SDK owns communication between them.

---

# Plugin Lifecycle

Plugin Discovery

↓

Plugin Registration

↓

Plugin Validation

↓

Plugin Initialization

↓

Plugin Execution

↓

Plugin Cleanup

↓

Plugin Unloading

---

# Plugin Manager

Responsibilities

- Discover plugins
- Register plugins
- Load plugins
- Unload plugins
- Manage versions
- Resolve dependencies
- Provide plugins to the runtime

The runtime never loads plugins directly.

---

# Plugin Registry

Responsibilities

Maintain information about installed plugins.

Information stored

Plugin Name

Version

Author

Description

Supported Website

Capabilities

Status

Compatibility

Configuration

---

# Plugin Loader

Responsibilities

Load plugin

Unload plugin

Reload plugin

Validate plugin

Handle plugin failures

---

# Plugin Metadata

Every plugin must expose metadata.

Example

Plugin Name

Version

Author

Supported Domain

Description

Capabilities

Permissions Required

Minimum SDK Version

---

# Plugin Interface

Every plugin must implement the following lifecycle.

Initialize

Validate

Authenticate

Execute

Recover

Cleanup

Health Check

Shutdown

---

# Plugin Responsibilities

A plugin is responsible for

Website navigation

Selectors

Business rules

Validation

Recovery strategies

Workflow execution

Data extraction

Result formatting

---

# Plugin Non Responsibilities

Plugins must never

Perform AI reasoning

Store user accounts

Manage databases

Handle authentication tokens

Control browser lifecycle

Plan workflows

Modify runtime state

---

# Plugin Communication

Runtime

↓

Task Executor

↓

Plugin Manager

↓

Plugin

↓

Browser Engine

↓

Website

Plugins never communicate directly with the runtime.

---

# Plugin Execution Flow

Task Received

↓

Validate Task

↓

Translate Task

↓

Invoke Browser Engine

↓

Receive Browser Result

↓

Validate Output

↓

Return Structured Result

---

# Plugin Configuration

Plugins should support configurable settings.

Examples

Default timeout

Language

Region

Preferred browser

Retry count

Feature flags

Configuration should never be hardcoded.

---

# Capabilities

Plugins declare supported capabilities.

Examples

Search

Booking

Authentication

Download

Payment Initiation

Data Extraction

Notification

The runtime should query capabilities instead of assuming them.

---

# Error Categories

Recoverable

Slow page

Popup

Temporary network issue

Retry allowed.

Non Recoverable

Website redesign

Unsupported workflow

Authentication failure

Missing permissions

Abort execution.

---

# Recovery Strategy

Plugins may

Retry

Navigate alternative path

Refresh page

Dismiss popup

Request runtime clarification

Return failure

Plugins never retry forever.

---

# Browser Interaction

Plugins never use Playwright directly.

Plugins communicate only with the Browser Engine.

The Browser Engine exposes abstract browser actions.

---

# Result Format

Every plugin should return a standardized result.

Status

Success

Failure

Cancelled

Warnings

Extracted Data

Logs

Artifacts

Downloaded Files

Screenshots

Suggested Recovery

---

# Logging

Plugins must log

Execution ID

Plugin Name

Task

Operation

Duration

Result

Errors

Warnings

---

# Security

Plugins must never

Log passwords

Store payment information

Store authentication cookies outside approved storage

Leak user data

Hardcode credentials

---

# Versioning

Plugins should follow semantic versioning.

MAJOR.MINOR.PATCH

The runtime should validate SDK compatibility before loading.

---

# Testing Requirements

Every plugin must provide

Unit tests

Integration tests

Mock browser tests

Failure scenario tests

Health check tests

---

# Example Plugin Structure

plugins/

bookmyshow/

metadata

configuration

workflow

validators

recovery

parsers

tests

README

---

# Current Plugin

BookMyShow

Capabilities

Search Movies

Select Theatre

Select Show

Seat Selection

Payment Initiation

Ticket Download

---

# Future Plugins

Amazon

Flipkart

Swiggy

Zomato

LinkedIn

Google Calendar

Gmail

GitHub

The runtime should not require modification to support them.

---

# Engineering Principles

Plugins own website knowledge.

Browser Engine owns browser control.

Runtime owns reasoning.

Execution Engine owns execution.

Plugin SDK owns integration.

Every plugin must remain isolated.

No plugin should affect another plugin.

Implementation must follow this document.