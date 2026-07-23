import React from 'react';
import { Card } from '@/components/common/Card';
import { Button } from '@/components/common/Button';

interface ErrorCardProps {
  errors: string[];
  onRetry: () => void;
}

export const ErrorCard: React.FC<ErrorCardProps> = ({ errors, onRetry }) => {
  if (!errors || errors.length === 0) return null;

  return (
    <Card 
      title="Booking Failed" 
      style={{ borderColor: 'var(--color-error)' }}
    >
      <div style={{ color: 'var(--color-error)', marginBottom: 'var(--spacing-md)' }}>
        <ul style={{ margin: 0, paddingLeft: '1.2rem' }}>
          {errors.map((error, idx) => (
            <li key={idx} style={{ marginBottom: '0.25rem' }}>{error}</li>
          ))}
        </ul>
      </div>

      <div style={{ marginTop: 'var(--spacing-md)' }}>
        <Button variant="outline" onClick={onRetry}>
          Try Again
        </Button>
      </div>
    </Card>
  );
};
