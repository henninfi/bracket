import { ColorSchemeScript, MantineProvider, createTheme } from '@mantine/core';
import '@mantine/core/styles.css';
import '@mantine/dates/styles.css';
import '@mantine/dropzone/styles.css';
import '@mantine/notifications/styles.css';
import '@mantine/spotlight/styles.css';
import { appWithTranslation } from 'next-i18next';
import Head from 'next/head';
import React from 'react';
import { RequiredAuthProvider, RedirectToLogin } from '@propelauth/react';
import type { AppProps } from 'next/app';
import AuthTokenUpdater from '../components/auth/token_updater';
import { useAuthInfo } from '@propelauth/react';
import { registerUser } from '../services/user';

import { BracketSpotlight } from '../components/modals/spotlight';

const theme = createTheme({
  colors: {
    dark: [
      '#C1C2C5',
      '#A6A7AB',
      '#909296',
      '#5c5f66',
      '#373A40',
      '#2C2E33',
      '#25262b',
      '#1A1B1E',
      '#141517',
      '#101113',
    ],
  },
});

function AnalyticsScript() {
  if (process.env.ANALYTICS_SCRIPT_SRC == null) {
    return null;
  }

  return (
    <script
      async
      data-domain={process.env.ANALYTICS_DATA_DOMAIN}
      data-website-id={process.env.ANALYTICS_DATA_WEBSITE_ID}
      src={process.env.ANALYTICS_SCRIPT_SRC}
    />
  );
}

async function InitiateBracketUser() {
  const authInfo = useAuthInfo();
  if (authInfo.user?.properties?.bracket_id == null) {
    
    const response = await registerUser();
    console.log("User Created", response);
    return null;
  }
  else {
    console.log("User already registered");
    return null
  } 
  
}


const App = ({ Component, pageProps }: AppProps) => {
  
  return (
    <>
      <RequiredAuthProvider
        authUrl={process.env.NEXT_PUBLIC_AUTH_URL!}
        displayIfLoggedOut={<RedirectToLogin />}
      >
        <Head>
          <title>Bracket</title>
          <meta charSet="UTF-8" />
          <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <link rel="shortcut icon" href="/favicon.svg" />
          <InitiateBracketUser />
          <AnalyticsScript />

          <ColorSchemeScript defaultColorScheme="auto" />
        </Head>
        <AuthTokenUpdater />
        <MantineProvider defaultColorScheme="auto" theme={theme}>
          <BracketSpotlight />
          <Component {...pageProps} />
        </MantineProvider>
      </RequiredAuthProvider>

    </>
  );
};

export default appWithTranslation(App);
