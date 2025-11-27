import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { ProgressBar } from '@/components/ProgressBar';
import { StatusBadge } from '@/components/StatusBadge';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { useMigrationStore } from '@/store/useMigrationStore';
import { usePolling } from '@/hooks/usePolling';
import { formatDate, formatDuration, formatProgress, formatFileSize } from '@/utils/formatters';
import { migrationService } from '@/services/migrationService';
import toast from 'react-hot-toast';

export const MigrationDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const migrationId = id ? parseInt(id, 10) : null;
  const { currentMigration, fetchMigration, fetchProgress, progress, updateMigration } =
    useMigrationStore();

  useEffect(() => {
    if (migrationId) {
      fetchMigration(migrationId);
    }
  }, [migrationId, fetchMigration]);

  // Polling para atualizar progresso
  usePolling(
    () => {
      if (migrationId && currentMigration?.status === 'in_progress') {
        return fetchProgress(migrationId);
      }
      return Promise.resolve();
    },
    2000,
    currentMigration?.status === 'in_progress'
  );

  const handlePause = async () => {
    if (!migrationId) return;
    try {
      const result = await migrationService.pause(migrationId);
      updateMigration(migrationId, { status: result.status as any });
      toast.success('Migração pausada');
    } catch (_error) {
      toast.error('Erro ao pausar migração');
    }
  };

  const handleResume = async () => {
    if (!migrationId) return;
    try {
      const result = await migrationService.resume(migrationId);
      updateMigration(migrationId, { status: result.status as any });
      toast.success('Migração retomada');
    } catch (_error) {
      toast.error('Erro ao retomar migração');
    }
  };

  const handleCancel = async () => {
    if (!migrationId) return;
    if (!confirm('Deseja realmente cancelar esta migração? O progresso atual será perdido.')) {
      return;
    }
    try {
      await migrationService.delete(migrationId);
      toast.success('Migração cancelada');
      navigate('/history');
    } catch (_error) {
      toast.error('Erro ao cancelar migração');
    }
  };

  if (!currentMigration) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  const displayProgress = progress || {
    migration_id: currentMigration.id,
    status: currentMigration.status,
    total_photos: currentMigration.total_photos,
    migrated_photos: currentMigration.migrated_photos,
    failed_photos: currentMigration.failed_photos,
    progress: formatProgress(currentMigration.migrated_photos, currentMigration.total_photos),
  };

  return (
    <div className="space-y-md sm:space-y-lg">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-sm sm:gap-md">
        <div className="w-full sm:w-auto">
          <Button variant="secondary" onClick={() => navigate('/history')} className="mb-sm sm:mb-0">
            ← Voltar
          </Button>
          <h1 className="text-h2 sm:text-h1 mt-sm sm:mt-md">Detalhes da Migração</h1>
        </div>
        <StatusBadge status={currentMigration.status} />
      </div>

      <Card>
        <h3 className="text-h4 mb-md">Progresso</h3>
        <ProgressBar
          value={displayProgress.migrated_photos}
          max={displayProgress.total_photos}
          showLabel
          color={
            currentMigration.status === 'completed'
              ? 'success'
              : currentMigration.status === 'failed'
              ? 'error'
              : 'primary'
          }
        />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-sm sm:gap-md mt-md sm:mt-lg">
          <div>
            <p className="text-body-xs sm:text-body-sm text-neutral-tertiary mb-xs">Total de fotos</p>
            <p className="text-h5 sm:text-h4 font-semibold">{displayProgress.total_photos}</p>
          </div>
          <div>
            <p className="text-body-xs sm:text-body-sm text-neutral-tertiary mb-xs">Migradas</p>
            <p className="text-h5 sm:text-h4 font-semibold text-success">
              {displayProgress.migrated_photos}
            </p>
          </div>
          <div>
            <p className="text-body-xs sm:text-body-sm text-neutral-tertiary mb-xs">Falhas</p>
            <p className="text-h5 sm:text-h4 font-semibold text-error">
              {displayProgress.failed_photos}
            </p>
          </div>
          <div>
            <p className="text-body-xs sm:text-body-sm text-neutral-tertiary mb-xs">Progresso</p>
            <p className="text-h5 sm:text-h4 font-semibold">{displayProgress.progress}%</p>
          </div>
        </div>
        {displayProgress.current_photo && (
          <div className="mt-sm sm:mt-md p-sm sm:p-md bg-neutral-background rounded">
            <p className="text-body-xs sm:text-body-sm text-neutral-tertiary mb-xs">Foto atual</p>
            <p className="text-body-sm sm:text-body font-semibold break-words">{displayProgress.current_photo}</p>
          </div>
        )}
        {displayProgress.speed_mbps && (
          <div className="mt-sm text-body-xs sm:text-body-sm text-neutral-secondary">
            ⚡ Velocidade: {displayProgress.speed_mbps.toFixed(2)} MB/s
          </div>
        )}
        {displayProgress.estimated_time_remaining_minutes && (
          <div className="mt-sm text-body-xs sm:text-body-sm text-neutral-secondary">
            ⏱️ Tempo restante: ~{Math.round(displayProgress.estimated_time_remaining_minutes)} minutos
          </div>
        )}
      </Card>

      <Card>
        <h3 className="text-h5 sm:text-h4 mb-sm sm:mb-md">Informações</h3>
        <div className="space-y-sm">
          <div className="flex flex-col sm:flex-row sm:justify-between gap-xs sm:gap-0">
            <span className="text-body-sm sm:text-body text-neutral-secondary">Status:</span>
            <StatusBadge status={currentMigration.status} />
          </div>
          {currentMigration.started_at && (
            <div className="flex flex-col sm:flex-row sm:justify-between gap-xs sm:gap-0">
              <span className="text-body-sm sm:text-body text-neutral-secondary">Data de início:</span>
              <span className="text-body-sm sm:text-body break-words">{formatDate(currentMigration.started_at)}</span>
            </div>
          )}
          {currentMigration.completed_at && (
            <div className="flex flex-col sm:flex-row sm:justify-between gap-xs sm:gap-0">
              <span className="text-body-sm sm:text-body text-neutral-secondary">Data de conclusão:</span>
              <span className="text-body-sm sm:text-body break-words">{formatDate(currentMigration.completed_at)}</span>
            </div>
          )}
          {currentMigration.started_at && currentMigration.completed_at && (
            <div className="flex flex-col sm:flex-row sm:justify-between gap-xs sm:gap-0">
              <span className="text-body-sm sm:text-body text-neutral-secondary">Duração:</span>
              <span className="text-body-sm sm:text-body">
                {formatDuration(
                  (new Date(currentMigration.completed_at).getTime() -
                    new Date(currentMigration.started_at).getTime()) /
                    60000
                )}
              </span>
            </div>
          )}
        </div>
      </Card>

      {currentMigration.error_message && (
        <Card>
          <h3 className="text-h5 sm:text-h4 mb-sm sm:mb-md text-error">Erro</h3>
          <div className="p-sm sm:p-md bg-error-light rounded">
            <p className="text-body-sm sm:text-body text-error break-words">{currentMigration.error_message}</p>
          </div>
        </Card>
      )}

      <div className="flex flex-col sm:flex-row gap-sm sm:gap-md">
        {currentMigration.status === 'in_progress' && (
          <>
            <Button variant="secondary" onClick={handlePause} className="w-full sm:w-auto">
              ⏸️ Pausar
            </Button>
            <Button variant="danger" onClick={handleCancel} className="w-full sm:w-auto">
              ❌ Cancelar
            </Button>
          </>
        )}
        {currentMigration.status === 'paused' && (
          <>
            <Button variant="primary" onClick={handleResume} className="w-full sm:w-auto">
              ▶️ Retomar
            </Button>
            <Button variant="danger" onClick={handleCancel} className="w-full sm:w-auto">
              ❌ Cancelar
            </Button>
          </>
        )}
        {currentMigration.status === 'completed' && (
          <Button
            variant="primary"
            onClick={() => window.open('https://drive.google.com', '_blank')}
            className="w-full sm:w-auto"
          >
            Abrir no Google Drive
          </Button>
        )}
      </div>
    </div>
  );
};

