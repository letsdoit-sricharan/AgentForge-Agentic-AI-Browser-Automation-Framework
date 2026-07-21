# AgentForge Architecture

## Overview

AgentForge is a production-grade Agentic AI Browser Automation Framework built on **Clean Architecture** principles. It transforms natural language requests into browser automation through a layered, plugin-based architecture.

## Core Principles

1. **Clean Architecture** - Clear separation of concerns across layers
2. **Dependency Inversion** - All layers depend on abstractions, not implementations
3. **Browser Independence** - Playwright is isolated to the Browser Engine layer only
4. **Plugin Independence** - Framework has zero knowledge of specific plugins
5. **SOLID Principles** - Every component has a single, well-defined responsibility
6. **Production Quality** - Comprehensive error handling, logging, and testing

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                     User / AI Planner                           │
│                   Natural Language Request                      │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                  EXECUTION ORCHESTRATOR                         │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  • Accepts OrchestratedRequest                         │    │
│  │  • Resolves plugin by name or capability              │    │
│  │  • Resolves workflow within plugin                    │    │
│  │  • Creates WorkflowContext                            │    │
│  │  • Executes workflow                                  │    │
│  │  • Returns standardized OrchestratedResult            │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                     PLUGIN FRAMEWORK                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Plugin Registry:     Track all registered plugins     │    │
│  │  Plugin Loader:       Dynamically load plugin modules  │    │
│  │  Plugin Manager:      Lifecycle management             │    │
│  │  Plugin State:        Track execution states           │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                          PLUGINS                                │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  • BookMyShow (reference implementation)              │    │
│  │  • Amazon (future)                                     │    │
│  │  • Flipkart (future)                                   │    │
│  │  • IRCTC (future)                                      │    │
│  │  • LinkedIn (future)                                   │    │
│  │  • MakeMyTrip (future)                                 │    │
│  │                                                         │    │
│  │  Each plugin contains:                                 │    │
│  │    - Workflows (business orchestration)               │    │
│  │    - Workflow Steps (task execution)                  │    │
│  │    - Page Objects (browser interactions)              │    │
│  │    - Models (domain data)                             │    │
│  │    - Validators (input validation)                    │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                      ACTION LIBRARY                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Browser-independent actions:                          │    │
│  │  • Navigation: Navigate, WaitAction                    │    │
│  │  • Element: Click, Fill, Hover, Select                │    │
│  │  • Keyboard: Type, Press, Shortcut                    │    │
│  │  • Mouse: Move, Drag, Scroll                          │    │
│  │  • Page: Screenshot, PDF, Evaluate                    │    │
│  │  • File: Upload, Download                             │    │
│  │  • Locator: Find, WaitFor, WaitUntilHidden           │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BROWSER ENGINE                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Abstractions:                                         │    │
│  │  • Browser (interface)                                 │    │
│  │  • Session (interface)                                 │    │
│  │  • Page (interface)                                    │    │
│  │  • Locator (interface)                                 │    │
│  │                                                         │    │
│  │  Playwright Implementation:                            │    │
│  │  • PlaywrightBrowser                                   │    │
│  │  • PlaywrightSession                                   │    │
│  │  • PlaywrightPage                                      │    │
│  │  • PlaywrightLocator                                   │    │
│  │                                                         │    │
│  │  ⚠️  ONLY layer that imports Playwright                │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
                     Playwright Library
                           ↓
                    Browser (Chrome/Firefox/Safari)
```

## Execution Flow

### High-Level Flow

```
1. User Request
   ↓
2. AI Planner (future) converts to OrchestratedRequest
   ↓
3. Execution Orchestrator
   ├─→ Resolves Plugin
   ├─→ Resolves Workflow
   ├─→ Creates WorkflowContext
   └─→ Executes Workflow
   ↓
4. Workflow
   ├─→ Validates Input
   └─→ Executes Steps Sequentially
   ↓
5. Each Step
   ├─→ Extracts data from WorkflowContext
   ├─→ Delegates to Page Object
   └─→ Returns StepResult
   ↓
6. Page Object
   ├─→ Uses Action Library
   └─→ Interacts with Browser
   ↓
7. Action Library
   ├─→ Uses Browser Engine Interfaces
   └─→ Never imports Playwright
   ↓
8. Browser Engine
   ├─→ Implements browser abstractions
   └─→ Only layer that imports Playwright
   ↓
9. Result propagates back up
   ↓
10. OrchestratedResult returned to user
```

### Detailed Example: Movie Booking

```
User: "Book Inception in Mumbai"
     ↓
AI Planner (future): Creates OrchestratedRequest
     ↓
ExecutionOrchestrator:
     ├─→ PluginResolver.resolve("bookmyshow")
     ├─→ WorkflowResolver.resolve(plugin, "booking_workflow")
     ├─→ Create WorkflowContext(plugin_context, session, page, input_data)
     └─→ Execute BookingWorkflow
          ↓
BookingWorkflow:
     ├─→ Validate BookingRequest
     └─→ Execute Steps:
          1. OpenHomepageStep
               └─→ HomePage.open() → NavigateAction
          2. SelectCityStep
               └─→ HomePage.select_city("Mumbai") → FillAction, ClickAction
          3. SearchMovieStep
               └─→ MoviePage.search_movie("Inception") → FillAction
          4. SelectMovieStep
               └─→ MoviePage.select_movie() → ClickAction
          5. ChooseDateStep
               └─→ DatePage.select_date() → ClickAction
          6. ChooseTheatreStep
               └─→ TheatrePage.select_theatre() → ClickAction
          7. ChooseShowStep
               └─→ ShowPage.select_show() → ClickAction
          8. ChooseSeatsStep
               └─→ SeatPage.select_seats() → ClickAction
          9. InitiatePaymentStep
               └─→ PaymentPage.initiate() → ClickAction
          10. DownloadTicketStep
               └─→ TicketPage.download() → ClickAction
     ↓
OrchestratedResult: {success: true, output: {...}}
```

## Component Responsibilities

### Execution Orchestrator

**Purpose**: Bridge between runtime and plugins

**Responsibilities**:
- Accept OrchestratedRequest with plugin/workflow names
- Resolve plugin using PluginResolver
- Resolve workflow using WorkflowResolver
- Create WorkflowContext with browser resources
- Execute workflow
- Return standardized OrchestratedResult

**Does NOT**:
- Know about specific plugins (BookMyShow, Amazon, etc.)
- Know about specific workflows
- Import Playwright
- Manage browser lifecycle directly

### Plugin Framework

**Purpose**: Dynamic plugin management

**Components**:
- **PluginRegistry**: Centralized plugin storage and lookup
- **PluginLoader**: Dynamic module loading and instantiation
- **PluginManager**: Lifecycle orchestration (load, initialize, execute, shutdown)
- **PluginState**: State machine for plugin lifecycle

**Responsibilities**:
- Load plugins dynamically from filesystem
- Track plugin states (UNLOADED → LOADING → LOADED → INITIALIZED → READY)
- Provide capability-based plugin discovery
- Manage plugin lifecycle

**Does NOT**:
- Execute browser automation
- Know about Playwright
- Contain business logic

### Plugins

**Purpose**: Business domain automation

**Structure**:
```
plugin/
├── metadata.py          # PluginMetadata
├── plugin.py            # Plugin implementation
├── models/              # Domain models
├── workflows/           # Business orchestration
├── steps/               # Task execution
├── pages/               # Browser interactions
├── validators/          # Input validation
├── exceptions/          # Plugin-specific errors
└── tests/               # Plugin tests
```

**Responsibilities**:
- Implement Plugin interface
- Define workflows for business processes
- Validate inputs
- Coordinate execution

**Does NOT**:
- Import Playwright
- Know about Runtime internals
- Access browser directly (uses Page Objects)

### Workflows

**Purpose**: Business process orchestration

**Responsibilities**:
- Validate workflow inputs
- Execute steps sequentially
- Stop on first failure
- Return WorkflowResult

**Does NOT**:
- Perform browser automation
- Import Playwright
- Contain selectors

### Workflow Steps

**Purpose**: Discrete task execution

**Responsibilities**:
- Extract data from WorkflowContext
- Delegate to Page Objects
- Return StepResult

**Does NOT**:
- Contain selectors
- Import Playwright
- Perform browser operations directly

### Page Objects

**Purpose**: Encapsulate page interactions

**Responsibilities**:
- Encapsulate all selectors
- Use Action Library for browser operations
- Expose business-oriented methods
- Handle element timing and waits

**Does NOT**:
- Import Playwright
- Contain business logic
- Execute workflow logic

### Action Library

**Purpose**: Browser-independent actions

**Responsibilities**:
- Provide high-level browser operations
- Work with Browser Engine interfaces
- Abstract away browser implementation details

**Does NOT**:
- Import Playwright
- Know about specific browsers
- Contain business logic

### Browser Engine

**Purpose**: Browser abstraction layer

**Responsibilities**:
- Define browser interfaces (Browser, Session, Page, Locator)
- Implement Playwright adapters
- Manage browser lifecycle
- **ONLY layer that imports Playwright**

**Does NOT**:
- Contain business logic
- Know about workflows or plugins

## Dependency Rules

### Layer Dependencies (Strict)

```
User/AI Planner
    ↓ (depends on)
Execution Orchestrator
    ↓ (depends on)
Plugin Framework
    ↓ (depends on)
Plugins
    ↓ (depends on)
Action Library
    ↓ (depends on)
Browser Engine
    ↓ (depends on)
Playwright
```

**Rule**: Higher layers can depend on lower layers, NEVER the reverse.

### Import Rules

1. **Playwright imports**: ONLY in `app/browser_engine/implementations/`
2. **Plugin imports**: Runtime/Orchestrator NEVER imports specific plugins
3. **Workflow imports**: Framework NEVER imports specific workflows
4. **Page Object imports**: Only in workflow steps within same plugin

## Key Design Patterns

### 1. Dependency Inversion

All layers depend on abstractions:

```python
# ✅ GOOD: Depends on interface
from app.browser_engine.interfaces.page import Page

async def navigate(page: Page):
    await page.navigate("https://example.com")

# ❌ BAD: Depends on implementation
from playwright.async_api import Page

async def navigate(page: Page):
    await page.goto("https://example.com")
```

### 2. Plugin Independence

Framework doesn't know about specific plugins:

```python
# ✅ GOOD: Generic plugin resolution
resolution = plugin_resolver.resolve("bookmyshow")
plugin = resolution.plugin

# ❌ BAD: Direct plugin import
from app.plugins.bookmyshow.plugin import BookMyShowPlugin
plugin = BookMyShowPlugin()
```

### 3. Action Composition

Page Objects compose actions:

```python
# ✅ GOOD: Uses Action Library
from app.actions.element import FillAction

await FillAction(
    locator=search_box,
    text="Inception",
).execute(self.page)

# ❌ BAD: Direct Playwright call
await search_box.fill("Inception")
```

### 4. Strategy Pattern

Browser implementation is swappable:

```python
# ✅ GOOD: Factory creates implementation
browser = await factory.create_browser(browser_type="chromium")

# In future, can add:
# browser = await factory.create_browser(browser_type="selenium")
# browser = await factory.create_browser(browser_type="puppeteer")
```

## Testing Strategy

### Unit Tests

Test each component in isolation:

```python
# Test Page Object
@pytest.mark.asyncio
async def test_search_movie(mock_page):
    page = MoviePage(context, workflow_context)
    await page.search_movie("Inception")
    # Assert action was called correctly

# Test Workflow Step
@pytest.mark.asyncio
async def test_search_step():
    step = SearchMovieStep()
    result = await step.execute(context)
    assert result.success

# Test Orchestrator
@pytest.mark.asyncio
async def test_plugin_resolution():
    orchestrator = ExecutionOrchestrator(plugin_manager)
    plugins = orchestrator.get_available_plugins()
    assert "bookmyshow" in plugins
```

### Integration Tests

Test component interactions:

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_complete_booking_flow():
    # Setup browser, plugins, orchestrator
    request = OrchestratedRequest(
        plugin_name="bookmyshow",
        workflow_name="booking_workflow",
        input_data={...},
    )
    
    result = await orchestrator.execute(
        request, session, page, plugin_context
    )
    
    assert result.success
```

### End-to-End Tests

Test full user scenarios:

```python
@pytest.mark.e2e
@pytest.mark.asyncio
async def test_user_books_ticket():
    # Simulate complete user journey
    # From request to final result
    pass
```

## Extension Points

### Adding a New Plugin

1. Create plugin directory: `app/plugins/myplugin/`
2. Implement Plugin interface
3. Define PluginMetadata
4. Create workflows, steps, page objects
5. Register with PluginManager (automatic via discovery)

### Adding a New Action

1. Create action: `app/actions/category/new_action.py`
2. Extend BaseAction
3. Implement `execute(page)` method
4. Use Browser Engine interfaces only

### Adding a New Browser Implementation

1. Create implementation: `app/browser_engine/implementations/mybrowser/`
2. Implement Browser, Session, Page, Locator interfaces
3. Update BrowserFactory
4. All existing code works unchanged

## Production Considerations

### Error Handling

- Every layer has specific exception types
- Errors propagate with context
- Failed steps stop workflow immediately
- OrchestratedResult includes error details

### Logging

- Each component logs at appropriate level
- Request IDs trace through all layers
- Performance metrics captured
- Debug mode available

### Scalability

- Stateless architecture
- Horizontal scaling possible
- Plugin isolation
- Resource pooling in Browser Engine

### Security

- Plugin sandboxing (future)
- Input validation at every layer
- Browser context isolation
- Secrets management (future)

## Future Enhancements

### AI Planner Layer

Will convert natural language to OrchestratedRequest:

```python
class AIPlanner:
    async def plan(self, user_request: str) -> OrchestratedRequest:
        # Use LLM to understand intent
        # Map to plugin + workflow + parameters
        # Return OrchestratedRequest
        pass
```

### Distributed Execution

- Execution queue
- Worker pool
- Task distribution
- Result aggregation

### Advanced Plugin Features

- Plugin versioning
- Plugin dependencies
- Plugin marketplace
- Hot reload

## Conclusion

AgentForge's architecture provides:

✅ **Clean separation** between layers  
✅ **Browser independence** through abstraction  
✅ **Plugin independence** through dynamic loading  
✅ **Production quality** with comprehensive error handling  
✅ **Extensibility** at every level  
✅ **Testability** through dependency inversion  
✅ **Scalability** through stateless design  

The architecture is ready for production use and can support any browser automation use case through plugins.
