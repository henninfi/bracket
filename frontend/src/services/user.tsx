import { UserBodyInterface, UserToRegisterInterface } from '../interfaces/user';
import { createAxios, handleRequestError } from './adapter';
import { useAuthInfo } from '@propelauth/react';

export async function performLogin(username: string, password: string) {
  const bodyFormData = new FormData();
  bodyFormData.append('grant_type', 'password');
  bodyFormData.append('username', username);
  bodyFormData.append('password', password);

  const { data } = await createAxios()
    .post('token', bodyFormData)
    .catch((err_response: any) => {
      handleRequestError(err_response);
      return { data: null };
    });

  if (data == null) {
    return false;
  }

  localStorage.setItem('login', JSON.stringify(data));

  handleRequestError(data);

  // Reload axios object.
  createAxios();
  return true;
}

export async function updateUser(user_id: number, user: UserBodyInterface) {
  return createAxios()
    .put(`users/${user_id}`, user)
    .catch((response: any) => handleRequestError(response));
}

export async function updatePassword(user_id: number, password: string) {
  return createAxios()
    .put(`users/${user_id}/password`, { password })
    .catch((response: any) => handleRequestError(response));
}

export async function registerUser() {
  const authInfo = useAuthInfo();
  const rankit_user = authInfo.user
  return createAxios()
    .post('users/register', {
      email: rankit_user?.email,
      name: '',
      password: '2ø4tn4¤#T3t34sdfgre#¤53453',
    })
    .catch((response: any) => handleRequestError(response));
}

export async function registerDemoUser(captchaToken: string | null) {
  return createAxios()
    .post('users/register_demo', {
      captcha_token: captchaToken,
    })
    .catch((response: any) => handleRequestError(response));
}
