import { useState, useEffect } from 'react';
import { dashboardService } from '@/services/dashboardService';
import { Plugin } from '@/types';

export const usePlugins = () => {
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    
    const fetchPlugins = async () => {
      try {
        setIsLoading(true);
        const data = await dashboardService.getPlugins();
        if (isMounted) {
          setPlugins(data);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err?.message || 'Failed to fetch plugins.');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchPlugins();
    
    return () => {
      isMounted = false;
    };
  }, []);

  return { plugins, isLoading, error };
};
