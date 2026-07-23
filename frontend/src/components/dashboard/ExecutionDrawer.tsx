import React from 'react';
import { ExecutionRecord } from '@/types';
import { StatusBadge } from '@/components/common/StatusBadge';
import { Button } from '@/components/common/Button';
import { useExecutionEvents } from '@/hooks/useExecutionEvents';
import { WorkflowTimeline } from '@/components/booking/WorkflowTimeline';
import { WorkflowStatus } from '@/types';

interface ExecutionDrawerProps {
  execution: ExecutionRecord | null;
  onClose: () => void;
}

export const ExecutionDrawer: React.FC<ExecutionDrawerProps> = ({ execution, onClose }) => {
  const { events, isSubscribed, error } = useExecutionEvents(execution?.id || null);

  if (!execution) return null;

  const overlayStyle: React.CSSProperties = {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.5)',
    zIndex: 40,
    display: 'flex',
    justifyContent: 'flex-end',
  };

  const drawerStyle: React.CSSProperties = {
    width: '400px',
    maxWidth: '100%',
    height: '100%',
    backgroundColor: 'var(--color-surface)',
    boxShadow: 'var(--shadow-lg)',
    padding: 'var(--spacing-xl)',
    display: 'flex',
    flexDirection: 'column',
    overflowY: 'auto',
    animation: 'slideIn 0.3s forwards',
  };

  const rowStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    marginBottom: 'var(--spacing-md)',
    paddingBottom: 'var(--spacing-sm)',
    borderBottom: '1px solid var(--color-border)',
  };

  const labelStyle: React.CSSProperties = {
    fontSize: 'var(--font-size-sm)',
    color: 'var(--color-text-secondary)',
    marginBottom: 'var(--spacing-xs)',
  };

  const valueStyle: React.CSSProperties = {
    fontWeight: 'var(--font-weight-medium)',
    wordBreak: 'break-all',
  };

  return (
    <div style={overlayStyle} onClick={onClose}>
      <style>
        {`
          @keyframes slideIn {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
          }
        `}
      </style>
      <div style={drawerStyle} onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-xl)' }}>
          <h2 style={{ margin: 0 }}>Execution Details</h2>
          <Button variant="ghost" onClick={onClose} style={{ padding: '0.25rem 0.5rem', fontSize: '1.25rem' }}>✕</Button>
        </div>

        <div style={rowStyle}>
          <span style={labelStyle}>Execution ID</span>
          <span style={{ ...valueStyle, fontFamily: 'monospace' }}>{execution.id}</span>
        </div>

        <div style={rowStyle}>
          <span style={labelStyle}>Plugin</span>
          <span style={valueStyle}>{execution.plugin}</span>
        </div>

        <div style={rowStyle}>
          <span style={labelStyle}>Workflow Status</span>
          <div><StatusBadge status={execution.status} /></div>
        </div>
        
        {execution.currentStep && (
          <div style={rowStyle}>
            <span style={labelStyle}>Current Step</span>
            <span style={valueStyle}>{execution.currentStep}</span>
          </div>
        )}

        <div style={rowStyle}>
          <span style={labelStyle}>Started Time</span>
          <span style={valueStyle}>{new Date(execution.startedAt).toLocaleString()}</span>
        </div>

        <div style={rowStyle}>
          <span style={labelStyle}>Completed Time</span>
          <span style={valueStyle}>{execution.completedAt ? new Date(execution.completedAt).toLocaleString() : 'Not Available'}</span>
        </div>

        <div style={rowStyle}>
          <span style={labelStyle}>Duration</span>
          <span style={valueStyle}>{execution.duration || 'Not Available'}</span>
        </div>

        {execution.result && (
          <div style={rowStyle}>
            <span style={labelStyle}>Execution Result</span>
            <span style={{ ...valueStyle, color: execution.result.success ? 'var(--color-success)' : 'inherit' }}>
              {execution.result.message}
            </span>
          </div>
        )}

        {execution.error && (
          <div style={{ ...rowStyle }}>
            <span style={labelStyle}>Error Message</span>
            <span style={{ ...valueStyle, color: 'var(--color-error)' }}>{execution.error}</span>
          </div>
        )}

        <div style={{ marginTop: 'var(--spacing-xl)', borderTop: '1px solid var(--color-border)', paddingTop: 'var(--spacing-md)' }}>
          <WorkflowTimeline 
            events={events} 
            status={execution.status as WorkflowStatus} 
            isSubscribed={isSubscribed} 
            error={error} 
          />
        </div>

      </div>
    </div>
  );
};
