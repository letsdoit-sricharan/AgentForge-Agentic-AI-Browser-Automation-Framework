import React from 'react';
import { Card } from '@/components/common/Card';
import { StatusBadge } from '@/components/common/StatusBadge';
import { BookingStatus } from '@/types';
import { STATUS } from '@/utils/status';

interface ResultCardProps {
  result: BookingStatus['result'];
}

export const ResultCard: React.FC<ResultCardProps> = ({ result }) => {
  if (!result || !result.success) return null;

  const rowStyle: React.CSSProperties = {
    display: 'flex',
    justifyContent: 'space-between',
    padding: 'var(--spacing-sm) 0',
    borderBottom: '1px solid var(--color-border)',
  };

  const labelStyle: React.CSSProperties = {
    fontWeight: 'var(--font-weight-medium)',
    color: 'var(--color-text-secondary)',
  };

  // Extract data (handling potential missing keys gracefully)
  const data = result.data || {};

  return (
    <Card 
      title="Booking Successful 🎉" 
      style={{ borderColor: 'var(--color-success)' }}
    >
      <div style={{ marginBottom: 'var(--spacing-md)' }}>
        <p style={{ color: 'var(--color-success)', fontWeight: 'bold' }}>
          {result.message}
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <div style={rowStyle}>
          <span style={labelStyle}>Execution Status</span>
          <StatusBadge status={STATUS.COMPLETED} />
        </div>
        
        {/* Render data from the backend result if available */}
        {Object.entries(data).map(([key, value]) => (
          <div key={key} style={rowStyle}>
            <span style={labelStyle}>
              {key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' ')}
            </span>
            <span>{String(value)}</span>
          </div>
        ))}
      </div>
    </Card>
  );
};
