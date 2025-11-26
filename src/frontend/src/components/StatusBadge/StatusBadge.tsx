import React from 'react';
import { cn } from '@/utils/cn';
import { MIGRATION_STATUS_COLORS, MIGRATION_STATUS_LABELS } from '@/utils/constants';
import type { Migration } from '@/types';

export interface StatusBadgeProps {
  status: Migration['status'];
  className?: string;
}

const statusIcons = {
  pending: '⏳',
  in_progress: '🔄',
  completed: '✅',
  failed: '❌',
  paused: '⏸️',
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, className }) => {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-sm px-md py-sm rounded text-body-sm font-semibold',
        MIGRATION_STATUS_COLORS[status],
        'bg-opacity-10',
        className
      )}
    >
      <span>{statusIcons[status]}</span>
      <span>{MIGRATION_STATUS_LABELS[status]}</span>
    </span>
  );
};

