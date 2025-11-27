import { create } from 'zustand';
import type { Credential } from '@/types';
import { credentialService } from '@/services/credentialService';

interface CredentialState {
  credentials: Credential[];
  isLoading: boolean;
  error: string | null;
  fetchCredentials: () => Promise<void>;
  addCredential: (credential: Credential) => void;
  removeCredential: (id: number) => void;
  clearError: () => void;
}

export const useCredentialStore = create<CredentialState>((set: (partial: Partial<CredentialState> | ((state: CredentialState) => Partial<CredentialState>)) => void) => ({
  credentials: [],
  isLoading: false,
  error: null,

  fetchCredentials: async () => {
    set({ isLoading: true, error: null });
    try {
      const { credentials } = await credentialService.list();
      set({ credentials, isLoading: false });
    } catch (_error) {
      set({ error: 'Erro ao carregar credenciais', isLoading: false });
    }
  },

  addCredential: (credential: Credential) => {
    set((state: CredentialState) => ({
      credentials: [...state.credentials, credential],
    }));
  },

  removeCredential: (id: number) => {
    set((state: CredentialState) => ({
      credentials: state.credentials.filter((c: Credential) => c.id !== id),
    }));
  },

  clearError: () => set({ error: null }),
}));

