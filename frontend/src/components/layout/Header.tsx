import React from 'react';

export const Header: React.FC = () => {
  const headerStyle: React.CSSProperties = {
    height: '64px',
    backgroundColor: 'var(--color-surface)',
    borderBottom: '1px solid var(--color-border)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 var(--spacing-xl)',
    position: 'sticky',
    top: 0,
    zIndex: 10,
  };

  const logoStyle: React.CSSProperties = {
    fontWeight: 'var(--font-weight-bold)',
    fontSize: 'var(--font-size-xl)',
    color: 'var(--color-primary)',
  };

  const rightSideStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: 'var(--spacing-md)',
  };

  return (
    <header style={headerStyle}>
      <div style={logoStyle}>AgentForge</div>
      
      <div style={rightSideStyle}>
        <span>Plugin: <strong>None</strong></span>
        <span>Theme: <em>System</em></span>
        <span style={{ 
          width: '10px', height: '10px', borderRadius: '50%', 
          backgroundColor: 'var(--color-success)', display: 'inline-block' 
        }} title="System Online" />
      </div>
    </header>
  );
};
