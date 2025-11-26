import { useEffect, useRef } from 'react';
import { io, Socket } from 'socket.io-client';
import { WS_URL } from '@/utils/constants';

export const useWebSocket = (migrationId: number | null, onProgress?: (data: any) => void) => {
  const socketRef = useRef<Socket | null>(null);

  useEffect(() => {
    if (!migrationId) return;

    const socket = io(WS_URL, {
      transports: ['websocket'],
    });

    socketRef.current = socket;

    socket.on('connect', () => {
      console.log('WebSocket connected');
      socket.emit('subscribe', { migration_id: migrationId });
    });

    socket.on('migration_progress', (data) => {
      onProgress?.(data);
    });

    socket.on('migration_complete', (data) => {
      onProgress?.(data);
    });

    socket.on('migration_error', (data) => {
      console.error('Migration error:', data);
      onProgress?.(data);
    });

    socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    return () => {
      socket.emit('unsubscribe', { migration_id: migrationId });
      socket.disconnect();
    };
  }, [migrationId, onProgress]);

  return socketRef.current;
};



