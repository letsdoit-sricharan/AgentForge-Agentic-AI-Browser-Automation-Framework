import React from 'react';
import { WorkflowStatus } from '@/types';
import { STATUS } from '@/utils/status';

export interface StatusBadgeProps {
  status: WorkflowStatus;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  let bgColor = 'var(--color-secondary)';
  let color = 'white';

  switch (status) {
    case STATUS.QUEUED:
      bgColor = 'var(--color-secondary)';
      break;
    case STATUS.RUNNING:
      bgColor = 'var(--color-info)';
      break;
    case STATUS.COMPLETED:
      bgColor = 'var(--color-success)';
      break;
    case STATUS.FAILED:
      bgColor = 'var(--color-error)';
      break;
  }

  const style: React.CSSProperties = {
    display: 'inline-block',
    padding: '0.25rem 0.75rem',
    borderRadius: 'var(--radius-full)',
    backgroundColor: bgColor,
    color: color,
    fontSize: 'var(--font-size-sm)',
    fontWeight: 'bold',
    textTransform: 'uppercase',
  };

  return <span style={style}>{status}</span>;
};
