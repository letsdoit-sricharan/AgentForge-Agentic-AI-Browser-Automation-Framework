import React from 'react';
import { WorkflowEvent } from '@/services/eventService';
import { WorkflowStatus } from '@/types';
import { STATUS } from '@/utils/status';

interface WorkflowTimelineProps {
  events: WorkflowEvent[];
  status: WorkflowStatus | null;
  isSubscribed: boolean;
  error: Error | null;
}

export const WorkflowTimeline: React.FC<WorkflowTimelineProps> = ({ events, status, isSubscribed, error }) => {
  if (!status || status === STATUS.QUEUED) {
    return (
      <div style={{ padding: 'var(--spacing-md) 0' }}>
         <h3 style={{ marginBottom: 'var(--spacing-md)' }}>Execution Timeline</h3>
         <p style={{ color: 'var(--color-text-secondary)' }}>Connecting...</p>
      </div>
    );
  }

  if (events.length === 0) {
    return (
      <div style={{ padding: 'var(--spacing-md) 0' }}>
         <h3 style={{ marginBottom: 'var(--spacing-md)' }}>Execution Timeline</h3>
         <p style={{ color: 'var(--color-text-secondary)' }}>Waiting for events...</p>
         {error && <p style={{ color: 'var(--color-error)' }}>{error.message}</p>}
      </div>
    );
  }

  return (
    <div style={{ padding: 'var(--spacing-md) 0', width: '100%' }}>
      <h3 style={{ marginBottom: 'var(--spacing-md)' }}>Execution Timeline</h3>
      {error && <p style={{ color: 'var(--color-error)', marginBottom: 'var(--spacing-sm)' }}>{error.message}</p>}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-sm)' }}>
        {events.map((event, index) => {
          let icon = '○';
          let color = 'var(--color-text-secondary)';
          let fontWeight = 'normal';

          if (event.status === 'completed') {
            icon = '✔';
            color = 'var(--color-success)';
          } else if (event.status === 'running') {
            icon = '●';
            color = 'var(--color-info)';
            fontWeight = 'bold';
          } else if (event.status === 'failed') {
            icon = '✕';
            color = 'var(--color-error)';
            fontWeight = 'bold';
          } else {
            // skipped or pending
            icon = '○';
            color = 'var(--color-text-secondary)';
          }

          return (
            <div key={`${event.step}-${index}`} style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)', color, fontWeight }}>
              <span style={{ display: 'inline-block', width: '20px', textAlign: 'center' }}>
                {icon}
              </span>
              <span>{event.step}</span>
            </div>
          );
        })}
        {isSubscribed && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)', color: 'var(--color-text-secondary)' }}>
            <span style={{ display: 'inline-block', width: '20px', textAlign: 'center' }}>○</span>
            <span>Receiving updates...</span>
          </div>
        )}
      </div>
    </div>
  );
};
