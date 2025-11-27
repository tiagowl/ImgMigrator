import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { useCredentialStore } from '@/store/useCredentialStore';
import { credentialService } from '@/services/credentialService';
import { authService } from '@/services/authService';
import toast from 'react-hot-toast';

const icloudSchema = z.object({
  apple_id: z.string().email('Email inválido'),
  password: z.string().min(1, 'Senha é obrigatória'),
});

type ICloudFormData = z.infer<typeof icloudSchema>;

export const Settings: React.FC = () => {
  const { credentials, fetchCredentials, removeCredential, isLoading } = useCredentialStore();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ICloudFormData>({
    resolver: zodResolver(icloudSchema),
  });

  const googleCredential = credentials.find((c) => c.service_type === 'google_drive');
  const icloudCredential = credentials.find((c) => c.service_type === 'icloud');

  useEffect(() => {
    fetchCredentials();
    
    // Check for OAuth callback in URL
    const urlParams = new URLSearchParams(window.location.search);
    const oauthStatus = urlParams.get('oauth');
    const service = urlParams.get('service');
    const errorMessage = urlParams.get('message');
    
    if (oauthStatus === 'success' && service === 'google_drive') {
      toast.success('Google Drive conectado com sucesso!');
      fetchCredentials();
      // Clean URL
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (oauthStatus === 'error' && service === 'google_drive') {
      const message = errorMessage || 'Erro ao conectar Google Drive. Tente novamente.';
      toast.error(message);
      // Clean URL
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [fetchCredentials]);

  const handleConnectGoogle = async () => {
    try {
      const { auth_url } = await authService.initGoogleOAuth();
      // Redirect directly to Google OAuth
      window.location.href = auth_url;
    } catch (_error) {
      toast.error('Erro ao iniciar autenticação do Google');
    }
  };

  const handleDisconnectGoogle = async () => {
    if (!googleCredential) return;

    if (!confirm('Deseja realmente desconectar sua conta Google Drive?')) {
      return;
    }

    try {
      await credentialService.delete(googleCredential.id);
      removeCredential(googleCredential.id);
      toast.success('Google Drive desconectado com sucesso');
    } catch (_error) {
      toast.error('Erro ao desconectar Google Drive');
    }
  };

  const handleRemoveICloud = async () => {
    if (!icloudCredential) return;

    if (!confirm('Deseja realmente remover as credenciais do iCloud?')) {
      return;
    }

    try {
      await credentialService.delete(icloudCredential.id);
      removeCredential(icloudCredential.id);
      reset();
      toast.success('Credenciais do iCloud removidas com sucesso');
    } catch (_error) {
      toast.error('Erro ao remover credenciais');
    }
  };

  const onSubmitICloud = async (data: ICloudFormData) => {
    setIsSubmitting(true);
    try {
      // Validate before submitting
      if (!data.apple_id || !data.password) {
        toast.error('Por favor, preencha todos os campos');
        setIsSubmitting(false);
        return;
      }

      if (!data.apple_id.includes('@') || !data.apple_id.includes('.')) {
        toast.error('Por favor, insira um email válido');
        setIsSubmitting(false);
        return;
      }

      await credentialService.create({
        service_type: 'icloud',
        apple_id: data.apple_id,
        password: data.password,
      });
      await fetchCredentials();
      reset();
      toast.success('Credenciais do iCloud configuradas e criptografadas com sucesso!');
    } catch (error: any) {
      // Extract error message from response
      const errorMessage = error?.response?.data?.detail || 
                          error?.message || 
                          'Erro ao configurar credenciais do iCloud. Verifique os dados e tente novamente.';
      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-md sm:space-y-lg">
      <div>
        <h1 className="text-h2 sm:text-h1 mb-sm sm:mb-md">Configurações</h1>
        <p className="text-body-sm sm:text-body text-neutral-secondary">
          Gerencie suas credenciais e configurações de migração
        </p>
      </div>

      {/* Google Drive */}
      <Card>
        <h3 className="text-h4 mb-md">Google Drive</h3>
        {googleCredential ? (
          <div className="space-y-md">
            <div className="p-sm sm:p-md bg-success-light rounded">
              <p className="text-body-sm sm:text-body font-semibold text-success mb-xs sm:mb-sm">
                ✅ Google Drive Conectado
              </p>
              <p className="text-body-xs sm:text-body-sm text-neutral-secondary">
                Sua conta Google Drive está conectada e pronta para uso.
              </p>
            </div>
            <Button variant="danger" onClick={handleDisconnectGoogle} className="w-full sm:w-auto">
              Desconectar Google Drive
            </Button>
          </div>
        ) : (
          <div className="space-y-sm sm:space-y-md">
            <p className="text-body-sm sm:text-body text-neutral-secondary">
              Conecte sua conta Google Drive para permitir o upload de fotos.
            </p>
            <Button variant="primary" onClick={handleConnectGoogle} className="w-full sm:w-auto">
              Conectar Google Drive
            </Button>
          </div>
        )}
      </Card>

      {/* iCloud */}
      <Card>
        <h3 className="text-h4 mb-md">iCloud</h3>
        {icloudCredential ? (
          <div className="space-y-md">
            <div className="p-sm sm:p-md bg-success-light rounded">
              <p className="text-body-sm sm:text-body font-semibold text-success mb-xs sm:mb-sm">
                ✅ iCloud Configurado
              </p>
              <p className="text-body-xs sm:text-body-sm text-neutral-secondary">
                Suas credenciais do iCloud estão configuradas e criptografadas com segurança.
              </p>
            </div>
            <div className="p-sm sm:p-md bg-neutral-background rounded">
              <p className="text-body-xs sm:text-body-sm text-neutral-secondary mb-xs sm:mb-sm">
                🔒 Segurança
              </p>
              <ul className="text-body-xs sm:text-body-sm text-neutral-secondary space-y-xs list-disc list-inside">
                <li>Criptografia AES-256</li>
                <li>Credenciais nunca expostas</li>
                <li>Conformidade com LGPD</li>
              </ul>
            </div>
            <Button variant="danger" onClick={handleRemoveICloud} className="w-full sm:w-auto">
              Remover Credenciais
            </Button>
          </div>
        ) : (
          <form onSubmit={handleSubmit(onSubmitICloud)} className="space-y-sm sm:space-y-md">
            <div className="p-sm sm:p-md bg-primary-light rounded mb-sm sm:mb-md">
              <p className="text-body-xs sm:text-body-sm text-neutral-secondary">
                ℹ️ Suas credenciais são criptografadas e armazenadas com segurança.
              </p>
            </div>
            <Input
              label="Apple ID (Email)"
              type="email"
              placeholder="usuario@icloud.com"
              error={errors.apple_id?.message}
              {...register('apple_id')}
            />
            <div className="relative">
              <Input
                label="Senha"
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••"
                error={errors.password?.message}
                {...register('password')}
              />
              <button
                type="button"
                className="absolute right-md top-[38px] text-neutral-tertiary hover:text-neutral-primary"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            <div className="p-sm sm:p-md bg-warning-light rounded">
              <p className="text-body-xs sm:text-body-sm text-neutral-secondary mb-xs sm:mb-sm">
                ⚠️ Conta com 2FA?
              </p>
              <p className="text-body-xs sm:text-body-sm text-neutral-secondary">
                Se sua conta usa autenticação de dois fatores, você precisará gerar uma senha de
                app específica nas configurações da Apple.
              </p>
            </div>
            <Button variant="primary" type="submit" isLoading={isSubmitting} className="w-full sm:w-auto">
              Salvar e Validar
            </Button>
          </form>
        )}
      </Card>
    </div>
  );
};

