import React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  className = '',
  disabled,
  ...props
}) => {
  // Placeholder basic inline styles for foundational sprint.
  // We'll move to CSS modules or styled system in later sprints.
  const baseStyle: React.CSSProperties = {
    padding: size === 'sm' ? '0.25rem 0.5rem' : size === 'lg' ? '0.75rem 1.5rem' : '0.5rem 1rem',
    borderRadius: 'var(--radius-md)',
    border: variant === 'outline' ? '1px solid var(--color-border)' : 'none',
    backgroundColor: variant === 'primary' ? 'var(--color-primary)' : variant === 'secondary' ? 'var(--color-secondary)' : 'transparent',
    color: variant === 'outline' || variant === 'ghost' ? 'var(--color-text)' : 'white',
    cursor: disabled || isLoading ? 'not-allowed' : 'pointer',
    opacity: disabled || isLoading ? 0.6 : 1,
    fontWeight: 'var(--font-weight-medium)',
  };

  return (
    <button
      style={baseStyle}
      disabled={disabled || isLoading}
      className={className}
      {...props}
    >
      {isLoading ? 'Loading...' : children}
    </button>
  );
};
