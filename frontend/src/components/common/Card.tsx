import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  footer?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({
  title,
  children,
  footer,
  className = '',
  style,
  ...props
}) => {
  const baseStyle: React.CSSProperties = {
    backgroundColor: 'var(--color-surface)',
    borderRadius: 'var(--radius-lg)',
    boxShadow: 'var(--shadow-sm)',
    border: '1px solid var(--color-border)',
    overflow: 'hidden',
    ...style,
  };

  const headerStyle: React.CSSProperties = {
    padding: 'var(--spacing-md)',
    borderBottom: '1px solid var(--color-border)',
    fontWeight: 'bold',
  };

  const bodyStyle: React.CSSProperties = {
    padding: 'var(--spacing-md)',
  };

  const footerStyle: React.CSSProperties = {
    padding: 'var(--spacing-md)',
    borderTop: '1px solid var(--color-border)',
    backgroundColor: 'var(--color-background)',
  };

  return (
    <div style={baseStyle} className={className} {...props}>
      {title && <div style={headerStyle}>{title}</div>}
      <div style={bodyStyle}>{children}</div>
      {footer && <div style={footerStyle}>{footer}</div>}
    </div>
  );
};
