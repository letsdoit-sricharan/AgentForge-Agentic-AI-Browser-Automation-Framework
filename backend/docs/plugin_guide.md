# AgentForge Plugin Authoring Guide

AgentForge plugins are isolated automation packages that provide capabilities to the AI Agent.

## Scaffold a new plugin
Use the CLI to scaffold a new plugin:

```bash
python -m app.cli create-plugin my_plugin
```

## Structure
A plugin typically contains:
- `__init__.py`: Exports the plugin metadata and class.
- `models/`: Pydantic models for workflow inputs/outputs.
- `pages/`: Page Objects encapsulating DOM locators and interactions.
- `steps/`: Reusable workflow steps that orchestrate Page Objects.
- `workflows/`: High-level workflows composed of steps.

## Rules
1. **Never import Playwright**: Always use the `self.page` abstraction (e.g. `self.page.locator(...)`).
2. **Never leak DOM Selectors**: Selectors belong *only* in Page Objects, never in workflows or steps.
3. **Use Metrics & Logs**: Use `from app.core.logger import contextual_logger` and `from app.core.metrics import track_time`.
