# BookMyShow Plugin - Complete Implementation Plan

## Objective

Complete the BookMyShow reference plugin to demonstrate the full AgentForge architecture end-to-end. This will serve as the template for all future plugins.

## Current Status (~70% Complete)

### ✅ Completed
- Plugin structure and metadata
- Basic page objects (skeleton)
- Basic workflow steps (skeleton)
- BookingWorkflow structure
- Models (BookingRequest, Theatre, Show, Seat, etc.)
- Validators
- Exception hierarchy
- Basic tests

### 🚧 Remaining Implementation
1. Complete all Page Objects with real selectors
2. Complete all Workflow Steps
3. Integration with Execution Orchestrator
4. End-to-end integration tests
5. Comprehensive documentation

## Implementation Strategy

### Phase 1: Complete Page Objects

Each Page Object must:
- Use ONLY the Action Library (no Playwright imports)
- Encapsulate all selectors as class constants
- Expose business-oriented methods
- Include proper error handling
- Be independently testable

#### HomePage
- ✅ Navigate to homepage
- ✅ Wait until loaded
- ✅ Search city
- ✅ Select city
- ✅ Verify city selection

#### MoviePage
- Search for movie
- Verify search results
- Select movie from results
- Verify movie selection
- Navigate to movie details

####DatePage (New)
- Display available dates
- Select specific date
- Verify date selection
- Handle unavailable dates

#### TheatrePage
- List available theatres
- Filter by location/preferences
- Select theatre
- Verify theatre selection

#### ShowPage (New)
- List available showtimes
- Select specific showtime
- Verify showtime selection
- Display pricing information

#### SeatPage
- Display seat layout
- Select seats (single/multiple)
- Verify seat selection
- Calculate total price
- Handle unavailable seats

#### PaymentPage
- Display payment summary
- Initiate payment
- Redirect to payment gateway
- Handle payment confirmation

#### TicketPage (New)
- Verify booking confirmation
- Download ticket
- Retrieve booking reference

### Phase 2: Complete Workflow Steps

Each step must:
- Extend BaseBookMyShowStep
- Delegate ALL browser work to Page Objects
- Return StepResult with success/failure
- Contain NO selectors
- Contain NO browser logic

Steps to implement:
1. ✅ OpenHomepageStep
2. ✅ SelectCityStep  
3. SearchMovieStep - Search for movie
4. SelectMovieStep - Select from search results
5. ChooseDateStep - Select show date
6. ChooseTheatreStep - Select theatre
7. ChooseShowStep - Select showtime
8. ChooseSeatsStep - Select seats
9. InitiatePaymentStep - Start payment
10. DownloadTicketStep - Get ticket

### Phase 3: BookingWorkflow Enhancement

Enhancements:
- Add proper error propagation
- Add step-level logging
- Add progress tracking
- Add recovery hints
- Return enriched WorkflowResult

### Phase 4: Integration Tests

Create comprehensive tests:
1. **Happy Path**: Complete booking flow
2. **Error Cases**:
   - Invalid city
   - Movie not found
   - No theatres available
   - No shows available
   - Seats unavailable
   - Payment failure
3. **Timeout Scenarios**
4. **Browser Failures**
5. **Recovery Scenarios**

### Phase 5: Orchestrator Integration

Demonstrate complete flow:
```python
request = OrchestratedRequest(
    plugin_name="bookmyshow",
    workflow_name="booking_workflow",
    input_data={
        "booking_request": BookingRequest(...)
    }
)

result = await orchestrator.execute(
    request=request,
    session=session,
    page=page,
    plugin_context=context,
)
```

## Selector Strategy

Since BookMyShow's actual selectors change frequently, we'll use:

1. **Realistic Patterns**: Based on common web app patterns
2. **Multiple Fallbacks**: Primary + backup selectors
3. **Semantic Selectors**: Prefer data attributes and ARIA labels
4. **Defensive Programming**: Handle missing elements gracefully

Example selector hierarchy:
```python
SEARCH_INPUT = [
    '[data-test-id="search-input"]',  # Preferred
    'input[placeholder*="Search"]',    # Fallback 1
    'input[type="search"]',            # Fallback 2
    '#search',                         # Last resort
]
```

## Quality Checklist

For each component:
- [ ] Uses only Action Library
- [ ] No Playwright imports
- [ ] Comprehensive error handling
- [ ] Type hints throughout
- [ ] Docstrings on all methods
- [ ] Unit tests
- [ ] Integration tests
- [ ] Clean Architecture compliance
- [ ] SOLID principles
- [ ] Dependency Inversion

## Documentation Requirements

1. **Plugin README**: Overview and usage
2. **Architecture Guide**: Component relationships
3. **Workflow Guide**: Step-by-step execution
4. **Extension Guide**: How to create new plugins
5. **API Reference**: All public methods
6. **Testing Guide**: How to test plugins

## Timeline

| Phase | Component | Status |
|-------|-----------|--------|
| 1 | Complete Page Objects | In Progress |
| 2 | Complete Workflow Steps | Pending |
| 3 | Enhance BookingWorkflow | Pending |
| 4 | Integration Tests | Pending |
| 5 | Orchestrator Integration | Pending |
| 6 | Documentation | Pending |

## Success Criteria

The reference plugin is complete when:

1. ✅ All Page Objects implemented with realistic selectors
2. ✅ All Workflow Steps delegate to Page Objects
3. ✅ BookingWorkflow executes all steps successfully
4. ✅ Integration tests pass (happy path + error cases)
5. ✅ Works end-to-end with Execution Orchestrator
6. ✅ Zero Playwright imports outside Browser Engine
7. ✅ Comprehensive documentation
8. ✅ Can serve as template for future plugins

## Notes

- This is a **reference implementation**
- Focus on architecture demonstration, not production BookMyShow automation
- Selectors are realistic but may need updating for actual use
- The goal is to validate the AgentForge architecture
- Future plugins (Amazon, Flipkart, etc.) will follow this exact pattern
