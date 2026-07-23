import React from 'react';
import { PageContainer } from '@/components/common/PageContainer';
import { EmptyState } from '@/components/dashboard/EmptyState';

export const Settings: React.FC = () => {
  return (
    <PageContainer title="Settings">
      <EmptyState 
        title="Coming Soon" 
        description="Global platform settings and configuration will be available here in a future update." 
        icon="⚙️"
      />
    </PageContainer>
  );
};
