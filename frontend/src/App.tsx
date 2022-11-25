import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import Router from './routes';
import ThemeConfig from './theme';
import RtlLayout from './components/RtlLayout';
import ScrollToTop from './components/ScrollToTop';
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
              <Router />
              <ReactQueryDevtools initialIsOpen={true} />
            </QueryClientProvider>
          </NotistackProvider>
        </RtlLayout>
      </ThemePrimaryColor>
    </ThemeConfig>
  );
}
