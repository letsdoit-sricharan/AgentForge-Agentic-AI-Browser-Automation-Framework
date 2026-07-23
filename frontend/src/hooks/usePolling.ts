import { useEffect, useRef } from 'react';

/**
 * Custom hook for polling an API endpoint.
 * @param callback The function to execute on every interval
 * @param interval The interval time in milliseconds
 * @param shouldPoll Boolean indicating if polling should be active
 */
export const usePolling = (callback: () => void, interval: number, shouldPoll: boolean) => {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (!shouldPoll) {
      return;
    }

    const tick = () => {
      savedCallback.current();
    };

    const id = setInterval(tick, interval);
    return () => clearInterval(id);
  }, [interval, shouldPoll]);
};
