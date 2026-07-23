import React from 'react';
import { Card } from '@/components/common/Card';
import { Button } from '@/components/common/Button';
import { Plugin } from '@/types';
import { useNavigate } from 'react-router-dom';

interface PluginCardProps {
  plugin: Plugin;
  onClick?: () => void;
}

export const PluginCard: React.FC<PluginCardProps> = ({ plugin, onClick }) => {
  const navigate = useNavigate();

  const handleOpen = () => {
    if (onClick) onClick();
    else if (plugin.id === 'bookmyshow') navigate('/bookmyshow');
  };

  return (
    <Card style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--spacing-sm)' }}>
        <h3 style={{ margin: 0 }}>{plugin.name}</h3>
        <span style={{ 
          fontSize: 'var(--font-size-sm)', 
          padding: '2px 8px', 
          borderRadius: 'var(--radius-full)', 
          backgroundColor: plugin.isActive ? 'var(--color-success)' : 'var(--color-secondary)',
          color: 'white',
          fontWeight: 'bold'
        }}>
          {plugin.isActive ? 'Enabled' : 'Coming Soon'}
        </span>
      </div>
      
      {plugin.version && <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', marginBottom: 'var(--spacing-md)' }}>Version: {plugin.version}</div>}
      
      <p style={{ margin: 0, color: 'var(--color-text-secondary)', flex: 1 }}>{plugin.description}</p>
      
      <div style={{ marginTop: 'var(--spacing-lg)' }}>
        <Button 
          variant={plugin.isActive ? 'primary' : 'outline'} 
          disabled={!plugin.isActive}
          onClick={handleOpen}
          style={{ width: '100%' }}
        >
          {plugin.isActive ? 'Open Plugin' : 'Disabled'}
        </Button>
      </div>
    </Card>
  );
};
