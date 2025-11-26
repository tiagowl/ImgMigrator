export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

export const API_ENDPOINTS = {
  AUTH: {
    REGISTER: '/api/v1/auth/register',
    OAUTH_GOOGLE_INIT: '/api/v1/auth/oauth/google/init',
    OAUTH_GOOGLE_CALLBACK: '/api/v1/auth/oauth/google/callback',
  },
  CREDENTIALS: {
    LIST: '/api/v1/credentials',
    CREATE: '/api/v1/credentials',
    DELETE: '/api/v1/credentials',
    VERIFY_GOOGLE: '/api/v1/credentials/google/verify',
  },
  MIGRATIONS: {
    LIST: '/api/v1/migrations',
    CREATE: '/api/v1/migrations',
    GET: (id: number) => `/api/v1/migrations/${id}`,
    PROGRESS: (id: number) => `/api/v1/migrations/${id}/progress`,
    PAUSE: (id: number) => `/api/v1/migrations/${id}/pause`,
    RESUME: (id: number) => `/api/v1/migrations/${id}/resume`,
    DELETE: (id: number) => `/api/v1/migrations/${id}`,
  },
} as const;

export const MIGRATION_STATUS_COLORS = {
  pending: 'text-neutral-tertiary',
  in_progress: 'text-warning',
  completed: 'text-success',
  failed: 'text-error',
  paused: 'text-neutral-secondary',
} as const;

export const MIGRATION_STATUS_LABELS = {
  pending: 'Pendente',
  in_progress: 'Em Progresso',
  completed: 'Concluída',
  failed: 'Falhou',
  paused: 'Pausada',
} as const;

