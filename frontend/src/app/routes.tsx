import { createBrowserRouter, Navigate } from 'react-router-dom';
import { ROUTES } from '@/utils/routes';
import { MainLayout } from '@/layouts/MainLayout';
import { Dashboard } from '@/pages/Dashboard';
import { Booking } from '@/pages/Booking';
import { Plugins } from '@/pages/Plugins';
import { Executions } from '@/pages/Executions';
import { Settings } from '@/pages/Settings';
import { NotFound } from '@/pages/NotFound';

export const router = createBrowserRouter([
  {
    path: ROUTES.HOME,
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <Navigate to={ROUTES.DASHBOARD} replace />,
      },
      {
        path: ROUTES.DASHBOARD,
        element: <Dashboard />,
      },
      {
        path: ROUTES.BOOKMYSHOW,
        element: <Booking />,
      },
      {
        path: ROUTES.PLUGINS,
        element: <Plugins />,
      },
      {
        path: ROUTES.EXECUTIONS,
        element: <Executions />,
      },
      {
        path: ROUTES.SETTINGS,
        element: <Settings />,
      },
      {
        path: ROUTES.NOT_FOUND,
        element: <NotFound />,
      },
    ],
  },
]);
