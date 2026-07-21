# Execution Orchestrator

## Overview

The **Execution Orchestrator** is the critical architectural layer that sits between the Runtime and Plugin Framework, transforming AgentForge from a plugin framework into an AI automation platform.

It provides the execution backbone that future AI planners will invoke.

## Architecture Position

```
User Request
     ↓
Execution Orchestrator  ← YOU ARE HERE
     ↓
Plugin Registry
     ↓
Plugin Manager
     ↓
Plugin
     ↓
Workflow
     ↓
Workflow Steps
     ↓
Page Objects
     ↓
Action Library
     ↓
Browser Engine
```

## Key Principle

**The orchestrator is completely plugin-independent and browser-independent.**

It knows NOTHING about:
- BookMyShow or any specific plugin
- Specific workflows (BookingWorkflow, etc.)
- Playwright or browser implementations
- Website-specific logic

## Components

### 1. ExecutionOrchestrator (`execution_orchestrator.py`)

**Purpose**: Public entry point for runtime execution

**Responsibilities**:
- Accept `OrchestratedRequest`
- Coordinate entire execution lifecycle
- Return standardized `OrchestratedResult`
- Handle failures consistently
- Remain plugin/browser independent

**Does NOT**:
- Know about specific plugins
- Manage browser lifecycle directly
- Contain business logic

**Key Methods**:
```python
async def execute(
    request: OrchestratedRequest,
    session: Session,
    page: Page,
    plugin_context: PluginContext,
) -> OrchestratedResult
```

**Query Methods**:
- `get_available_plugins()` - List all plugins
- `get_plugin_capabilities(plugin_name)` - Get plugin capabilities
- `find_plugins_by_capability(capability)` - Find by capability

### 2. PluginResolver (`plugin_resolver.py`)

**Purpose**: Determine which plugin should satisfy an execution request

**Responsibilities**:
- Query Plugin Registry
- Validate plugin availability
- Validate plugin capabilities
- Return plugin resolution result

**Does NOT**:
- Initialize plugins
- Execute plugins
- Know about specific plugins

**Key Methods**:
```python
def resolve(
    plugin_name: str,
    required_capabilities: list[str] | None = None,
) -> PluginResolution

def resolve_by_capability(
    capability: str,
) -> list[PluginResolution]
```

### 3. WorkflowResolver (`workflow_resolver.py`)

**Purpose**: Resolve which workflow should execute inside a plugin

**Responsibilities**:
- Locate workflow within plugin
- Validate workflow existence
- Prepare execution configuration
- Return workflow resolution result

**Does NOT**:
- Execute workflows
- Know about specific workflows
- Manage browser lifecycle

**Key Methods**:
```python
def resolve(
    plugin: Any,
    workflow_name: str,
) -> WorkflowResolution

def list_workflows(
    plugin: Any,
) -> list[str]
```

**Workflow Discovery**:
The resolver searches for workflows in this order:
1. Direct attribute: `plugin.workflow_name`
2. Workflows dict: `plugin.workflows[workflow_name]`
3. Private attribute: `plugin._workflow_name`
4. Workflow suffix: `plugin._workflow_name_workflow`

### 4. ExecutionPipeline (`execution_pipeline.py`)

**Purpose**: Execute orchestration stages in order

**Responsibilities**:
- Execute stages sequentially
- Standardize error propagation
- Track execution progress
- Support middleware extension

**Does NOT**:
- Know about specific plugins/workflows
- Manage browser lifecycle
- Contain business logic

**Pipeline Stages**:
```python
class PipelineStage(Enum):
    PLUGIN_RESOLUTION = auto()
    PLUGIN_INITIALIZATION = auto()
    WORKFLOW_RESOLUTION = auto()
    CONTEXT_CREATION = auto()
    WORKFLOW_EXECUTION = auto()
    RESULT_COLLECTION = auto()
    CLEANUP = auto()
```

**Key Methods**:
```python
def register_stage(
    stage: PipelineStage,
    handler: Callable,
) -> None

def register_middleware(
    middleware: Callable,
) -> None

async def execute(
    context: PipelineContext,
) -> PipelineContext
```

## Data Models

### OrchestratedRequest

High-level request entering the orchestrator:

```python
@dataclass
class OrchestratedRequest:
    request_id: str
    plugin_name: str
    workflow_name: str
    input_data: dict[str, Any]
    configuration: dict[str, Any]
    metadata: dict[str, Any]
    created_at: datetime
```

### OrchestratedResult

Standardized result returned by orchestrator:

```python
@dataclass
class OrchestratedResult:
    request_id: str
    plugin_name: str
    workflow_name: str
    success: bool
    output: dict[str, Any]
    errors: list[str]
    execution_time: float | None
    started_at: datetime | None
    completed_at: datetime | None
    metadata: dict[str, Any]
```

### PluginResolution

Result of plugin resolution:

```python
@dataclass
class PluginResolution:
    plugin_name: str
    found: bool
    plugin: Any  # Actual Plugin instance
    error: str | None
    capabilities: tuple[str, ...]
```

### WorkflowResolution

Result of workflow resolution:

```python
@dataclass
class WorkflowResolution:
    workflow_name: str
    found: bool
    workflow: Any  # Actual Workflow instance
    error: str | None
    requires_context: bool
    configuration: dict[str, Any]
```

## Exception Hierarchy

```
OrchestrationError
├── PluginResolutionError
├── WorkflowResolutionError
├── ExecutionPreparationError
├── WorkflowContextCreationError
└── OrchestrationPipelineError
```

All exceptions include detailed context for debugging.

## Usage Examples

### Basic Execution

```python
from app.runtime.orchestrator import ExecutionOrchestrator
from app.runtime.orchestrator.models import OrchestratedRequest
from app.plugins import PluginManager

# Setup
plugin_manager = PluginManager()
plugin_manager.load_all_plugins()

orchestrator = ExecutionOrchestrator(plugin_manager)

# Create request
request = OrchestratedRequest(
    plugin_name="bookmyshow",
    workflow_name="booking_workflow",
    input_data={
        "movie": "Inception",
        "city": "Mumbai",
        "date": "2024-12-25",
    },
)

# Execute
result = await orchestrator.execute(
    request=request,
    session=browser_session,
    page=browser_page,
    plugin_context=plugin_context,
)

# Check result
if result.success:
    print(f"Success! Output: {result.output}")
    print(f"Completed in {result.execution_time:.2f}s")
else:
    print(f"Failed: {result.errors}")
```

### Finding Plugins by Capability

```python
# Find all plugins that support booking
booking_plugins = orchestrator.find_plugins_by_capability("movie_booking")

for plugin_name in booking_plugins:
    capabilities = orchestrator.get_plugin_capabilities(plugin_name)
    print(f"{plugin_name}: {capabilities}")
```

### Error Handling

```python
try:
    result = await orchestrator.execute(
        request=request,
        session=session,
        page=page,
        plugin_context=context,
    )
    
    if not result.success:
        # Handle graceful failures
        for error in result.errors:
            logger.error(f"Execution error: {error}")
            
except PluginResolutionError as e:
    # Plugin not found or invalid
    print(f"Plugin resolution failed: {e}")
    
except WorkflowResolutionError as e:
    # Workflow not found in plugin
    print(f"Workflow resolution failed: {e}")
    
except OrchestrationPipelineError as e:
    # Pipeline stage failed
    print(f"Pipeline error at {e.stage}: {e.reason}")
```

### Custom Pipeline Middleware

```python
async def logging_middleware(context: PipelineContext):
    """Log each pipeline stage."""
    stage = context.current_stage
    print(f"Executing stage: {stage.name}")
    return context

async def timing_middleware(context: PipelineContext):
    """Track stage execution time."""
    import time
    start = time.time()
    # ... stage execution ...
    duration = time.time() - start
    print(f"Stage took {duration:.2f}s")
    return context

# Register middleware
orchestrator._pipeline.register_middleware(logging_middleware)
orchestrator._pipeline.register_middleware(timing_middleware)
```

## Integration with Runtime

The orchestrator integrates seamlessly with the existing runtime:

```python
from app.runtime import Runtime
from app.runtime.orchestrator import ExecutionOrchestrator

class AgentForgeRuntime(Runtime):
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.orchestrator = ExecutionOrchestrator(self.plugin_manager)
        
    async def execute_task(self, task_spec):
        # Create orchestrated request from task
        request = OrchestratedRequest(
            plugin_name=task_spec.plugin,
            workflow_name=task_spec.workflow,
            input_data=task_spec.input,
        )
        
        # Execute through orchestrator
        result = await self.orchestrator.execute(
            request=request,
            session=self.session,
            page=self.page,
            plugin_context=self.plugin_context,
        )
        
        return result
```

## Future AI Planner Integration

The orchestrator is designed to be the execution backbone for AI planners:

```python
# Future AI Planner usage:

class AIPlanner:
    def __init__(self, orchestrator: ExecutionOrchestrator):
        self.orchestrator = orchestrator
    
    async def execute_natural_language_request(
        self, 
        user_request: str
    ):
        # AI converts natural language to execution plan
        plan = await self.convert_to_execution_plan(user_request)
        
        # Each step uses the orchestrator
        results = []
        for step in plan.steps:
            request = OrchestratedRequest(
                plugin_name=step.plugin,
                workflow_name=step.workflow,
                input_data=step.input,
            )
            
            result = await self.orchestrator.execute(
                request=request,
                session=self.session,
                page=self.page,
                plugin_context=self.context,
            )
            
            results.append(result)
        
        return results
```

## Testing

Run orchestrator tests:

```bash
# All orchestrator tests
pytest backend/app/runtime/orchestrator/tests/ -v

# Specific test file
pytest backend/app/runtime/orchestrator/tests/test_execution_orchestrator.py -v

# With coverage
pytest backend/app/runtime/orchestrator/tests/ --cov=app.runtime.orchestrator
```

## Design Principles Compliance

✅ **Clean Architecture** - Clear layer separation  
✅ **SOLID** - Single responsibility per class  
✅ **Dependency Inversion** - Depends on abstractions  
✅ **Plugin Independence** - No knowledge of specific plugins  
✅ **Browser Independence** - No Playwright dependencies  
✅ **Testability** - All components independently testable  
✅ **Extensibility** - Pipeline supports middleware and custom stages  
✅ **Production Quality** - Comprehensive error handling and logging  

## Benefits

1. **Decoupling**: Plugins never directly talk to runtime
2. **Flexibility**: Easy to add new plugins without changing orchestrator
3. **Consistency**: Standardized execution flow for all plugins
4. **Observability**: Central point for monitoring and logging
5. **Extensibility**: Pipeline pattern allows middleware injection
6. **Testability**: Each component independently testable
7. **Future-Proof**: Ready for AI planner integration

## Comparison: Before vs After

### Before (Direct Plugin Execution)
```python
# Runtime directly calls plugin
plugin = plugin_manager.get_plugin("bookmyshow")
plugin.initialize(context)
result = await plugin.execute(workflow_context)
```

### After (Orchestrated Execution)
```python
# Orchestrator handles everything
request = OrchestratedRequest(
    plugin_name="bookmyshow",
    workflow_name="booking_workflow",
    input_data=data,
)
result = await orchestrator.execute(request, session, page, context)
```

Benefits:
- Plugin resolution is handled
- Workflow resolution is handled
- Error handling is standardized
- Result format is consistent
- Easy to add hooks/middleware
- Ready for AI planning layer

## Next Steps

The Execution Orchestrator is now complete. Future enhancements:

1. **Execution History** - Track all executions
2. **Execution Metrics** - Performance monitoring
3. **Execution Hooks** - Before/after execution callbacks
4. **Execution Policies** - Rate limiting, retries, timeouts
5. **Execution Streaming** - Real-time execution updates
6. **Distributed Execution** - Execute across multiple workers
7. **AI Planner Integration** - Natural language to execution

The foundation is complete and production-ready! 🚀
