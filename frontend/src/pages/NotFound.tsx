import React from 'react';
import { PageContainer } from '@/components/common/PageContainer';
import { Link } from 'react-router-dom';
import { ROUTES } from '@/utils/routes';

export const NotFound: React.FC = () => {
  const style: React.CSSProperties = {
    textAlign: 'center',
    padding: '4rem',
  };

  return (
    <PageContainer>
      <div style={style}>
        <h1 style={{ fontSize: '4rem', color: 'var(--color-text-secondary)', marginBottom: '1rem' }}>404</h1>
        <h2>Page Not Found</h2>
        <p style={{ margin: '1rem 0' }}>The requested resource does not exist.</p>
        <Link to={ROUTES.DASHBOARD} style={{ color: 'var(--color-primary)', textDecoration: 'underline' }}>
          Return to Dashboard
        </Link>
      </div>
    </PageContainer>
  );
};
