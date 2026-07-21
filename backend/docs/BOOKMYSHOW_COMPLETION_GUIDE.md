# BookMyShow Plugin - Complete Implementation Guide

## Executive Summary

This guide provides the complete blueprint for finishing the BookMyShow reference plugin. It includes implementation templates, selector patterns, test strategies, and quality checklist.

**Goal**: Create a production-quality reference plugin that demonstrates the complete AgentForge architecture and serves as a template for all future plugins.

## Architecture Overview

```
OrchestratedRequest
     ↓
ExecutionOrchestrator
     ↓
PluginManager
     ↓
BookMyShowPlugin
     ↓
BookingWorkflow
     ├─→ OpenHomepageStep → HomePage
     ├─→ SelectCityStep → HomePage  
     ├─→ SearchMovieStep → MoviePage
     ├─→ SelectMovieStep → MoviePage
     ├─→ ChooseDateStep → DatePage
     ├─→ ChooseTheatreStep → TheatrePage
     ├─→ ChooseShowStep → ShowPage
     ├─→ ChooseSeatsStep → SeatPage
     ├─→ InitiatePaymentStep → PaymentPage
     └─→ DownloadTicketStep → TicketPage
          ↓
     Action Library
          ↓
     Browser Engine
```

## Implementation Checklist

### Phase 1: Page Objects ✅

| Page | Status | Methods | Tests |
|------|--------|---------|-------|
| HomePage | ✅ Complete | open, wait_until_loaded, search_city, select_city | ✅ |
| MoviePage | 🔄 Enhance | search_movie, select_movie, verify_selected, get_results_count | 🔄 |
| DatePage | ⚠️ Create | list_dates, select_date, verify_selection | ⚠️ |
| TheatrePage | ⚠️ Create | list_theatres, filter_by_location, select_theatre | ⚠️ |
| ShowPage | ⚠️ Create | list_shows, select_show, get_pricing | ⚠️ |
| SeatPage | ⚠️ Create | display_layout, select_seats, verify_selection, get_total | ⚠️ |
| PaymentPage | ⚠️ Enhance | display_summary, initiate_payment, verify_redirect | ⚠️ |
| TicketPage | ⚠️ Create | verify_confirmation, get_booking_id, download_ticket | ⚠️ |

### Phase 2: Workflow Steps

| Step | Status | Delegates To | Returns |
|------|--------|--------------|---------|
| OpenHomepageStep | ✅ | HomePage.open() | StepResult |
| SelectCityStep | ✅ | HomePage.search_city(), select_city() | StepResult |
| SearchMovieStep | ⚠️ | MoviePage.search_movie() | StepResult |
| SelectMovieStep | ⚠️ | MoviePage.select_movie() | StepResult |
| ChooseDateStep | ⚠️ | DatePage.select_date() | StepResult |
| ChooseTheatreStep | ⚠️ | TheatrePage.select_theatre() | StepResult |
| ChooseShowStep | ⚠️ | ShowPage.select_show() | StepResult |
| ChooseSeatsStep | ⚠️ | SeatPage.select_seats() | StepResult |
| InitiatePaymentStep | ⚠️ | PaymentPage.initiate_payment() | StepResult |
| DownloadTicketStep | ⚠️ | TicketPage.download_ticket() | StepResult |

### Phase 3: Integration

- [ ] BookingWorkflow executes all steps
- [ ] Orchestrator integration example
- [ ] End-to-end test (happy path)
- [ ] End-to-end test (error cases)

### Phase 4: Documentation

- [ ] Plugin README
- [ ] Architecture documentation
- [ ] Extension guide
- [ ] API reference

## Implementation Templates

### Template: Page Object

```python
"""
Purpose:
    Represents the [Page Name] page.

Responsibilities:
    - [List responsibilities]
    
Does NOT:
    - Execute workflow logic
    - Import Playwright
    - Contain business rules
"""

from __future__ import annotations

from typing import Optional

from app.actions.element import ClickAction, FillAction
from app.actions.navigation import WaitAction
from app.browser_engine.exceptions.timeout_errors import BrowserTimeoutError
from app.browser_engine.models.load_state import LoadState
from app.plugin_framework.pages import BasePage


class [PageName]Page(BasePage):
    """
    Page Object representing the [Page Name] page.
    """

    # Selectors (with fallbacks)
    PRIMARY_ELEMENT = '[data-id="element"]'
    PRIMARY_ELEMENT_FALLBACK = '.element-class'
    
    async def key_action(self, param: str) -> None:
        """
        Perform key action.
        
        Args:
            param: Description
            
        Raises:
            BrowserTimeoutError: If element not found
        """
        # Implementation using Action Library only
        pass
        
    async def verify_state(self) -> bool:
        """
        Verify page state.
        
        Returns:
            True if in expected state
        """
        try:
            # Verification logic
            return True
        except Exception:
            return False
```

### Template: Workflow Step

```python
"""
Purpose:
    [Step purpose]

Responsibilities:
    - [List responsibilities]
    
Does NOT:
    - Contain selectors
    - Import Playwright
    - Perform browser actions directly
"""

from __future__ import annotations

from app.plugin_framework.steps.step_result import StepResult
from app.plugins.bookmyshow.pages.[page_name] import [PageName]Page
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class [StepName]Step(BaseBookMyShowStep):
    """
    [Step description]
    """

    @property
    def name(self) -> str:
        return "[step_name]"

    @property
    def success_message(self) -> str:
        return "[Success message]"

    async def perform(self) -> StepResult:
        """
        Execute the step logic.
        
        Returns:
            StepResult with success/failure status
        """
        try:
            # Get booking request from context
            booking_request = self.context.input_data.get("booking_request")
            
            # Create page object
            page = [PageName]Page(
                context=self.context,
                workflow_context=self.workflow_context,
            )
            
            # Delegate to page object
            await page.key_action(booking_request.field)
            
            # Verify success
            if not await page.verify_state():
                return StepResult(
                    success=False,
                    message="[Error message]",
                )
            
            return StepResult(
                success=True,
                message=self.success_message,
            )
            
        except Exception as e:
            return StepResult(
                success=False,
                message=f"[Step name] failed: {str(e)}",
            )
```

### Template: Integration Test

```python
"""
Integration test for [workflow/feature].
"""

import pytest

from app.browser_engine.factory import BrowserFactory
from app.browser_engine.managers import BrowserManager
from app.plugins import PluginManager
from app.plugins.interfaces import PluginContext
from app.runtime.orchestrator import ExecutionOrchestrator
from app.runtime.orchestrator.models import OrchestratedRequest
from app.plugins.bookmyshow.models.booking_request import BookingRequest
from datetime import date


@pytest.mark.integration
@pytest.mark.asyncio
async def test_[test_name]():
    """Test [description]."""
    
    # Setup browser
    factory = BrowserFactory()
    browser = await factory.create_browser(browser_type="chromium")
    manager = BrowserManager(browser)
    session = await manager.create_session()
    page = await session.create_page()
    
    # Setup plugins
    plugin_manager = PluginManager()
    plugin_manager.load_plugin("bookmyshow")
    
    # Create contexts
    plugin_context = PluginContext(None, None, None, None, None)
    plugin_manager.initialize_plugin("bookmyshow", plugin_context)
    
    # Create orchestrator
    orchestrator = ExecutionOrchestrator(plugin_manager)
    
    # Create request
    booking_request = BookingRequest(
        city="Mumbai",
        movie="Inception",
        show_date=date(2024, 12, 25),
        ticket_count=2,
    )
    
    request = OrchestratedRequest(
        plugin_name="bookmyshow",
        workflow_name="booking_workflow",
        input_data={"booking_request": booking_request},
    )
    
    # Execute
    result = await orchestrator.execute(
        request=request,
        session=session,
        page=page,
        plugin_context=plugin_context,
    )
    
    # Assert
    assert result.success is True
    assert result.errors == []
    
    # Cleanup
    await browser.close()
```

## Selector Patterns

### Best Practices

1. **Use Data Attributes** (most stable):
   ```python
   '[data-test-id="element"]'
   '[data-id="element"]'
   ```

2. **Use ARIA Labels** (accessible):
   ```python
   '[aria-label="Search"]'
   'button[aria-label="Book Now"]'
   ```

3. **Use Semantic Selectors**:
   ```python
   'button:has-text("Book Tickets")'
   'input[type="search"]'
   ```

4. **Provide Fallbacks**:
   ```python
   PRIMARY = '[data-id="btn"]'
   FALLBACK_1 = 'button.book-now'
   FALLBACK_2 = 'button:has-text("Book")'
   ```

### Common Patterns

```python
# Search inputs
SEARCH = 'input[placeholder*="Search"]'
SEARCH_ALT = 'input[type="search"]'

# Buttons
BUTTON = 'button:has-text("Text")'
BUTTON_ALT = '[data-id="button-id"]'

# Lists/Grids
ITEM = '[data-id="item"]'
ITEM_ALT = '.item-class'

# Dropdowns
DROPDOWN = 'select[name="field"]'
DROPDOWN_ALT = '[data-id="dropdown"]'

# Checkboxes/Radio
CHECKBOX = 'input[type="checkbox"][value="value"]'
RADIO = 'input[type="radio"][value="value"]'
```

## Testing Strategy

### Unit Tests (Page Objects)

Test each method in isolation:

```python
@pytest.mark.asyncio
async def test_search_movie(mock_page):
    """Test movie search functionality."""
    page = MoviePage(context=mock_context, workflow_context=mock_wf_context)
    
    await page.search_movie("Inception")
    
    # Assert fill action was called
    assert mock_page.locator.called
    assert "Inception" in mock_page.fill_calls
```

### Unit Tests (Workflow Steps)

Test step logic:

```python
@pytest.mark.asyncio
async def test_search_movie_step_success():
    """Test search movie step succeeds."""
    step = SearchMovieStep()
    
    result = await step.execute(mock_context)
    
    assert result.success is True
    assert "movie" in result.message.lower()
```

### Integration Tests

Test complete flows:

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_complete_booking_flow():
    """Test end-to-end booking."""
    # Setup real browser
    # Execute complete workflow
    # Verify final state
    pass
```

### Error Case Tests

Test failure scenarios:

```python
@pytest.mark.asyncio
async def test_movie_not_found():
    """Test movie not found error."""
    # Create request with non-existent movie
    # Execute
    # Assert failure with appropriate error message
    pass
```

## Quality Checklist

For **each component**, verify:

### Architecture Compliance
- [ ] No Playwright imports outside Browser Engine
- [ ] Uses only Action Library for browser operations
- [ ] Follows Dependency Inversion
- [ ] Maintains Clean Architecture layers
- [ ] Implements SOLID principles

### Code Quality
- [ ] Type hints on all parameters and returns
- [ ] Docstrings on all classes and public methods
- [ ] Proper exception handling
- [ ] Defensive programming (null checks, fallbacks)
- [ ] No magic numbers or strings

### Testing
- [ ] Unit tests for all public methods
- [ ] Integration tests for critical paths
- [ ] Error case tests
- [ ] Edge case tests
- [ ] Test coverage > 80%

### Documentation
- [ ] Purpose stated clearly
- [ ] Responsibilities documented
- [ ] "Does NOT" section included
- [ ] Examples provided
- [ ] Usage notes added

## Common Implementation Patterns

### Pattern: Selector with Fallback

```python
async def click_element(self) -> None:
    """Click element with fallback strategy."""
    try:
        # Try primary selector
        element = self.page.locator(self.PRIMARY_SELECTOR)
        await element.wait(timeout=5_000)
    except BrowserTimeoutError:
        # Try fallback
        element = self.page.locator(self.FALLBACK_SELECTOR)
        await element.wait(timeout=3_000)
    
    await ClickAction(locator=element).execute(self.page)
```

### Pattern: Verification with Multiple Indicators

```python
async def verify_loaded(self) -> bool:
    """Verify page loaded using multiple indicators."""
    for selector in self.LOAD_INDICATORS:
        try:
            locator = self.page.locator(selector)
            if await locator.is_visible(timeout=3_000):
                return True
        except:
            continue
    return False
```

### Pattern: List Processing

```python
async def get_items(self) -> list[str]:
    """Get list of items from page."""
    items = []
    
    locator = self.page.locator(self.ITEM_SELECTOR)
    count = await locator.count()
    
    for i in range(count):
        item = locator.nth(i)
        text = await item.text_content()
        if text:
            items.append(text.strip())
    
    return items
```

### Pattern: Error Handling in Steps

```python
async def perform(self) -> StepResult:
    """Execute step with comprehensive error handling."""
    try:
        # Get inputs
        booking_request = self.context.input_data.get("booking_request")
        if not booking_request:
            return StepResult(
                success=False,
                message="Booking request not found in context",
            )
        
        # Create page object
        page = MyPage(context=self.context, workflow_context=self.workflow_context)
        
        # Perform action
        await page.do_something(booking_request.field)
        
        # Verify
        if not await page.verify_success():
            return StepResult(
                success=False,
                message="Verification failed after action",
            )
        
        # Success
        return StepResult(
            success=True,
            message=self.success_message,
            data={"key": "value"},  # Optional output data
        )
        
    except BrowserTimeoutError as e:
        return StepResult(
            success=False,
            message=f"Timeout: {str(e)}",
        )
    except Exception as e:
        return StepResult(
            success=False,
            message=f"Unexpected error: {str(e)}",
        )
```

## Extension Guide for Future Plugins

When creating a new plugin (Amazon, Flipkart, etc.), follow this exact structure:

```
plugins/
└── myplugin/
    ├── __init__.py
    ├── metadata.py          # PluginMetadata
    ├── plugin.py            # Plugin implementation
    ├── models/              # Domain models
    │   ├── __init__.py
    │   └── request.py
    ├── pages/               # Page Objects
    │   ├── __init__.py
    │   ├── home_page.py
    │   └── ...
    ├── steps/               # Workflow Steps
    │   ├── __init__.py
    │   ├── base_step.py
    │   └── ...
    ├── workflows/           # Workflows
    │   ├── __init__.py
    │   └── main_workflow.py
    ├── validators/          # Input validators
    │   ├── __init__.py
    │   └── request_validator.py
    ├── exceptions/          # Plugin-specific exceptions
    │   ├── __init__.py
    │   └── errors.py
    └── tests/               # Tests
        ├── __init__.py
        └── ...
```

## Next Steps

1. **Complete Missing Page Objects**:
   - DatePage
   - ShowPage
   - TicketPage
   - Enhance: TheatrePage, SeatPage, PaymentPage

2. **Complete Workflow Steps**:
   - Implement perform() for all steps
   - Add error handling
   - Add verification

3. **Integration Testing**:
   - Happy path test
   - Error case tests
   - Timeout tests

4. **Documentation**:
   - Plugin README
   - Architecture guide
   - Extension guide

5. **Validation**:
   - Run all tests
   - Verify orchestrator integration
   - Check architecture compliance

## Success Criteria

The BookMyShow plugin is complete when:

✅ All Page Objects implemented with realistic selectors  
✅ All Workflow Steps delegate to Page Objects  
✅ BookingWorkflow executes end-to-end  
✅ Integration tests pass  
✅ Works with Execution Orchestrator  
✅ Zero Playwright imports outside Browser Engine  
✅ Complete documentation  
✅ Can serve as template for future plugins  

This plugin will validate the **entire AgentForge architecture** and serve as the blueprint for all future automation plugins!
