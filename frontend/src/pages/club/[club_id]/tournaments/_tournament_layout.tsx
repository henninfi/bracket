import React from 'react';

import { TournamentLinks } from '../../../../components/navbar/_main_links';
import { responseIsValid } from '../../../../components/utils/util';
import { checkForAuthError, getTournamentById } from '../../../../services/adapter';
import Layout from '../../../_layout';

export default function TournamentLayout({ children, tournament_id }: any) {
  const tournamentResponse = getTournamentById(tournament_id);
  const club_id = tournamentResponse.data?.data?.club_id as string;
  
  const tournamentLinks = <TournamentLinks club_id={club_id} tournament_id={tournament_id} />;
  const breadcrumbs = responseIsValid(tournamentResponse) ? (
    <h2>/ {tournamentResponse.data.data.name}</h2>
  ) : null;

  return (
    <Layout additionalNavbarLinks={tournamentLinks} breadcrumbs={breadcrumbs}>
      {children}
    </Layout>
  );
}
