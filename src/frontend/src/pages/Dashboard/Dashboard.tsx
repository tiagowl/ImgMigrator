import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { ProgressBar } from '@/components/ProgressBar';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { StatusBadge } from '@/components/StatusBadge';
import { useCredentialStore } from '@/store/useCredentialStore';
import { useMigrationStore } from '@/store/useMigrationStore';
import { migrationService } from '@/services/migrationService';
import { authService } from '@/services/authService';
import { formatProgress, formatFileSize, formatDuration } from '@/utils/formatters';
import toast from 'react-hot-toast';
import type { MigrationOptions } from '@/types';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { credentials, fetchCredentials, isLoading: credentialsLoading } = useCredentialStore();
  const { migrations, fetchMigrations, addMigration, isLoading: migrationsLoading } = useMigrationStore();
  const [isStartingMigration, setIsStartingMigration] = useState(false);

  const googleCredential = credentials.find((c) => c.service_type === 'google_drive');
  const icloudCredential = credentials.find((c) => c.service_type === 'icloud');
  const activeMigration = migrations.find((m) => m.status === 'in_progress' || m.status === 'pending');

  useEffect(() => {
    fetchCredentials();
    fetchMigrations();
    
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
  }, [fetchCredentials, fetchMigrations]);


  const handleConnectGoogle = async () => {
    try {
      const { auth_url } = await authService.initGoogleOAuth();
      // Redirect directly to Google OAuth
      window.location.href = auth_url;
    } catch (error) {
      toast.error('Erro ao iniciar autenticação do Google');
    }
  };

  const handleStartMigration = async () => {
    if (!googleCredential || !icloudCredential) {
      toast.error('Configure as credenciais antes de iniciar a migração');
      return;
    }

    setIsStartingMigration(true);
    try {
      const options: MigrationOptions = {
        preserve_structure: true,
        skip_duplicates: true,
      };
      const migration = await migrationService.create(options);
      addMigration(migration);
      toast.success('Migração iniciada com sucesso!');
    } catch (error) {
      toast.error('Erro ao iniciar migração');
    } finally {
      setIsStartingMigration(false);
    }
  };

  if (credentialsLoading || migrationsLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-md sm:space-y-lg">
      <div>
        <h1 className="text-h2 sm:text-h1 mb-sm sm:mb-md">Dashboard</h1>
        <p className="text-body-sm sm:text-body text-neutral-secondary">
          Configure suas credenciais e inicie a migração de fotos do iCloud para Google Drive
        </p>
      </div>

      {/* Aviso de Status de Conexão Google */}
      {googleCredential && (
        <div
          className={`p-sm sm:p-md rounded ${
            googleCredential.status === 'connected'
              ? 'bg-success-light border border-success'
              : googleCredential.status === 'expired'
              ? 'bg-warning-light border border-warning'
              : 'bg-error-light border border-error'
          }`}
        >
          <div className="flex items-start sm:items-center gap-sm sm:gap-md">
            {googleCredential.status === 'connected' ? (
              <>
                <span className="text-xl sm:text-2xl flex-shrink-0">✅</span>
                <div className="min-w-0 flex-1">
                  <p className="text-body-sm sm:text-body font-semibold text-success">
                    Google Drive Conectado
                  </p>
                  <p className="text-body-xs sm:text-body-sm text-neutral-secondary">
                    Sua conta Google Drive está conectada e pronta para uso.
                  </p>
                </div>
              </>
            ) : googleCredential.status === 'expired' ? (
              <>
                <span className="text-xl sm:text-2xl flex-shrink-0">⚠️</span>
                <div className="min-w-0 flex-1">
                  <p className="text-body-sm sm:text-body font-semibold text-warning">
                    Conexão Expirada
                  </p>
                  <p className="text-body-xs sm:text-body-sm text-neutral-secondary">
                    Sua conexão com o Google Drive expirou. Reconecte para continuar.
                  </p>
                </div>
              </>
            ) : (
              <>
                <span className="text-xl sm:text-2xl flex-shrink-0">❌</span>
                <div className="min-w-0 flex-1">
                  <p className="text-body-sm sm:text-body font-semibold text-error">
                    Erro na Conexão
                  </p>
                  <p className="text-body-xs sm:text-body-sm text-neutral-secondary">
                    Houve um problema com sua conexão Google Drive. Tente reconectar.
                  </p>
                </div>
              </>
            )}
          </div>
        </div>
      )}

      {/* Status das Credenciais */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-md sm:gap-lg">
        <Card>
          <div className="flex items-center justify-between mb-sm sm:mb-md">
            <h3 className="text-h5 sm:text-h4">Google Drive</h3>
            {googleCredential?.status === 'connected' ? (
              <span className="text-success text-body-xs sm:text-body">✅ Conectado</span>
            ) : googleCredential?.status === 'expired' ? (
              <span className="text-warning text-body-xs sm:text-body">⚠️ Expirado</span>
            ) : googleCredential?.status === 'error' ? (
              <span className="text-error text-body-xs sm:text-body">❌ Erro</span>
            ) : (
              <span className="text-neutral-tertiary text-body-xs sm:text-body">⚪ Não conectado</span>
            )}
          </div>
          {googleCredential ? (
            <div className="space-y-sm sm:space-y-md">
              <p className="text-body-sm sm:text-body text-neutral-secondary">
                Status: {googleCredential.status === 'connected' ? 'Conectado' : googleCredential.status === 'expired' ? 'Expirado' : 'Erro'}
              </p>
              <div className="flex flex-col sm:flex-row gap-sm sm:gap-md">
                <Button variant="secondary" onClick={() => navigate('/settings')} className="w-full sm:w-auto">
                  Gerenciar
                </Button>
                {(googleCredential.status === 'expired' || googleCredential.status === 'error') && (
                  <Button variant="primary" onClick={handleConnectGoogle} className="w-full sm:w-auto">
                    Reconectar
                  </Button>
                )}
              </div>
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

        <Card>
          <div className="flex items-center justify-between mb-sm sm:mb-md">
            <h3 className="text-h5 sm:text-h4">iCloud</h3>
            {icloudCredential?.status === 'configured' ? (
              <span className="text-success text-body-xs sm:text-body">✅ Configurado</span>
            ) : (
              <span className="text-neutral-tertiary text-body-xs sm:text-body">⚪ Não configurado</span>
            )}
          </div>
          {icloudCredential ? (
            <div className="space-y-sm sm:space-y-md">
              <p className="text-body-sm sm:text-body text-neutral-secondary">
                Credenciais configuradas
              </p>
              <Button variant="secondary" onClick={() => navigate('/settings')} className="w-full sm:w-auto">
                Gerenciar
              </Button>
            </div>
          ) : (
            <Button variant="primary" onClick={() => navigate('/settings')} className="w-full sm:w-auto">
              Configurar iCloud
            </Button>
          )}
        </Card>
      </div>

      {/* Migração Ativa */}
      {activeMigration && (
        <Card>
          <div className="mb-md">
            <div className="flex items-center justify-between mb-sm">
              <h3 className="text-h4">Migração em Andamento</h3>
              <StatusBadge status={activeMigration.status} />
            </div>
            <ProgressBar
              value={activeMigration.migrated_photos}
              max={activeMigration.total_photos}
              showLabel
              color={activeMigration.status === 'in_progress' ? 'primary' : 'warning'}
            />
            <div className="mt-md grid grid-cols-2 md:grid-cols-4 gap-sm sm:gap-md text-body-xs sm:text-body-sm">
              <div>
                <p className="text-neutral-tertiary mb-xs">Fotos migradas</p>
                <p className="text-h5 sm:text-h4 font-semibold">
                  {activeMigration.migrated_photos} / {activeMigration.total_photos}
                </p>
              </div>
              <div>
                <p className="text-neutral-tertiary mb-xs">Progresso</p>
                <p className="text-h5 sm:text-h4 font-semibold">
                  {formatProgress(activeMigration.migrated_photos, activeMigration.total_photos)}%
                </p>
              </div>
              <div>
                <p className="text-neutral-tertiary mb-xs">Falhas</p>
                <p className="text-h5 sm:text-h4 font-semibold text-error">
                  {activeMigration.failed_photos}
                </p>
              </div>
              <div className="col-span-2 md:col-span-1">
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => navigate(`/migrations/${activeMigration.id}`)}
                  className="w-full sm:w-auto"
                >
                  Ver Detalhes
                </Button>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Iniciar Nova Migração */}
      {!activeMigration && googleCredential && icloudCredential && (
        <Card>
          <h3 className="text-h4 mb-md">Iniciar Nova Migração</h3>
          <p className="text-body text-neutral-secondary mb-lg">
            Todas as suas fotos do iCloud serão migradas para o Google Drive, mantendo a estrutura
            de pastas original.
          </p>
          <Button
            variant="primary"
            size="lg"
            onClick={handleStartMigration}
            isLoading={isStartingMigration}
          >
            Iniciar Migração
          </Button>
        </Card>
      )}

      {/* Migrações Recentes */}
      {migrations.length > 0 && (
        <Card>
          <h3 className="text-h4 mb-md">Migrações Recentes</h3>
          <div className="space-y-md">
            {migrations.slice(0, 5).map((migration) => (
              <div
                key={migration.id}
                className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-sm sm:p-md bg-neutral-background rounded hover:bg-opacity-80 cursor-pointer gap-sm sm:gap-md"
                onClick={() => navigate(`/migrations/${migration.id}`)}
              >
                <div className="flex items-center gap-sm sm:gap-md flex-1 min-w-0">
                  <StatusBadge status={migration.status} />
                  <div className="min-w-0 flex-1">
                    <p className="text-body-sm sm:text-body font-semibold truncate">
                      {migration.migrated_photos} de {migration.total_photos} fotos
                    </p>
                    <p className="text-body-xs sm:text-body-sm text-neutral-tertiary">
                      {new Date(migration.created_at).toLocaleDateString('pt-BR')}
                    </p>
                  </div>
                </div>
                <Button variant="secondary" size="sm" className="w-full sm:w-auto">
                  Ver Detalhes
                </Button>
              </div>
            ))}
          </div>
          {migrations.length > 5 && (
            <div className="mt-md">
              <Button variant="secondary" onClick={() => navigate('/history')}>
                Ver Todas as Migrações
              </Button>
            </div>
          )}
        </Card>
      )}
    </div>
  );
};

