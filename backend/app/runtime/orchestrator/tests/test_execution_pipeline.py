"""
Tests for ExecutionPipeline.
"""

import pytest

from app.runtime.orchestrator.exceptions import OrchestrationPipelineError
from app.runtime.orchestrator.execution_pipeline import (
    ExecutionPipeline,
    PipelineContext,
    PipelineStage,
)


class TestExecutionPipeline:
    """Tests for ExecutionPipeline."""

    @pytest.fixture
    def pipeline(self):
        """Create an execution pipeline."""
        return ExecutionPipeline()

    @pytest.fixture
    def context(self):
        """Create a pipeline context."""
        request = type("Request", (), {"plugin_name": "test", "workflow_name": "test"})()
        return PipelineContext(request=request)

    def test_register_stage(self, pipeline):
        """Test registering a pipeline stage."""

        def handler(ctx):
            return ctx

        pipeline.register_stage(PipelineStage.PLUGIN_RESOLUTION, handler)

        assert pipeline.has_stage(PipelineStage.PLUGIN_RESOLUTION)

    def test_register_middleware(self, pipeline):
        """Test registering middleware."""
        called = []

        def middleware(ctx):
            called.append(True)
            return ctx

        pipeline.register_middleware(middleware)

        assert len(called) == 0  # Not called yet

    @pytest.mark.asyncio
    async def test_execute_pipeline(self, pipeline, context):
        """Test executing the pipeline."""
        executed_stages = []

        def stage1(ctx):
            executed_stages.append("stage1")
            return ctx

        def stage2(ctx):
            executed_stages.append("stage2")
            return ctx

        pipeline.register_stage(PipelineStage.PLUGIN_RESOLUTION, stage1)
        pipeline.register_stage(PipelineStage.WORKFLOW_RESOLUTION, stage2)

        result = await pipeline.execute(context)

        assert "stage1" in executed_stages
        assert "stage2" in executed_stages
        assert result.completed_at is not None

    @pytest.mark.asyncio
    async def test_execute_pipeline_with_middleware(self, pipeline, context):
        """Test executing pipeline with middleware."""
        middleware_calls = []

        def middleware(ctx):
            middleware_calls.append(True)
            return ctx

        def stage1(ctx):
            return ctx

        pipeline.register_middleware(middleware)
        pipeline.register_stage(PipelineStage.PLUGIN_RESOLUTION, stage1)

        await pipeline.execute(context)

        assert len(middleware_calls) > 0

    @pytest.mark.asyncio
    async def test_execute_pipeline_stage_failure(self, pipeline, context):
        """Test pipeline failure handling."""

        def failing_stage(ctx):
            raise ValueError("Stage failed")

        pipeline.register_stage(PipelineStage.PLUGIN_RESOLUTION, failing_stage)

        with pytest.raises(OrchestrationPipelineError):
            await pipeline.execute(context)

    @pytest.mark.asyncio
    async def test_execute_async_stages(self, pipeline, context):
        """Test executing async stages."""
        executed = []

        async def async_stage(ctx):
            executed.append("async")
            return ctx

        pipeline.register_stage(PipelineStage.PLUGIN_RESOLUTION, async_stage)

        result = await pipeline.execute(context)

        assert "async" in executed
        assert result.completed_at is not None

    def test_clear_stages(self, pipeline):
        """Test clearing pipeline stages."""

        def handler(ctx):
            return ctx

        pipeline.register_stage(PipelineStage.PLUGIN_RESOLUTION, handler)
        pipeline.clear_stages()

        assert len(pipeline.get_stages()) == 0

    def test_get_stages(self, pipeline):
        """Test getting registered stages."""

        def handler(ctx):
            return ctx

        pipeline.register_stage(PipelineStage.PLUGIN_RESOLUTION, handler)
        pipeline.register_stage(PipelineStage.WORKFLOW_RESOLUTION, handler)

        stages = pipeline.get_stages()

        assert len(stages) == 2
        assert PipelineStage.PLUGIN_RESOLUTION in stages
        assert PipelineStage.WORKFLOW_RESOLUTION in stages
