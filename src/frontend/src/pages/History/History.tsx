import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { StatusBadge } from '@/components/StatusBadge';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { useMigrationStore } from '@/store/useMigrationStore';
import { formatDate, formatDuration, formatProgress } from '@/utils/formatters';

export const History: React.FC = () => {
  const navigate = useNavigate();
  const { migrations, fetchMigrations, isLoading } = useMigrationStore();

  useEffect(() => {
    fetchMigrations();
  }, [fetchMigrations]);

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
        <h1 className="text-h2 sm:text-h1 mb-sm sm:mb-md">Histórico de Migrações</h1>
        <p className="text-body-sm sm:text-body text-neutral-secondary">
          Visualize todas as migrações realizadas
        </p>
      </div>

      {migrations.length === 0 ? (
        <Card>
          <div className="text-center py-2xl">
            <p className="text-body-lg text-neutral-secondary mb-md">
              Nenhuma migração encontrada
            </p>
            <Button variant="primary" onClick={() => navigate('/')}>
              Iniciar Primeira Migração
            </Button>
          </div>
        </Card>
      ) : (
        <div className="space-y-md">
          {migrations.map((migration) => (
            <Card key={migration.id}>
              <div className="flex flex-col sm:flex-row items-start justify-between gap-md">
                <div className="flex-1 w-full min-w-0">
                  <div className="flex flex-wrap items-center gap-sm sm:gap-md mb-sm">
                    <StatusBadge status={migration.status} />
                    <span className="text-body-xs sm:text-body-sm text-neutral-tertiary">
                      {formatDate(migration.created_at)}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-sm sm:gap-md mt-sm sm:mt-md">
                    <div>
                      <p className="text-body-xs sm:text-body-sm text-neutral-tertiary mb-xs">Total de fotos</p>
                      <p className="text-h5 sm:text-h4 font-semibold">{migration.total_photos}</p>
                    </div>
                    <div>
                      <p className="text-body-xs sm:text-body-sm text-neutral-tertiary mb-xs">Migradas</p>
                      <p className="text-h5 sm:text-h4 font-semibold text-success">
                        {migration.migrated_photos}
                      </p>
                    </div>
                    <div>
                      <p className="text-body-xs sm:text-body-sm text-neutral-tertiary mb-xs">Falhas</p>
                      <p className="text-h5 sm:text-h4 font-semibold text-error">
                        {migration.failed_photos}
                      </p>
                    </div>
                    <div>
                      <p className="text-body-xs sm:text-body-sm text-neutral-tertiary mb-xs">Progresso</p>
                      <p className="text-h5 sm:text-h4 font-semibold">
                        {formatProgress(migration.migrated_photos, migration.total_photos)}%
                      </p>
                    </div>
                  </div>
                  {migration.started_at && migration.completed_at && (
                    <p className="text-body-xs sm:text-body-sm text-neutral-tertiary mt-sm sm:mt-md">
                      ⏱️ Duração: {formatDuration(
                        (new Date(migration.completed_at).getTime() -
                          new Date(migration.started_at).getTime()) /
                          60000
                      )}
                    </p>
                  )}
                  {migration.error_message && (
                    <div className="mt-sm sm:mt-md p-sm sm:p-md bg-error-light rounded">
                      <p className="text-body-xs sm:text-body-sm text-error break-words">
                        ❌ Erro: {migration.error_message}
                      </p>
                    </div>
                  )}
                </div>
                <div className="w-full sm:w-auto sm:ml-lg">
                  <Button
                    variant="secondary"
                    onClick={() => navigate(`/migrations/${migration.id}`)}
                    className="w-full sm:w-auto"
                  >
                    Ver Detalhes
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

