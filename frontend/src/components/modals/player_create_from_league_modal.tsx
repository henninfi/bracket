import { Button, Modal, Text } from '@mantine/core';
import { useTranslation } from 'next-i18next';
import { useState } from 'react';
import { SWRResponse } from 'swr';
import { createMultiplePlayers } from '../../services/player';
import { PlayersService } from '../../client'; '../../client/services/PlayersService';
import { IconUsersPlus } from '@tabler/icons-react';
import SaveButton from '../buttons/save';


const ImportPlayersModal = ({ club_id, tournament_id, swrPlayersResponse }: {
  club_id: string,
  tournament_id: number, 
  swrPlayersResponse: SWRResponse
}) => {
  const { t } = useTranslation();
  const [opened, setOpened] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');



const handleImportPlayers = async () => {
  setLoading(true);
  setError('');
  const sessionId = club_id.toString();
  console.log('sessionId', sessionId)
  try {
    // Fetching players from the external API
    const response = await PlayersService.listPlayersBySession({sessionId: sessionId});
    console.log('response', response)

    // Transform the fetched data to match the required payload format
    // Assuming 'response' is an array of player objects retrieved from somewhere
    const names = response.map(player => player.name).join('\n');
    const uuids = response.map(player => player.id).join('\n');

    const payload = {
      names: names,
      uuids: uuids,
      active: !response.some(player => player.isRetired)
    };
    console.log('payload', payload)
    // Sending transformed data to the same API as the multiple players creation
    await createMultiplePlayers(tournament_id, payload.names, payload.active, payload.uuids);
    await swrPlayersResponse.mutate();
    setLoading(false);
    setOpened(false);
  } catch (err) {
    setError('Failed to import players');
    setLoading(false);
  }
};


  return (
    <>
      <SaveButton
        onClick={() => setOpened(true)}
        leftSection={<IconUsersPlus size={24} />}
        title={t('add_players_from_mini_league_button')}
      />
      <Modal
        opened={opened}
        onClose={() => setOpened(false)}
        title={t('import_players_from_mini_league_modal_title')}
      >
        {/* <Text>{t('import_players_instruction')}</Text> */}
        <Button 
        onClick={handleImportPlayers} 
        loading={loading}>
          {t('add_players_from_mini_league_button')}
          
        </Button>




        {error && <Text color="red">{error}</Text>}
      </Modal>
    </>
  );
};

export default ImportPlayersModal;
