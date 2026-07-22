import typer
import asyncio
from typing import Optional
from pathlib import Path

app = typer.Typer(help="AgentForge Command Line Interface")

@app.command()
def run(prompt: str, headless: bool = True):
    """
    Run an agent workflow from a prompt.
    """
    from app.agent.loop import DefaultAgent
    # ... mock init for now
    typer.echo(f"Running prompt: {prompt}")

@app.command()
def validate(plugin_name: str):
    """
    Validate a plugin's architecture (static analysis).
    """
    plugin_dir = Path(f"app/plugins/{plugin_name}")
    if not plugin_dir.exists():
        typer.secho(f"Plugin {plugin_name} not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
        
    # Check for direct playwright imports in pages/
    pages_dir = plugin_dir / "pages"
    if pages_dir.exists():
        for py_file in pages_dir.rglob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            if "playwright" in text:
                typer.secho(f"Validation failed: Playwright imported in {py_file}", fg=typer.colors.RED)
                raise typer.Exit(1)
                
    typer.secho(f"Plugin {plugin_name} validated successfully.", fg=typer.colors.GREEN)

@app.command()
def doctor():
    """
    Validate the environment.
    """
    try:
        import playwright
        import typer
        import sqlalchemy
        typer.secho("Environment is healthy.", fg=typer.colors.GREEN)
    except ImportError as e:
        typer.secho(f"Environment check failed: {e}", fg=typer.colors.RED)

@app.command()
def test(plugin_name: str):
    """
    Run tests for a specific plugin.
    """
    import pytest
    import sys
    result = pytest.main([f"app/plugins/{plugin_name}/tests/"])
    sys.exit(result)

@app.command()
def create_plugin(name: str):
    """
    Scaffold a new plugin.
    """
    import os
    from cookiecutter.main import cookiecutter
    template_dir = Path(__file__).parent.parent / "templates" / "plugin_template"
    if not template_dir.exists():
        typer.secho("Template not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
        
    output_dir = Path("app/plugins")
    output_dir.mkdir(exist_ok=True)
    
    cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context={"plugin_name": name},
        output_dir=str(output_dir)
    )
    typer.secho(f"Plugin {name} created in {output_dir / name}", fg=typer.colors.GREEN)

@app.command()
def list_plugins():
    """
    List all active plugins.
    """
    plugins_dir = Path("app/plugins")
    if plugins_dir.exists():
        for d in plugins_dir.iterdir():
            if d.is_dir() and (d / "__init__.py").exists():
                typer.echo(f"- {d.name}")

if __name__ == "__main__":
    app()
