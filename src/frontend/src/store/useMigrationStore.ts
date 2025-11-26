import { create } from 'zustand';
import type { Migration, MigrationProgress } from '@/types';
import { migrationService } from '@/services/migrationService';

interface MigrationState {
  migrations: Migration[];
  currentMigration: Migration | null;
  progress: MigrationProgress | null;
  isLoading: boolean;
  error: string | null;
  fetchMigrations: (params?: { status?: string; page?: number; limit?: number }) => Promise<void>;
  fetchMigration: (id: number) => Promise<void>;
  fetchProgress: (id: number) => Promise<void>;
  addMigration: (migration: Migration) => void;
  updateMigration: (id: number, updates: Partial<Migration>) => void;
  setProgress: (progress: MigrationProgress | null) => void;
  clearError: () => void;
}

export const useMigrationStore = create<MigrationState>((set: (partial: Partial<MigrationState> | ((state: MigrationState) => Partial<MigrationState>)) => void) => ({
  migrations: [],
  currentMigration: null,
  progress: null,
  isLoading: false,
  error: null,

  fetchMigrations: async (params) => {
    set({ isLoading: true, error: null });
    try {
      const data = await migrationService.list(params);
      set({ migrations: data.migrations, isLoading: false });
    } catch (error) {
      set({ error: 'Erro ao carregar migrações', isLoading: false });
    }
  },

  fetchMigration: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const migration = await migrationService.get(id);
      set({ currentMigration: migration, isLoading: false });
    } catch (error) {
      set({ error: 'Erro ao carregar migração', isLoading: false });
    }
  },

  fetchProgress: async (id) => {
    try {
      const progress = await migrationService.getProgress(id);
      set({ progress });
    } catch (error) {
      // Silenciar erro de progresso para não poluir a UI
    }
  },

  addMigration: (migration) => {
    set((state) => ({
      migrations: [migration, ...state.migrations],
    }));
  },

  updateMigration: (id, updates) => {
    set((state) => ({
      migrations: state.migrations.map((m) =>
        m.id === id ? { ...m, ...updates } : m
      ),
      currentMigration:
        state.currentMigration?.id === id
          ? { ...state.currentMigration, ...updates }
          : state.currentMigration,
    }));
  },

  setProgress: (progress) => {
    set({ progress });
  },

  clearError: () => set({ error: null }),
}));

