import { api } from './api';
import { API_ENDPOINTS } from '@/utils/constants';
import type { User } from '@/types';

export const authService = {
  async register(email: string): Promise<User> {
    const response = await api.post<User>(API_ENDPOINTS.AUTH.REGISTER, { email });
    return response.data;
  },

  async initGoogleOAuth(userId: number = 1): Promise<{ auth_url: string; state: string; user_id: number }> {
    const response = await api.get<{ auth_url: string; state: string; user_id: number }>(
      API_ENDPOINTS.AUTH.OAUTH_GOOGLE_INIT,
      { params: { user_id: userId } }
    );
    return response.data;
  },

  async handleGoogleCallback(code: string, state?: string): Promise<{ success: boolean; message: string }> {
    const response = await api.get<{ success: boolean; message: string }>(
      API_ENDPOINTS.AUTH.OAUTH_GOOGLE_CALLBACK,
      { params: { code, state } }
    );
    return response.data;
  },
};


