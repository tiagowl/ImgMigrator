import React from 'react';
import { cn } from '@/utils/cn';

export interface ProgressBarProps {
  value: number;
  max?: number;
  showLabel?: boolean;
  className?: string;
  color?: 'primary' | 'success' | 'warning' | 'error';
}

const colorClasses = {
  primary: 'bg-primary',
  success: 'bg-success',
  warning: 'bg-warning',
  error: 'bg-error',
};

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  showLabel = true,
  className,
  color = 'primary',
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  return (
    <div className={cn('w-full', className)}>
      <div className="w-full h-2 bg-neutral-background rounded-full overflow-hidden">
        <div
          className={cn('h-full transition-all duration-500 ease-in-out', colorClasses[color])}
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={value}
          aria-valuemin={0}
          aria-valuemax={max}
        />
      </div>
      {showLabel && (
        <p className="mt-sm text-body-sm text-neutral-secondary">{Math.round(percentage)}%</p>
      )}
    </div>
  );
};

