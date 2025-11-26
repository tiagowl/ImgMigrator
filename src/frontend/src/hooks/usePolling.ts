import { useEffect, useRef } from 'react';

export const usePolling = <T>(
  callback: () => Promise<T>,
  interval: number = 2000,
  enabled: boolean = true
) => {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!enabled) return;

    const poll = async () => {
      try {
        await callback();
      } catch (error) {
        console.error('Polling error:', error);
      }
    };

    // Executar imediatamente
    poll();

    // Configurar intervalo
    intervalRef.current = setInterval(poll, interval);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [callback, interval, enabled]);
};






