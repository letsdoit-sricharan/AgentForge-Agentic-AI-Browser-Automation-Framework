import { apiClient } from '@/api/client';

export interface WorkflowEvent {
  step: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'skipped';
  timestamp: string;
  message?: string;
  event_type?: string;
}

export const eventService = {
  /**
   * Subscribes to live execution events via Server-Sent Events (SSE).
   * 
   * @param bookingId The execution ID to subscribe to.
   * @param onEvent Callback triggered when a new event arrives.
   * @param onError Callback triggered on connection error.
   * @returns An EventSource instance that can be closed.
   */
  subscribeToExecutionEvents: (
    bookingId: string,
    onEvent: (event: WorkflowEvent) => void,
    onError?: (error: Event) => void
  ): EventSource => {
    // Determine base URL from apiClient config to match the environment
    const baseURL = apiClient.defaults.baseURL || 'http://localhost:8000';
    
    const eventSource = new EventSource(`${baseURL}/api/bookings/${bookingId}/stream`);

    eventSource.addEventListener('workflow', (e: MessageEvent) => {
      try {
        const data = JSON.parse(e.data) as WorkflowEvent;
        onEvent(data);
      } catch (err) {
        console.error('Failed to parse SSE event data:', err);
      }
    });

    eventSource.onerror = (e) => {
      if (onError) {
        onError(e);
      }
    };

    return eventSource;
  },

  /**
   * Fallback: fetches execution events via polling if SSE fails.
   */
  getExecutionEvents: async (bookingId: string): Promise<WorkflowEvent[]> => {
    const response = await apiClient.get<WorkflowEvent[]>(`/api/bookings/${bookingId}/events`);
    return response.data;
  }
};
