import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import Router from './routes';
import ThemeConfig from './theme';
// import useAuth from './hooks/useAuth';
import RtlLayout from './components/RtlLayout';
import ScrollToTop from './components/ScrollToTop';
// import LoadingScreen from './components/LoadingScreen';
import GoogleAnalytics from './components/GoogleAnalytics';
import NotistackProvider from './components/NotistackProvider';
import ThemePrimaryColor from './components/ThemePrimaryColor';

// ----------------------------------------------------------------------
const queryClient = new QueryClient();

export default function App() {
  // const { isInitialized } = useAuth();

  return (
    <ThemeConfig>
      <ThemePrimaryColor>
        <RtlLayout>
          <NotistackProvider>
            <QueryClientProvider client={queryClient}>
              <ScrollToTop />
              <GoogleAnalytics />
              {/* {isInitialized ? <Router /> : <LoadingScreen />} */}
              <Router />
              <ReactQueryDevtools initialIsOpen={true} />
            </QueryClientProvider>
          </NotistackProvider>
        </RtlLayout>
      </ThemePrimaryColor>
    </ThemeConfig>
  );
}
