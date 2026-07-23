import { useEffect, useState } from 'react';
import { eventService, WorkflowEvent } from '@/services/eventService';

interface UseExecutionEventsResult {
  events: WorkflowEvent[];
  isSubscribed: boolean;
  error: Error | null;
}

export const useExecutionEvents = (bookingId: string | null): UseExecutionEventsResult => {
  const [events, setEvents] = useState<WorkflowEvent[]>([]);
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [useFallback, setUseFallback] = useState(false);

  useEffect(() => {
    if (!bookingId) return;

    setEvents([]);
    setError(null);
    setIsSubscribed(true);

    if (useFallback) {
      // Fallback polling mode
      const interval = setInterval(async () => {
        try {
          const polledEvents = await eventService.getExecutionEvents(bookingId);
          setEvents(polledEvents);
          
          const lastEvent = polledEvents[polledEvents.length - 1];
          if (lastEvent && (lastEvent.event_type === 'WORKFLOW_COMPLETED' || lastEvent.event_type === 'WORKFLOW_FAILED' || lastEvent.step.includes('workflow.completed') || lastEvent.step.includes('workflow.failed'))) {
            clearInterval(interval);
            setIsSubscribed(false);
          }
        } catch (err) {
          console.error("Polling failed", err);
          setError(err instanceof Error ? err : new Error('Polling failed'));
        }
      }, 1000);

      return () => {
        clearInterval(interval);
        setIsSubscribed(false);
      };
    }

    // SSE Mode
    const eventSource = eventService.subscribeToExecutionEvents(
      bookingId,
      (newEvent) => {
        setEvents((prev) => {
          // Prevent duplicates by checking timestamp and step name (basic heuristic)
          const isDuplicate = prev.some(
            (e) => e.step === newEvent.step && e.status === newEvent.status
          );
          if (isDuplicate) return prev;
          return [...prev, newEvent];
        });

        if (newEvent.event_type === 'WORKFLOW_COMPLETED' || newEvent.event_type === 'WORKFLOW_FAILED' || newEvent.step.includes('workflow.completed') || newEvent.step.includes('workflow.failed')) {
          eventSource.close();
          setIsSubscribed(false);
        }
      },
      (errEvent) => {
        console.warn('SSE connection error. Switching to polling fallback.', errEvent);
        eventSource.close();
        setIsSubscribed(false);
        setError(new Error('Realtime connection lost. Switching to polling mode...'));
        setUseFallback(true);
      }
    );

    return () => {
      eventSource.close();
      setIsSubscribed(false);
    };
  }, [bookingId, useFallback]);

  return { events, isSubscribed, error };
};
