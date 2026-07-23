import React from 'react';
import { ExecutionRecord } from '@/types';
import { StatusBadge } from '@/components/common/StatusBadge';
import { Button } from '@/components/common/Button';

interface ExecutionTableProps {
  executions: ExecutionRecord[];
  onViewDetails: (execution: ExecutionRecord) => void;
}

export const ExecutionTable: React.FC<ExecutionTableProps> = ({ executions, onViewDetails }) => {
  const tableStyle: React.CSSProperties = {
    width: '100%',
    borderCollapse: 'collapse',
  };

  const thStyle: React.CSSProperties = {
    textAlign: 'left',
    padding: 'var(--spacing-md)',
    borderBottom: '2px solid var(--color-border)',
    color: 'var(--color-text-secondary)',
    fontWeight: 'var(--font-weight-medium)',
  };

  const tdStyle: React.CSSProperties = {
    padding: 'var(--spacing-md)',
    borderBottom: '1px solid var(--color-border)',
  };

  if (executions.length === 0) {
    return null; // Empty state handled by parent
  }

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={thStyle}>Execution ID</th>
            <th style={thStyle}>Plugin</th>
            <th style={thStyle}>Status</th>
            <th style={thStyle}>Started</th>
            <th style={thStyle}>Duration</th>
            <th style={thStyle}>Action</th>
          </tr>
        </thead>
        <tbody>
          {executions.map((exec) => (
            <tr key={exec.id} style={{ transition: 'background-color 0.2s' }} onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--color-background)'} onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}>
              <td style={{ ...tdStyle, fontFamily: 'monospace' }}>{exec.id.substring(0, 13)}...</td>
              <td style={tdStyle}>{exec.plugin}</td>
              <td style={tdStyle}><StatusBadge status={exec.status} /></td>
              <td style={tdStyle}>{new Date(exec.startedAt).toLocaleString()}</td>
              <td style={tdStyle}>{exec.duration || 'Running...'}</td>
              <td style={tdStyle}>
                <Button size="sm" variant="outline" onClick={() => onViewDetails(exec)}>View Details</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
