import React, { useState } from 'react';
import { PageContainer } from '@/components/common/PageContainer';
import { ExecutionTable } from '@/components/dashboard/ExecutionTable';
import { ExecutionDrawer } from '@/components/dashboard/ExecutionDrawer';
import { EmptyState } from '@/components/dashboard/EmptyState';
import { Loader } from '@/components/common/Loader';
import { Input } from '@/components/common/Input';
import { useExecutions } from '@/hooks/useExecutions';
import { ErrorCard } from '@/components/booking/ErrorCard';
import { ExecutionRecord } from '@/types';

export const Executions: React.FC = () => {
  const { executions, isLoading, error } = useExecutions();
  const [selectedExecution, setSelectedExecution] = useState<ExecutionRecord | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');

  const filteredExecutions = executions.filter(exec => {
    const matchesSearch = exec.plugin.toLowerCase().includes(searchTerm.toLowerCase()) || exec.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'ALL' || exec.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  if (isLoading) {
    return (
      <PageContainer title="Executions">
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '4rem' }}>
          <Loader size="lg" text="Loading executions history..." />
        </div>
      </PageContainer>
    );
  }

  if (error) {
    return (
      <PageContainer title="Executions">
        <ErrorCard errors={[error]} onRetry={() => window.location.reload()} />
      </PageContainer>
    );
  }

  return (
    <PageContainer title="Execution History">
      <div style={{ display: 'flex', gap: 'var(--spacing-md)', marginBottom: 'var(--spacing-lg)', flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: '250px' }}>
          <Input 
            placeholder="Search by ID or Plugin..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div>
          <select 
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            style={{ 
              padding: '0.6rem', 
              borderRadius: 'var(--radius-md)', 
              border: '1px solid var(--color-border)',
              backgroundColor: 'var(--color-surface)',
              color: 'var(--color-text)',
              minWidth: '150px'
            }}
          >
            <option value="ALL">All Statuses</option>
            <option value="RUNNING">Running</option>
            <option value="COMPLETED">Completed</option>
            <option value="FAILED">Failed</option>
            <option value="QUEUED">Queued</option>
          </select>
        </div>
      </div>

      {filteredExecutions.length > 0 ? (
        <ExecutionTable executions={filteredExecutions} onViewDetails={setSelectedExecution} />
      ) : (
        <EmptyState title="No Executions Found" description="Try adjusting your search or filters." icon="🔍" />
      )}

      <ExecutionDrawer execution={selectedExecution} onClose={() => setSelectedExecution(null)} />
    </PageContainer>
  );
};
