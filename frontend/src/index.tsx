// scroll bar
import 'simplebar/src/simplebar.css';

// lightbox
import 'react-image-lightbox/style.css';

// slick-carousel
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

// lazy image
import 'lazysizes';
import 'lazysizes/plugins/attrchange/ls.attrchange';
import 'lazysizes/plugins/object-fit/ls.object-fit';
import 'lazysizes/plugins/parent-fit/ls.parent-fit';

import ReactDOM from 'react-dom';
import { StrictMode } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import { Provider as ReduxProvider } from 'react-redux';
import { PersistGate } from 'redux-persist/lib/integration/react';
// redux
import { store, persistor } from './redux/store';
// contexts
import { SettingsProvider } from './contexts/SettingsContext';
// components
import LoadingScreen from './components/LoadingScreen';


import App from './App';

// ----------------------------------------------------------------------

ReactDOM.render(
  <StrictMode>
    <HelmetProvider>
      <ReduxProvider store={store}>
        <PersistGate loading={<LoadingScreen />} persistor={persistor}>
          <SettingsProvider>
            <BrowserRouter>
              <App />
            </BrowserRouter>
          </SettingsProvider>
        </PersistGate>
      </ReduxProvider>
    </HelmetProvider>
  </StrictMode>,
  document.getElementById('root')
);
