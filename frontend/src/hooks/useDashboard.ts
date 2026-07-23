import { useState, useEffect } from 'react';
import { dashboardService } from '@/services/dashboardService';
import { PlatformStats, ExecutionRecord, Plugin } from '@/types';

export const useDashboard = () => {
  const [stats, setStats] = useState<PlatformStats | null>(null);
  const [recentExecutions, setRecentExecutions] = useState<ExecutionRecord[]>([]);
  const [activePlugins, setActivePlugins] = useState<Plugin[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [statsData, executionsData, pluginsData] = await Promise.all([
          dashboardService.getPlatformStats(),
          dashboardService.getExecutions(),
          dashboardService.getPlugins(),
        ]);

        if (isMounted) {
          setStats(statsData);
          setRecentExecutions(executionsData.slice(0, 5)); // Top 5
          setActivePlugins(pluginsData.filter(p => p.isActive));
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err?.message || 'Failed to fetch dashboard data.');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, []);

  return { stats, recentExecutions, activePlugins, isLoading, error };
};
