const API_BASE = "/api/v1";

const els = {
  authStatus: document.getElementById("auth-status"),
  greetingName: document.getElementById("greeting-name"),
  greetingPhrase: document.getElementById("greeting-phrase"),
  userName: document.getElementById("user-name"),
  userAvatar: document.getElementById("user-avatar"),
  chatForm: document.getElementById("chat-form"),
  chatInput: document.getElementById("chat-input"),
  voiceInputBtn: document.getElementById("voice-input-btn"),
  chatWindow: document.getElementById("chat-window"),
  navBadgeTasks: document.getElementById("nav-badge-tasks"),
  projectsTbody: document.getElementById("projects-tbody"),
  projectsEmpty: document.getElementById("projects-empty"),
  tasksList: document.getElementById("tasks-list"),
  tasksEmpty: document.getElementById("tasks-empty"),
  activityFeed: document.getElementById("activity-feed"),
  activityEmpty: document.getElementById("activity-empty"),
  edithStatus: document.getElementById("edith-status"),
  newProjectBtn: document.getElementById("new-project-btn"),
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
  clientModalSave: document.getElementById("client-modal-save"),
  clientModalCancel: document.getElementById("client-modal-cancel"),
  clientModalDelete: document.getElementById("client-modal-delete"),
  clientModalNewMeetingBtn: document.getElementById("client-modal-new-meeting-btn"),
  clientModalNewTaskTitle: document.getElementById("client-modal-new-task-title"),
  clientModalNewTaskStartAt: document.getElementById("client-modal-new-task-start-at"),
  clientModalNewTaskDueAt: document.getElementById("client-modal-new-task-due-at"),
  clientModalNewTaskAdd: document.getElementById("client-modal-new-task-add"),
  newTaskBtn: document.getElementById("new-task-btn"),
  newTaskModal: document.getElementById("new-task-modal"),
  newTaskTitle: document.getElementById("new-task-title"),
  newTaskStartAt: document.getElementById("new-task-start-at"),
  newTaskDueAt: document.getElementById("new-task-due-at"),
  newTaskSave: document.getElementById("new-task-save"),
  newTaskCancel: document.getElementById("new-task-cancel"),
  editTaskModal: document.getElementById("edit-task-modal"),
  editTaskTitle: document.getElementById("edit-task-title"),
  editTaskStartAt: document.getElementById("edit-task-start-at"),
  editTaskDueAt: document.getElementById("edit-task-due-at"),
  editTaskProject: document.getElementById("edit-task-project"),
  editTaskClient: document.getElementById("edit-task-client"),
  editTaskSave: document.getElementById("edit-task-save"),
  editTaskCancel: document.getElementById("edit-task-cancel"),
  editTaskDelete: document.getElementById("edit-task-delete"),
  notificationsBtn: document.getElementById("notifications-btn"),
  notificationsBadge: document.getElementById("notifications-badge"),
  notificationsPanel: document.getElementById("notifications-panel"),
  notificationsList: document.getElementById("notifications-list"),
  notificationsEmpty: document.getElementById("notifications-empty"),
  notificationsMarkAll: document.getElementById("notifications-mark-all"),
  notificationsWrap: document.querySelector(".notifications-wrap"),
  calendarList: document.getElementById("calendar-list"),
  calendarEmpty: document.getElementById("calendar-empty"),
  newEventBtn: document.getElementById("new-event-btn"),
  newEventModal: document.getElementById("new-event-modal"),
  newEventSummary: document.getElementById("new-event-summary"),
  newEventStart: document.getElementById("new-event-start"),
  newEventEnd: document.getElementById("new-event-end"),
  newEventDescription: document.getElementById("new-event-description"),
  newEventSave: document.getElementById("new-event-save"),
  newEventCancel: document.getElementById("new-event-cancel"),
  filesTbody: document.getElementById("files-tbody"),
  filesEmpty: document.getElementById("files-empty"),
  newFileBtn: document.getElementById("new-file-btn"),
  newFileModal: document.getElementById("new-file-modal"),
  newFileName: document.getElementById("new-file-name"),
  newFileContent: document.getElementById("new-file-content"),
  newFileSave: document.getElementById("new-file-save"),
  newFileCancel: document.getElementById("new-file-cancel"),
  shareFileModal: document.getElementById("share-file-modal"),
  shareFileEmail: document.getElementById("share-file-email"),
  shareFileRole: document.getElementById("share-file-role"),
  shareFileSave: document.getElementById("share-file-save"),
  shareFileCancel: document.getElementById("share-file-cancel"),
  showMonthBtn: document.getElementById("show-month-btn"),
  calendarMonthModal: document.getElementById("calendar-month-modal"),
  monthViewTitle: document.getElementById("month-view-title"),
  monthPrevBtn: document.getElementById("month-prev-btn"),
  monthNextBtn: document.getElementById("month-next-btn"),
  monthViewClose: document.getElementById("month-view-close"),
  monthGrid: document.getElementById("month-grid"),
  installAppBtn: document.getElementById("install-app-btn"),
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

function timeOfDayGreeting() {
  const hour = new Date().getHours();
  if (hour >= 5 && hour < 12) return "בוקר טוב";
  if (hour >= 12 && hour < 17) return "צהריים טובים";
  if (hour >= 17 && hour < 21) return "ערב טוב";
  return "לילה טוב";
}

let hasSpokenGreeting = false;

function speakGreeting(greeting) {
  if (hasSpokenGreeting || !("speechSynthesis" in window)) return;
  hasSpokenGreeting = true;
  const utterance = new SpeechSynthesisUtterance(`${greeting}, בוס. טוב שחזרת.`);
  utterance.lang = "he-IL";
  window.speechSynthesis.speak(utterance);
}

async function checkAuth() {
  try {
    const user = await apiFetch("/auth/google/me");
    isAuthenticated = true;
    els.authStatus.innerHTML = `מחובר כ-${user.name}`;
    const greeting = timeOfDayGreeting();
    els.greetingPhrase.textContent = greeting;
    els.greetingName.textContent = user.name;
    els.userName.textContent = user.name;
    els.userAvatar.textContent = user.name.charAt(0).toUpperCase();
    els.edithStatus.innerHTML = '<span class="dot dot--green"></span> מחוברת ומוכנה';
    els.edithStatus.classList.remove("status-pill--offline");
    speakGreeting(greeting);
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

const SpeechRecognitionCtor = window.SpeechRecognition || window.webkitSpeechRecognition;
let voiceRecognition = null;
let isRecording = false;

if (SpeechRecognitionCtor) {
  els.voiceInputBtn.hidden = false;

  voiceRecognition = new SpeechRecognitionCtor();
  voiceRecognition.lang = "he-IL";
  voiceRecognition.continuous = true;
  voiceRecognition.interimResults = true;

  voiceRecognition.addEventListener("result", (event) => {
    let transcript = "";
    for (let i = 0; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript;
    }
    els.chatInput.value = transcript;
  });

  voiceRecognition.addEventListener("error", (event) => {
    if (event.error === "not-allowed" || event.error === "service-not-allowed") {
      alert("אין הרשאה למיקרופון. אפשר הרשאת מיקרופון לאתר בהגדרות הדפדפן ונסה שוב.");
    } else if (event.error !== "no-speech" && event.error !== "aborted") {
      alert("לא הצלחתי להקליט. נסה שוב.");
    }
  });

  voiceRecognition.addEventListener("end", () => {
    isRecording = false;
    els.voiceInputBtn.classList.remove("recording");
  });

  els.voiceInputBtn.addEventListener("click", () => {
    if (isRecording) {
      voiceRecognition.stop();
      return;
    }
    els.chatInput.value = "";
    isRecording = true;
    els.voiceInputBtn.classList.add("recording");
    voiceRecognition.start();
  });
}

document.querySelectorAll(".nav-item").forEach((item) => {
  if (item.tagName === "A") return; // real links (e.g. Gmail) navigate on their own
  item.addEventListener("click", () => {
    const target = item.dataset.nav;
    setNavActive(target);
    closeSidebar();
    const sectionMap = {
      chat: "chat-form",
      overview: "greeting",
      tasks: "tasks-section",
      projects: "projects-section",
      clients: "clients-section",
      calendar: "calendar-section",
      files: "files-section",
    };
    if (sectionMap[target]) {
      document.getElementById(sectionMap[target]).scrollIntoView({ behavior: "smooth", block: "start" });
      if (target === "chat") els.chatInput.focus();
    } else {
      addBubble("assistant", "האזור הזה עוד לא זמין — בקרוב.");
    }
  });
});

els.newProjectBtn.addEventListener("click", () => {
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
  els.newTaskStartAt.value = "";
  els.newTaskDueAt.value = "";
  els.newTaskTitle.focus();
});
els.newTaskCancel.addEventListener("click", () => {
  els.newTaskModal.hidden = true;
});
els.newTaskSave.addEventListener("click", async () => {
  const title = els.newTaskTitle.value.trim();
  const startValue = els.newTaskStartAt.value;
  const dueValue = els.newTaskDueAt.value;
  if (!title) return;
  if (!startValue || !dueValue) {
    alert("צריך להזין גם זמן התחלה וגם זמן סיום למשימה.");
    return;
  }
  try {
    await apiFetch("/tasks", {
      method: "POST",
      body: JSON.stringify({
        title,
        start_at: new Date(startValue).toISOString(),
        due_at: new Date(dueValue).toISOString(),
      }),
    });
    els.newTaskModal.hidden = true;
    refreshWorkspace();
  } catch (err) {
    alert(err.message);
  }
});

els.newEventBtn.addEventListener("click", () => {
  els.newEventModal.hidden = false;
  els.newEventSummary.value = "";
  els.newEventStart.value = "";
  els.newEventEnd.value = "";
  els.newEventDescription.value = "";
  els.newEventSummary.focus();
});
els.newEventCancel.addEventListener("click", () => {
  els.newEventModal.hidden = true;
});
els.newEventSave.addEventListener("click", async () => {
  const summary = els.newEventSummary.value.trim();
  const startValue = els.newEventStart.value;
  const endValue = els.newEventEnd.value;
  if (!summary || !startValue || !endValue) {
    alert("צריך נושא, זמן התחלה וזמן סיום.");
    return;
  }
  try {
    await apiFetch("/calendar/events", {
      method: "POST",
      body: JSON.stringify({
        summary,
        start_time: new Date(startValue).toISOString(),
        end_time: new Date(endValue).toISOString(),
        description: els.newEventDescription.value.trim() || null,
      }),
    });
    els.newEventModal.hidden = true;
    loadCalendar();
    loadDashboardSummary();
  } catch (err) {
    alert(err.message);
  }
});

els.newFileBtn.addEventListener("click", () => {
  els.newFileModal.hidden = false;
  els.newFileName.value = "";
  els.newFileContent.value = "";
  els.newFileName.focus();
});
els.newFileCancel.addEventListener("click", () => {
  els.newFileModal.hidden = true;
});
els.newFileSave.addEventListener("click", async () => {
  const name = els.newFileName.value.trim();
  if (!name) return;
  try {
    await apiFetch("/files", {
      method: "POST",
      body: JSON.stringify({ name, content: els.newFileContent.value }),
    });
    els.newFileModal.hidden = true;
    loadFiles();
  } catch (err) {
    alert(err.message);
  }
});

let currentShareFileId = null;

els.shareFileCancel.addEventListener("click", () => {
  els.shareFileModal.hidden = true;
});
els.shareFileSave.addEventListener("click", async () => {
  const email = els.shareFileEmail.value.trim();
  if (!currentShareFileId || !email) return;
  try {
    await apiFetch(`/files/${currentShareFileId}/share`, {
      method: "POST",
      body: JSON.stringify({ email, role: els.shareFileRole.value }),
    });
    els.shareFileModal.hidden = true;
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

    renderClientModalProjectGroups(detail.projects, detail.tasks);

    els.clientModal.hidden = false;
  } catch (err) {
    alert(err.message);
  }
}

function buildClientModalTaskRow(task) {
  const row = document.createElement("div");
  row.className = `client-modal-list-item client-modal-task-item${task.status === "done" ? " done" : ""}`;
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = task.status === "done";
  checkbox.addEventListener("change", async (event) => {
    event.stopPropagation();
    await apiFetch(`/tasks/${task.id}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status: checkbox.checked ? "done" : "open" }),
    });
    loadTasks();
    loadDashboardSummary();
    openClientModal(currentClientId);
  });
  const title = document.createElement("span");
  title.className = "client-modal-task-title";
  title.textContent = task.title;
  title.addEventListener("click", () => {
    editTaskOpenedFromClientBoard = true;
    els.clientModal.hidden = true;
    openEditTaskModal(task.id);
  });
  row.appendChild(checkbox);
  row.appendChild(title);
  const badge = dueDateBadge(task);
  if (badge) row.appendChild(badge);
  const deleteBtn = document.createElement("button");
  deleteBtn.type = "button";
  deleteBtn.className = "task-delete-btn";
  deleteBtn.title = "מחיקת משימה";
  deleteBtn.textContent = "✕";
  deleteBtn.addEventListener("click", async (event) => {
    event.stopPropagation();
    if (!confirm(`למחוק את המשימה "${task.title}"?`)) return;
    await apiFetch(`/tasks/${task.id}`, { method: "DELETE" });
    loadTasks();
    loadDashboardSummary();
    openClientModal(currentClientId);
  });
  row.appendChild(deleteBtn);
  return row;
}

function buildClientModalProjectGroup(titleText, statusBadgeHtml, tasks) {
  const group = document.createElement("div");
  group.className = "client-modal-project-group";
  const header = document.createElement("div");
  header.className = statusBadgeHtml
    ? "client-modal-project-header"
    : "client-modal-project-header client-modal-project-header--none";
  header.innerHTML = statusBadgeHtml
    ? `<span>${escapeHtml(titleText)}</span> ${statusBadgeHtml}`
    : `<span>${escapeHtml(titleText)}</span>`;
  group.appendChild(header);

  const tasksContainer = document.createElement("div");
  tasksContainer.className = "client-modal-list";
  if (tasks.length) {
    for (const task of tasks) {
      tasksContainer.appendChild(buildClientModalTaskRow(task));
    }
  } else {
    tasksContainer.innerHTML = '<div class="client-modal-list-empty">אין משימות בפרויקט הזה.</div>';
  }
  group.appendChild(tasksContainer);
  return group;
}

function renderClientModalProjectGroups(projects, tasks) {
  els.clientModalProjects.innerHTML = "";

  const tasksByProject = new Map();
  const unassignedTasks = [];
  for (const task of tasks) {
    if (task.project_id) {
      if (!tasksByProject.has(task.project_id)) tasksByProject.set(task.project_id, []);
      tasksByProject.get(task.project_id).push(task);
    } else {
      unassignedTasks.push(task);
    }
  }

  if (!projects.length && !unassignedTasks.length) {
    els.clientModalProjects.innerHTML =
      '<div class="client-modal-list-empty">אין פרויקטים או משימות משויכים.</div>';
    return;
  }

  for (const project of projects) {
    const statusBadge = `<span class="status-badge status-badge--${project.status}">${STATUS_LABELS[project.status]}</span>`;
    const group = buildClientModalProjectGroup(
      project.name,
      statusBadge,
      tasksByProject.get(project.id) || []
    );
    els.clientModalProjects.appendChild(group);
  }

  if (unassignedTasks.length) {
    els.clientModalProjects.appendChild(
      buildClientModalProjectGroup("ללא פרויקט", "", unassignedTasks)
    );
  }
}

els.clientModalNewTaskAdd.addEventListener("click", async () => {
  const title = els.clientModalNewTaskTitle.value.trim();
  const startValue = els.clientModalNewTaskStartAt.value;
  const dueValue = els.clientModalNewTaskDueAt.value;
  if (!title || !currentClientId) return;
  if (!startValue || !dueValue) {
    alert("צריך להזין גם זמן התחלה וגם זמן סיום למשימה.");
    return;
  }
  try {
    await apiFetch("/tasks", {
      method: "POST",
      body: JSON.stringify({
        title,
        client_id: currentClientId,
        start_at: new Date(startValue).toISOString(),
        due_at: new Date(dueValue).toISOString(),
      }),
    });
    els.clientModalNewTaskTitle.value = "";
    els.clientModalNewTaskStartAt.value = "";
    els.clientModalNewTaskDueAt.value = "";
    loadTasks();
    loadDashboardSummary();
    openClientModal(currentClientId);
  } catch (err) {
    alert(err.message);
  }
});
els.clientModalNewTaskTitle.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    els.clientModalNewTaskAdd.click();
  }
});

els.clientModalNewMeetingBtn.addEventListener("click", () => {
  els.newEventModal.hidden = false;
  els.newEventSummary.value = `פגישה עם ${els.clientModalName.textContent}`;
  els.newEventStart.value = "";
  els.newEventEnd.value = "";
  els.newEventDescription.value = "";
  els.newEventStart.focus();
});

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

els.clientModalDelete.addEventListener("click", async () => {
  if (!currentClientId) return;
  if (!confirm(`למחוק את הלקוח "${els.clientModalName.textContent}"? הפרויקטים והמשימות שלו יישארו, רק הקישור ללקוח יוסר.`)) {
    return;
  }
  try {
    await apiFetch(`/clients/${currentClientId}`, { method: "DELETE" });
    els.clientModal.hidden = true;
    loadClients();
    loadTasks();
    loadProjects();
    loadDashboardSummary();
  } catch (err) {
    alert(err.message);
  }
});

async function loadDashboardSummary() {
  try {
    const summary = await apiFetch("/dashboard/summary");
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

let currentTasks = [];

async function loadTasks() {
  try {
    const [tasks, clientsList] = await Promise.all([apiFetch("/tasks"), apiFetch("/clients")]);
    currentTasks = tasks;
    const clientNameById = new Map(clientsList.map((c) => [c.id, c.name]));
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
      title.addEventListener("click", () => openEditTaskModal(task.id));
      row.appendChild(checkbox);
      row.appendChild(title);
      if (task.client_id && clientNameById.has(task.client_id)) {
        const clientBadge = document.createElement("span");
        clientBadge.className = "task-client-badge";
        clientBadge.textContent = clientNameById.get(task.client_id);
        row.appendChild(clientBadge);
      }
      const badge = dueDateBadge(task);
      if (badge) row.appendChild(badge);
      const deleteBtn = document.createElement("button");
      deleteBtn.type = "button";
      deleteBtn.className = "task-delete-btn";
      deleteBtn.title = "מחיקת משימה";
      deleteBtn.textContent = "✕";
      deleteBtn.addEventListener("click", async (event) => {
        event.stopPropagation();
        if (!confirm(`למחוק את המשימה "${task.title}"?`)) return;
        await apiFetch(`/tasks/${task.id}`, { method: "DELETE" });
        loadTasks();
        loadDashboardSummary();
      });
      row.appendChild(deleteBtn);
      els.tasksList.appendChild(row);
    }
  } catch {
    // not authenticated yet
  }
}

function toDatetimeLocalValue(isoString) {
  const date = new Date(isoString);
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, "0");
  const dd = String(date.getDate()).padStart(2, "0");
  const hh = String(date.getHours()).padStart(2, "0");
  const min = String(date.getMinutes()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}T${hh}:${min}`;
}

let currentEditTaskId = null;
let editTaskOpenedFromClientBoard = false;

async function openEditTaskModal(taskId) {
  const task = currentTasks.find((t) => t.id === taskId);
  if (!task) return;
  currentEditTaskId = taskId;

  try {
    const [projects, clientsList] = await Promise.all([
      apiFetch("/projects"),
      apiFetch("/clients"),
    ]);
    els.editTaskProject.innerHTML =
      '<option value="">ללא פרויקט</option>' +
      projects
        .map((p) => `<option value="${p.id}">${escapeHtml(p.name)}</option>`)
        .join("");
    els.editTaskClient.innerHTML =
      '<option value="">ללא לקוח</option>' +
      clientsList
        .map((c) => `<option value="${c.id}">${escapeHtml(c.name)}</option>`)
        .join("");
  } catch (err) {
    alert(err.message);
    return;
  }

  els.editTaskTitle.value = task.title;
  els.editTaskStartAt.value = task.start_at ? toDatetimeLocalValue(task.start_at) : "";
  els.editTaskDueAt.value = task.due_at ? toDatetimeLocalValue(task.due_at) : "";
  els.editTaskProject.value = task.project_id || "";
  els.editTaskClient.value = task.client_id || "";
  els.editTaskModal.hidden = false;
}

function returnToClientBoardIfNeeded() {
  if (editTaskOpenedFromClientBoard && currentClientId) {
    editTaskOpenedFromClientBoard = false;
    openClientModal(currentClientId);
  }
}

els.editTaskCancel.addEventListener("click", () => {
  els.editTaskModal.hidden = true;
  returnToClientBoardIfNeeded();
});

els.editTaskSave.addEventListener("click", async () => {
  if (!currentEditTaskId) return;
  const title = els.editTaskTitle.value.trim();
  if (!title) return;
  try {
    const startValue = els.editTaskStartAt.value;
    const dueValue = els.editTaskDueAt.value;
    await apiFetch(`/tasks/${currentEditTaskId}`, {
      method: "PATCH",
      body: JSON.stringify({
        title,
        start_at: startValue ? new Date(startValue).toISOString() : null,
        due_at: dueValue ? new Date(dueValue).toISOString() : null,
        project_id: els.editTaskProject.value || null,
        client_id: els.editTaskClient.value || null,
      }),
    });
    els.editTaskModal.hidden = true;
    loadTasks();
    loadProjects();
    loadDashboardSummary();
    returnToClientBoardIfNeeded();
  } catch (err) {
    alert(err.message);
  }
});

els.editTaskDelete.addEventListener("click", async () => {
  if (!currentEditTaskId) return;
  const task = currentTasks.find((t) => t.id === currentEditTaskId);
  if (!confirm(`למחוק את המשימה "${task ? task.title : ""}"?`)) return;
  try {
    await apiFetch(`/tasks/${currentEditTaskId}`, { method: "DELETE" });
    els.editTaskModal.hidden = true;
    loadTasks();
    loadDashboardSummary();
    returnToClientBoardIfNeeded();
  } catch (err) {
    alert(err.message);
  }
});

async function loadClients() {
  try {
    const [clientsList, tasks] = await Promise.all([apiFetch("/clients"), apiFetch("/tasks")]);
    const tasksByClient = new Map();
    for (const t of tasks) {
      if (!t.client_id) continue;
      if (!tasksByClient.has(t.client_id)) tasksByClient.set(t.client_id, []);
      tasksByClient.get(t.client_id).push(t);
    }
    els.clientsTbody.innerHTML = "";
    els.clientsEmpty.hidden = clientsList.length > 0;
    for (const c of clientsList) {
      const tr = document.createElement("tr");
      tr.className = "clickable-row";
      const followup = c.next_follow_up_at
        ? new Date(c.next_follow_up_at).toLocaleDateString("he-IL")
        : "—";
      const clientTasks = tasksByClient.get(c.id) || [];
      const tasksHtml = clientTasks.length
        ? `<div class="clients-table-tasks">${clientTasks
            .map(
              (t) =>
                `<span class="clients-table-task-chip${t.status === "done" ? " done" : ""}">${escapeHtml(t.title)}</span>`
            )
            .join("")}</div>`
        : "";
      tr.innerHTML = `
        <td>${escapeHtml(c.name)}${tasksHtml}</td>
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

function startOfDay(date) {
  const d = new Date(date);
  d.setHours(0, 0, 0, 0);
  return d;
}

function addDays(date, days) {
  const d = new Date(date);
  d.setDate(d.getDate() + days);
  return d;
}

async function loadCalendar() {
  try {
    const start = startOfDay(new Date());
    const end = addDays(start, 1);
    const events = await apiFetch(
      `/calendar/events?time_min=${encodeURIComponent(start.toISOString())}&time_max=${encodeURIComponent(end.toISOString())}`
    );
    els.calendarList.innerHTML = "";
    els.calendarEmpty.hidden = events.length > 0;
    for (const event of events) {
      const row = document.createElement("div");
      row.className = "calendar-item";
      const time = document.createElement("span");
      time.className = "calendar-item-time";
      time.textContent = formatEventTime(event.start, event.end);
      const summary = document.createElement("span");
      summary.className = "calendar-item-summary";
      summary.textContent = event.summary;
      const deleteBtn = document.createElement("button");
      deleteBtn.className = "icon-btn calendar-item-delete";
      deleteBtn.title = "מחק פגישה";
      deleteBtn.innerHTML =
        '<svg viewBox="0 0 24 24"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6h14z"/></svg>';
      deleteBtn.addEventListener("click", async () => {
        try {
          await apiFetch(`/calendar/events/${event.id}`, { method: "DELETE" });
          loadCalendar();
          loadDashboardSummary();
        } catch (err) {
          alert(err.message);
        }
      });
      row.appendChild(time);
      row.appendChild(summary);
      row.appendChild(deleteBtn);
      els.calendarList.appendChild(row);
    }
  } catch {
    // not authenticated yet
  }
}

function formatEventTime(startIso, endIso) {
  const start = new Date(startIso);
  const end = new Date(endIso);
  const dateStr = start.toLocaleDateString("he-IL", { day: "2-digit", month: "2-digit" });
  const startStr = start.toLocaleTimeString("he-IL", { hour: "2-digit", minute: "2-digit" });
  const endStr = end.toLocaleTimeString("he-IL", { hour: "2-digit", minute: "2-digit" });
  return `${dateStr}, ${startStr}–${endStr}`;
}

const WEEKDAY_LABELS = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"];

let currentMonthDate = new Date();

function toLocalDateInputValue(date) {
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, "0");
  const dd = String(date.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}T09:00`;
}

async function renderMonthView() {
  const year = currentMonthDate.getFullYear();
  const month = currentMonthDate.getMonth();
  els.monthViewTitle.textContent = currentMonthDate.toLocaleDateString("he-IL", {
    year: "numeric",
    month: "long",
  });

  const firstOfMonth = new Date(year, month, 1);
  const gridStart = addDays(firstOfMonth, -firstOfMonth.getDay());
  const lastOfMonth = new Date(year, month + 1, 0);
  const gridEnd = addDays(lastOfMonth, 6 - lastOfMonth.getDay() + 1);

  let events = [];
  try {
    events = await apiFetch(
      `/calendar/events?time_min=${encodeURIComponent(gridStart.toISOString())}&time_max=${encodeURIComponent(gridEnd.toISOString())}`
    );
  } catch {
    // not authenticated yet
  }

  const eventsByDay = {};
  for (const event of events) {
    const key = startOfDay(new Date(event.start)).toDateString();
    (eventsByDay[key] = eventsByDay[key] || []).push(event);
  }

  els.monthGrid.innerHTML = "";
  for (const label of WEEKDAY_LABELS) {
    const header = document.createElement("div");
    header.className = "month-weekday";
    header.textContent = label;
    els.monthGrid.appendChild(header);
  }

  const today = startOfDay(new Date()).toDateString();
  let cursor = gridStart;
  while (cursor <= gridEnd) {
    const cell = document.createElement("div");
    const isOutside = cursor.getMonth() !== month;
    cell.className = "month-day-cell";
    if (isOutside) cell.classList.add("month-day-cell--outside");
    if (cursor.toDateString() === today) cell.classList.add("month-day-cell--today");

    const dayNumber = document.createElement("div");
    dayNumber.className = "month-day-number";
    dayNumber.textContent = cursor.getDate();
    cell.appendChild(dayNumber);

    const dayEvents = eventsByDay[cursor.toDateString()] || [];
    const shown = dayEvents.slice(0, 3);
    for (const event of shown) {
      const eventEl = document.createElement("div");
      eventEl.className = "month-day-event";
      eventEl.textContent = event.summary;
      cell.appendChild(eventEl);
    }
    if (dayEvents.length > shown.length) {
      const more = document.createElement("div");
      more.className = "month-day-more";
      more.textContent = `+${dayEvents.length - shown.length} נוספות`;
      cell.appendChild(more);
    }

    const cellDate = new Date(cursor);
    cell.addEventListener("click", () => {
      els.calendarMonthModal.hidden = true;
      els.newEventModal.hidden = false;
      els.newEventSummary.value = "";
      els.newEventStart.value = toLocalDateInputValue(cellDate);
      els.newEventEnd.value = toLocalDateInputValue(cellDate);
      els.newEventDescription.value = "";
      els.newEventSummary.focus();
    });

    els.monthGrid.appendChild(cell);
    cursor = addDays(cursor, 1);
  }
}

els.showMonthBtn.addEventListener("click", () => {
  currentMonthDate = new Date();
  els.calendarMonthModal.hidden = false;
  renderMonthView();
});
els.monthViewClose.addEventListener("click", () => {
  els.calendarMonthModal.hidden = true;
});
els.monthPrevBtn.addEventListener("click", () => {
  currentMonthDate = new Date(currentMonthDate.getFullYear(), currentMonthDate.getMonth() - 1, 1);
  renderMonthView();
});
els.monthNextBtn.addEventListener("click", () => {
  currentMonthDate = new Date(currentMonthDate.getFullYear(), currentMonthDate.getMonth() + 1, 1);
  renderMonthView();
});

async function loadFiles() {
  try {
    const files = await apiFetch("/files?max_results=8&order_by=viewedByMeTime%20desc");
    els.filesTbody.innerHTML = "";
    els.filesEmpty.hidden = files.length > 0;
    for (const file of files) {
      const tr = document.createElement("tr");
      const modified = file.modified_time
        ? new Date(file.modified_time).toLocaleDateString("he-IL")
        : "—";
      const nameCell = file.web_view_link
        ? `<a href="${file.web_view_link}" target="_blank" rel="noopener">${escapeHtml(file.name)}</a>`
        : escapeHtml(file.name);
      tr.innerHTML = `
        <td>${nameCell}</td>
        <td>${escapeHtml(file.mime_type)}</td>
        <td>${modified}</td>
        <td></td>
      `;
      const shareBtn = document.createElement("button");
      shareBtn.className = "btn btn--ghost file-share-btn";
      shareBtn.textContent = "שתף";
      shareBtn.addEventListener("click", () => {
        currentShareFileId = file.id;
        els.shareFileEmail.value = "";
        els.shareFileRole.value = "reader";
        els.shareFileModal.hidden = false;
        els.shareFileEmail.focus();
      });
      tr.lastElementChild.appendChild(shareBtn);
      els.filesTbody.appendChild(tr);
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
  loadCalendar();
  loadFiles();
  loadActivity();
  loadNotifications();
}

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {
      // Non-fatal — the app works fine without it, just without an install prompt.
    });
  });
}

let deferredInstallPrompt = null;

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  els.installAppBtn.hidden = false;
});

els.installAppBtn.addEventListener("click", async () => {
  if (!deferredInstallPrompt) return;
  deferredInstallPrompt.prompt();
  await deferredInstallPrompt.userChoice;
  deferredInstallPrompt = null;
  els.installAppBtn.hidden = true;
});

window.addEventListener("appinstalled", () => {
  els.installAppBtn.hidden = true;
  deferredInstallPrompt = null;
});

(async function init() {
  await checkAuth();
  refreshWorkspace();
})();
