"""
Tests for TaskFactory

Tests cover:
    - Task class registration
    - Task creation from dict
    - Task creation with parameters
    - Error handling
"""

from dataclasses import dataclass
from typing import Any

import pytest

from app.runtime.tasks.exceptions import TaskError
from app.runtime.tasks.task import Task
from app.runtime.tasks.task_factory import TaskFactory


# Test task implementations
@dataclass
class TestTask(Task):
    """Simple task for testing."""
    
    name: str
    value: int = 0
    
    @property
    def task_type(self) -> str:
        return "test_task"
    
    def validate(self) -> tuple[bool, list[str]]:
        errors = []
        if not self.name:
            errors.append("Name is required")
        return (len(errors) == 0, errors)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "task_type": self.task_type,
            "name": self.name,
            "value": self.value,
        }


@dataclass
class AnotherTask(Task):
    """Another task for testing."""
    
    data: str
    
    @property
    def task_type(self) -> str:
        return "another_task"
    
    def validate(self) -> tuple[bool, list[str]]:
        return (True, [])
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "task_type": self.task_type,
            "data": self.data,
        }


class TestTaskFactoryRegistration:
    """Test task class registration."""
    
    def test_register_task_class(self):
        """Test registering a task class."""
        factory = TaskFactory()
        
        factory.register_task_class("test_task", TestTask)
        
        assert factory.is_registered("test_task")
    
    def test_register_multiple_task_classes(self):
        """Test registering multiple task classes."""
        factory = TaskFactory()
        
        factory.register_task_class("test_task", TestTask)
        factory.register_task_class("another_task", AnotherTask)
        
        assert factory.is_registered("test_task")
        assert factory.is_registered("another_task")
    
    def test_is_not_registered(self):
        """Test checking unregistered task type."""
        factory = TaskFactory()
        
        assert not factory.is_registered("unknown_task")
    
    def test_get_registered_task_types(self):
        """Test getting all registered task types."""
        factory = TaskFactory()
        
        factory.register_task_class("test_task", TestTask)
        factory.register_task_class("another_task", AnotherTask)
        
        types = factory.get_registered_task_types()
        
        assert len(types) == 2
        assert "test_task" in types
        assert "another_task" in types
    
    def test_register_same_type_twice_replaces(self):
        """Test registering same type twice replaces previous."""
        factory = TaskFactory()
        
        factory.register_task_class("test_task", TestTask)
        factory.register_task_class("test_task", AnotherTask)
        
        # Should use the latest registration
        types = factory.get_registered_task_types()
        assert len(types) == 1


class TestTaskCreation:
    """Test task creation."""
    
    def test_create_task_with_kwargs(self):
        """Test creating task with keyword arguments."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        
        task = factory.create_task(
            "test_task",
            name="test",
            value=42,
        )
        
        assert isinstance(task, TestTask)
        assert task.name == "test"
        assert task.value == 42
        assert task.task_type == "test_task"
    
    def test_create_task_minimal_args(self):
        """Test creating task with minimal arguments."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        
        task = factory.create_task(
            "test_task",
            name="test",
        )
        
        assert isinstance(task, TestTask)
        assert task.name == "test"
        assert task.value == 0  # Default value
    
    def test_create_task_unregistered_type(self):
        """Test creating task with unregistered type raises error."""
        factory = TaskFactory()
        
        with pytest.raises(TaskError) as exc_info:
            factory.create_task("unknown_task", name="test")
        
        assert "not registered" in str(exc_info.value).lower()
    
    def test_create_task_invalid_args(self):
        """Test creating task with invalid arguments raises error."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        
        with pytest.raises(Exception):
            # Missing required argument 'name'
            factory.create_task("test_task", value=42)


class TestTaskCreationFromDict:
    """Test task creation from dictionary."""
    
    def test_create_from_dict_complete(self):
        """Test creating task from complete dictionary."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        
        data = {
            "task_type": "test_task",
            "name": "test",
            "value": 42,
        }
        
        task = factory.create_from_dict(data)
        
        assert isinstance(task, TestTask)
        assert task.name == "test"
        assert task.value == 42
    
    def test_create_from_dict_minimal(self):
        """Test creating task from minimal dictionary."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        
        data = {
            "task_type": "test_task",
            "name": "test",
        }
        
        task = factory.create_from_dict(data)
        
        assert isinstance(task, TestTask)
        assert task.name == "test"
        assert task.value == 0
    
    def test_create_from_dict_with_metadata(self):
        """Test creating task from dict with metadata."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        
        data = {
            "task_type": "test_task",
            "name": "test",
            "priority": 5,
            "correlation_id": "corr-123",
            "metadata": {"key": "value"},
        }
        
        task = factory.create_from_dict(data)
        
        assert task.priority == 5
        assert task.correlation_id == "corr-123"
        assert task.metadata["key"] == "value"
    
    def test_create_from_dict_missing_task_type(self):
        """Test creating from dict without task_type raises error."""
        factory = TaskFactory()
        
        data = {"name": "test"}
        
        with pytest.raises(TaskError) as exc_info:
            factory.create_from_dict(data)
        
        assert "task_type" in str(exc_info.value).lower()
    
    def test_create_from_dict_unregistered_type(self):
        """Test creating from dict with unregistered type raises error."""
        factory = TaskFactory()
        
        data = {
            "task_type": "unknown_task",
            "name": "test",
        }
        
        with pytest.raises(TaskError) as exc_info:
            factory.create_from_dict(data)
        
        assert "not registered" in str(exc_info.value).lower()
    
    def test_create_from_dict_extra_fields_ignored(self):
        """Test that extra fields in dict are ignored."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        
        data = {
            "task_type": "test_task",
            "name": "test",
            "value": 42,
            "extra_field": "ignored",
        }
        
        task = factory.create_from_dict(data)
        
        assert isinstance(task, TestTask)
        assert task.name == "test"
        assert task.value == 42


class TestTaskFactoryMultipleTypes:
    """Test factory with multiple task types."""
    
    def test_create_different_task_types(self):
        """Test creating different task types."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        factory.register_task_class("another_task", AnotherTask)
        
        task1 = factory.create_task("test_task", name="test")
        task2 = factory.create_task("another_task", data="data")
        
        assert isinstance(task1, TestTask)
        assert isinstance(task2, AnotherTask)
        assert task1.task_type == "test_task"
        assert task2.task_type == "another_task"
    
    def test_create_from_dict_different_types(self):
        """Test creating different types from dicts."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        factory.register_task_class("another_task", AnotherTask)
        
        data1 = {"task_type": "test_task", "name": "test"}
        data2 = {"task_type": "another_task", "data": "data"}
        
        task1 = factory.create_from_dict(data1)
        task2 = factory.create_from_dict(data2)
        
        assert isinstance(task1, TestTask)
        assert isinstance(task2, AnotherTask)


class TestTaskFactoryClear:
    """Test factory clearing."""
    
    def test_clear_registrations(self):
        """Test clearing all registrations."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        factory.register_task_class("another_task", AnotherTask)
        
        assert len(factory.get_registered_task_types()) == 2
        
        factory.clear()
        
        assert len(factory.get_registered_task_types()) == 0
        assert not factory.is_registered("test_task")
        assert not factory.is_registered("another_task")


class TestTaskFactoryEdgeCases:
    """Test edge cases."""
    
    def test_empty_factory(self):
        """Test factory with no registrations."""
        factory = TaskFactory()
        
        assert factory.get_registered_task_types() == []
        assert not factory.is_registered("any_task")
    
    def test_task_with_custom_task_id(self):
        """Test creating task with custom task_id."""
        factory = TaskFactory()
        factory.register_task_class("test_task", TestTask)
        
        data = {
            "task_type": "test_task",
            "task_id": "custom-id-123",
            "name": "test",
        }
        
        task = factory.create_from_dict(data)
        
        assert task.task_id == "custom-id-123"
