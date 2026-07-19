const API_BASE = "/api/v1";

const els = {
  authStatus: document.getElementById("auth-status"),
  greetingName: document.getElementById("greeting-name"),
  userName: document.getElementById("user-name"),
  userAvatar: document.getElementById("user-avatar"),
  chatForm: document.getElementById("chat-form"),
  chatInput: document.getElementById("chat-input"),
  chatWindow: document.getElementById("chat-window"),
  statOpenTasks: document.getElementById("stat-open-tasks"),
  statActiveProjects: document.getElementById("stat-active-projects"),
  statUnreadEmails: document.getElementById("stat-unread-emails"),
  statMeetingsToday: document.getElementById("stat-meetings-today"),
  navBadgeTasks: document.getElementById("nav-badge-tasks"),
  projectsTbody: document.getElementById("projects-tbody"),
  projectsEmpty: document.getElementById("projects-empty"),
  tasksList: document.getElementById("tasks-list"),
  tasksEmpty: document.getElementById("tasks-empty"),
  activityFeed: document.getElementById("activity-feed"),
  activityEmpty: document.getElementById("activity-empty"),
  edithStatus: document.getElementById("edith-status"),
  newProjectChip: document.getElementById("new-project-chip"),
  newProjectModal: document.getElementById("new-project-modal"),
  newProjectName: document.getElementById("new-project-name"),
  newProjectSave: document.getElementById("new-project-save"),
  newProjectCancel: document.getElementById("new-project-cancel"),
  shell: document.getElementById("shell"),
  sidebarToggle: document.getElementById("sidebar-toggle"),
  sidebarBackdrop: document.getElementById("sidebar-backdrop"),
  clientsTbody: document.getElementById("clients-tbody"),
  clientsEmpty: document.getElementById("clients-empty"),
  newClientBtn: document.getElementById("new-client-btn"),
  newClientModal: document.getElementById("new-client-modal"),
  newClientName: document.getElementById("new-client-name"),
  newClientSave: document.getElementById("new-client-save"),
  newClientCancel: document.getElementById("new-client-cancel"),
  clientModal: document.getElementById("client-modal"),
  clientModalName: document.getElementById("client-modal-name"),
  clientEditName: document.getElementById("client-edit-name"),
  clientEditEmail: document.getElementById("client-edit-email"),
  clientEditPhone: document.getElementById("client-edit-phone"),
  clientEditFollowup: document.getElementById("client-edit-followup"),
  clientEditNotes: document.getElementById("client-edit-notes"),
  clientModalProjects: document.getElementById("client-modal-projects"),
  clientModalTasks: document.getElementById("client-modal-tasks"),
  clientModalSave: document.getElementById("client-modal-save"),
  clientModalCancel: document.getElementById("client-modal-cancel"),
  newTaskBtn: document.getElementById("new-task-btn"),
  newTaskModal: document.getElementById("new-task-modal"),
  newTaskTitle: document.getElementById("new-task-title"),
  newTaskDueAt: document.getElementById("new-task-due-at"),
  newTaskSave: document.getElementById("new-task-save"),
  newTaskCancel: document.getElementById("new-task-cancel"),
  notificationsBtn: document.getElementById("notifications-btn"),
  notificationsBadge: document.getElementById("notifications-badge"),
  notificationsPanel: document.getElementById("notifications-panel"),
  notificationsList: document.getElementById("notifications-list"),
  notificationsEmpty: document.getElementById("notifications-empty"),
  notificationsMarkAll: document.getElementById("notifications-mark-all"),
  notificationsWrap: document.querySelector(".notifications-wrap"),
};

let isAuthenticated = false;

const STATUS_LABELS = { in_progress: "בתהליך", on_hold: "בהקפאה", done: "הושלם" };

const TOOL_LABELS = {
  drive_list_files: "חיפש קבצים ב-Drive",
  drive_get_file_content: "קרא קובץ מ-Drive",
  drive_create_file: "יצר קובץ ב-Drive",
  drive_share_file: "שיתף קובץ ב-Drive",
  gmail_list_recent_emails: "בדק מיילים",
  gmail_get_email: "קרא מייל",
  gmail_send_email: "שלח מייל",
  calendar_list_upcoming_events: "בדק את היומן",
  calendar_create_event: "קבע פגישה ביומן",
  calendar_delete_event: "מחק פגישה מהיומן",
  sheets_read_range: "קרא נתונים מ-Sheets",
  sheets_write_range: "עדכן נתונים ב-Sheets",
  sheets_append_row: "הוסיף שורה ב-Sheets",
  sheets_create_spreadsheet: "יצר גיליון חדש",
  workspace_create_client: "יצר לקוח חדש",
  workspace_update_client: "עדכן פרטי לקוח",
  workspace_get_client_detail: "הציג היסטוריית לקוח",
  workspace_create_project: "יצר פרויקט חדש",
  workspace_update_project_status: "עדכן סטטוס פרויקט",
  workspace_list_projects: "הציג פרויקטים",
  workspace_create_task: "יצר משימה חדשה",
  workspace_update_task_status: "עדכן סטטוס משימה",
  workspace_set_task_due_date: "עדכן תאריך יעד למשימה",
  workspace_list_tasks: "הציג משימות",
};

const AGENT_ICONS = {
  google_drive: "🗂️",
  gmail: "✉️",
  google_calendar: "📅",
  google_sheets: "📊",
  project_management: "✅",
};

async function apiFetch(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: response.statusText }));
    throw new Error(error.message || "בקשה נכשלה");
  }
  if (response.status === 204) return null;
  return response.json();
}

function relativeTime(isoString) {
  const diffMs = Date.now() - new Date(isoString).getTime();
  const minutes = Math.floor(diffMs / 60000);
  if (minutes < 1) return "עכשיו";
  if (minutes < 60) return `לפני ${minutes} דקות`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `לפני ${hours} שעות`;
  const days = Math.floor(hours / 24);
  return `לפני ${days} ימים`;
}

function setNavActive(name) {
  document.querySelectorAll(".nav-item").forEach((el) => {
    el.classList.toggle("active", el.dataset.nav === name);
  });
}

function closeSidebar() {
  els.shell.classList.remove("sidebar-open");
}

els.sidebarToggle.addEventListener("click", () => {
  els.shell.classList.toggle("sidebar-open");
});
els.sidebarBackdrop.addEventListener("click", closeSidebar);

async function checkAuth() {
  try {
    const user = await apiFetch("/auth/google/me");
    isAuthenticated = true;
    els.authStatus.innerHTML = `מחובר כ-${user.name}`;
    els.greetingName.textContent = user.name;
    els.userName.textContent = user.name;
    els.userAvatar.textContent = user.name.charAt(0).toUpperCase();
    els.edithStatus.innerHTML = '<span class="dot dot--green"></span> מחוברת ומוכנה';
    els.edithStatus.classList.remove("status-pill--offline");
  } catch {
    isAuthenticated = false;
    els.authStatus.innerHTML = `<a href="${API_BASE}/auth/google/login">התחבר עם Google</a>`;
    els.edithStatus.innerHTML = '<span class="dot"></span> לא מחוברת';
    els.edithStatus.classList.add("status-pill--offline");
  }
}

function addBubble(role, text) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  els.chatWindow.appendChild(bubble);
  els.chatWindow.scrollIntoView({ behavior: "smooth", block: "end" });
  return bubble;
}

function addToolTrace(toolCalls) {
  if (!toolCalls || toolCalls.length === 0) return;
  const trace = document.createElement("div");
  trace.className = "tool-trace";
  trace.textContent = `בוצע: ${toolCalls.map((t) => TOOL_LABELS[t.tool_name] || t.tool_name).join(", ")}`;
  els.chatWindow.appendChild(trace);
}

let conversationId = null;

async function sendCommand(text) {
  if (!isAuthenticated) {
    addBubble("assistant", "יש להתחבר עם Google כדי לדבר עם Edith.");
    return;
  }
  addBubble("user", text);
  try {
    const data = await apiFetch("/chat/commands", {
      method: "POST",
      body: JSON.stringify({ text, conversation_id: conversationId }),
    });
    conversationId = data.conversation_id;
    addBubble("assistant", data.reply);
    addToolTrace(data.tool_calls_made);
    refreshWorkspace();
  } catch (err) {
    addBubble("error", err.message);
  }
}

els.chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = els.chatInput.value.trim();
  if (!text) return;
  els.chatInput.value = "";
  sendCommand(text);
});

document.querySelectorAll(".chip[data-command]").forEach((chip) => {
  chip.addEventListener("click", () => sendCommand(chip.dataset.command));
});

document.querySelectorAll(".nav-item").forEach((item) => {
  item.addEventListener("click", () => {
    const target = item.dataset.nav;
    setNavActive(target);
    closeSidebar();
    const sectionMap = {
      chat: "chat-form",
      overview: "overview-section",
      tasks: "tasks-section",
      projects: "projects-section",
      clients: "clients-section",
    };
    if (sectionMap[target]) {
      document.getElementById(sectionMap[target]).scrollIntoView({ behavior: "smooth", block: "start" });
      if (target === "chat") els.chatInput.focus();
    } else {
      addBubble("assistant", "האזור הזה עוד לא זמין — בקרוב.");
    }
  });
});

els.newProjectChip.addEventListener("click", () => {
  els.newProjectModal.hidden = false;
  els.newProjectName.value = "";
  els.newProjectName.focus();
});
els.newProjectCancel.addEventListener("click", () => {
  els.newProjectModal.hidden = true;
});
els.newProjectSave.addEventListener("click", async () => {
  const name = els.newProjectName.value.trim();
  if (!name) return;
  try {
    await apiFetch("/projects", { method: "POST", body: JSON.stringify({ name }) });
    els.newProjectModal.hidden = true;
    refreshWorkspace();
  } catch (err) {
    alert(err.message);
  }
});

els.newTaskBtn.addEventListener("click", () => {
  els.newTaskModal.hidden = false;
  els.newTaskTitle.value = "";
  els.newTaskDueAt.value = "";
  els.newTaskTitle.focus();
});
els.newTaskCancel.addEventListener("click", () => {
  els.newTaskModal.hidden = true;
});
els.newTaskSave.addEventListener("click", async () => {
  const title = els.newTaskTitle.value.trim();
  if (!title) return;
  try {
    const dueValue = els.newTaskDueAt.value;
    await apiFetch("/tasks", {
      method: "POST",
      body: JSON.stringify({
        title,
        due_at: dueValue ? new Date(dueValue).toISOString() : null,
      }),
    });
    els.newTaskModal.hidden = true;
    refreshWorkspace();
  } catch (err) {
    alert(err.message);
  }
});

els.newClientBtn.addEventListener("click", () => {
  els.newClientModal.hidden = false;
  els.newClientName.value = "";
  els.newClientName.focus();
});
els.newClientCancel.addEventListener("click", () => {
  els.newClientModal.hidden = true;
});
els.newClientSave.addEventListener("click", async () => {
  const name = els.newClientName.value.trim();
  if (!name) return;
  try {
    await apiFetch("/clients", { method: "POST", body: JSON.stringify({ name }) });
    els.newClientModal.hidden = true;
    loadClients();
  } catch (err) {
    alert(err.message);
  }
});

let currentClientId = null;

async function openClientModal(clientId) {
  try {
    const detail = await apiFetch(`/clients/${clientId}`);
    currentClientId = clientId;
    els.clientModalName.textContent = detail.client.name;
    els.clientEditName.value = detail.client.name;
    els.clientEditEmail.value = detail.client.email || "";
    els.clientEditPhone.value = detail.client.phone || "";
    els.clientEditFollowup.value = detail.client.next_follow_up_at
      ? detail.client.next_follow_up_at.slice(0, 10)
      : "";
    els.clientEditNotes.value = detail.client.notes || "";

    els.clientModalProjects.innerHTML = detail.projects.length
      ? detail.projects
          .map(
            (p) =>
              `<div class="client-modal-list-item">${escapeHtml(p.name)} <span class="status-badge status-badge--${p.status}">${STATUS_LABELS[p.status]}</span></div>`
          )
          .join("")
      : '<div class="client-modal-list-empty">אין פרויקטים משויכים.</div>';

    els.clientModalTasks.innerHTML = detail.tasks.length
      ? detail.tasks
          .map(
            (t) =>
              `<div class="client-modal-list-item${t.status === "done" ? " done" : ""}">${escapeHtml(t.title)}</div>`
          )
          .join("")
      : '<div class="client-modal-list-empty">אין משימות משויכות.</div>';

    els.clientModal.hidden = false;
  } catch (err) {
    alert(err.message);
  }
}

els.clientModalCancel.addEventListener("click", () => {
  els.clientModal.hidden = true;
});
els.clientModalSave.addEventListener("click", async () => {
  if (!currentClientId) return;
  try {
    const followupValue = els.clientEditFollowup.value;
    await apiFetch(`/clients/${currentClientId}`, {
      method: "PATCH",
      body: JSON.stringify({
        name: els.clientEditName.value.trim() || null,
        email: els.clientEditEmail.value.trim() || null,
        phone: els.clientEditPhone.value.trim() || null,
        notes: els.clientEditNotes.value.trim() || null,
        next_follow_up_at: followupValue ? new Date(followupValue).toISOString() : null,
      }),
    });
    els.clientModal.hidden = true;
    loadClients();
  } catch (err) {
    alert(err.message);
  }
});

async function loadDashboardSummary() {
  try {
    const summary = await apiFetch("/dashboard/summary");
    els.statOpenTasks.textContent = summary.open_tasks;
    els.statActiveProjects.textContent = summary.active_projects;
    els.statUnreadEmails.textContent = summary.unread_emails ?? "—";
    els.statMeetingsToday.textContent = summary.meetings_today ?? "—";
    els.navBadgeTasks.textContent = summary.open_tasks;
  } catch {
    // not authenticated yet — leave placeholders
  }
}

async function loadProjects() {
  try {
    const projects = await apiFetch("/projects");
    els.projectsTbody.innerHTML = "";
    els.projectsEmpty.hidden = projects.length > 0;
    for (const project of projects) {
      const tr = document.createElement("tr");
      const updated = new Date(project.updated_at).toLocaleDateString("he-IL");
      tr.innerHTML = `
        <td>${escapeHtml(project.name)}</td>
        <td>${project.client_name ? escapeHtml(project.client_name) : "—"}</td>
        <td><span class="status-badge status-badge--${project.status}">${STATUS_LABELS[project.status]}</span></td>
        <td>${project.last_task_title ? escapeHtml(project.last_task_title) : "—"}</td>
        <td>${updated}</td>
      `;
      els.projectsTbody.appendChild(tr);
    }
  } catch {
    // not authenticated yet
  }
}

function dueDateBadge(task) {
  if (!task.due_at) return null;
  const due = new Date(task.due_at);
  const badge = document.createElement("span");
  badge.className = "task-due";
  badge.textContent = due.toLocaleString("he-IL", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
  if (task.status !== "done") {
    const diffHours = (due.getTime() - Date.now()) / 3600000;
    if (diffHours < 0) badge.classList.add("task-due--overdue");
    else if (diffHours <= 24) badge.classList.add("task-due--soon");
  }
  return badge;
}

async function loadTasks() {
  try {
    const tasks = await apiFetch("/tasks");
    els.tasksList.innerHTML = "";
    els.tasksEmpty.hidden = tasks.length > 0;
    for (const task of tasks) {
      const row = document.createElement("div");
      row.className = `task-row${task.status === "done" ? " done" : ""}`;
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = task.status === "done";
      checkbox.addEventListener("change", async () => {
        await apiFetch(`/tasks/${task.id}/status`, {
          method: "PATCH",
          body: JSON.stringify({ status: checkbox.checked ? "done" : "open" }),
        });
        loadTasks();
        loadDashboardSummary();
      });
      const title = document.createElement("span");
      title.className = "task-title";
      title.textContent = task.title;
      row.appendChild(checkbox);
      row.appendChild(title);
      const badge = dueDateBadge(task);
      if (badge) row.appendChild(badge);
      els.tasksList.appendChild(row);
    }
  } catch {
    // not authenticated yet
  }
}

async function loadClients() {
  try {
    const clientsList = await apiFetch("/clients");
    els.clientsTbody.innerHTML = "";
    els.clientsEmpty.hidden = clientsList.length > 0;
    for (const c of clientsList) {
      const tr = document.createElement("tr");
      tr.className = "clickable-row";
      const followup = c.next_follow_up_at
        ? new Date(c.next_follow_up_at).toLocaleDateString("he-IL")
        : "—";
      tr.innerHTML = `
        <td>${escapeHtml(c.name)}</td>
        <td>${c.email ? escapeHtml(c.email) : "—"}</td>
        <td>${c.phone ? escapeHtml(c.phone) : "—"}</td>
        <td>${followup}</td>
      `;
      tr.addEventListener("click", () => openClientModal(c.id));
      els.clientsTbody.appendChild(tr);
    }
  } catch {
    // not authenticated yet
  }
}

function toggleNotificationsPanel(forceOpen) {
  const shouldOpen = forceOpen ?? els.notificationsPanel.hidden;
  els.notificationsPanel.hidden = !shouldOpen;
}

els.notificationsBtn.addEventListener("click", (event) => {
  event.stopPropagation();
  toggleNotificationsPanel();
});
document.addEventListener("click", (event) => {
  if (!els.notificationsWrap.contains(event.target)) {
    toggleNotificationsPanel(false);
  }
});
els.notificationsMarkAll.addEventListener("click", async () => {
  try {
    await apiFetch("/notifications/read-all", { method: "POST" });
    loadNotifications();
  } catch (err) {
    alert(err.message);
  }
});

async function loadNotifications() {
  try {
    const notifications = await apiFetch("/notifications");
    els.notificationsBadge.hidden = notifications.length === 0;
    els.notificationsBadge.textContent = notifications.length;
    els.notificationsList.innerHTML = "";
    els.notificationsEmpty.hidden = notifications.length > 0;
    for (const n of notifications) {
      const item = document.createElement("div");
      item.className = "notification-item";
      item.innerHTML = `
        <div class="notification-title">${escapeHtml(n.title)}</div>
        <div class="notification-body">${escapeHtml(n.body)}</div>
        <div class="notification-time">${relativeTime(n.created_at)}</div>
      `;
      item.addEventListener("click", async () => {
        try {
          await apiFetch(`/notifications/${n.id}/read`, { method: "PATCH" });
          loadNotifications();
        } catch (err) {
          alert(err.message);
        }
      });
      els.notificationsList.appendChild(item);
    }
  } catch {
    // not authenticated yet
  }
}

async function loadActivity() {
  try {
    const items = await apiFetch("/dashboard/activity");
    els.activityFeed.innerHTML = "";
    els.activityEmpty.hidden = items.length > 0;
    for (const item of items) {
      const row = document.createElement("div");
      row.className = "activity-item";
      row.innerHTML = `
        <div class="activity-icon">${AGENT_ICONS[item.agent_name] || "•"}</div>
        <div>
          <div class="activity-text">${TOOL_LABELS[item.tool_name] || item.tool_name}</div>
          <div class="activity-time">${relativeTime(item.created_at)}</div>
        </div>
      `;
      els.activityFeed.appendChild(row);
    }
  } catch {
    // not authenticated yet
  }
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function refreshWorkspace() {
  loadDashboardSummary();
  loadProjects();
  loadTasks();
  loadClients();
  loadActivity();
  loadNotifications();
}

(async function init() {
  await checkAuth();
  refreshWorkspace();
})();
