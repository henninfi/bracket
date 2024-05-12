import { createAxios, handleRequestError } from './adapter';

export async function createClub(name: string) {
  return createAxios()
    .post('clubs', { name })
    .catch((response: any) => handleRequestError(response));
}

export async function deleteClub(club_id: string) {
  return createAxios()
    .delete(`clubs/${club_id}`)
    .catch((response: any) => handleRequestError(response));
}

export async function updateClub(club_id: string, name: string) {
  return createAxios()
    .put(`clubs/${club_id}`, {
      name,
    })
    .catch((response: any) => handleRequestError(response));
}
