import { api } from './api';
import { API_ENDPOINTS } from '@/utils/constants';
import type { Migration, MigrationProgress, MigrationOptions } from '@/types';

export const migrationService = {
  async list(params?: { status?: string; page?: number; limit?: number }): Promise<{
    migrations: Migration[];
    total: number;
    page: number;
    limit: number;
  }> {
    const response = await api.get<{
      migrations: Migration[];
      total: number;
      page: number;
      limit: number;
    }>(API_ENDPOINTS.MIGRATIONS.LIST, { params });
    return response.data;
  },

  async create(options?: MigrationOptions): Promise<Migration> {
    const response = await api.post<Migration>(API_ENDPOINTS.MIGRATIONS.CREATE, { options });
    return response.data;
  },

  async get(id: number): Promise<Migration> {
    const response = await api.get<Migration>(API_ENDPOINTS.MIGRATIONS.GET(id));
    return response.data;
  },

  async getProgress(id: number): Promise<MigrationProgress> {
    const response = await api.get<MigrationProgress>(API_ENDPOINTS.MIGRATIONS.PROGRESS(id));
    return response.data;
  },

  async pause(id: number): Promise<{ success: boolean; status: string }> {
    const response = await api.post<{ success: boolean; status: string }>(
      API_ENDPOINTS.MIGRATIONS.PAUSE(id)
    );
    return response.data;
  },

  async resume(id: number): Promise<{ success: boolean; status: string }> {
    const response = await api.post<{ success: boolean; status: string }>(
      API_ENDPOINTS.MIGRATIONS.RESUME(id)
    );
    return response.data;
  },

  async delete(id: number): Promise<{ success: boolean; message: string }> {
    const response = await api.delete<{ success: boolean; message: string }>(
      API_ENDPOINTS.MIGRATIONS.DELETE(id)
    );
    return response.data;
  },
};






