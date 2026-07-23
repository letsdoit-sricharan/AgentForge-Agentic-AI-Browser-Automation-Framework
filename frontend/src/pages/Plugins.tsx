import React from 'react';
import { PageContainer } from '@/components/common/PageContainer';
import { PluginCard } from '@/components/dashboard/PluginCard';
import { EmptyState } from '@/components/dashboard/EmptyState';
import { Loader } from '@/components/common/Loader';
import { usePlugins } from '@/hooks/usePlugins';
import { ErrorCard } from '@/components/booking/ErrorCard';

export const Plugins: React.FC = () => {
  const { plugins, isLoading, error } = usePlugins();

  if (isLoading) {
    return (
      <PageContainer title="Plugins">
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '4rem' }}>
          <Loader size="lg" text="Loading plugins..." />
        </div>
      </PageContainer>
    );
  }

  if (error) {
    return (
      <PageContainer title="Plugins">
        <ErrorCard errors={[error]} onRetry={() => window.location.reload()} />
      </PageContainer>
    );
  }

  return (
    <PageContainer title="Plugins">
      <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--spacing-lg)' }}>
        Manage and launch available AgentForge browser automation plugins.
      </p>

      {plugins.length > 0 ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 'var(--spacing-md)' }}>
          {plugins.map(plugin => (
            <PluginCard key={plugin.id} plugin={plugin} />
          ))}
        </div>
      ) : (
        <EmptyState title="No Plugins Found" description="There are no plugins available in the registry." icon="🔌" />
      )}
    </PageContainer>
  );
};
