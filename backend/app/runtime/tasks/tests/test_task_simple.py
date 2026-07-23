"""
Simple tests for Task Base Class (without circular imports)

Tests cover:
    - Task creation
    - Task validation
    - Task serialization
"""

from dataclasses import dataclass
from typing import Any

# Import directly to avoid circular import through __init__.py
from app.runtime.tasks.task import Task


# Test task implementations
@dataclass
class SimpleTask(Task):
    """Simple task for testing."""

    name: str
    value: int = 0

    @property
    def task_type(self) -> str:
        return "simple_task"

    def validate(self) -> tuple[bool, list[str]]:
        errors = []

        if not self.name:
            errors.append("Name is required")

        if self.value < 0:
            errors.append("Value must be non-negative")

        return (len(errors) == 0, errors)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_type": self.task_type,
            "task_id": self.task_id,
            "name": self.name,
            "value": self.value,
        }


class TestTaskCreation:
    """Test task creation and initialization."""

    def test_create_simple_task(self):
        """Test creating a simple task."""
        task = SimpleTask(name="test", value=42)

        assert task.name == "test"
        assert task.value == 42
        assert task.task_type == "simple_task"
        assert task.priority == 0

    def test_task_id_auto_generated(self):
        """Test that task ID is auto-generated."""
        task1 = SimpleTask(name="test1")
        task2 = SimpleTask(name="test2")

        assert task1.task_id != task2.task_id
        assert len(task1.task_id) > 0


class TestTaskValidation:
    """Test task validation logic."""

    def test_valid_task(self):
        """Test validating a valid task."""
        task = SimpleTask(name="test", value=10)

        is_valid, errors = task.validate()

        assert is_valid
        assert errors == []

    def test_invalid_task_missing_name(self):
        """Test validating task with missing name."""
        task = SimpleTask(name="", value=10)

        is_valid, errors = task.validate()

        assert not is_valid
        assert "Name is required" in errors

    def test_invalid_task_negative_value(self):
        """Test validating task with negative value."""
        task = SimpleTask(name="test", value=-1)

        is_valid, errors = task.validate()

        assert not is_valid
        assert "Value must be non-negative" in errors


class TestTaskSerialization:
    """Test task serialization."""

    def test_to_dict_simple(self):
        """Test serializing simple task to dict."""
        task = SimpleTask(name="test", value=42)

        data = task.to_dict()

        assert data["task_type"] == "simple_task"
        assert data["name"] == "test"
        assert data["value"] == 42
        assert "task_id" in data
