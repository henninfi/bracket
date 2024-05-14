import { Grid, Title } from '@mantine/core';
import { GetStaticProps } from 'next';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import TournamentModal from '../components/modals/tournament_modal';
import TournamentsTable from '../components/tables/tournaments';
import { capitalize } from '../components/utils/util';
import { getTournaments } from '../services/adapter';
import Layout from './_layout';
import { useAuthInfo } from '@propelauth/react'



export default function HomePage() {
  const authInfo = useAuthInfo();

  const swrTournamentsResponse = getTournaments();

  // checkForAuthError(swrTournamentsResponse);
  const { t } = useTranslation();

  return (
    <Layout>
      <Grid justify="space-between">
        <Grid.Col span="auto">
          <Title>{capitalize(t('tournaments_title'))}</Title>
        </Grid.Col>
        <Grid.Col span="content">
          <TournamentModal swrTournamentsResponse={swrTournamentsResponse} />
        </Grid.Col>
      </Grid>
      <TournamentsTable swrTournamentsResponse={swrTournamentsResponse} />
    </Layout>
  );
}

type Props = {};
export const getStaticProps: GetStaticProps<Props> = async ({ locale }) => ({
  props: {
    ...(await serverSideTranslations(locale ?? 'en', ['common'])),
  },
});
