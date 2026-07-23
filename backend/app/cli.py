from pathlib import Path

import typer

app = typer.Typer(help="AgentForge Command Line Interface")

@app.command()
def run(prompt: str, headless: bool = True):
    """
    Run an agent workflow from a prompt.
    """
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
    Validate the AgentForge environment by checking that all required
    dependencies are installed and importable.
    """
    import importlib.util

    dependencies = ["playwright", "sqlalchemy", "fastapi", "pydantic"]
    missing = [d for d in dependencies if importlib.util.find_spec(d) is None]
    if missing:
        typer.secho(f"Missing dependencies: {', '.join(missing)}", fg=typer.colors.RED)
        raise typer.Exit(1)
    typer.secho("Environment is healthy. All dependencies found.", fg=typer.colors.GREEN)

@app.command()
def test(plugin_name: str):
    """
    Run tests for a specific plugin.
    """
    import sys

    import pytest
    result = pytest.main([f"app/plugins/{plugin_name}/tests/"])
    sys.exit(result)

@app.command()
def create_plugin(name: str):
    """
    Scaffold a new plugin.
    """
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
