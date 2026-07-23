import React from 'react';
import { NavLink } from 'react-router-dom';
import { ROUTES } from '@/utils/routes';

export const Sidebar: React.FC = () => {
  const sidebarStyle: React.CSSProperties = {
    width: '250px',
    backgroundColor: 'var(--color-surface)',
    borderRight: '1px solid var(--color-border)',
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    padding: 'var(--spacing-lg) 0',
  };

  const linkStyle = (isActive: boolean, isDisabled: boolean = false): React.CSSProperties => ({
    padding: 'var(--spacing-md) var(--spacing-xl)',
    display: 'block',
    textDecoration: 'none',
    color: isDisabled ? 'var(--color-text-secondary)' : isActive ? 'var(--color-primary)' : 'var(--color-text)',
    backgroundColor: isActive ? 'var(--color-background)' : 'transparent',
    fontWeight: isActive ? 'var(--font-weight-bold)' : 'var(--font-weight-medium)',
    borderRight: isActive ? '3px solid var(--color-primary)' : '3px solid transparent',
    pointerEvents: isDisabled ? 'none' : 'auto',
    opacity: isDisabled ? 0.5 : 1,
  });

  return (
    <aside style={sidebarStyle}>
      <nav>
        <NavLink to={ROUTES.DASHBOARD} style={({ isActive }) => linkStyle(isActive)}>
          Dashboard
        </NavLink>
        <NavLink to={ROUTES.BOOKMYSHOW} style={({ isActive }) => linkStyle(isActive)}>
          BookMyShow
        </NavLink>
        <NavLink to={ROUTES.PLUGINS} style={({ isActive }) => linkStyle(isActive)}>
          Plugins
        </NavLink>
        <NavLink to={ROUTES.EXECUTIONS} style={({ isActive }) => linkStyle(isActive)}>
          Executions
        </NavLink>
        <NavLink to={ROUTES.SETTINGS} style={({ isActive }) => linkStyle(isActive)}>
          Settings
        </NavLink>
      </nav>
    </aside>
  );
};
