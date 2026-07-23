import { useState, useEffect } from 'react';
import { dashboardService } from '@/services/dashboardService';
import { ExecutionRecord } from '@/types';

export const useExecutions = () => {
  const [executions, setExecutions] = useState<ExecutionRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    
    const fetchExecutions = async () => {
      try {
        setIsLoading(true);
        const data = await dashboardService.getExecutions();
        if (isMounted) {
          setExecutions(data);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err?.message || 'Failed to fetch executions.');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchExecutions();
    
    return () => {
      isMounted = false;
    };
  }, []);

  return { executions, isLoading, error };
};
