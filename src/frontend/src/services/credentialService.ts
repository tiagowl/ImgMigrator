import { api } from './api';
import { API_ENDPOINTS } from '@/utils/constants';
import type { Credential, CredentialFormData } from '@/types';

export const credentialService = {
  async list(): Promise<{ credentials: Credential[] }> {
    const response = await api.get<{ credentials: Credential[] }>(API_ENDPOINTS.CREDENTIALS.LIST);
    return response.data;
  },

  async create(data: CredentialFormData): Promise<Credential> {
    try {
      const response = await api.post<Credential>(API_ENDPOINTS.CREDENTIALS.CREATE, data);
      return response.data;
    } catch (error: any) {
      // Re-throw with more context
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw error;
    }
  },

  async delete(id: number): Promise<{ success: boolean; message: string }> {
    const response = await api.delete<{ success: boolean; message: string }>(
      `${API_ENDPOINTS.CREDENTIALS.DELETE}/${id}`
    );
    return response.data;
  },

  async verifyGoogleConnection(): Promise<{
    connected: boolean;
    status: string;
    message: string;
    storage_quota?: any;
  }> {
    const response = await api.get<{
      connected: boolean;
      status: string;
      message: string;
      storage_quota?: any;
    }>(API_ENDPOINTS.CREDENTIALS.VERIFY_GOOGLE);
    return response.data;
  },
};


