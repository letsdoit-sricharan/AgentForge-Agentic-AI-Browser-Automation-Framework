import React, { forwardRef } from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = '', id, ...props }, ref) => {
    const inputId = id || Math.random().toString(36).substring(7);

    const containerStyle: React.CSSProperties = {
      display: 'flex',
      flexDirection: 'column',
      gap: 'var(--spacing-xs)',
      marginBottom: 'var(--spacing-md)',
    };

    const labelStyle: React.CSSProperties = {
      fontSize: 'var(--font-size-sm)',
      fontWeight: 'var(--font-weight-medium)',
      color: 'var(--color-text-secondary)',
    };

    const inputStyle: React.CSSProperties = {
      padding: 'var(--spacing-sm) var(--spacing-md)',
      borderRadius: 'var(--radius-md)',
      border: `1px solid ${error ? 'var(--color-error)' : 'var(--color-border)'}`,
      fontFamily: 'inherit',
      fontSize: 'var(--font-size-base)',
      outline: 'none',
    };

    const errorStyle: React.CSSProperties = {
      fontSize: 'var(--font-size-sm)',
      color: 'var(--color-error)',
    };

    return (
      <div style={containerStyle} className={className}>
        {label && (
          <label htmlFor={inputId} style={labelStyle}>
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          style={inputStyle}
          {...props}
        />
        {error && <span style={errorStyle}>{error}</span>}
      </div>
    );
  }
);

Input.displayName = 'Input';
