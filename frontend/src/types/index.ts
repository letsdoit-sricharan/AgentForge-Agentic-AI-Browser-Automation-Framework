export type WorkflowStatus = 'QUEUED' | 'RUNNING' | 'COMPLETED' | 'FAILED';

export interface ApiResponse<T = unknown> {
  data: T;
  message?: string;
}

export interface BookingRequest {
  city: string;
  movie: string;
  show_date: string;
  preferred_time?: string;
  preferred_theatre?: string;
  seat_preference?: string;
  ticket_count: number;
}

export interface BookingStatus {
  request_id: string;
  status: WorkflowStatus;
  result?: {
    success: boolean;
    message: string;
    data: Record<string, unknown>;
    error?: string;
  };
  errors: string[];
}

export interface Plugin {
  id: string;
  name: string;
  description: string;
  isActive: boolean;
  version?: string;
}

export interface PlatformStats {
  registeredPlugins: number;
  runningExecutions: number;
  completedToday: number;
  failedExecutions: number;
}

export interface ExecutionRecord {
  id: string;
  plugin: string;
  status: WorkflowStatus;
  startedAt: string;
  completedAt?: string;
  duration?: string;
  currentStep?: string;
  result?: {
    success: boolean;
    message: string;
    data?: Record<string, unknown>;
  };
  error?: string;
}
