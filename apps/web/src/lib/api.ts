"use client";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8007";

export type LoginResponse = {
  access_token: string;
  token_type: string;
  expires_at: string;
  user: {
    user_id: string;
    employee_id: string;
    name: string;
    email: string;
    org_id: string;
    tenant_slug: string;
    department_id?: string | null;
    team_id?: string | null;
    roles: string[];
    permissions: string[];
    employment_status: string;
  };
  available_routes: string[];
  sso_launch_url?: string | null;
};

export type AttendanceCalendarDay = {
  date: string;
  day_label: string;
  attendance_status: string;
  total_hours?: number | null;
  check_in_at?: string | null;
  check_out_at?: string | null;
  leave_type?: string | null;
  leave_status?: string | null;
  holiday_name?: string | null;
  is_weekend: boolean;
  geofence_passed?: boolean | null;
  location_label?: string | null;
  notes?: string | null;
};

export type NotificationItem = {
  notification_id: string;
  title: string;
  message: string;
  severity: string;
  tags: string[];
  action_url?: string | null;
  created_at: string;
  is_read: boolean;
};

export type DashboardResponse = {
  month: string;
  employee: {
    employee_id: string;
    full_name: string;
    work_email: string;
    department_id: string;
    position_id: string;
    role: string;
    employment_status: string;
    manager_id?: string | null;
  };
  summary: {
    present_days: number;
    remote_days: number;
    leave_days: number;
    holiday_days: number;
    absent_days: number;
    average_hours: number;
  };
  calendar: AttendanceCalendarDay[];
  leave_balances: Array<{
    leave_type: string;
    allocated_days: number;
    used_days: number;
    pending_days: number;
    available_days: number;
  }>;
  alerts: NotificationItem[];
};

export type AssistantResponse = {
  answer: string;
  strategy: string;
  intent: string;
  citations: Array<{
    title: string;
    source: string;
    snippet: string;
  }>;
  follow_up_actions: string[];
};

const SESSION_STORAGE_KEY = "nexushr.session";

export function buildApiUrl(path: string): string {
  return `${API_BASE_URL}${path}`;
}

export function buildWebSocketUrl(path: string): string {
  return API_BASE_URL.replace(/^http/, "ws") + path;
}

export function persistSession(payload: LoginResponse): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(payload));
}

export function readSession(): LoginResponse | null {
  if (typeof window === "undefined") {
    return null;
  }
  const rawValue = window.localStorage.getItem(SESSION_STORAGE_KEY);
  if (!rawValue) {
    return null;
  }
  try {
    return JSON.parse(rawValue) as LoginResponse;
  } catch {
    return null;
  }
}

export function clearSession(): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.removeItem(SESSION_STORAGE_KEY);
}
