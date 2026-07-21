"""
Tests for Task Base Class

Tests cover:
    - Task creation
    - Task validation
    - Task serialization
    - Task metadata
"""

from dataclasses import dataclass
from typing import Any

import pytest

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
            "priority": self.priority,
            "correlation_id": self.correlation_id,
            "metadata": self.metadata,
        }


@dataclass
class ComplexTask(Task):
    """Complex task with multiple validation rules."""
    
    required_field: str
    optional_field: str | None = None
    
    @property
    def task_type(self) -> str:
        return "complex_task"
    
    def validate(self) -> tuple[bool, list[str]]:
        errors = []
        
        if not self.required_field:
            errors.append("required_field is required")
        
        if len(self.required_field) < 3:
            errors.append("required_field must be at least 3 characters")
        
        return (len(errors) == 0, errors)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "task_type": self.task_type,
            "required_field": self.required_field,
            "optional_field": self.optional_field,
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
        assert task.correlation_id is None
        assert task.metadata == {}
    
    def test_task_id_auto_generated(self):
        """Test that task ID is auto-generated."""
        task1 = SimpleTask(name="test1")
        task2 = SimpleTask(name="test2")
        
        assert task1.task_id != task2.task_id
        assert len(task1.task_id) > 0
        assert len(task2.task_id) > 0
    
    def test_create_task_with_priority(self):
        """Test creating task with custom priority."""
        task = SimpleTask(name="test", priority=5)
        
        assert task.priority == 5
    
    def test_create_task_with_correlation_id(self):
        """Test creating task with correlation ID."""
        task = SimpleTask(name="test", correlation_id="corr-123")
        
        assert task.correlation_id == "corr-123"
    
    def test_create_task_with_metadata(self):
        """Test creating task with metadata."""
        metadata = {"key": "value", "number": 42}
        task = SimpleTask(name="test", metadata=metadata)
        
        assert task.metadata == metadata
        assert task.metadata["key"] == "value"
        assert task.metadata["number"] == 42


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
    
    def test_invalid_task_multiple_errors(self):
        """Test validating task with multiple errors."""
        task = SimpleTask(name="", value=-1)
        
        is_valid, errors = task.validate()
        
        assert not is_valid
        assert len(errors) == 2
        assert "Name is required" in errors
        assert "Value must be non-negative" in errors
    
    def test_complex_task_validation(self):
        """Test validation of complex task."""
        task = ComplexTask(required_field="ab")
        
        is_valid, errors = task.validate()
        
        assert not is_valid
        assert "required_field must be at least 3 characters" in errors


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
    
    def test_to_dict_with_metadata(self):
        """Test serializing task with metadata."""
        task = SimpleTask(
            name="test",
            priority=5,
            correlation_id="corr-123",
            metadata={"key": "value"},
        )
        
        data = task.to_dict()
        
        assert data["priority"] == 5
        assert data["correlation_id"] == "corr-123"
        assert data["metadata"]["key"] == "value"
    
    def test_to_dict_complex(self):
        """Test serializing complex task."""
        task = ComplexTask(
            required_field="test",
            optional_field="optional",
        )
        
        data = task.to_dict()
        
        assert data["task_type"] == "complex_task"
        assert data["required_field"] == "test"
        assert data["optional_field"] == "optional"


class TestTaskRepresentation:
    """Test task string representation."""
    
    def test_repr(self):
        """Test task __repr__ method."""
        task = SimpleTask(name="test")
        
        repr_str = repr(task)
        
        assert "SimpleTask" in repr_str
        assert task.task_id in repr_str
        assert "simple_task" in repr_str


class TestTaskType:
    """Test task type property."""
    
    def test_task_type_simple(self):
        """Test task type for simple task."""
        task = SimpleTask(name="test")
        
        assert task.task_type == "simple_task"
    
    def test_task_type_complex(self):
        """Test task type for complex task."""
        task = ComplexTask(required_field="test")
        
        assert task.task_type == "complex_task"
    
    def test_task_type_consistency(self):
        """Test that task type is consistent."""
        task = SimpleTask(name="test")
        
        type1 = task.task_type
        type2 = task.task_type
        
        assert type1 == type2


class TestTaskEquality:
    """Test task equality and comparison."""
    
    def test_tasks_with_different_ids(self):
        """Test that tasks with different IDs are different objects."""
        task1 = SimpleTask(name="test", value=10)
        task2 = SimpleTask(name="test", value=10)
        
        # Different task IDs
        assert task1.task_id != task2.task_id
        
        # Same data
        assert task1.name == task2.name
        assert task1.value == task2.value
