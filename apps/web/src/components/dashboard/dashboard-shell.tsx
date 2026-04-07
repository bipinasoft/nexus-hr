"use client";

import Link from "next/link";
import { startTransition, useDeferredValue, useEffect, useState } from "react";

import {
  type AssistantResponse,
  type DashboardResponse,
  type LoginResponse,
  type NotificationItem,
  buildApiUrl,
  buildWebSocketUrl,
  clearSession,
  readSession
} from "@/lib/api";

const statusStyles: Record<string, string> = {
  present: "border-emerald-200 bg-emerald-50 text-emerald-800",
  remote: "border-sky-200 bg-sky-50 text-sky-800",
  late: "border-amber-200 bg-amber-50 text-amber-800",
  absent: "border-rose-200 bg-rose-50 text-rose-800",
  leave: "border-violet-200 bg-violet-50 text-violet-800",
  holiday: "border-cyan-200 bg-cyan-50 text-cyan-800",
  weekend: "border-slate-200 bg-slate-100 text-slate-600",
  upcoming: "border-slate-200 bg-white text-slate-500",
  "manual-review": "border-orange-200 bg-orange-50 text-orange-800",
  not_marked: "border-slate-200 bg-white text-slate-500"
};

function formatMonth(month: string) {
  const [year, monthIndex] = month.split("-").map(Number);
  return new Date(year, monthIndex - 1, 1).toLocaleDateString("en-IN", {
    month: "long",
    year: "numeric"
  });
}

function shiftMonth(month: string, delta: number) {
  const [year, monthIndex] = month.split("-").map(Number);
  const next = new Date(year, monthIndex - 1 + delta, 1);
  return `${next.getFullYear()}-${String(next.getMonth() + 1).padStart(2, "0")}`;
}

function parseCalendarDate(value: string) {
  return new Date(`${value}T12:00:00`);
}

function formatTime(value?: string | null) {
  if (!value) {
    return "Not recorded";
  }

  return new Date(value).toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit"
  });
}

function buildCalendarCells(calendar: DashboardResponse["calendar"]) {
  if (calendar.length === 0) {
    return [];
  }

  const firstDay = parseCalendarDate(calendar[0].date);
  const offset = (firstDay.getDay() + 6) % 7;
  return [...Array.from({ length: offset }, () => null), ...calendar];
}

export function DashboardShell() {
  const [session, setSession] = useState<LoginResponse | null>(null);
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [activeMonth, setActiveMonth] = useState(new Date().toISOString().slice(0, 7));
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [assistantPrompt, setAssistantPrompt] = useState(
    "What should I prioritize this month based on attendance and leave?"
  );
  const deferredAssistantPrompt = useDeferredValue(assistantPrompt);
  const [assistantResponse, setAssistantResponse] = useState<AssistantResponse | null>(null);
  const [assistantStream, setAssistantStream] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isStreaming, setIsStreaming] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    setSession(readSession());
  }, []);

  useEffect(() => {
    if (!session) {
      setIsLoading(false);
      return;
    }
    const activeSession = session;

    let cancelled = false;

    async function loadWorkspace() {
      setIsLoading(true);
      setErrorMessage(null);

      try {
        const [dashboardResponse, notificationsResponse] = await Promise.all([
          fetch(buildApiUrl(`/v1/dashboard/me?month=${activeMonth}`), {
            headers: { Authorization: `Bearer ${activeSession.access_token}` }
          }),
          fetch(buildApiUrl("/v1/notifications/me"), {
            headers: { Authorization: `Bearer ${activeSession.access_token}` }
          })
        ]);

        if (!dashboardResponse.ok || !notificationsResponse.ok) {
          throw new Error("Unable to load the employee workspace.");
        }

        const nextDashboard = (await dashboardResponse.json()) as DashboardResponse;
        const nextNotifications = (await notificationsResponse.json()) as NotificationItem[];

        if (cancelled) {
          return;
        }

        startTransition(() => {
          setDashboard(nextDashboard);
          setNotifications(nextNotifications);
          setSelectedDate((current) => current ?? nextDashboard.calendar[0]?.date ?? null);
        });
      } catch (error) {
        if (!cancelled) {
          setErrorMessage(error instanceof Error ? error.message : "Unknown workspace error.");
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void loadWorkspace();

    return () => {
      cancelled = true;
    };
  }, [activeMonth, session]);

  useEffect(() => {
    if (!session) {
      return;
    }
    const activeSession = session;

    const socket = new WebSocket(
      `${buildWebSocketUrl("/v1/notifications/ws/notifications")}?token=${encodeURIComponent(
        activeSession.access_token
      )}`
    );

    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data) as {
          type: string;
          payload?: NotificationItem;
        };
        if (message.type === "notification.created" && message.payload) {
          startTransition(() => {
            setNotifications((current) => [message.payload as NotificationItem, ...current]);
          });
        }
      } catch {
        return;
      }
    };

    const ping = window.setInterval(() => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.send("ping");
      }
    }, 20000);

    return () => {
      window.clearInterval(ping);
      socket.close();
    };
  }, [session]);

  const selectedDay = dashboard?.calendar.find((item) => item.date === selectedDate) ?? null;
  const calendarCells = buildCalendarCells(dashboard?.calendar ?? []);

  async function markAsRead(notificationId: string) {
    if (!session) {
      return;
    }

    await fetch(buildApiUrl(`/v1/notifications/${notificationId}/read`), {
      method: "POST",
      headers: { Authorization: `Bearer ${session.access_token}` }
    });

    startTransition(() => {
      setNotifications((current) =>
        current.map((item) =>
          item.notification_id === notificationId ? { ...item, is_read: true } : item
        )
      );
    });
  }

  async function streamAssistant() {
    if (!session || !deferredAssistantPrompt.trim()) {
      return;
    }

    setAssistantStream("");
    setAssistantResponse(null);
    setIsStreaming(true);

    try {
      const response = await fetch(buildApiUrl("/v1/assistant/stream"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.access_token}`
        },
        body: JSON.stringify({ question: deferredAssistantPrompt, top_k: 4, include_actions: true })
      });

      if (!response.body) {
        throw new Error("No assistant stream returned.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let remainder = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }
        remainder += decoder.decode(value, { stream: true });
        const lines = remainder.split("\n");
        remainder = lines.pop() ?? "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            setAssistantStream((current) => `${current}${line.slice(6)} `);
          }
        }
      }

      const finalResponse = await fetch(buildApiUrl("/v1/assistant/query"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.access_token}`
        },
        body: JSON.stringify({ question: deferredAssistantPrompt, top_k: 4, include_actions: true })
      });

      if (finalResponse.ok) {
        setAssistantResponse((await finalResponse.json()) as AssistantResponse);
      }
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Assistant stream failed.");
    } finally {
      setIsStreaming(false);
    }
  }

  if (!session) {
    return (
      <div className="shell py-16">
        <div className="panel mx-auto max-w-3xl px-8 py-10 text-center">
          <p className="eyebrow">Secure Workspace Access</p>
          <h1 className="mt-6 font-display text-4xl font-semibold text-slate-950">
            Sign in to view attendance, leave markers, holidays, and tagged alerts.
          </h1>
          <p className="mt-4 text-base leading-8 text-slate-600">
            The new employee dashboard loads after authentication and combines the monthly calendar,
            notifications, and AI guidance in one workspace.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <Link className="button-primary" href="/login">
              Open login
            </Link>
            <Link className="button-secondary" href="/">
              Return to landing page
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <main className="shell py-8 md:py-10">
      <div className="grid gap-6">
        <section className="panel px-6 py-6 md:px-8">
          <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
            <div>
              <p className="eyebrow">Employee Command Center</p>
              <h1 className="mt-5 font-display text-4xl font-semibold text-slate-950 md:text-5xl">
                {dashboard?.employee.full_name ?? session.user.name}
              </h1>
              <p className="mt-3 max-w-3xl text-base leading-8 text-slate-600">
                Attendance, leave visibility, holidays, and action-oriented notifications are now unified
                for a faster daily HR workflow.
              </p>
              <div className="mt-5 flex flex-wrap gap-3 text-sm text-slate-500">
                <span className="pill">{session.user.tenant_slug}</span>
                <span className="pill">{session.user.roles.join(", ")}</span>
                <span className="pill">{dashboard?.employee.department_id ?? session.user.department_id}</span>
              </div>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <MetricCard label="Present" value={dashboard?.summary.present_days ?? 0} />
              <MetricCard label="Remote" value={dashboard?.summary.remote_days ?? 0} />
              <MetricCard label="Leave" value={dashboard?.summary.leave_days ?? 0} />
              <MetricCard label="Average Hours" value={dashboard?.summary.average_hours ?? 0} suffix=" hrs" />
            </div>
          </div>
        </section>

        {errorMessage ? (
          <div className="rounded-3xl border border-rose-200 bg-rose-50 px-5 py-4 text-sm text-rose-700">
            {errorMessage}
          </div>
        ) : null}

        <section className="grid gap-6 xl:grid-cols-[1.18fr_0.82fr]">
          <div className="grid gap-6">
            <div className="panel px-6 py-6 md:px-8">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Monthly Calendar</p>
                  <h2 className="mt-2 font-display text-3xl font-semibold text-slate-950">
                    {dashboard ? formatMonth(dashboard.month) : formatMonth(activeMonth)}
                  </h2>
                </div>
                <div className="flex gap-3">
                  <button
                    className="button-secondary"
                    onClick={() => setActiveMonth((current) => shiftMonth(current, -1))}
                    type="button"
                  >
                    Previous
                  </button>
                  <button
                    className="button-secondary"
                    onClick={() => setActiveMonth((current) => shiftMonth(current, 1))}
                    type="button"
                  >
                    Next
                  </button>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-7 gap-3 text-center text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
                {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day) => (
                  <span key={day}>{day}</span>
                ))}
              </div>

              <div className="mt-4 grid grid-cols-7 gap-3">
                {calendarCells.map((day, index) =>
                  day ? (
                    <button
                      className={`min-h-28 rounded-[24px] border px-3 py-3 text-left transition hover:-translate-y-0.5 ${
                        statusStyles[day.attendance_status] ?? statusStyles.not_marked
                      } ${day.date === selectedDate ? "ring-2 ring-slate-950/20" : ""}`}
                      key={day.date}
                      onClick={() => setSelectedDate(day.date)}
                      type="button"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <span className="font-display text-2xl font-semibold">
                          {parseCalendarDate(day.date).getDate()}
                        </span>
                        <span className="rounded-full bg-white/70 px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.18em]">
                          {day.attendance_status.replace("-", " ")}
                        </span>
                      </div>
                      <div className="mt-3 space-y-1 text-xs leading-5">
                        {day.holiday_name ? <p>{day.holiday_name}</p> : null}
                        {day.leave_type ? <p>{day.leave_type}</p> : null}
                        {day.total_hours ? <p>{day.total_hours} hrs</p> : null}
                        {day.location_label ? <p>{day.location_label}</p> : null}
                      </div>
                    </button>
                  ) : (
                    <div className="min-h-28 rounded-[24px] border border-dashed border-slate-200 bg-transparent" key={`blank-${index}`} />
                  )
                )}
              </div>
            </div>

            <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
              <div className="panel px-6 py-6 md:px-8">
                <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Selected Day</p>
                <h3 className="mt-3 font-display text-2xl font-semibold text-slate-950">
                  {selectedDay
                    ? parseCalendarDate(selectedDay.date).toLocaleDateString("en-IN", {
                        weekday: "long",
                        day: "numeric",
                        month: "long"
                      })
                    : "Select a day"}
                </h3>
                {selectedDay ? (
                  <div className="mt-5 space-y-3 text-sm leading-7 text-slate-600">
                    <p><span className="font-semibold text-slate-900">Status:</span> {selectedDay.attendance_status}</p>
                    <p><span className="font-semibold text-slate-900">Check-in:</span> {formatTime(selectedDay.check_in_at)}</p>
                    <p><span className="font-semibold text-slate-900">Check-out:</span> {formatTime(selectedDay.check_out_at)}</p>
                    <p><span className="font-semibold text-slate-900">Leave:</span> {selectedDay.leave_type ? `${selectedDay.leave_type} (${selectedDay.leave_status})` : "No leave"}</p>
                    <p><span className="font-semibold text-slate-900">Holiday:</span> {selectedDay.holiday_name ?? "No holiday"}</p>
                    <p><span className="font-semibold text-slate-900">Notes:</span> {selectedDay.notes ?? "No additional notes."}</p>
                  </div>
                ) : null}
              </div>

              <div className="panel px-6 py-6 md:px-8">
                <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Leave Balances</p>
                <div className="mt-5 grid gap-4">
                  {(dashboard?.leave_balances ?? []).map((item) => (
                    <div className="rounded-[24px] border border-slate-200 bg-slate-50 px-5 py-4" key={item.leave_type}>
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <h3 className="font-display text-2xl font-semibold text-slate-950">{item.leave_type}</h3>
                          <p className="text-sm text-slate-500">{item.available_days} days available</p>
                        </div>
                        <span className="pill">{item.allocated_days} allocated</span>
                      </div>
                      <div className="mt-4 grid gap-3 sm:grid-cols-3">
                        <MiniMetric label="Used" value={item.used_days} />
                        <MiniMetric label="Pending" value={item.pending_days} />
                        <MiniMetric label="Available" value={item.available_days} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="grid gap-6">
            <div className="panel px-6 py-6 md:px-8">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Alerts & Notifications</p>
                  <h2 className="mt-2 font-display text-3xl font-semibold text-slate-950">Tagged for response</h2>
                </div>
                <span className="pill">{notifications.filter((item) => !item.is_read).length} unread</span>
              </div>
              <div className="mt-6 space-y-4">
                {notifications.map((item) => (
                  <button
                    className={`w-full rounded-[24px] border px-5 py-4 text-left transition ${
                      item.is_read ? "border-slate-200 bg-slate-50" : "border-teal-200 bg-teal-50"
                    }`}
                    key={item.notification_id}
                    onClick={() => markAsRead(item.notification_id)}
                    type="button"
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="font-semibold text-slate-950">{item.title}</p>
                        <p className="mt-2 text-sm leading-7 text-slate-600">{item.message}</p>
                      </div>
                      <span className="pill">{item.severity}</span>
                    </div>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {item.tags.map((tag) => (
                        <span className="rounded-full bg-white px-3 py-1 text-xs font-semibold text-slate-600" key={tag}>
                          {tag}
                        </span>
                      ))}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            <div className="panel-dark px-6 py-6 md:px-8">
              <p className="text-xs uppercase tracking-[0.24em] text-teal-200">NexusHR Copilot</p>
              <h2 className="mt-3 font-display text-3xl font-semibold">Stream answers with policy retrieval.</h2>
              <textarea
                className="field mt-5 min-h-32 resize-none border-white/10 bg-white/10 text-white placeholder:text-slate-300"
                onChange={(event) => setAssistantPrompt(event.target.value)}
                placeholder="Ask about leave policy, payroll deductions, attendance anomalies, or review cycles."
                value={assistantPrompt}
              />
              <button
                className="button-primary mt-4 w-full bg-teal-500 text-slate-950 hover:bg-teal-300"
                disabled={isStreaming}
                onClick={() => { void streamAssistant(); }}
                type="button"
              >
                {isStreaming ? "Streaming..." : "Stream guidance"}
              </button>
              <div className="mt-5 rounded-[24px] border border-white/10 bg-white/5 p-4">
                <p className="text-sm leading-7 text-slate-200">
                  {assistantStream || assistantResponse?.answer || "The assistant response will appear here."}
                </p>
              </div>
              {assistantResponse ? (
                <div className="mt-5 grid gap-4">
                  <div className="rounded-[24px] border border-white/10 bg-white/5 p-4">
                    <p className="text-sm font-semibold text-white">Strategy: {assistantResponse.strategy}</p>
                    <p className="mt-2 text-sm leading-7 text-slate-300">Intent: {assistantResponse.intent}</p>
                  </div>
                  <div className="rounded-[24px] border border-white/10 bg-white/5 p-4">
                    <p className="text-sm font-semibold text-white">Next actions</p>
                    <div className="mt-3 space-y-2">
                      {assistantResponse.follow_up_actions.map((item) => (
                        <p className="text-sm leading-7 text-slate-300" key={item}>{item}</p>
                      ))}
                    </div>
                  </div>
                </div>
              ) : null}
            </div>

            <div className="panel px-6 py-6 md:px-8">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Session Controls</p>
                  <h2 className="mt-2 font-display text-2xl font-semibold text-slate-950">Workspace status</h2>
                </div>
                <button
                  className="button-secondary"
                  onClick={() => {
                    clearSession();
                    window.location.href = "/login";
                  }}
                  type="button"
                >
                  Sign out
                </button>
              </div>
              <div className="mt-5 grid gap-3">
                {[
                  "Calendar markers distinguish attendance, leave, holidays, weekends, and anomalies.",
                  "Notifications are delivered in real time through a WebSocket channel.",
                  "JWT and tenant-scoped APIs keep the employee view isolated."
                ].map((item) => (
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600" key={item}>
                    {item}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      </div>

      {isLoading ? (
        <div className="fixed inset-x-0 bottom-6 mx-auto flex w-fit rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white shadow-lg">
          Loading workspace...
        </div>
      ) : null}
    </main>
  );
}

function MetricCard({
  label,
  value,
  suffix = ""
}: {
  label: string;
  value: number;
  suffix?: string;
}) {
  return (
    <div className="rounded-[24px] border border-slate-200 bg-slate-50 px-5 py-4">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-2 font-display text-3xl font-semibold text-slate-950">
        {value}
        {suffix}
      </p>
    </div>
  );
}

function MiniMetric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-2xl border border-white bg-white px-4 py-3">
      <p className="text-xs uppercase tracking-[0.22em] text-slate-400">{label}</p>
      <p className="mt-2 font-display text-2xl font-semibold text-slate-950">{value}</p>
    </div>
  );
}
