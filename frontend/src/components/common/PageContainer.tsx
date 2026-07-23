import React from 'react';

export interface PageContainerProps {
  title?: string;
  children: React.ReactNode;
}

export const PageContainer: React.FC<PageContainerProps> = ({ title, children }) => {
  const containerStyle: React.CSSProperties = {
    padding: 'var(--spacing-xl)',
    maxWidth: '1200px',
    margin: '0 auto',
    width: '100%',
  };

  const titleStyle: React.CSSProperties = {
    marginBottom: 'var(--spacing-lg)',
    fontSize: 'var(--font-size-xxl)',
    fontWeight: 'var(--font-weight-bold)',
  };

  return (
    <div style={containerStyle}>
      {title && <h1 style={titleStyle}>{title}</h1>}
      {children}
    </div>
  );
};
