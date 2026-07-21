# Task Abstraction Layer

## Overview

The **Task Abstraction Layer** transforms AgentForge from a workflow-driven to a **task-driven** execution system. Tasks represent business objectives without specifying implementation details, enabling AI planners to reason about goals rather than workflows.

## Architecture Evolution

### Before: Workflow-Driven
```
User Request
     ↓
Execution Orchestrator
     ↓
Plugin.BookingWorkflow  (knows specific workflow)
     ↓
Browser Automation
```

### After: Task-Driven
```
User Request / AI Planner
     ↓
Tasks (business objectives)
     ↓
Task Executor
     ↓
Task Registry (resolves plugin)
     ↓
Execution Orchestrator
     ↓
Plugin Workflow
     ↓
Browser Automation
```

## Key Concepts

### What is a Task?

A **Task** represents a single business objective that needs to be accomplished.

**Examples**:
- `SearchMovieTask`: Find a movie
- `SelectSeatsTask`: Choose theater seats
- `PurchaseTicketTask`: Complete payment
- `SearchProductTask`: Find product on e-commerce
- `AddToCartTask`: Add item to shopping cart

**Key Characteristics**:
- Describes WHAT, not HOW
- Plugin-agnostic
- Browser-agnostic
- Serializable
- Validatable

### Task vs Workflow

| Aspect | Task | Workflow |
|--------|------|----------|
| **Abstraction** | High-level business goal | Implementation steps |
| **Knowledge** | What needs to be done | How to do it |
| **Plugin Awareness** | Plugin-agnostic | Plugin-specific |
| **Browser Awareness** | Browser-agnostic | Uses browser through Page Objects |
| **Created By** | AI Planner / User | Plugin developer |
| **Example** | "Search for a movie" | Open page → fill search → click search |

## Components

### 1. Task (Base Class)

```python
@dataclass
class Task(ABC):
    task_id: str
    priority: int = 0
    correlation_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @property
    @abstractmethod
    def task_type(self) -> str:
        """Task type identifier (e.g., 'search_movie')"""
        
    @abstractmethod
    def validate(self) -> tuple[bool, list[str]]:
        """Validate task inputs"""
        
    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize task"""
```

**Purpose**: Base interface for all tasks

**Responsibilities**:
- Define task contract
- Encapsulate business intent
- Support validation
- Enable serialization

**Does NOT**:
- Execute anything
- Know about plugins
- Know about browser

### 2. TaskResult

```python
@dataclass
class TaskResult:
    task_id: str
    task_type: str
    status: TaskStatus  # PENDING, EXECUTING, COMPLETED, FAILED, etc.
    started_at: datetime | None
    completed_at: datetime | None
    output: dict[str, Any]
    errors: list[str]
    plugin_name: str | None
    workflow_name: str | None
```

**Purpose**: Standardized task execution result

**Benefits**:
- Consistent result format across all tasks
- Success/failure clearly indicated
- Execution metadata captured
- Easy to serialize and transmit

### 3. TaskContext

```python
@dataclass
class TaskContext:
    task_id: str
    task_type: str
    input_data: dict[str, Any]
    priority: int
    correlation_id: str | None
    timeout: float | None
    max_retries: int
```

**Purpose**: Business-level execution context

**Key Difference from WorkflowContext**:
- TaskContext: Business information (what, priority, correlation)
- WorkflowContext: Technical information (browser, page, session)

**Separation Allows**:
- Tasks to remain browser-independent
- TaskContext to be serialized and queued
- WorkflowContext to be created just-in-time

### 4. TaskMetadata

```python
@dataclass(frozen=True)
class TaskMetadata:
    task_type: str
    name: str
    description: str
    category: str
    required_inputs: tuple[str, ...]
    optional_inputs: tuple[str, ...]
    output_fields: tuple[str, ...]
    capabilities: tuple[str, ...]
    estimated_duration: float | None
    idempotent: bool
```

**Purpose**: Describe task types

**Used By**:
- Task discovery
- AI Planner reasoning
- Input validation
- Documentation generation

### 5. TaskCapability

```python
class TaskCapability(Enum):
    REQUIRES_BROWSER = auto()
    REQUIRES_AUTHENTICATION = auto()
    REQUIRES_PAYMENT = auto()
    REQUIRES_HUMAN_CONFIRMATION = auto()
    REQUIRES_CAPTCHA_SOLVE = auto()
    # ... and many more
```

**Purpose**: Describe task requirements

**Used For**:
- AI Planner decision-making
- Resource allocation
- Permission checking
- User confirmation

**Benefits**:
- AI can reason: "This task requires payment, do I have payment method?"
- AI can plan: "This task requires auth, I need to login first"
- System can validate: "This task needs browser, is browser available?"

### 6. TaskRegistry

```python
class TaskRegistry:
    def register_task(
        self,
        task_type: str,
        plugin_name: str,
        metadata: TaskMetadata | None = None,
    ) -> None
    
    def get_supporting_plugins(
        self,
        task_type: str,
    ) -> list[str]
    
    def is_task_supported(
        self,
        task_type: str,
    ) -> bool
```

**Purpose**: Map task types to plugins

**Architecture**:
```
TaskRegistry maintains:
    task_type → [plugin1, plugin2, ...]
    plugin → [task_type1, task_type2, ...]
```

**Benefits**:
- Plugin discovery by task
- Task discovery by plugin
- Decouples tasks from plugins
- Enables multiple implementations

**Example**:
```python
registry.register_task("search_movie", "bookmyshow")
registry.register_task("search_movie", "paytm")

plugins = registry.get_supporting_plugins("search_movie")
# Returns: ["bookmyshow", "paytm"]
```

### 7. TaskFactory

```python
class TaskFactory:
    def register_task_class(
        self,
        task_type: str,
        task_class: Type[Task],
    ) -> None
    
    def create_task(
        self,
        task_type: str,
        **kwargs,
    ) -> Task
    
    def create_from_dict(
        self,
        data: dict[str, Any],
    ) -> Task
```

**Purpose**: Create task instances from data

**Used By**:
- AI Planner (converts plans to tasks)
- API layer (parses task requests)
- Task deserialization

**Example**:
```python
# From dictionary
task = factory.create_from_dict({
    "task_type": "search_movie",
    "movie": "Inception",
    "city": "Mumbai",
})

# Direct creation
task = factory.create_task(
    "search_movie",
    movie="Inception",
    city="Mumbai",
)
```

### 8. TaskExecutor

```python
class TaskExecutor:
    async def execute_task(
        self,
        task: Task,
        session: Session,
        page: Page,
        plugin_context: PluginContext,
    ) -> TaskResult
```

**Purpose**: Execute tasks by delegating to plugins

**Execution Flow**:
```
1. Accept Task
2. Validate task inputs
3. Resolve which plugin supports the task (via TaskRegistry)
4. Determine workflow name
5. Convert Task → OrchestratedRequest
6. Delegate to Execution Orchestrator
7. Convert OrchestratedResult → TaskResult
8. Return standardized TaskResult
```

**Key Achievement**: Complete plugin independence - TaskExecutor knows NOTHING about specific plugins or workflows.

## Usage Examples

### Example 1: Defining a Task

```python
from dataclasses import dataclass
from app.runtime.tasks import Task

@dataclass
class SearchMovieTask(Task):
    """Task to search for a movie."""
    
    movie: str
    city: str
    date: str | None = None
    
    @property
    def task_type(self) -> str:
        return "search_movie"
    
    def validate(self) -> tuple[bool, list[str]]:
        errors = []
        
        if not self.movie:
            errors.append("Movie name is required")
        if not self.city:
            errors.append("City is required")
        
        return (len(errors) == 0, errors)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "task_type": self.task_type,
            "movie": self.movie,
            "city": self.city,
            "date": self.date,
        }
```

### Example 2: Registering Tasks with Plugins

```python
# In plugin initialization
registry = TaskRegistry()

# Register tasks supported by BookMyShow plugin
registry.register_task(
    "search_movie",
    "bookmyshow",
    metadata=TaskMetadata(
        task_type="search_movie",
        name="Search Movie",
        description="Search for a movie on BookMyShow",
        category="search",
        required_inputs=("movie", "city"),
        optional_inputs=("date",),
        output_fields=("results", "count"),
        capabilities=("REQUIRES_BROWSER",),
        estimated_duration=5.0,
    ),
)

registry.register_task("select_seats", "bookmyshow")
registry.register_task("purchase_ticket", "bookmyshow")
```

### Example 3: Creating Tasks via Factory

```python
factory = TaskFactory()

# Register task class
factory.register_task_class("search_movie", SearchMovieTask)

# Create task from dictionary (AI Planner use case)
task = factory.create_from_dict({
    "task_type": "search_movie",
    "movie": "Inception",
    "city": "Mumbai",
})

# Create task directly
task = factory.create_task(
    "search_movie",
    movie="Inception",
    city="Mumbai",
)
```

### Example 4: Executing Tasks

```python
# Setup
executor = TaskExecutor(orchestrator, task_registry)

# Create task
task = SearchMovieTask(
    movie="Inception",
    city="Mumbai",
)

# Execute
result = await executor.execute_task(
    task=task,
    session=browser_session,
    page=browser_page,
    plugin_context=plugin_context,
)

# Check result
if result.success:
    print(f"Success! Output: {result.output}")
    print(f"Executed by: {result.plugin_name}")
else:
    print(f"Failed: {result.errors}")
```

### Example 5: AI Planner Integration (Future)

```python
class AIPlanner:
    def __init__(self, task_executor: TaskExecutor):
        self.executor = task_executor
    
    async def execute_goal(self, user_goal: str):
        """
        Convert natural language goal to tasks and execute.
        """
        # AI converts: "Book Inception in Mumbai"
        # → List of tasks
        
        tasks = [
            SearchMovieTask(movie="Inception", city="Mumbai"),
            SelectSeatsTask(count=2, preference="middle"),
            PurchaseTicketTask(payment_method="credit_card"),
        ]
        
        # Execute tasks
        results = []
        for task in tasks:
            result = await self.executor.execute_task(
                task, session, page, context
            )
            
            if not result.success:
                return f"Failed at: {task.task_type}"
            
            results.append(result)
        
        return "All tasks completed!"
```

## Benefits

### 1. AI Planner Ready

AI can now work with abstract business objectives:

```
AI doesn't need to know:
❌ "Which plugin handles movie booking?"
❌ "What workflow should I call?"
❌ "What are the workflow parameters?"

AI only needs to know:
✅ "What task represents this goal?"
✅ "What inputs does the task need?"
✅ "What capabilities does the task require?"
```

### 2. Plugin Independence

Tasks are completely decoupled from plugins:

```python
# AI generates this task
task = SearchMovieTask(movie="Inception", city="Mumbai")

# TaskExecutor resolves at runtime:
# - Could be BookMyShow plugin
# - Could be Paytm plugin
# - Could be any future plugin
# AI doesn't need to know or care!
```

### 3. Multi-Plugin Orchestration

Same task can be executed by multiple plugins:

```python
# Register multiple implementations
registry.register_task("search_movie", "bookmyshow")
registry.register_task("search_movie", "paytm")
registry.register_task("search_movie", "ticketmaster")

# System can choose best plugin based on:
# - Availability
# - Performance
# - User preference
# - Load balancing
```

### 4. Testability

Tasks are easy to test in isolation:

```python
def test_search_movie_task():
    task = SearchMovieTask(movie="Inception", city="Mumbai")
    
    # Test validation
    is_valid, errors = task.validate()
    assert is_valid
    
    # Test serialization
    data = task.to_dict()
    assert data["movie"] == "Inception"
```

### 5. Future-Proof

Adding new capabilities doesn't break existing code:

```python
# Today
task = SearchMovieTask(movie="Inception", city="Mumbai")

# Tomorrow (add optional parameter)
task = SearchMovieTask(
    movie="Inception",
    city="Mumbai",
    preferred_language="Hindi",  # New field
)

# Existing code continues to work!
```

## Integration with Existing Architecture

### Task → Orchestrator Bridge

```
Task
  ↓
TaskExecutor
  ├─→ TaskRegistry.get_supporting_plugins("search_movie")
  │   Returns: ["bookmyshow"]
  │
  ├─→ Convert Task → OrchestratedRequest
  │   {
  │     plugin_name: "bookmyshow",
  │     workflow_name: "search_movie_workflow",
  │     input_data: task.to_dict(),
  │   }
  │
  └─→ Execution Orchestrator.execute(request)
       ↓
     Plugin Workflow Execution
       ↓
     OrchestratedResult
  ↓
TaskExecutor converts → TaskResult
```

### Backward Compatibility

The task system is **additive** - it doesn't break existing functionality:

```python
# Old way (still works)
request = OrchestratedRequest(
    plugin_name="bookmyshow",
    workflow_name="booking_workflow",
    input_data={...},
)
result = await orchestrator.execute(request, ...)

# New way (task-driven)
task = SearchMovieTask(movie="Inception", city="Mumbai")
result = await task_executor.execute_task(task, ...)
```

## Future Enhancements

### 1. Task Composition

```python
# Composite task
class BookMovieTicketTask(Task):
    """High-level task composed of sub-tasks."""
    
    def decompose(self) -> list[Task]:
        return [
            SearchMovieTask(...),
            SelectSeatsTask(...),
            PurchaseTicketTask(...),
        ]
```

### 2. Task Dependencies

```python
@dataclass
class TaskDependency:
    task_id: str
    dependency_type: str  # "requires", "optional", "conflicts_with"
```

### 3. Task Scheduling

```python
@dataclass
class ScheduledTask(Task):
    scheduled_at: datetime
    recurring: bool = False
    interval: timedelta | None = None
```

### 4. Task Pipelines

```python
class TaskPipeline:
    """Execute tasks in sequence or parallel."""
    
    def add_task(self, task: Task, dependencies: list[str] = None)
    async def execute(self) -> PipelineResult
```

## Testing Strategy

### Unit Tests

```python
def test_task_validation():
    """Test task validation logic."""
    task = SearchMovieTask(movie="", city="Mumbai")
    is_valid, errors = task.validate()
    assert not is_valid
    assert "Movie name is required" in errors

def test_task_registry():
    """Test task registration."""
    registry = TaskRegistry()
    registry.register_task("search_movie", "bookmyshow")
    assert registry.is_task_supported("search_movie")

def test_task_factory():
    """Test task creation."""
    factory = TaskFactory()
    factory.register_task_class("search_movie", SearchMovieTask)
    task = factory.create_task("search_movie", movie="Inception", city="Mumbai")
    assert task.movie == "Inception"
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_task_execution_end_to_end():
    """Test complete task execution flow."""
    # Setup
    registry = TaskRegistry()
    registry.register_task("search_movie", "bookmyshow")
    
    executor = TaskExecutor(orchestrator, registry)
    
    # Create task
    task = SearchMovieTask(movie="Inception", city="Mumbai")
    
    # Execute
    result = await executor.execute_task(task, session, page, context)
    
    # Verify
    assert result.success
    assert result.plugin_name == "bookmyshow"
```

## Conclusion

The Task Abstraction Layer transforms AgentForge into a truly **task-driven AI automation platform**:

✅ **Business-level abstraction** - Tasks represent goals, not implementations  
✅ **Plugin independence** - Tasks don't know about plugins  
✅ **Browser independence** - Tasks don't know about browser  
✅ **AI-ready** - Easy for AI to reason about and generate  
✅ **Testable** - Clean boundaries and validation  
✅ **Extensible** - New tasks and plugins without changes  
✅ **Future-proof** - Foundation for advanced orchestration  

**The task system is ready for AI planner integration** 🚀
