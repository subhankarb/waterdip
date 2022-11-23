import { Suspense, lazy } from 'react';
import { Navigate, useRoutes, useLocation } from 'react-router-dom';
// layouts
import DashboardLayout from '../layouts/app';
import LogoOnlyLayout from '../layouts/LogoOnlyLayout';
// guards
// import GuestGuard from '../guards/GuestGuard';
// import AuthGuard from '../guards/AuthGuard';
// components
import LoadingScreen from '../components/LoadingScreen';
import MonitorList from 'pages/Monitors/MonitorList/MonitorList';
import MonitorCreate from 'pages/Monitors/MonitorCreate/MonitorCreate';
import AlertList from 'pages/Alerts/AlertList';

// ----------------------------------------------------------------------

const Loadable = (Component: any) => (props: any) => {
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const { pathname } = useLocation();
  const isDashboard = pathname.includes('/app');

  return (
    <Suspense
      fallback={
        <LoadingScreen
          sx={{
            ...(!isDashboard && {
              top: 0,
              left: 0,
              width: 1,
              zIndex: 9999,
              position: 'fixed'
            })
          }}
        />
      }
    >
      <Component {...props} />
    </Suspense>
  );
};

export default function Router() {
  return useRoutes([
    {
      path: 'app',
      element: (
        <>
          <DashboardLayout />
        </>
      ),
      children: [
        { path: '/', element: <Navigate to="/app/models" replace /> },
        {
          path: 'models',
          children: [
            { path: '/', element: <ModelList /> },
            {
              path: ':modelId/:tabName',
              element: <ModelDetails />
            }
          ]
        },
        {
          path: 'monitors',
          children: [
            { path: '/', element: <MonitorList /> },
            { path: '/create', element: <MonitorCreate /> }
          ]
        },
        {
          path: 'alerts',
          children: [{ path: '/', element: <AlertList /> }]
        }
        // { path: 'members', element: <Members /> }
      ]
    },

    // Main Routes
    {
      path: '*',
      element: <LogoOnlyLayout />,
      children: [
        { path: '404', element: <NotFound /> },
        { path: '*', element: <Navigate to="/404" replace /> }
      ]
    },
    {
      path: '/',
      element: <Navigate to="/app" replace />
    },
    { path: '*', element: <Navigate to="/404" replace /> }
  ]);
}

// IMPORT COMPONENTS
// Authentication
// const Login = Loadable(lazy(() => import('../pages/authentication/Login')));
// Dashboard
const ModelDetails = Loadable(lazy(() => import('../pages/Models/ModelDetails/ModelDetails')));
const ModelList = Loadable(lazy(() => import('../pages/Models/ModelList/ModelList')));
// const Monitors = Loadable(lazy(() => import('../pages/APIKeys')));
// const Members = Loadable(lazy(() => import('../pages/Members/Members')));
const NotFound = Loadable(lazy(() => import('../pages/Page404')));
// const ModelCreate = Loadable(lazy(() => import('../pages/Monitors/MonitorCreate/MonitorCreate')));
