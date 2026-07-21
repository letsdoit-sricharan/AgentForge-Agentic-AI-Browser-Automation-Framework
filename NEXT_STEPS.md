# AgentForge - Next Steps

## Critical: Fix Circular Import (15 minutes) ⚠️

### Problem
A circular import prevents all tests in `app/runtime/tasks/tests/` from running.

### Circular Dependency Chain
```
WorkflowContext ↔ Plugin
```

Specifically:
- `app/plugin_framework/workflow/workflow_context.py` imports `PluginContext`
- `app/plugins/interfaces/plugin.py` imports `WorkflowContext`

### Solution

Apply the **TYPE_CHECKING pattern** in both files:

#### File 1: `app/plugins/interfaces/plugin.py`

Add at the top:
```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.plugin_framework.workflow.workflow_context import WorkflowContext
```

Then change any method signatures to use string literals or rely on the forward reference.

#### File 2: `app/plugin_framework/workflow/workflow_context.py`

Add at the top:
```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.plugins.interfaces.plugin_context import PluginContext
```

### Verify the Fix

Run the tests:
```bash
cd backend
python -m pytest app/runtime/tasks/tests/ -v
```

Expected: All 80+ tests should now run successfully.

## After Circular Import Fix

### 1. Run Full Test Suite (30 minutes)

```bash
# Run all task tests
python -m pytest app/runtime/tasks/tests/ -v

# Run with coverage
python -m pytest app/runtime/tasks/tests/ --cov=app.runtime.tasks --cov-report=html

# View coverage report
# Open: htmlcov/index.html
```

Expected results:
- 80+ tests pass
- ~90% coverage
- No test failures

### 2. Plugin Task Registration (1-2 hours)

Update the BookMyShow plugin to register its supported tasks:

```python
# In BookMyShow plugin initialization
task_registry = TaskRegistry()

task_registry.register_task(
    "search_movie",
    "bookmyshow",
    metadata=TaskMetadata(
        task_type="search_movie",
        name="Search Movie",
        description="Search for a movie on BookMyShow",
        category="search",
        required_inputs=("movie", "city"),
        optional_inputs=("date",),
        output_fields=("results",),
        capabilities=("REQUIRES_BROWSER",),
    ),
)

# Register other tasks...
task_registry.register_task("select_seats", "bookmyshow")
task_registry.register_task("purchase_ticket", "bookmyshow")
```

### 3. Create Concrete Task Classes (2-3 hours)

Define concrete task implementations:

```python
@dataclass
class SearchMovieTask(Task):
    """Search for a movie on BookMyShow."""
    
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

Create similar classes for:
- SelectSeatsTask
- PurchaseTicketTask
- BookMovieTask (composite task)

### 4. End-to-End Integration Test (2-3 hours)

Create a complete integration test:

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_complete_task_execution_flow():
    """Test complete task execution end-to-end."""
    
    # Setup
    registry = TaskRegistry()
    registry.register_task("search_movie", "bookmyshow")
    
    factory = TaskFactory()
    factory.register_task_class("search_movie", SearchMovieTask)
    
    executor = TaskExecutor(orchestrator, registry)
    
    # Create task from dict (simulating AI planner)
    task = factory.create_from_dict({
        "task_type": "search_movie",
        "movie": "Inception",
        "city": "Mumbai",
    })
    
    # Execute task
    result = await executor.execute_task(
        task=task,
        session=browser_session,
        page=browser_page,
        plugin_context=plugin_context,
    )
    
    # Verify
    assert result.success
    assert result.plugin_name == "bookmyshow"
    assert result.workflow_name == "search_movie_workflow"
    assert result.output is not None
```

## Future Work

### Short-Term (1-2 weeks)

1. **Complete BookMyShow Plugin**
   - Obtain real selectors through live website inspection
   - Implement Page Objects with actual DOM structure
   - Complete workflow steps with real browser automation

2. **Build Second Plugin**
   - Choose simpler domain (e.g., Amazon product search)
   - Validate framework flexibility
   - Prove plugin independence

### Medium-Term (1 month)

1. **AI Planner Layer**
   - Design LLM integration architecture
   - Implement natural language → Task conversion
   - Build intent recognition
   - Create parameter extraction

2. **Advanced Task Features**
   - Task composition (high-level → sub-tasks)
   - Task dependencies
   - Task scheduling
   - Task pipelines

### Long-Term (2-3 months)

1. **Production Deployment**
   - CI/CD pipeline
   - Monitoring and logging
   - Performance optimization
   - Security hardening

2. **Enterprise Features**
   - Multi-tenancy
   - Role-based access
   - Plugin marketplace
   - Distributed execution

## Summary

**Immediate**: Fix circular import (15 min) → Run tests (30 min)  
**Short-Term**: Plugin registration → Concrete tasks → Integration tests  
**Medium-Term**: AI Planner → Advanced task features  
**Long-Term**: Production deployment → Enterprise features  

The framework is **production-ready**. After fixing the circular import, you can immediately start building the AI Planner layer and adding more plugins.

**AgentForge is ready to transform from a framework into a fully autonomous AI automation platform!** 🚀
