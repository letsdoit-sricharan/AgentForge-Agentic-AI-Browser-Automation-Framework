import asyncio
import logging
from datetime import date, timedelta, datetime
from app.browser_engine.factory.browser_factory import BrowserFactory
from app.browser_engine.managers.browser_manager import BrowserManager
from app.plugins.manager import PluginManager
from app.plugins.interfaces.plugin_context import PluginContext
from app.runtime.tasks.task_registry import TaskRegistry
from app.runtime.tasks.task_executor import TaskExecutor
from app.runtime.orchestrator.execution_orchestrator import ExecutionOrchestrator
from app.plugins.bookmyshow.tasks.book_ticket_task import BookTicketTask

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Initializing Browser Engine...")
    from app.browser_engine.models.browser_options import BrowserOptions
    
    options = BrowserOptions(headless=False)
    browser_manager = BrowserManager(options)
    await browser_manager.start()
    session_manager = await browser_manager.create_session()
    page = await session_manager.new_page()
    session = session_manager._session
    logger.info("Browser Engine ready.")

    logger.info("Setting up Plugin Framework...")
    plugin_manager = PluginManager()
    plugin_manager.load_all_plugins()
    
    plugin_context = PluginContext(
        runtime=None,
        actions=None,
        memory=None,
        configuration=None,
        logger=logger,
    )
    for plugin_name in plugin_manager.list_plugins():
        plugin_manager.initialize_plugin(plugin_name, plugin_context)
    
    logger.info("Setting up Runtime layer...")
    task_registry = TaskRegistry()
    # Register the task map: "booking" task type -> "bookmyshow" plugin
    task_registry.register_task("booking", "bookmyshow")
    
    orchestrator = ExecutionOrchestrator(plugin_manager)
    task_executor = TaskExecutor(orchestrator, task_registry)
    
    task = BookTicketTask(
        city="Mumbai",
        movie="Alpha",
        show_date=datetime.now() + timedelta(days=0),
        preferred_theatre="Cinepolis",
        preferred_time="10:10 PM",
        seat_preference="EXECUTIVE",
    )
    
    logger.info("Executing Task...")

    import json
    import os
    os.makedirs("network_logs", exist_ok=True)
    
    playwright_page = page._page
    req_count = [0]
    
    async def handle_response(response):
        if response.request.resource_type in ["fetch", "xhr", "websocket", "document", "script", "other"]:
            try:
                text = await response.text()
                req_count[0] += 1
                with open(f"network_logs/req_{req_count[0]}.txt", "w", encoding="utf-8") as f:
                    f.write(f"URL: {response.url}\n")
                    f.write(f"Method: {response.request.method}\n")
                    f.write(f"Content-Type: {response.headers.get('content-type', '')}\n")
                    f.write("="*50 + "\n")
                    f.write(text)
            except Exception as e:
                pass
                
    playwright_page.on("response", handle_response)

    result = await task_executor.execute_task(
        task=task,
        session=session,
        page=page,
        plugin_context=plugin_context
    )
    
    logger.info("=" * 50)
    if result.success:
        logger.info(f"Task SUCCESS!")
        logger.info(f"Output: {result.output}")
    else:
        logger.error(f"Task FAILED!")
        logger.error(f"Errors: {result.errors}")
        import traceback
        for err in result.errors:
            logger.error("Traceback:\n" + "".join(traceback.format_exception(type(err), err, err.__traceback__)))
        try:
            from app.browser_engine.models.screenshot_options import ScreenshotOptions
            from pathlib import Path
            await page.screenshot(options=ScreenshotOptions(path=Path("bookmyshow_error.png")))
        except Exception as e:
            logger.error(f"Could not take screenshot: {e}")
    logger.info("=" * 50)

    # Save a screenshot and HTML snapshot for debugging
    try:
        pw_page = page._page
        await pw_page.screenshot(path="bms_test_failure.png", full_page=True)
        with open("bms_test_failure.html", "w", encoding="utf-8") as f:
            f.write(await pw_page.content())
        logger.info("Saved bms_test_failure.png and bms_test_failure.html")
    except Exception:
        logger.exception("Task Execution Failed Exception:")
    finally:
        if session:
            await browser_manager.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
