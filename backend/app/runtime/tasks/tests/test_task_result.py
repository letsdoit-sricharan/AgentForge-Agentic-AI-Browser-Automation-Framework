"""
Tests for TaskResult

Tests cover:
    - TaskResult creation
    - TaskStatus values
    - Success/failure detection
    - Timing calculations
"""

from datetime import datetime, timedelta

import pytest

from app.runtime.tasks.task_result import TaskResult, TaskStatus


class TestTaskStatus:
    """Test TaskStatus enum."""
    
    def test_status_values(self):
        """Test all status values are defined."""
        assert TaskStatus.PENDING
        assert TaskStatus.EXECUTING
        assert TaskStatus.COMPLETED
        assert TaskStatus.FAILED
        assert TaskStatus.CANCELLED
        assert TaskStatus.TIMEOUT
    
    def test_status_names(self):
        """Test status enum names."""
        assert TaskStatus.PENDING.name == "PENDING"
        assert TaskStatus.EXECUTING.name == "EXECUTING"
        assert TaskStatus.COMPLETED.name == "COMPLETED"
        assert TaskStatus.FAILED.name == "FAILED"
        assert TaskStatus.CANCELLED.name == "CANCELLED"
        assert TaskStatus.TIMEOUT.name == "TIMEOUT"


class TestTaskResultCreation:
    """Test TaskResult creation."""
    
    def test_create_minimal_result(self):
        """Test creating result with minimal fields."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.PENDING,
        )
        
        assert result.task_id == "task-123"
        assert result.task_type == "test_task"
        assert result.status == TaskStatus.PENDING
        assert result.started_at is None
        assert result.completed_at is None
        assert result.output == {}
        assert result.errors == []
        assert result.plugin_name is None
        assert result.workflow_name is None
        assert result.metadata == {}
    
    def test_create_complete_result(self):
        """Test creating result with all fields."""
        start = datetime.utcnow()
        end = start + timedelta(seconds=5)
        
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
            started_at=start,
            completed_at=end,
            output={"result": "success"},
            errors=[],
            plugin_name="test_plugin",
            workflow_name="test_workflow",
            metadata={"key": "value"},
        )
        
        assert result.task_id == "task-123"
        assert result.task_type == "test_task"
        assert result.status == TaskStatus.COMPLETED
        assert result.started_at == start
        assert result.completed_at == end
        assert result.output == {"result": "success"}
        assert result.errors == []
        assert result.plugin_name == "test_plugin"
        assert result.workflow_name == "test_workflow"
        assert result.metadata == {"key": "value"}
    
    def test_create_failed_result(self):
        """Test creating failed result."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.FAILED,
            errors=["Error 1", "Error 2"],
        )
        
        assert result.status == TaskStatus.FAILED
        assert len(result.errors) == 2
        assert "Error 1" in result.errors
        assert "Error 2" in result.errors


class TestTaskResultSuccess:
    """Test success detection."""
    
    def test_success_when_completed(self):
        """Test success property for completed task."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
        )
        
        assert result.success
    
    def test_not_success_when_failed(self):
        """Test success property for failed task."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.FAILED,
        )
        
        assert not result.success
    
    def test_not_success_when_pending(self):
        """Test success property for pending task."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.PENDING,
        )
        
        assert not result.success
    
    def test_not_success_when_executing(self):
        """Test success property for executing task."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.EXECUTING,
        )
        
        assert not result.success
    
    def test_not_success_when_cancelled(self):
        """Test success property for cancelled task."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.CANCELLED,
        )
        
        assert not result.success
    
    def test_not_success_when_timeout(self):
        """Test success property for timeout task."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.TIMEOUT,
        )
        
        assert not result.success


class TestTaskResultTiming:
    """Test timing calculations."""
    
    def test_duration_calculated(self):
        """Test duration calculation."""
        start = datetime.utcnow()
        end = start + timedelta(seconds=5.5)
        
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
            started_at=start,
            completed_at=end,
        )
        
        assert result.duration is not None
        assert 5.4 < result.duration < 5.6
    
    def test_duration_none_when_not_started(self):
        """Test duration is None when not started."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.PENDING,
        )
        
        assert result.duration is None
    
    def test_duration_none_when_not_completed(self):
        """Test duration is None when not completed."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.EXECUTING,
            started_at=datetime.utcnow(),
        )
        
        assert result.duration is None
    
    def test_duration_zero(self):
        """Test duration when start and end are very close."""
        now = datetime.utcnow()
        
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
            started_at=now,
            completed_at=now,
        )
        
        assert result.duration is not None
        assert result.duration >= 0
        assert result.duration < 0.1


class TestTaskResultOutput:
    """Test output handling."""
    
    def test_output_empty_by_default(self):
        """Test output is empty dict by default."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
        )
        
        assert result.output == {}
    
    def test_output_with_data(self):
        """Test output with data."""
        output = {
            "result": "success",
            "data": {"key": "value"},
            "count": 42,
        }
        
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
            output=output,
        )
        
        assert result.output == output
        assert result.output["result"] == "success"
        assert result.output["data"]["key"] == "value"
        assert result.output["count"] == 42


class TestTaskResultErrors:
    """Test error handling."""
    
    def test_errors_empty_by_default(self):
        """Test errors is empty list by default."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
        )
        
        assert result.errors == []
    
    def test_single_error(self):
        """Test result with single error."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.FAILED,
            errors=["Something went wrong"],
        )
        
        assert len(result.errors) == 1
        assert "Something went wrong" in result.errors
    
    def test_multiple_errors(self):
        """Test result with multiple errors."""
        errors = [
            "Error 1",
            "Error 2",
            "Error 3",
        ]
        
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.FAILED,
            errors=errors,
        )
        
        assert len(result.errors) == 3
        assert all(error in result.errors for error in errors)


class TestTaskResultMetadata:
    """Test metadata handling."""
    
    def test_metadata_empty_by_default(self):
        """Test metadata is empty dict by default."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
        )
        
        assert result.metadata == {}
    
    def test_metadata_with_plugin_info(self):
        """Test metadata with plugin information."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
            plugin_name="test_plugin",
            workflow_name="test_workflow",
        )
        
        assert result.plugin_name == "test_plugin"
        assert result.workflow_name == "test_workflow"
    
    def test_custom_metadata(self):
        """Test custom metadata."""
        metadata = {
            "orchestrated_result_id": "orch-123",
            "execution_time": 5.5,
            "custom_field": "custom_value",
        }
        
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
            metadata=metadata,
        )
        
        assert result.metadata == metadata
        assert result.metadata["orchestrated_result_id"] == "orch-123"
        assert result.metadata["execution_time"] == 5.5
        assert result.metadata["custom_field"] == "custom_value"


class TestTaskResultRepresentation:
    """Test string representation."""
    
    def test_repr(self):
        """Test __repr__ method."""
        result = TaskResult(
            task_id="task-123",
            task_type="test_task",
            status=TaskStatus.COMPLETED,
        )
        
        repr_str = repr(result)
        
        assert "TaskResult" in repr_str
        assert "task-123" in repr_str
        assert "test_task" in repr_str
        assert "COMPLETED" in repr_str
