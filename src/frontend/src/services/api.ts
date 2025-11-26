import axios, { AxiosInstance, AxiosError } from 'axios';
import { API_BASE_URL } from '@/utils/constants';
import toast from 'react-hot-toast';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        // Adicionar token se existir
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response) {
          const status = error.response.status;
          const data = error.response.data as { detail?: string; message?: string };

          switch (status) {
            case 401:
              // Token inválido ou expirado
              localStorage.removeItem('token');
              window.location.href = '/';
              toast.error('Sessão expirada. Por favor, faça login novamente.');
              break;
            case 403:
              toast.error('Você não tem permissão para esta ação.');
              break;
            case 404:
              toast.error('Recurso não encontrado.');
              break;
            case 500:
              toast.error('Erro interno do servidor. Tente novamente mais tarde.');
              break;
            default:
              const message = data?.detail || data?.message || 'Erro ao processar requisição.';
              toast.error(message);
          }
        } else if (error.request) {
          toast.error('Erro de conexão. Verifique sua internet.');
        } else {
          toast.error('Erro inesperado. Tente novamente.');
        }

        return Promise.reject(error);
      }
    );
  }

  get instance(): AxiosInstance {
    return this.api;
  }
}

export const apiService = new ApiService();
export const api = apiService.instance;



