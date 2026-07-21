# Plugin Framework Implementation

## Overview

The Plugin Framework has been implemented following AgentForge's Clean Architecture and SOLID principles. This document provides an overview of what was implemented and how to use it.

## Architecture

The plugin system follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         Plugin Manager                  │  ← Orchestrates lifecycle
├─────────────────────────────────────────┤
│  Plugin Loader    │  Plugin Registry    │  ← Load & Store
├─────────────────────────────────────────┤
│         Plugin Interfaces               │  ← Contracts
├─────────────────────────────────────────┤
│         Plugin Implementations          │  ← BookMyShow, etc.
└─────────────────────────────────────────┘
```

## Components Implemented

### 1. Interfaces (`app/plugins/interfaces/`)

#### Plugin (`plugin.py`)
- Base interface for all plugins
- Defines contract: `metadata`, `initialize()`, `execute()`, `shutdown()`
- Ensures plugins are framework-agnostic

#### PluginContext (`plugin_context.py`)
- Controlled execution context provided to plugins
- Gateway to framework services (runtime, actions, memory, config, logger)
- Isolates plugins from framework internals

#### PluginMetadata (`plugin_metadata.py`)
- Immutable plugin descriptors
- Contains: name, version, description, author, capabilities, homepage
- Used for discovery and capability matching

### 2. Models (`app/plugins/models/`)

#### PluginState (`plugin_state.py`)
- Tracks plugin lifecycle state with enum values:
  - `UNLOADED`, `LOADING`, `LOADED`
  - `INITIALIZING`, `READY`, `EXECUTING`
  - `ERROR`, `SHUTTING_DOWN`, `SHUTDOWN`
- Validates state transitions
- Tracks execution statistics (count, timestamps, errors)
- Methods: `can_initialize()`, `can_execute()`, `can_shutdown()`
- Marks state changes: `mark_loaded()`, `mark_ready()`, etc.

#### ManagedPlugin (`managed_plugin.py`)
- Wrapper for plugin instances with runtime metadata
- Tracks: status, context, execution count, errors, timestamps
- Used internally by the plugin system

### 3. Registry (`app/plugins/registry/`)

#### PluginRegistry (`plugin_registry.py`)
- Central registry for managing plugin instances
- Operations:
  - `register(plugin)` - Register a plugin
  - `unregister(plugin_name)` - Remove a plugin
  - `get(plugin_name)` - Retrieve by name
  - `get_state(plugin_name)` - Get plugin state
  - `has_plugin(plugin_name)` - Check existence
  - `find_by_capability(capability)` - Capability-based lookup
  - `get_all()` - List all plugins
  - `get_plugins_by_status(status)` - Filter by status
- Maintains capability index for fast lookup
- Thread-safe operations

### 4. Loader (`app/plugins/manager/`)

#### PluginLoader (`plugin_loader.py`)
- Dynamically loads plugin modules from filesystem
- Operations:
  - `discover_plugins()` - Find all plugin directories
  - `load_plugin(name)` - Import and instantiate a plugin
  - `load_all_plugins()` - Bulk loading
  - `reload_plugin(name)` - Hot reload for development
- Validates plugin structure and interface compliance
- Provides detailed error messages on failures

### 5. Manager (`app/plugins/manager/`)

#### PluginManager (`plugin_manager.py`)
- Central orchestrator for plugin lifecycle
- High-level operations:
  - `load_plugin(name)` - Load and register
  - `load_all_plugins()` - Discover and load all
  - `initialize_plugin(name, context)` - Initialize with context
  - `execute_plugin(name, workflow_context)` - Execute workflow
  - `shutdown_plugin(name)` - Graceful shutdown
  - `shutdown_all_plugins()` - Bulk shutdown
- Query operations:
  - `get_plugin(name)` - Get instance
  - `get_plugin_state(name)` - Get state
  - `list_plugins()` - List all names
  - `find_plugins_by_capability(capability)` - Capability search
  - `get_all_plugin_states()` - Get all states
- Enforces state machine transitions
- Comprehensive error handling and logging

### 6. Exceptions (`app/plugins/exceptions/`)

Comprehensive exception hierarchy:
- `PluginError` - Base exception
- `PluginNotFoundError` - Plugin doesn't exist
- `PluginLoadError` - Loading failure
- `PluginInitializationError` - Initialization failure
- `PluginExecutionError` - Execution failure
- `PluginAlreadyRegisteredError` - Duplicate registration
- `PluginDependencyError` - Missing dependencies
- `PluginValidationError` - Structure validation failure
- `PluginStateError` - Invalid state transition

All exceptions include detailed context (plugin name, reason, etc.)

### 7. Tests (`app/plugins/tests/`)

Complete test coverage:
- `test_plugin_metadata.py` - Metadata creation, immutability
- `test_plugin_context.py` - Context creation and access
- `test_plugin_state.py` - State transitions, validations
- `test_plugin_registry.py` - Registration, lookup, capabilities
- `test_plugin_loader.py` - Discovery, loading, validation
- `test_plugin_manager.py` - Lifecycle orchestration

## Usage Examples

### Loading and Using a Plugin

```python
from app.plugins import PluginManager, PluginContext
from app.plugin_framework.workflow import WorkflowContext

# Initialize manager
manager = PluginManager()

# Load the BookMyShow plugin
manager.load_plugin("bookmyshow")

# Create plugin context
plugin_context = PluginContext(
    runtime=runtime_instance,
    actions=action_library,
    memory=memory_instance,
    configuration=config,
    logger=logger,
)

# Initialize plugin
manager.initialize_plugin("bookmyshow", plugin_context)

# Create workflow context
workflow_context = WorkflowContext(
    plugin_context=plugin_context,
    page=page_instance,
    session=session_instance,
    input_data={
        "booking_request": booking_request,
    },
)

# Execute plugin
result = await manager.execute_plugin("bookmyshow", workflow_context)

# Shutdown when done
manager.shutdown_plugin("bookmyshow")
```

### Finding Plugins by Capability

```python
# Find all plugins that support movie booking
booking_plugins = manager.find_plugins_by_capability("movie_booking")

for plugin in booking_plugins:
    print(f"Found: {plugin.metadata.name} v{plugin.metadata.version}")
```

### Checking Plugin State

```python
# Get plugin state
state = manager.get_plugin_state("bookmyshow")

print(f"Status: {state.status}")
print(f"Executions: {state.execution_count}")
print(f"Last executed: {state.last_executed_at}")

# Check if plugin can execute
if state.can_execute():
    result = await manager.execute_plugin("bookmyshow", context)
```

### Loading All Available Plugins

```python
# Discover and load all plugins
results = manager.load_all_plugins()

for name, success in results.items():
    if success:
        print(f"✓ Loaded {name}")
    else:
        print(f"✗ Failed to load {name}")
```

## Plugin Development

### Creating a New Plugin

1. **Create plugin directory**: `app/plugins/myplugin/`

2. **Define metadata** (`metadata.py`):
```python
from app.plugins.interfaces import PluginMetadata

METADATA = PluginMetadata(
    name="myplugin",
    version="1.0.0",
    description="My custom plugin",
    author="Your Name",
    capabilities=("capability1", "capability2"),
)
```

3. **Implement plugin** (`plugin.py`):
```python
from app.plugins.interfaces import Plugin, PluginContext
from app.plugin_framework.workflow import WorkflowContext
from .metadata import METADATA

class MyPlugin(Plugin):
    @property
    def metadata(self):
        return METADATA
    
    def initialize(self, context: PluginContext) -> None:
        self._context = context
    
    async def execute(self, context: WorkflowContext):
        # Your workflow logic here
        pass
    
    def shutdown(self) -> None:
        self._context = None
```

4. **The plugin loader will automatically discover and load it**

### Plugin Rules

1. **Never import Playwright** - Use browser abstractions
2. **Never manage browser lifecycle** - Use provided Page/Session
3. **Use Action Library** - Don't write raw browser commands
4. **Validate inputs** - Use validators from plugin_framework
5. **Handle errors** - Raise appropriate PluginErrors
6. **Clean up resources** - Implement shutdown properly

## State Machine

```
UNLOADED → LOADING → LOADED → INITIALIZING → READY → EXECUTING → READY
                ↓                                 ↓         ↓
              ERROR ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← 
                ↓
          SHUTTING_DOWN → SHUTDOWN
```

## Integration Points

### With Runtime
- Runtime creates PluginManager
- Runtime provides PluginContext to plugins
- Runtime manages browser lifecycle
- Runtime handles execution flow

### With Action Library
- Plugins access actions via PluginContext
- Actions are browser-independent
- Plugins compose actions into workflows

### With Plugin Framework
- Plugins use Workflow, WorkflowStep, BasePage
- Framework provides WorkflowContext
- Framework handles validation and errors

## Next Steps

### Completed ✅
- Core interfaces and contracts
- Plugin state management
- Registry for plugin lookup
- Dynamic plugin loading
- Lifecycle orchestration
- Comprehensive exception handling
- Complete test coverage

### Remaining 🚧

1. **Plugin Discovery & Versioning**
   - Version conflict resolution
   - Semantic versioning support
   - Backward compatibility checks

2. **Plugin Dependencies**
   - Dependency declaration
   - Dependency resolution
   - Loading order management

3. **Plugin Configuration**
   - Per-plugin configuration
   - Configuration validation
   - Environment-specific configs

4. **Plugin Hooks**
   - Before/After workflow hooks
   - Before/After step hooks
   - Error handling hooks
   - Custom event hooks

5. **Plugin Isolation**
   - Sandboxing plugins
   - Resource limits
   - Security boundaries

6. **Hot Reloading**
   - Development mode hot reload
   - Safe reload without restart
   - State preservation

7. **Plugin Metrics & Observability**
   - Execution metrics
   - Performance tracking
   - Error tracking
   - Audit logs

## Python Version Note

**IMPORTANT**: This project requires Python 3.10+ due to the use of `dataclass(slots=True)` and other modern Python features. Ensure your environment uses Python 3.10 or higher.

```bash
python --version  # Should show 3.10 or higher
```

## Testing

Run plugin framework tests:

```bash
# All tests
pytest backend/app/plugins/tests/ -v

# Specific test
pytest backend/app/plugins/tests/test_plugin_manager.py -v

# With coverage
pytest backend/app/plugins/tests/ --cov=app.plugins --cov-report=html
```

## Architecture Compliance

✅ **Clean Architecture** - Layers are clearly separated  
✅ **SOLID Principles** - Each class has a single responsibility  
✅ **Dependency Inversion** - Depends on abstractions, not concretions  
✅ **Browser Independence** - No Playwright in plugin layer  
✅ **Testability** - All components independently testable  
✅ **Scalability** - Easy to add new plugins  

## Summary

The Plugin Framework provides a production-ready foundation for AgentForge's plugin system. It enables:

- **Dynamic plugin discovery and loading**
- **Lifecycle management with state tracking**
- **Capability-based plugin discovery**
- **Clean separation from framework internals**
- **Comprehensive error handling**
- **Full test coverage**

The framework is ready for use with the BookMyShow reference plugin and can support future plugins (Amazon, Flipkart, IRCTC, etc.) without modification.
