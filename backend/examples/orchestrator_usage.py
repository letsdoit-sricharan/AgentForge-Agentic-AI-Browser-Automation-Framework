"""
Execution Orchestrator Usage Examples

Demonstrates how to use the Execution Orchestrator in AgentForge.
"""

import asyncio

from app.browser_engine.factory import BrowserFactory
from app.browser_engine.managers import BrowserManager
from app.plugins import PluginManager
from app.plugins.interfaces import PluginContext
from app.runtime.orchestrator import ExecutionOrchestrator
from app.runtime.orchestrator.models import OrchestratedRequest


async def basic_execution_example():
    """
    Basic example: Execute a plugin workflow through the orchestrator.
    """
    print("=" * 60)
    print("Basic Execution Example")
    print("=" * 60)

    # 1. Setup browser
    browser_factory = BrowserFactory()
    browser = await browser_factory.create_browser(browser_type="chromium")
    browser_manager = BrowserManager(browser)
    session = await browser_manager.create_session()
    page = await session.create_page()

    # 2. Setup plugins
    plugin_manager = PluginManager()
    plugin_manager.load_all_plugins()

    # 3. Create plugin context
    plugin_context = PluginContext(
        runtime=None,
        actions=None,
        memory=None,
        configuration=None,
        logger=None,
    )

    # 4. Initialize plugins
    for plugin_name in plugin_manager.list_plugins():
        plugin_manager.initialize_plugin(plugin_name, plugin_context)

    # 5. Create orchestrator
    orchestrator = ExecutionOrchestrator(plugin_manager)

    # 6. Create execution request
    request = OrchestratedRequest(
        plugin_name="bookmyshow",
        workflow_name="booking_workflow",
        input_data={
            "movie": "Inception",
            "city": "Mumbai",
            "theatre": "INOX",
            "show_time": "18:00",
            "seats": ["A1", "A2"],
        },
    )

    # 7. Execute through orchestrator
    print(f"\nExecuting: {request.plugin_name}.{request.workflow_name}")
    result = await orchestrator.execute(
        request=request,
        session=session,
        page=page,
        plugin_context=plugin_context,
    )

    # 8. Handle result
    if result.success:
        print(f"\n✅ Success!")
        print(f"   Execution time: {result.execution_time:.2f}s")
        print(f"   Output: {result.output}")
    else:
        print(f"\n❌ Failed!")
        print(f"   Errors: {result.errors}")

    # 9. Cleanup
    await browser_manager.close_all_sessions()
    await browser.close()


async def plugin_discovery_example():
    """
    Example: Discover available plugins and their capabilities.
    """
    print("\n" + "=" * 60)
    print("Plugin Discovery Example")
    print("=" * 60)

    # Setup
    plugin_manager = PluginManager()
    plugin_manager.load_all_plugins()
    orchestrator = ExecutionOrchestrator(plugin_manager)

    # List all plugins
    print("\nAvailable Plugins:")
    for plugin_name in orchestrator.get_available_plugins():
        capabilities = orchestrator.get_plugin_capabilities(plugin_name)
        print(f"  • {plugin_name}")
        print(f"    Capabilities: {', '.join(capabilities)}")

    # Find by capability
    print("\nPlugins with 'movie_booking' capability:")
    booking_plugins = orchestrator.find_plugins_by_capability("movie_booking")
    for plugin_name in booking_plugins:
        print(f"  • {plugin_name}")


async def error_handling_example():
    """
    Example: Proper error handling with the orchestrator.
    """
    print("\n" + "=" * 60)
    print("Error Handling Example")
    print("=" * 60)

    # Setup
    plugin_manager = PluginManager()
    plugin_manager.load_all_plugins()
    orchestrator = ExecutionOrchestrator(plugin_manager)

    # Mock browser objects for this example
    mock_session = type("Session", (), {})()
    mock_page = type("Page", (), {})()
    plugin_context = PluginContext(None, None, None, None, None)

    # Test 1: Non-existent plugin
    print("\nTest 1: Non-existent plugin")
    request = OrchestratedRequest(
        plugin_name="nonexistent_plugin",
        workflow_name="some_workflow",
    )

    result = await orchestrator.execute(
        request=request,
        session=mock_session,
        page=mock_page,
        plugin_context=plugin_context,
    )

    print(f"Success: {result.success}")
    print(f"Errors: {result.errors}")

    # Test 2: Non-existent workflow
    print("\nTest 2: Non-existent workflow")
    request = OrchestratedRequest(
        plugin_name="bookmyshow",
        workflow_name="nonexistent_workflow",
    )

    result = await orchestrator.execute(
        request=request,
        session=mock_session,
        page=mock_page,
        plugin_context=plugin_context,
    )

    print(f"Success: {result.success}")
    print(f"Errors: {result.errors}")


async def capability_based_execution_example():
    """
    Example: Execute based on capability rather than specific plugin.
    """
    print("\n" + "=" * 60)
    print("Capability-Based Execution Example")
    print("=" * 60)

    # Setup
    plugin_manager = PluginManager()
    plugin_manager.load_all_plugins()
    orchestrator = ExecutionOrchestrator(plugin_manager)

    # Find plugins that can book movie tickets
    capability = "movie_booking"
    print(f"\nFinding plugins with '{capability}' capability...")

    booking_plugins = orchestrator.find_plugins_by_capability(capability)

    if booking_plugins:
        # Use the first available plugin
        plugin_name = booking_plugins[0]
        print(f"Selected plugin: {plugin_name}")

        # Create request
        request = OrchestratedRequest(
            plugin_name=plugin_name,
            workflow_name="booking_workflow",
            input_data={
                "movie": "The Matrix",
                "city": "Bangalore",
            },
        )

        print(f"Would execute: {plugin_name}.booking_workflow")
    else:
        print(f"No plugins found with '{capability}' capability")


async def multiple_workflow_execution_example():
    """
    Example: Execute multiple workflows in sequence.
    """
    print("\n" + "=" * 60)
    print("Multiple Workflow Execution Example")
    print("=" * 60)

    # Setup
    plugin_manager = PluginManager()
    plugin_manager.load_all_plugins()
    orchestrator = ExecutionOrchestrator(plugin_manager)

    # Mock browser objects
    mock_session = type("Session", (), {})()
    mock_page = type("Page", (), {})()
    plugin_context = PluginContext(None, None, None, None, None)

    # Define workflow sequence
    workflows = [
        {
            "plugin": "bookmyshow",
            "workflow": "search_workflow",
            "input": {"query": "Inception"},
        },
        {
            "plugin": "bookmyshow",
            "workflow": "booking_workflow",
            "input": {"movie": "Inception", "city": "Mumbai"},
        },
    ]

    # Execute workflows
    results = []
    for i, workflow_spec in enumerate(workflows, 1):
        print(f"\n[{i}/{len(workflows)}] Executing: {workflow_spec['plugin']}.{workflow_spec['workflow']}")

        request = OrchestratedRequest(
            plugin_name=workflow_spec["plugin"],
            workflow_name=workflow_spec["workflow"],
            input_data=workflow_spec["input"],
        )

        result = await orchestrator.execute(
            request=request,
            session=mock_session,
            page=mock_page,
            plugin_context=plugin_context,
        )

        results.append(result)
        print(f"  Result: {'✅ Success' if result.success else '❌ Failed'}")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Summary: {sum(r.success for r in results)}/{len(results)} succeeded")


async def main():
    """
    Run all examples.
    """
    print("\n🚀 AgentForge Execution Orchestrator Examples\n")

    # Run examples
    # await basic_execution_example()
    await plugin_discovery_example()
    await error_handling_example()
    await capability_based_execution_example()
    await multiple_workflow_execution_example()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
