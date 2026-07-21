"""
Complete Orchestration Flow Example

Demonstrates the full AgentForge architecture from user request to result.

This example shows how all layers work together:
    Browser Engine → Action Library → Runtime → Orchestrator 
    → Plugin Framework → Plugins → Workflows → Steps → Actions
"""

import asyncio
import logging
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def complete_orchestration_example():
    """
    Complete example showing all layers working together.
    """
    print("\n" + "=" * 80)
    print("AgentForge Complete Orchestration Flow")
    print("=" * 80)
    
    # ========================================================================
    # LAYER 1: Browser Engine Setup
    # ========================================================================
    print("\n[1/7] Setting up Browser Engine...")
    
    from app.browser_engine.factory import BrowserFactory
    from app.browser_engine.managers import BrowserManager
    
    # Create browser through factory (abstraction pattern)
    browser_factory = BrowserFactory()
    browser = await browser_factory.create_browser(browser_type="chromium")
    
    # Create browser manager
    browser_manager = BrowserManager(browser)
    
    # Create session
    session = await browser_manager.create_session()
    
    # Create page
    page = await session.create_page()
    
    print("   ✅ Browser Engine ready")
    print(f"      Browser: {type(browser).__name__}")
    print(f"      Session: {session}")
    print(f"      Page: {page}")
    
    # ========================================================================
    # LAYER 2: Action Library (Available to plugins)
    # ========================================================================
    print("\n[2/7] Action Library loaded...")
    print("   ✅ Actions available: Navigate, Click, Fill, Wait, etc.")
    
    # ========================================================================
    # LAYER 3: Plugin Framework Setup
    # ========================================================================
    print("\n[3/7] Setting up Plugin Framework...")
    
    from app.plugins import PluginManager
    from app.plugins.interfaces import PluginContext
    
    # Create plugin manager
    plugin_manager = PluginManager()
    
    # Load all available plugins
    load_results = plugin_manager.load_all_plugins()
    
    print(f"   ✅ Plugins loaded: {len(load_results)}")
    for name, success in load_results.items():
        status = "✅" if success else "❌"
        print(f"      {status} {name}")
    
    # Create plugin context (gives plugins access to framework)
    plugin_context = PluginContext(
        runtime=None,  # Would be actual runtime instance
        actions=None,  # Would be action library instance
        memory=None,   # Would be memory instance
        configuration=None,  # Would be config instance
        logger=logger,
    )
    
    # Initialize all loaded plugins
    print("\n   Initializing plugins...")
    for plugin_name in plugin_manager.list_plugins():
        try:
            plugin_manager.initialize_plugin(plugin_name, plugin_context)
            print(f"      ✅ {plugin_name} initialized")
        except Exception as e:
            print(f"      ❌ {plugin_name} failed: {e}")
    
    # ========================================================================
    # LAYER 4: Execution Orchestrator Setup
    # ========================================================================
    print("\n[4/7] Setting up Execution Orchestrator...")
    
    from app.runtime.orchestrator import ExecutionOrchestrator
    
    # Create orchestrator (connects runtime to plugins)
    orchestrator = ExecutionOrchestrator(plugin_manager)
    
    print("   ✅ Orchestrator ready")
    print(f"      Available plugins: {len(orchestrator.get_available_plugins())}")
    
    # Show available plugins and their capabilities
    print("\n   Available Plugins:")
    for plugin_name in orchestrator.get_available_plugins():
        capabilities = orchestrator.get_plugin_capabilities(plugin_name)
        print(f"      • {plugin_name}")
        print(f"        Capabilities: {', '.join(capabilities)}")
    
    # ========================================================================
    # LAYER 5: Create Execution Request
    # ========================================================================
    print("\n[5/7] Creating Execution Request...")
    
    from app.runtime.orchestrator.models import OrchestratedRequest
    
    # This is what would come from user input or AI planner
    request = OrchestratedRequest(
        plugin_name="bookmyshow",
        workflow_name="booking_workflow",
        input_data={
            "movie": "Inception",
            "city": "Mumbai",
            "theatre": "INOX Megaplex",
            "show_date": "2024-12-25",
            "show_time": "18:00",
            "seats": ["A1", "A2"],
            "ticket_type": "Standard",
        },
        configuration={
            "headless": False,
            "timeout": 30000,
        },
        metadata={
            "user_id": "user123",
            "session_id": "session456",
        },
    )
    
    print("   ✅ Request created")
    print(f"      Request ID: {request.request_id}")
    print(f"      Plugin: {request.plugin_name}")
    print(f"      Workflow: {request.workflow_name}")
    print(f"      Input keys: {list(request.input_data.keys())}")
    
    # ========================================================================
    # LAYER 6: Execute Through Orchestrator
    # ========================================================================
    print("\n[6/7] Executing through Orchestrator...")
    print("   (This demonstrates the flow, actual execution would happen here)")
    
    try:
        # Execute the request
        # The orchestrator will:
        #   1. Resolve plugin "bookmyshow"
        #   2. Resolve workflow "booking_workflow"
        #   3. Create WorkflowContext
        #   4. Execute workflow through plugin
        #   5. Return standardized result
        
        result = await orchestrator.execute(
            request=request,
            session=session,
            page=page,
            plugin_context=plugin_context,
        )
        
        # ====================================================================
        # LAYER 7: Handle Result
        # ====================================================================
        print("\n[7/7] Execution Result")
        print("   " + "=" * 70)
        
        if result.success:
            print("   ✅ Execution SUCCESSFUL")
            print(f"      Request ID: {result.request_id}")
            print(f"      Plugin: {result.plugin_name}")
            print(f"      Workflow: {result.workflow_name}")
            print(f"      Execution Time: {result.execution_time:.2f}s")
            print(f"      Started: {result.started_at}")
            print(f"      Completed: {result.completed_at}")
            
            if result.output:
                print("      Output:")
                for key, value in result.output.items():
                    print(f"         {key}: {value}")
            
            if result.metadata:
                print("      Metadata:")
                for key, value in result.metadata.items():
                    print(f"         {key}: {value}")
        else:
            print("   ❌ Execution FAILED")
            print(f"      Request ID: {result.request_id}")
            print(f"      Plugin: {result.plugin_name}")
            print(f"      Workflow: {result.workflow_name}")
            print(f"      Execution Time: {result.execution_time:.2f}s")
            print("      Errors:")
            for error in result.errors:
                print(f"         • {error}")
    
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        logger.exception("Execution failed")
    
    # ========================================================================
    # Cleanup
    # ========================================================================
    print("\n[Cleanup] Shutting down...")
    
    # Close page
    await page.close()
    print("   ✅ Page closed")
    
    # Close session
    await browser_manager.close_all_sessions()
    print("   ✅ Sessions closed")
    
    # Close browser
    await browser.close()
    print("   ✅ Browser closed")
    
    print("\n" + "=" * 80)
    print("Complete orchestration flow finished!")
    print("=" * 80)


def print_architecture_diagram():
    """
    Print the AgentForge architecture diagram.
    """
    print("\n" + "=" * 80)
    print("AgentForge Architecture")
    print("=" * 80)
    print("""
    ┌─────────────────────────────────────────────────────────────────┐
    │                        User Request                             │
    │                     "Book Inception in Mumbai"                  │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │                  AI Planner (Future)                            │
    │    Converts natural language → OrchestratedRequest             │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │                 Execution Orchestrator                          │
    │    - PluginResolver → Find "bookmyshow"                         │
    │    - WorkflowResolver → Find "booking_workflow"                 │
    │    - ExecutionPipeline → Coordinate execution                   │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │                    Plugin Registry                              │
    │    - Lookup plugins by name or capability                       │
    │    - Track plugin states                                        │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │                    Plugin Manager                               │
    │    - Initialize plugin                                          │
    │    - Provide PluginContext                                      │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │               BookMyShow Plugin                                 │
    │    - Execute booking_workflow                                   │
    │    - Return result                                              │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │                    Workflow                                     │
    │    - Execute workflow steps in sequence                         │
    │    - OpenHomepage → SelectCity → SelectMovie → ...             │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │                 Workflow Steps                                  │
    │    - Each step performs specific task                           │
    │    - Uses Page Objects                                          │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │                  Page Objects                                   │
    │    - HomePage, MoviePage, TheatrePage, etc.                     │
    │    - Encapsulate page interactions                              │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │                  Action Library                                 │
    │    - Navigate, Click, Fill, Wait, Select, etc.                  │
    │    - Browser-independent actions                                │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │                  Browser Engine                                 │
    │    - PlaywrightBrowser, PlaywrightSession, PlaywrightPage       │
    │    - Browser abstraction layer                                  │
    └──────────────────────────┬──────────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────────┐
    │                      Playwright                                 │
    │    - Actual browser automation                                  │
    └─────────────────────────────────────────────────────────────────┘
    """)
    print("=" * 80 + "\n")


async def main():
    """
    Run the complete orchestration example.
    """
    print_architecture_diagram()
    await complete_orchestration_example()


if __name__ == "__main__":
    asyncio.run(main())
