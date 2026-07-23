import React from 'react';
import { Card } from '@/components/common/Card';

interface StatCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon?: string;
}

export const StatCard: React.FC<StatCardProps> = ({ title, value, description, icon }) => {
  return (
    <Card style={{ flex: 1, minWidth: '200px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-sm)' }}>
        <h4 style={{ margin: 0, color: 'var(--color-text-secondary)', fontWeight: 'var(--font-weight-medium)' }}>{title}</h4>
        {icon && <span style={{ fontSize: 'var(--font-size-xl)' }}>{icon}</span>}
      </div>
      <div style={{ fontSize: '2rem', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--spacing-xs)' }}>
        {value}
      </div>
      {description && <p style={{ margin: 0, color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-sm)' }}>{description}</p>}
    </Card>
  );
};
