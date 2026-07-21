# AgentForge Backend

Production-grade Agentic AI Browser Automation Framework. AgentForge enables natural language-driven browser automation through a clean, layered architecture that separates concerns and maintains browser independence.

## 🏗️ Architecture

AgentForge follows **Clean Architecture** principles with strict dependency inversion:

```
User Request → AI Planner (future) → Execution Orchestrator
    → Plugin Framework → Plugins → Action Library → Browser Engine
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## ✅ Completed Components

### Browser Engine
- ✅ Browser abstraction layer (Browser, Session, Page, Locator interfaces)
- ✅ Playwright implementation (only layer that imports Playwright)
- ✅ Browser factory and managers
- ✅ Comprehensive error handling and timeouts
- ✅ Full test coverage

### Action Library
- ✅ Browser-independent actions for all operations
- ✅ Navigation, Element, Keyboard, Mouse, Page, File, Locator actions
- ✅ Composable action patterns
- ✅ Never imports Playwright (uses Browser Engine interfaces)
- ✅ Full test coverage

### Runtime (Version 1)
- ✅ Execution context and state management
- ✅ Execution engine and queue
- ✅ Browser, Task, and Workflow executors
- ✅ Memory and event systems
- ✅ Retry, wait, navigation, and recovery strategies
- ✅ Comprehensive tests

### Plugin Framework (Version 1)
- ✅ Plugin interface and metadata
- ✅ Plugin context for controlled framework access
- ✅ Workflow and WorkflowStep base classes
- ✅ Page Object base class
- ✅ StepResult and WorkflowResult models
- ✅ Validation framework
- ✅ Exception hierarchy

### Execution Orchestrator
- ✅ Central orchestration layer
- ✅ Plugin resolution (by name or capability)
- ✅ Workflow resolution within plugins
- ✅ Execution pipeline with middleware support
- ✅ Standardized OrchestratedRequest → OrchestratedResult flow
- ✅ Complete plugin/browser independence
- ✅ Full test coverage

### Plugin System
- ✅ PluginRegistry for centralized management
- ✅ PluginLoader for dynamic module loading
- ✅ PluginManager for lifecycle orchestration
- ✅ PluginState state machine
- ✅ Capability-based plugin discovery
- ✅ Full test coverage

### Reference Plugin: BookMyShow
- ✅ Plugin structure and metadata
- ✅ Domain models (BookingRequest, Theatre, Show, Seat, etc.)
- ✅ Validators and exception hierarchy
- ✅ Workflow and step structure
- ⚠️ **Note**: Page Objects require real BookMyShow selectors (see below)

## 🚧 Development Guidelines

### Working with Real Websites

AgentForge maintains **production quality** by never inventing selectors or assuming DOM structures. When implementing Page Objects for real websites:

1. **Inspect the actual website** using browser DevTools
2. **Provide real selectors** from the live site
3. **Document selector stability** and update frequency
4. **Use defensive patterns** with fallback selectors

**Example**: To complete BookMyShow Page Objects:
```python
# ❌ DON'T: Invent selectors
SEARCH_BOX = 'input[placeholder="Search"]'  # Guessed!

# ✅ DO: Use actual inspected selectors
SEARCH_BOX = 'input[data-id="movies-search"]'  # From DevTools
SEARCH_BOX_FALLBACK = 'input[placeholder="Search for Movies"]'  # Backup
```

### Architecture Over Implementation

When working on AgentForge:

**✅ FOCUS ON**:
- Architecture improvements
- Abstraction refinement
- Documentation
- Test coverage
- Error handling
- Extensibility
- Maintainability

**❌ AVOID**:
- Placeholder implementations
- Fake selectors
- Speculative browser automation
- Business logic without requirements

## 📚 Documentation

- [**ARCHITECTURE.md**](docs/ARCHITECTURE.md) - Complete architecture overview
- [**EXECUTION_ORCHESTRATOR.md**](docs/EXECUTION_ORCHESTRATOR.md) - Orchestrator layer details
- [**PLUGIN_FRAMEWORK_IMPLEMENTATION.md**](docs/PLUGIN_FRAMEWORK_IMPLEMENTATION.md) - Plugin system guide
- [**ORCHESTRATOR_IMPLEMENTATION_SUMMARY.md**](docs/ORCHESTRATOR_IMPLEMENTATION_SUMMARY.md) - Orchestrator summary
- [**BOOKMYSHOW_COMPLETION_GUIDE.md**](docs/BOOKMYSHOW_COMPLETION_GUIDE.md) - Reference plugin guide

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 16+ (for Playwright browsers)

### Installation

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Quick Start

```python
from app.browser_engine.factory import BrowserFactory
from app.browser_engine.managers import BrowserManager
from app.plugins import PluginManager
from app.plugins.interfaces import PluginContext
from app.runtime.orchestrator import ExecutionOrchestrator
from app.runtime.orchestrator.models import OrchestratedRequest

# Setup browser
factory = BrowserFactory()
browser = await factory.create_browser(browser_type="chromium")
manager = BrowserManager(browser)
session = await manager.create_session()
page = await session.create_page()

# Setup plugins
plugin_manager = PluginManager()
plugin_manager.load_all_plugins()

# Create contexts
plugin_context = PluginContext(None, None, None, None, None)

# Initialize plugins
for plugin_name in plugin_manager.list_plugins():
    plugin_manager.initialize_plugin(plugin_name, plugin_context)

# Create orchestrator
orchestrator = ExecutionOrchestrator(plugin_manager)

# Execute workflow
request = OrchestratedRequest(
    plugin_name="bookmyshow",
    workflow_name="booking_workflow",
    input_data={"booking_request": booking_request},
)

result = await orchestrator.execute(
    request=request,
    session=session,
    page=page,
    plugin_context=plugin_context,
)

# Check result
if result.success:
    print(f"Success! {result.output}")
else:
    print(f"Failed: {result.errors}")

# Cleanup
await browser.close()
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest app/plugins/tests/
pytest app/runtime/orchestrator/tests/

# Run with coverage
pytest --cov=app --cov-report=html

# Run integration tests
pytest -m integration

# Run end-to-end tests
pytest -m e2e
```

## 🏛️ Project Structure

```
backend/
├── app/
│   ├── actions/              # Action Library (browser-independent)
│   ├── browser_engine/       # Browser abstraction (only Playwright imports)
│   ├── runtime/              # Execution runtime
│   │   ├── orchestrator/     # Execution orchestrator
│   │   ├── execution/        # Execution models
│   │   ├── state/            # State management
│   │   ├── strategies/       # Execution strategies
│   │   └── memory/           # Runtime memory
│   ├── plugin_framework/     # Plugin framework base classes
│   │   ├── workflow/         # Workflow abstractions
│   │   ├── steps/            # Step abstractions
│   │   ├── pages/            # Page Object base
│   │   └── validators/       # Validation framework
│   ├── plugins/              # Plugin implementations
│   │   ├── interfaces/       # Plugin interfaces
│   │   ├── manager/          # Plugin lifecycle management
│   │   ├── registry/         # Plugin registry
│   │   ├── models/           # Plugin models
│   │   ├── exceptions/       # Plugin exceptions
│   │   └── bookmyshow/       # Reference plugin
│   └── core/                 # Core configuration
├── docs/                     # Comprehensive documentation
├── examples/                 # Usage examples
├── tests/                    # Test suite
└── pyproject.toml           # Dependencies and config
```

## 🎯 Design Principles

### 1. Clean Architecture
Every layer has a clear responsibility and depends only on inner layers.

### 2. Dependency Inversion
All dependencies point inward. Outer layers depend on interfaces defined by inner layers.

### 3. Browser Independence
Playwright is isolated to the Browser Engine. All other code uses abstractions.

### 4. Plugin Independence
Framework has zero knowledge of specific plugins. Plugins are discovered dynamically.

### 5. SOLID Principles
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Extensible without modification
- **Liskov Substitution**: Interfaces properly abstracted
- **Interface Segregation**: Focused, minimal interfaces
- **Dependency Inversion**: Depend on abstractions

### 6. Production Quality
- Comprehensive error handling
- Detailed logging
- Type hints throughout
- Extensive testing
- Complete documentation

## 🔮 Future Enhancements

### AI Planner Layer (Next Phase)
Convert natural language to OrchestratedRequest:
```python
user: "Book Inception in Mumbai for tomorrow"
  ↓
AI Planner: Understands intent, selects plugin, generates request
  ↓
OrchestratedRequest(plugin="bookmyshow", workflow="booking_workflow", ...)
  ↓
Execution Orchestrator: Handles execution
```

### Additional Plugins
- Amazon shopping automation
- Flipkart product search
- IRCTC train booking
- LinkedIn profile automation
- MakeMyTrip travel booking
- Custom enterprise plugins

### Advanced Features
- Plugin versioning and dependencies
- Distributed execution
- Execution history and replay
- Advanced error recovery
- Plugin marketplace

## 📝 Contributing

When contributing to AgentForge:

1. **Follow architecture principles** - Maintain layer separation
2. **Never import Playwright** outside Browser Engine
3. **Write tests** for all components
4. **Document** all public interfaces
5. **Use real selectors** when working with actual websites
6. **Focus on quality** over quick implementations

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

Built with:
- **Playwright** - Browser automation
- **Python 3.10+** - Modern Python features
- **Clean Architecture** - Robert C. Martin's principles
- **SOLID** - Object-oriented design principles
