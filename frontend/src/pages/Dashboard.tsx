import React, { useState } from 'react';
import { PageContainer } from '@/components/common/PageContainer';
import { StatCard } from '@/components/dashboard/StatCard';
import { ExecutionTable } from '@/components/dashboard/ExecutionTable';
import { PluginCard } from '@/components/dashboard/PluginCard';
import { ExecutionDrawer } from '@/components/dashboard/ExecutionDrawer';
import { EmptyState } from '@/components/dashboard/EmptyState';
import { Loader } from '@/components/common/Loader';
import { useDashboard } from '@/hooks/useDashboard';
import { ExecutionRecord } from '@/types';
import { ErrorCard } from '@/components/booking/ErrorCard'; // Reuse error card

export const Dashboard: React.FC = () => {
  const { stats, recentExecutions, activePlugins, isLoading, error } = useDashboard();
  const [selectedExecution, setSelectedExecution] = useState<ExecutionRecord | null>(null);

  if (isLoading) {
    return (
      <PageContainer>
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '4rem' }}>
          <Loader size="lg" text="Loading dashboard data..." />
        </div>
      </PageContainer>
    );
  }

  if (error) {
    return (
      <PageContainer title="Dashboard">
        <ErrorCard errors={[error]} onRetry={() => window.location.reload()} />
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <div style={{ marginBottom: 'var(--spacing-xl)' }}>
        <h1 style={{ marginBottom: 'var(--spacing-xs)' }}>AgentForge</h1>
        <p style={{ margin: 0, color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-lg)' }}>
          Production-Ready AI Browser Automation Framework
        </p>
      </div>

      {stats && (
        <div style={{ display: 'flex', gap: 'var(--spacing-md)', marginBottom: 'var(--spacing-xl)', flexWrap: 'wrap' }}>
          <StatCard title="Registered Plugins" value={stats.registeredPlugins} icon="🔌" />
          <StatCard title="Running Executions" value={stats.runningExecutions} description="Currently Active" icon="▶️" />
          <StatCard title="Completed Today" value={stats.completedToday} icon="✅" />
          <StatCard title="Failed Executions" value={stats.failedExecutions} icon="❌" />
        </div>
      )}

      <div style={{ display: 'flex', gap: 'var(--spacing-xl)', flexDirection: 'column' }}>
        <section>
          <h2 style={{ marginBottom: 'var(--spacing-md)' }}>Recent Executions</h2>
          {recentExecutions.length > 0 ? (
            <ExecutionTable executions={recentExecutions} onViewDetails={setSelectedExecution} />
          ) : (
            <EmptyState title="No Executions" description="There are no recent executions to display." icon="📊" />
          )}
        </section>

        <section>
          <h2 style={{ marginBottom: 'var(--spacing-md)' }}>Installed Plugins</h2>
          {activePlugins.length > 0 ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 'var(--spacing-md)' }}>
              {activePlugins.map(plugin => (
                <PluginCard key={plugin.id} plugin={plugin} />
              ))}
            </div>
          ) : (
            <EmptyState title="No Plugins Active" description="Install a plugin to get started." icon="🧩" />
          )}
        </section>
      </div>

      <ExecutionDrawer execution={selectedExecution} onClose={() => setSelectedExecution(null)} />
    </PageContainer>
  );
};
