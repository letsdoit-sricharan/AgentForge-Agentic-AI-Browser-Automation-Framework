import React from 'react';

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ title, description, icon }) => {
  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center',
      padding: 'var(--spacing-xl) 2rem',
      textAlign: 'center',
      color: 'var(--color-text-secondary)',
      backgroundColor: 'var(--color-background)',
      borderRadius: 'var(--radius-lg)',
      border: '1px dashed var(--color-border)'
    }}>
      {icon && <div style={{ fontSize: '3rem', marginBottom: 'var(--spacing-md)' }}>{icon}</div>}
      <h3 style={{ margin: '0 0 var(--spacing-sm) 0', color: 'var(--color-text)' }}>{title}</h3>
      <p style={{ margin: 0, maxWidth: '400px' }}>{description}</p>
    </div>
  );
};
