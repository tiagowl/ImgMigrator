export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface Credential {
  id: number;
  user_id: number;
  service_type: 'icloud' | 'google_drive';
  status: 'configured' | 'connected' | 'not_configured';
  created_at: string;
  updated_at?: string;
}

export interface Migration {
  id: number;
  user_id: number;
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'paused';
  total_photos: number;
  migrated_photos: number;
  failed_photos: number;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
  created_at: string;
}

export interface MigrationProgress {
  migration_id: number;
  status: Migration['status'];
  total_photos: number;
  migrated_photos: number;
  failed_photos: number;
  progress: number;
  current_photo?: string;
  speed_mbps?: number;
  estimated_time_remaining_minutes?: number;
}

export interface MigrationLog {
  id: number;
  migration_id: number;
  photo_name: string;
  photo_path?: string;
  status: 'pending' | 'downloading' | 'uploading' | 'completed' | 'failed';
  error_message?: string;
  file_size?: number;
  checksum?: string;
  timestamp: string;
}

export interface CredentialFormData {
  service_type: 'icloud' | 'google_drive';
  apple_id?: string;
  password?: string;
}

export interface MigrationOptions {
  preserve_structure?: boolean;
  skip_duplicates?: boolean;
}



