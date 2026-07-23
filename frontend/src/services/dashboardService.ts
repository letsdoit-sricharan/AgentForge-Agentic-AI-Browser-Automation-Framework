import { apiClient } from '@/api/client';
import { ExecutionRecord, PlatformStats, Plugin } from '@/types';

/**
 * Service for fetching dashboard data (stats, plugins, executions).
 */
export const dashboardService = {
  getPlatformStats: async (): Promise<PlatformStats> => {
    const response = await apiClient.get('/api/dashboard/stats');
    const data = response.data;
    return {
      registeredPlugins: data.plugins,
      runningExecutions: data.running,
      completedToday: data.completed_today,
      failedExecutions: data.failed_today,
    };
  },

  getPlugins: async (): Promise<Plugin[]> => {
    const response = await apiClient.get('/api/plugins');
    return response.data.map((p: any) => ({
      id: p.id,
      name: p.name,
      description: p.description,
      isActive: p.enabled,
      version: p.version,
    }));
  },

  getExecutions: async (): Promise<ExecutionRecord[]> => {
    const response = await apiClient.get('/api/executions');
    return response.data.map((e: any) => ({
      id: e.id,
      plugin: e.plugin,
      status: e.status,
      startedAt: e.started_at,
      completedAt: e.completed_at,
      duration: e.duration ? `${e.duration}s` : undefined,
    }));
  },
};
