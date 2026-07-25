const API_BASE = "/api/v1";

const els = {
  authStatus: document.getElementById("auth-status"),
  greetingName: document.getElementById("greeting-name"),
  greetingPhrase: document.getElementById("greeting-phrase"),
  greetingSub: document.getElementById("greeting-sub"),
  userName: document.getElementById("user-name"),
  userAvatar: document.getElementById("user-avatar"),
  chatForm: document.getElementById("chat-form"),
  chatInput: document.getElementById("chat-input"),
  voiceInputBtn: document.getElementById("voice-input-btn"),
  speakRepliesBtn: document.getElementById("speak-replies-btn"),
  chatWindow: document.getElementById("chat-window"),
  thoughtInput: document.getElementById("thought-input"),
  thoughtVoiceBtn: document.getElementById("thought-voice-btn"),
  thoughtSaveBtn: document.getElementById("thought-save-btn"),
  thoughtsList: document.getElementById("thoughts-list"),
  thoughtsEmpty: document.getElementById("thoughts-empty"),
  thoughtsShowAllBtn: document.getElementById("thoughts-show-all-btn"),
  navBadgeTasks: document.getElementById("nav-badge-tasks"),
  navBadgeClients: document.getElementById("nav-badge-clients"),
  tasksList: document.getElementById("tasks-list"),
  tasksEmpty: document.getElementById("tasks-empty"),
  tasksShowAllBtn: document.getElementById("tasks-show-all-btn"),
  listModal: document.getElementById("list-modal"),
  listModalTitle: document.getElementById("list-modal-title"),
  listModalBody: document.getElementById("list-modal-body"),
  listModalClose: document.getElementById("list-modal-close"),
  edithStatus: document.getElementById("edith-status"),
  shell: document.getElementById("shell"),
  sidebarToggle: document.getElementById("sidebar-toggle"),
  sidebarBackdrop: document.getElementById("sidebar-backdrop"),
  clientsGrid: document.getElementById("clients-grid"),
  clientsEmpty: document.getElementById("clients-empty"),
  clientsShowAllBtn: document.getElementById("clients-show-all-btn"),
  newClientBtn: document.getElementById("new-client-btn"),
  newClientModal: document.getElementById("new-client-modal"),
  newClientName: document.getElementById("new-client-name"),
  newClientSave: document.getElementById("new-client-save"),
  newClientCancel: document.getElementById("new-client-cancel"),
  clientModal: document.getElementById("client-modal"),
  clientModalName: document.getElementById("client-modal-name"),
  clientModalAvatar: document.getElementById("client-modal-avatar"),
  clientModalLogoInput: document.getElementById("client-modal-logo-input"),
  clientEditName: document.getElementById("client-edit-name"),
  clientEditEmail: document.getElementById("client-edit-email"),
  clientEditPhone: document.getElementById("client-edit-phone"),
  clientEditNotes: document.getElementById("client-edit-notes"),
  clientModalAttachments: document.getElementById("client-modal-attachments"),
  clientModalAttachmentsEmpty: document.getElementById("client-modal-attachments-empty"),
  clientModalAttachmentInput: document.getElementById("client-modal-attachment-input"),
  clientModalProjects: document.getElementById("client-modal-projects"),
  clientModalSave: document.getElementById("client-modal-save"),
  clientModalCancel: document.getElementById("client-modal-cancel"),
  clientModalDelete: document.getElementById("client-modal-delete"),
  clientModalNewMeetingBtn: document.getElementById("client-modal-new-meeting-btn"),
  clientModalNewProjectName: document.getElementById("client-modal-new-project-name"),
  clientModalNewProjectType: document.getElementById("client-modal-new-project-type"),
  clientModalNewProjectAdd: document.getElementById("client-modal-new-project-add"),
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
  editTaskClientOptions: document.getElementById("edit-task-client-options"),
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
  financeContent: document.getElementById("finance-content"),
  financeSummary: document.getElementById("finance-summary"),
  financeIncomeList: document.getElementById("finance-income-list"),
  financeIncomeEmpty: document.getElementById("finance-income-empty"),
  financeIncomeShowAllBtn: document.getElementById("finance-income-show-all-btn"),
  financeExpensesList: document.getElementById("finance-expenses-list"),
  financeExpensesEmpty: document.getElementById("finance-expenses-empty"),
  financeExpensesShowAllBtn: document.getElementById("finance-expenses-show-all-btn"),
  financeEmpty: document.getElementById("finance-empty"),
  cashFlowCard: document.getElementById("cash-flow-card"),
  cashFlowEmpty: document.getElementById("cash-flow-empty"),
  cashFlowBalance: document.getElementById("cash-flow-balance"),
  cashFlowFixedExpenses: document.getElementById("cash-flow-fixed-expenses"),
  cashFlowDues: document.getElementById("cash-flow-dues"),
  cashFlowProjected: document.getElementById("cash-flow-projected"),
  newEventBtn: document.getElementById("new-event-btn"),
  newEventModal: document.getElementById("new-event-modal"),
  newEventSummary: document.getElementById("new-event-summary"),
  newEventStart: document.getElementById("new-event-start"),
  newEventEnd: document.getElementById("new-event-end"),
  newEventDescription: document.getElementById("new-event-description"),
  newEventSave: document.getElementById("new-event-save"),
  newEventCancel: document.getElementById("new-event-cancel"),
  gmailList: document.getElementById("gmail-list"),
  gmailEmpty: document.getElementById("gmail-empty"),
  gmailShowAllBtn: document.getElementById("gmail-show-all-btn"),
  filesTbody: document.getElementById("files-tbody"),
  filesEmpty: document.getElementById("files-empty"),
  filesShowAllBtn: document.getElementById("files-show-all-btn"),
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
  dashboardView: document.getElementById("dashboard-view"),
  myDayView: document.getElementById("my-day-view"),
  focusView: document.getElementById("focus-view"),
  myDayInboxInput: document.getElementById("my-day-inbox-input"),
  myDayInboxUrgent: document.getElementById("my-day-inbox-urgent"),
  myDayInboxAdd: document.getElementById("my-day-inbox-add"),
  myDayGoalInput: document.getElementById("my-day-goal-input"),
  myDayGoalAdd: document.getElementById("my-day-goal-add"),
  myDayGoalsList: document.getElementById("my-day-goals-list"),
  myDayPicker: document.getElementById("my-day-picker"),
  myDayLockBtn: document.getElementById("my-day-lock-btn"),
  myDayPickerSection: document.getElementById("my-day-picker-section"),
  myDayLockedSection: document.getElementById("my-day-locked-section"),
  myDayLockedTasks: document.getElementById("my-day-locked-tasks"),
  myDaySummaryBtn: document.getElementById("my-day-summary-btn"),
  myDaySummaryContent: document.getElementById("my-day-summary-content"),
  urgentSwapModal: document.getElementById("urgent-swap-modal"),
  urgentSwapBumpedSelect: document.getElementById("urgent-swap-bumped-select"),
  urgentSwapDeliverable: document.getElementById("urgent-swap-deliverable"),
  urgentSwapNextStep: document.getElementById("urgent-swap-next-step"),
  urgentSwapMinutes: document.getElementById("urgent-swap-minutes"),
  urgentSwapImportance: document.getElementById("urgent-swap-importance"),
  urgentSwapGoal: document.getElementById("urgent-swap-goal"),
  urgentSwapSave: document.getElementById("urgent-swap-save"),
  urgentSwapCancel: document.getElementById("urgent-swap-cancel"),
  focusTaskTitle: document.getElementById("focus-task-title"),
  focusDeliverable: document.getElementById("focus-deliverable"),
  focusTimer: document.getElementById("focus-timer"),
  focusNextStepInput: document.getElementById("focus-next-step-input"),
  focusDoneBtn: document.getElementById("focus-done-btn"),
  focusStuckBtn: document.getElementById("focus-stuck-btn"),
  focusBreakBtn: document.getElementById("focus-break-btn"),
  stuckReasonModal: document.getElementById("stuck-reason-modal"),
  stuckReasonCancel: document.getElementById("stuck-reason-cancel"),
};

let isAuthenticated = false;
let currentUserEmail = "";

const PROJECT_TYPE_LABELS = { consulting: "ייעוץ", mentoring: "ליווי", setup: "הקמה" };

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
  workspace_update_project_type: "עדכן סוג פרויקט",
  workspace_list_projects: "הציג פרויקטים",
  workspace_create_task: "יצר משימה חדשה",
  workspace_update_task_status: "עדכן סטטוס משימה",
  workspace_set_task_due_date: "עדכן תאריך יעד למשימה",
  workspace_list_tasks: "הציג משימות",
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

function setAppMode(mode) {
  document.body.dataset.appMode = mode;
  els.dashboardView.hidden = mode !== "dashboard";
  els.myDayView.hidden = mode !== "my-day";
  els.focusView.hidden = mode !== "focus";
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

const MOTIVATIONAL_QUOTES = [
  "אני כאן כדי להוציא דברים מהכוח אל הפועל.",
  "כל צעד קטן היום הוא ניצחון גדול מחר.",
  "המשמעת עושה את ההבדל בין חלום למציאות.",
  "היום הוא ההזדמנות שלך להתקדם עוד קצת.",
  "עקביות מנצחת מוטיבציה רגעית.",
  "כל משימה שסגרת היום היא לבנה בבניין שלך.",
  "לא חייבים להרגיש מוכנים כדי להתחיל, מספיק להתחיל כדי להרגיש מוכנים.",
  "ההצלחה נבנית מהחלטות קטנות שחוזרות על עצמן כל יום.",
  "התקדמות, לא שלמות.",
  "בוס טוב מתמקד במה שבשליטתו — וזה מספיק כדי לנצח את היום.",
  "כל יום הוא דף חדש לכתוב עליו הישג.",
  "מי שממשיך לצעוד, מגיע.",
];

function motivationalQuoteOfTheDay() {
  const now = new Date();
  const startOfYear = new Date(now.getFullYear(), 0, 0);
  const dayOfYear = Math.floor((now - startOfYear) / 86400000);
  return MOTIVATIONAL_QUOTES[dayOfYear % MOTIVATIONAL_QUOTES.length];
}

function speakText(text) {
  if (!("speechSynthesis" in window) || !text) return;
  // Calling speak() in the same tick right after cancel() is a known
  // Chrome/Android quirk that silently drops the new utterance — deferring
  // to the next tick reliably avoids it.
  window.speechSynthesis.cancel();
  setTimeout(() => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "he-IL";
    window.speechSynthesis.speak(utterance);
  }, 60);
}

let hasSpokenGreeting = false;

function speakGreeting(greeting) {
  if (hasSpokenGreeting) return;
  hasSpokenGreeting = true;
  speakText(`${greeting}, בוס. טוב שחזרת.`);
}

const SPEAK_REPLIES_STORAGE_KEY = "idea_os_speak_replies";
let speakRepliesEnabled = localStorage.getItem(SPEAK_REPLIES_STORAGE_KEY) === "true";

function updateSpeakRepliesBtn() {
  if (!("speechSynthesis" in window)) {
    els.speakRepliesBtn.hidden = true;
    return;
  }
  els.speakRepliesBtn.classList.toggle("active", speakRepliesEnabled);
  els.speakRepliesBtn.title = speakRepliesEnabled
    ? "הקראת תשובות Edith בקול (פעיל — לחץ לכיבוי)"
    : "הקראת תשובות Edith בקול";
}

els.speakRepliesBtn.addEventListener("click", () => {
  speakRepliesEnabled = !speakRepliesEnabled;
  localStorage.setItem(SPEAK_REPLIES_STORAGE_KEY, String(speakRepliesEnabled));
  updateSpeakRepliesBtn();
  if (!speakRepliesEnabled) window.speechSynthesis.cancel();
});

updateSpeakRepliesBtn();

async function checkAuth() {
  try {
    const user = await apiFetch("/auth/google/me");
    isAuthenticated = true;
    currentUserEmail = user.email || "";
    els.authStatus.innerHTML = `מחובר כ-${user.name}`;
    const greeting = timeOfDayGreeting();
    els.greetingPhrase.textContent = greeting;
    els.greetingName.textContent = user.name;
    els.greetingSub.textContent = motivationalQuoteOfTheDay();
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
    if (speakRepliesEnabled) speakText(data.reply);
    addToolTrace(data.tool_calls_made);
    refreshWorkspace();
  } catch (err) {
    addBubble("error", err.message);
  }
}

els.chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  stopVoiceCaptureFor(els.chatInput);
  const text = els.chatInput.value.trim();
  if (!text) return;
  els.chatInput.value = "";
  sendCommand(text);
});

const SpeechRecognitionCtor = window.SpeechRecognition || window.webkitSpeechRecognition;
let voiceRecognition = null;
let isRecording = false;
let voiceFinalTranscript = "";
let voiceTargetInput = null;
let voiceTargetBtn = null;

// If the given input is actively being dictated into, stop the recognizer
// and immediately forget the target — otherwise a speech result already in
// flight can land just after the caller clears the input (e.g. on submit)
// and silently refill it right back.
function stopVoiceCaptureFor(inputEl) {
  if (voiceTargetInput !== inputEl) return;
  if (isRecording) {
    isRecording = false;
    voiceRecognition.stop();
  }
  // Null the target even if recording had just stopped on its own — a
  // final "result" event can still be in flight for a moment after stop().
  voiceTargetInput = null;
}

if (SpeechRecognitionCtor) {
  els.voiceInputBtn.hidden = false;
  els.thoughtVoiceBtn.hidden = false;

  voiceRecognition = new SpeechRecognitionCtor();
  voiceRecognition.lang = "he-IL";
  // continuous:true triggers a well-known Android Chrome bug where the
  // engine periodically restarts internally and re-emits already-final
  // results, tripling the transcript. Each recognition session only
  // captures one utterance instead; "end" restarts it manually so dictation
  // still feels continuous, without that duplication bug.
  voiceRecognition.continuous = false;
  voiceRecognition.interimResults = true;

  voiceRecognition.addEventListener("result", (event) => {
    if (!voiceTargetInput) return;
    let interimTranscript = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const result = event.results[i];
      if (result.isFinal) {
        voiceFinalTranscript += result[0].transcript;
      } else {
        interimTranscript += result[0].transcript;
      }
    }
    voiceTargetInput.value = voiceFinalTranscript + interimTranscript;
  });

  voiceRecognition.addEventListener("error", (event) => {
    if (event.error === "not-allowed" || event.error === "service-not-allowed") {
      alert("אין הרשאה למיקרופון. אפשר הרשאת מיקרופון לאתר בהגדרות הדפדפן ונסה שוב.");
      isRecording = false;
    } else if (event.error !== "no-speech" && event.error !== "aborted") {
      alert("לא הצלחתי להקליט. נסה שוב.");
      isRecording = false;
    }
  });

  voiceRecognition.addEventListener("end", () => {
    if (isRecording) {
      voiceRecognition.start();
      return;
    }
    voiceTargetBtn.classList.remove("recording");
  });

  const toggleVoiceCapture = (inputEl, btnEl) => {
    if (isRecording) {
      isRecording = false;
      voiceRecognition.stop();
      return;
    }
    voiceFinalTranscript = "";
    inputEl.value = "";
    voiceTargetInput = inputEl;
    voiceTargetBtn = btnEl;
    isRecording = true;
    btnEl.classList.add("recording");
    voiceRecognition.start();
  };

  els.voiceInputBtn.addEventListener("click", () => {
    toggleVoiceCapture(els.chatInput, els.voiceInputBtn);
  });
  els.thoughtVoiceBtn.addEventListener("click", () => {
    toggleVoiceCapture(els.thoughtInput, els.thoughtVoiceBtn);
  });
}

async function speakQuickOverview() {
  let tasks;
  try {
    tasks = await apiFetch("/tasks");
  } catch {
    return;
  }
  const openTasks = tasks.filter((t) => t.status !== "done");
  let text;
  if (openTasks.length === 0) {
    text = "אין לך משימות פתוחות כרגע. כל הכבוד בוס!";
  } else {
    const now = new Date();
    const overdue = openTasks.filter((t) => t.due_at && new Date(t.due_at) < now);
    text = `יש לך ${openTasks.length} משימות פתוחות: ${openTasks.map((t) => t.title).join(", ")}.`;
    if (overdue.length > 0) {
      text += ` שים לב, ${overdue.length} מהן באיחור: ${overdue.map((t) => t.title).join(", ")}.`;
    }
  }
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "he-IL";
  window.speechSynthesis.speak(utterance);
}

document.querySelectorAll(".nav-item").forEach((item) => {
  if (item.tagName === "A") return; // real links (e.g. Gmail) navigate on their own
  item.addEventListener("click", () => {
    const target = item.dataset.nav;
    setNavActive(target);
    closeSidebar();
    if (target === "my-day") {
      setAppMode("my-day");
      refreshMyDay();
      return;
    }
    setAppMode("dashboard");
    const sectionMap = {
      chat: "chat-form",
      overview: "greeting",
      tasks: "tasks-section",
      clients: "clients-section",
      calendar: "calendar-section",
      finance: "finance-section",
      files: "files-section",
      thoughts: "thoughts-section",
    };
    if (target === "overview") {
      document.getElementById(sectionMap[target]).scrollIntoView({ behavior: "smooth", block: "start" });
      speakQuickOverview();
    } else if (sectionMap[target]) {
      document.getElementById(sectionMap[target]).scrollIntoView({ behavior: "smooth", block: "start" });
      if (target === "chat") els.chatInput.focus();
      if (target === "finance") {
        loadFinance();
        loadCashFlow();
      }
    } else {
      addBubble("assistant", "האזור הזה עוד לא זמין — בקרוב.");
    }
  });
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

function openListModal(title, items, buildFn, { emptyText = "אין פריטים להצגה.", theadHtml } = {}) {
  els.listModalTitle.textContent = title;
  els.listModalBody.innerHTML = "";
  if (items.length === 0) {
    els.listModalBody.innerHTML = `<div class="empty-state">${escapeHtml(emptyText)}</div>`;
  } else if (theadHtml) {
    const table = document.createElement("table");
    table.className = "files-table";
    table.innerHTML = `<thead>${theadHtml}</thead>`;
    const tbody = document.createElement("tbody");
    for (const item of items) tbody.appendChild(buildFn(item));
    table.appendChild(tbody);
    els.listModalBody.appendChild(table);
  } else {
    for (const item of items) els.listModalBody.appendChild(buildFn(item));
  }
  els.listModal.hidden = false;
}

els.listModalClose.addEventListener("click", () => {
  els.listModal.hidden = true;
});

// Renders only the first `limit` items in `container`; wires `showAllBtn`
// (shown only when there are more) to open the full list in `list-modal`,
// since re-fetching everything just to render 3 of them would be wasteful.
function renderWithShowAll(
  container,
  items,
  buildFn,
  { limit = 3, showAllBtn, title, emptyText, theadHtml } = {}
) {
  container.innerHTML = "";
  for (const item of items.slice(0, limit)) container.appendChild(buildFn(item));
  if (showAllBtn) {
    showAllBtn.hidden = items.length <= limit;
    showAllBtn.onclick = () => openListModal(title, items, buildFn, { emptyText, theadHtml });
  }
}

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
    loadDashboardSummary();
  } catch (err) {
    alert(err.message);
  }
});

let currentClientId = null;

function setClientModalAvatar(client) {
  const html = client.has_logo
    ? `<img id="client-modal-avatar" class="client-avatar client-avatar--large" src="${API_BASE}/clients/${client.id}/logo" alt="" />`
    : `<span id="client-modal-avatar" class="client-avatar client-avatar--large client-avatar--placeholder">${escapeHtml(client.name ? client.name.charAt(0).toUpperCase() : "?")}</span>`;
  els.clientModalAvatar.outerHTML = html;
  els.clientModalAvatar = document.getElementById("client-modal-avatar");
}

async function openClientModal(clientId) {
  try {
    const detail = await apiFetch(`/clients/${clientId}`);
    currentClientId = clientId;
    els.clientModalName.textContent = detail.client.name;
    setClientModalAvatar(detail.client);
    els.clientEditName.value = detail.client.name;
    els.clientEditEmail.value = detail.client.email || "";
    els.clientEditPhone.value = detail.client.phone || "";
    els.clientEditNotes.value = detail.client.notes || "";

    renderClientModalProjectGroups(detail.projects, detail.tasks);
    renderClientModalAttachments(detail.attachments);

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

function buildClientModalProjectGroup(project, tasks) {
  const group = document.createElement("div");
  group.className = "client-modal-project-group";
  const header = document.createElement("div");
  header.className = project
    ? "client-modal-project-header"
    : "client-modal-project-header client-modal-project-header--none";

  const titleSpan = document.createElement("span");
  titleSpan.textContent = project ? project.name : "ללא פרויקט";
  header.appendChild(titleSpan);

  if (project) {
    const typeSelect = document.createElement("select");
    typeSelect.className = "project-type-select";
    for (const [value, label] of Object.entries(PROJECT_TYPE_LABELS)) {
      const opt = document.createElement("option");
      opt.value = value;
      opt.textContent = label;
      if (value === project.type) opt.selected = true;
      typeSelect.appendChild(opt);
    }
    typeSelect.addEventListener("change", async () => {
      try {
        await apiFetch(`/projects/${project.id}/type`, {
          method: "PATCH",
          body: JSON.stringify({ type: typeSelect.value }),
        });
        loadClients();
      } catch (err) {
        alert(err.message);
      }
    });
    header.appendChild(typeSelect);

    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "task-delete-btn";
    deleteBtn.title = "מחיקת פרויקט";
    deleteBtn.textContent = "✕";
    deleteBtn.addEventListener("click", async () => {
      if (
        !confirm(
          `למחוק את הפרויקט "${project.name}"? המשימות שלו יישארו, רק הקישור לפרויקט יוסר.`
        )
      ) {
        return;
      }
      try {
        await apiFetch(`/projects/${project.id}`, { method: "DELETE" });
        loadTasks();
        loadClients();
        openClientModal(currentClientId);
      } catch (err) {
        alert(err.message);
      }
    });
    header.appendChild(deleteBtn);
  }

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
    const group = buildClientModalProjectGroup(project, tasksByProject.get(project.id) || []);
    els.clientModalProjects.appendChild(group);
  }

  if (unassignedTasks.length) {
    els.clientModalProjects.appendChild(buildClientModalProjectGroup(null, unassignedTasks));
  }
}

els.clientModalNewProjectAdd.addEventListener("click", async () => {
  const name = els.clientModalNewProjectName.value.trim();
  const type = els.clientModalNewProjectType.value;
  if (!name || !currentClientId) return;
  try {
    await apiFetch("/projects", {
      method: "POST",
      body: JSON.stringify({ name, client_id: currentClientId, type }),
    });
    els.clientModalNewProjectName.value = "";
    loadClients();
    openClientModal(currentClientId);
  } catch (err) {
    alert(err.message);
  }
});
els.clientModalNewProjectName.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    els.clientModalNewProjectAdd.click();
  }
});

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
    await apiFetch(`/clients/${currentClientId}`, {
      method: "PATCH",
      body: JSON.stringify({
        name: els.clientEditName.value.trim() || null,
        email: els.clientEditEmail.value.trim() || null,
        phone: els.clientEditPhone.value.trim() || null,
        notes: els.clientEditNotes.value.trim() || null,
      }),
    });
    els.clientModal.hidden = true;
    loadClients();
  } catch (err) {
    alert(err.message);
  }
});

async function uploadClientLogo(clientId, file) {
  const formData = new FormData();
  formData.append("logo", file);
  const response = await fetch(`${API_BASE}/clients/${clientId}/logo`, {
    method: "POST",
    credentials: "include",
    body: formData,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: response.statusText }));
    throw new Error(error.message || "העלאת הלוגו נכשלה");
  }
  return response.json();
}

els.clientModalLogoInput.addEventListener("change", async () => {
  const file = els.clientModalLogoInput.files[0];
  if (!file || !currentClientId) return;
  try {
    const updated = await uploadClientLogo(currentClientId, file);
    setClientModalAvatar(updated);
    loadClients();
  } catch (err) {
    alert(err.message);
  } finally {
    els.clientModalLogoInput.value = "";
  }
});

function renderClientModalAttachments(attachments) {
  els.clientModalAttachments.innerHTML = "";
  els.clientModalAttachmentsEmpty.hidden = attachments.length > 0;
  for (const attachment of attachments) {
    const row = document.createElement("div");
    row.className = "client-modal-list-item client-modal-attachment-item";

    const icon = document.createElement("span");
    icon.className = "client-modal-attachment-icon";
    icon.textContent = attachment.mime_type.startsWith("image/") ? "🖼️" : "📄";
    row.appendChild(icon);

    const link = document.createElement("a");
    link.className = "client-modal-attachment-name";
    link.href = `${API_BASE}/clients/${currentClientId}/attachments/${attachment.id}`;
    link.target = "_blank";
    link.rel = "noopener";
    link.textContent = attachment.filename;
    row.appendChild(link);

    const time = document.createElement("span");
    time.className = "client-modal-attachment-time";
    time.textContent = relativeTime(attachment.created_at);
    row.appendChild(time);

    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "task-delete-btn";
    deleteBtn.title = "מחיקת קובץ";
    deleteBtn.textContent = "✕";
    deleteBtn.addEventListener("click", async () => {
      if (!confirm(`למחוק את "${attachment.filename}"?`)) return;
      try {
        await apiFetch(`/clients/${currentClientId}/attachments/${attachment.id}`, {
          method: "DELETE",
        });
        openClientModal(currentClientId);
      } catch (err) {
        alert(err.message);
      }
    });
    row.appendChild(deleteBtn);

    els.clientModalAttachments.appendChild(row);
  }
}

async function uploadClientAttachment(clientId, file) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await fetch(`${API_BASE}/clients/${clientId}/attachments`, {
    method: "POST",
    credentials: "include",
    body: formData,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: response.statusText }));
    throw new Error(error.message || "העלאת הקובץ נכשלה");
  }
  return response.json();
}

els.clientModalAttachmentInput.addEventListener("change", async () => {
  const files = Array.from(els.clientModalAttachmentInput.files);
  if (!files.length || !currentClientId) return;
  try {
    for (const file of files) {
      await uploadClientAttachment(currentClientId, file);
    }
    openClientModal(currentClientId);
  } catch (err) {
    alert(err.message);
  } finally {
    els.clientModalAttachmentInput.value = "";
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
    loadDashboardSummary();
  } catch (err) {
    alert(err.message);
  }
});

async function loadDashboardSummary() {
  try {
    const summary = await apiFetch("/dashboard/summary");
    els.navBadgeTasks.textContent = summary.open_tasks;
    els.navBadgeClients.textContent = summary.total_clients;
  } catch {
    // not authenticated yet — leave placeholders
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

function sortTasksForDisplay(tasks) {
  const dueTime = (task) => (task.due_at ? new Date(task.due_at).getTime() : Infinity);
  const open = tasks.filter((t) => t.status !== "done").sort((a, b) => dueTime(a) - dueTime(b));
  const done = tasks
    .filter((t) => t.status === "done")
    .sort((a, b) => dueTime(b) - dueTime(a));
  return { open, done };
}

function computeTimerDeadline(task) {
  if (!task.start_at || !task.due_at || !task.timer_started_at) return null;
  const duration = new Date(task.due_at).getTime() - new Date(task.start_at).getTime();
  return new Date(task.timer_started_at).getTime() + duration;
}

function formatCountdown(ms) {
  const totalSeconds = Math.max(0, Math.round(ms / 1000));
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${String(seconds).padStart(2, "0")}`;
}

function requestNotificationPermissionOnce() {
  if (!("Notification" in window)) return;
  if (Notification.permission === "default") {
    Notification.requestPermission();
  }
}

function showTimerExpiredNotification(title) {
  if (!("Notification" in window) || Notification.permission !== "granted") return;
  new Notification("נגמר הזמן למשימה", { body: title || "" });
}

function playTimerExpiredSound() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const oscillator = ctx.createOscillator();
    const gain = ctx.createGain();
    oscillator.type = "sine";
    oscillator.frequency.value = 880;
    gain.gain.setValueAtTime(0.15, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6);
    oscillator.connect(gain);
    gain.connect(ctx.destination);
    oscillator.start();
    oscillator.stop(ctx.currentTime + 0.6);
  } catch {
    // sound is a nice-to-have — never let it break the timer itself
  }
}

function tickTaskTimers() {
  const now = Date.now();
  document.querySelectorAll(".task-timer").forEach((el) => {
    if (el.dataset.alerted === "true") return;
    const remaining = Number(el.dataset.deadline) - now;
    if (remaining > 0) {
      el.textContent = formatCountdown(remaining);
      return;
    }
    el.dataset.alerted = "true";
    el.textContent = "⏰ נגמר הזמן!";
    const card = el.closest(".task-card");
    if (card) card.classList.add("task-card--timer-expired");
    playTimerExpiredSound();
    showTimerExpiredNotification(el.dataset.taskTitle || "");
  });
}

function buildTaskTimerRow(task) {
  const row = document.createElement("div");
  row.className = "task-timer-row";

  if (task.status === "in_progress" && task.timer_started_at) {
    const deadline = computeTimerDeadline(task);
    const countdown = document.createElement("span");
    countdown.className = "task-timer";
    countdown.dataset.deadline = String(deadline);
    countdown.dataset.taskTitle = task.title;
    countdown.textContent = formatCountdown(deadline - Date.now());
    row.appendChild(countdown);

    const stopBtn = document.createElement("button");
    stopBtn.type = "button";
    stopBtn.className = "task-timer-btn task-timer-btn--stop";
    stopBtn.textContent = "⏹ עצירה";
    stopBtn.addEventListener("click", async (event) => {
      event.stopPropagation();
      await apiFetch(`/tasks/${task.id}/timer/stop`, { method: "POST" });
      loadTasks();
    });
    row.appendChild(stopBtn);
  } else {
    const startBtn = document.createElement("button");
    startBtn.type = "button";
    startBtn.className = "task-timer-btn task-timer-btn--start";
    startBtn.textContent = "▶ התחלה";
    startBtn.addEventListener("click", async (event) => {
      event.stopPropagation();
      requestNotificationPermissionOnce();
      await apiFetch(`/tasks/${task.id}/timer/start`, { method: "POST" });
      loadTasks();
    });
    row.appendChild(startBtn);
  }
  return row;
}

function buildTaskCard(task, clientNameById) {
  const isTiming = task.status === "in_progress" && task.timer_started_at;
  const card = document.createElement("div");
  card.className = `task-card${task.status === "done" ? " done" : ""}${
    isTiming ? " task-card--timing" : ""
  }`;

  const top = document.createElement("div");
  top.className = "task-card-top";
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
  top.appendChild(checkbox);
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
  top.appendChild(deleteBtn);
  card.appendChild(top);

  const title = document.createElement("span");
  title.className = "task-title";
  title.textContent = task.title;
  title.addEventListener("click", () => openEditTaskModal(task.id));
  card.appendChild(title);

  if (task.status !== "done" && task.start_at && task.due_at) {
    card.appendChild(buildTaskTimerRow(task));
  }

  const footer = document.createElement("div");
  footer.className = "task-card-footer";
  if (task.client_id && clientNameById.has(task.client_id)) {
    const clientBadge = document.createElement("span");
    clientBadge.className = "task-client-badge";
    clientBadge.textContent = clientNameById.get(task.client_id);
    footer.appendChild(clientBadge);
  }
  const badge = dueDateBadge(task);
  footer.appendChild(badge || Object.assign(document.createElement("span"), {
    className: "task-due task-due--none",
    textContent: "ללא תאריך",
  }));
  card.appendChild(footer);

  return card;
}

async function loadTasks() {
  try {
    const [tasks, clientsList] = await Promise.all([apiFetch("/tasks"), apiFetch("/clients")]);
    currentTasks = tasks;
    const clientNameById = new Map(clientsList.map((c) => [c.id, c.name]));
    els.tasksEmpty.hidden = tasks.length > 0;

    const { open, done } = sortTasksForDisplay(tasks);
    renderWithShowAll(
      els.tasksList,
      [...open, ...done],
      (task) => buildTaskCard(task, clientNameById),
      { showAllBtn: els.tasksShowAllBtn, title: "כל המשימות", emptyText: "עדיין אין משימות." }
    );
  } catch {
    // not authenticated yet
  }
}

function buildThoughtRow(thought) {
  const row = document.createElement("div");
  row.className = "thought-row";
  const content = document.createElement("span");
  content.className = "thought-content";
  content.textContent = thought.content;
  const deleteBtn = document.createElement("button");
  deleteBtn.type = "button";
  deleteBtn.className = "task-delete-btn";
  deleteBtn.title = "מחיקת מחשבה";
  deleteBtn.textContent = "✕";
  deleteBtn.addEventListener("click", async () => {
    if (!confirm("למחוק את המחשבה הזאת?")) return;
    await apiFetch(`/thoughts/${thought.id}`, { method: "DELETE" });
    loadThoughts();
  });
  row.appendChild(content);
  row.appendChild(deleteBtn);
  return row;
}

async function loadThoughts() {
  try {
    const thoughts = await apiFetch("/thoughts");
    els.thoughtsEmpty.hidden = thoughts.length > 0;
    renderWithShowAll(els.thoughtsList, thoughts, buildThoughtRow, {
      showAllBtn: els.thoughtsShowAllBtn,
      title: "כל המחשבות",
      emptyText: "עדיין אין מחשבות שמורות.",
    });
  } catch {
    // not authenticated yet
  }
}

els.thoughtSaveBtn.addEventListener("click", async () => {
  stopVoiceCaptureFor(els.thoughtInput);
  const content = els.thoughtInput.value.trim();
  if (!content) return;
  try {
    await apiFetch("/thoughts", { method: "POST", body: JSON.stringify({ content }) });
    els.thoughtInput.value = "";
    loadThoughts();
  } catch (err) {
    alert(err.message);
  }
});

els.thoughtInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    els.thoughtSaveBtn.click();
  }
});

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
let editTaskClientsList = [];

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
    editTaskClientsList = clientsList;
    els.editTaskClientOptions.innerHTML = clientsList
      .map((c) => `<option value="${escapeHtml(c.name)}"></option>`)
      .join("");
  } catch (err) {
    alert(err.message);
    return;
  }

  const currentClient = editTaskClientsList.find((c) => c.id === task.client_id);
  els.editTaskTitle.value = task.title;
  els.editTaskStartAt.value = task.start_at ? toDatetimeLocalValue(task.start_at) : "";
  els.editTaskDueAt.value = task.due_at ? toDatetimeLocalValue(task.due_at) : "";
  els.editTaskProject.value = task.project_id || "";
  els.editTaskClient.value = currentClient ? currentClient.name : "";
  els.editTaskModal.hidden = false;
}

async function resolveClientIdByName(name) {
  const trimmed = name.trim();
  if (!trimmed) return null;
  const existing = editTaskClientsList.find(
    (c) => c.name.toLowerCase() === trimmed.toLowerCase()
  );
  if (existing) return existing.id;
  const created = await apiFetch("/clients", {
    method: "POST",
    body: JSON.stringify({ name: trimmed }),
  });
  editTaskClientsList.push(created);
  return created.id;
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
    const clientId = await resolveClientIdByName(els.editTaskClient.value);
    await apiFetch(`/tasks/${currentEditTaskId}`, {
      method: "PATCH",
      body: JSON.stringify({
        title,
        start_at: startValue ? new Date(startValue).toISOString() : null,
        due_at: dueValue ? new Date(dueValue).toISOString() : null,
        project_id: els.editTaskProject.value || null,
        client_id: clientId,
      }),
    });
    els.editTaskModal.hidden = true;
    loadTasks();
    loadClients();
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

function clientAvatarHtml(client, sizeClass) {
  const sizeCls = sizeClass ? ` ${sizeClass}` : "";
  if (client.has_logo) {
    return `<img class="client-avatar${sizeCls}" src="${API_BASE}/clients/${client.id}/logo" alt="" />`;
  }
  const initial = client.name ? client.name.charAt(0).toUpperCase() : "?";
  return `<span class="client-avatar client-avatar--placeholder${sizeCls}">${escapeHtml(initial)}</span>`;
}

function clientHealthStatus(clientTasks) {
  // Same overdue/soon/fine convention already used for individual task due
  // badges — just aggregated across a client's open tasks instead of one.
  const now = Date.now();
  let hasOverdue = false;
  let hasSoon = false;
  for (const t of clientTasks) {
    if (t.status === "done" || !t.due_at) continue;
    const diffHours = (new Date(t.due_at).getTime() - now) / 3600000;
    if (diffHours < 0) hasOverdue = true;
    else if (diffHours <= 24) hasSoon = true;
  }
  if (hasOverdue) return "red";
  if (hasSoon) return "yellow";
  return "green";
}

async function loadClients() {
  try {
    const [clientsList, tasks, projects] = await Promise.all([
      apiFetch("/clients"),
      apiFetch("/tasks"),
      apiFetch("/projects"),
    ]);
    const tasksByClient = new Map();
    for (const t of tasks) {
      if (!t.client_id) continue;
      if (!tasksByClient.has(t.client_id)) tasksByClient.set(t.client_id, []);
      tasksByClient.get(t.client_id).push(t);
    }
    const projectsByClient = new Map();
    for (const p of projects) {
      if (!p.client_id) continue;
      if (!projectsByClient.has(p.client_id)) projectsByClient.set(p.client_id, []);
      projectsByClient.get(p.client_id).push(p);
    }
    els.clientsEmpty.hidden = clientsList.length > 0;
    const buildCard = (c) => {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "client-card";
      const clientTasks = tasksByClient.get(c.id) || [];
      const openTaskCount = clientTasks.filter((t) => t.status !== "done").length;
      const tasksHtml = openTaskCount
        ? `<span class="client-card-tasks">${openTaskCount} משימות פתוחות</span>`
        : "";
      const clientProjects = projectsByClient.get(c.id) || [];
      const typesHtml = clientProjects.length
        ? `<div class="client-card-types">${clientProjects
            .map(
              (p) =>
                `<span class="project-type-chip project-type-chip--${p.type}">${PROJECT_TYPE_LABELS[p.type]}</span>`
            )
            .join("")}</div>`
        : "";
      // Health considers tasks linked directly to the client AND tasks
      // linked via one of the client's projects, same set the client modal
      // itself uses — a task filed under a project shouldn't be invisible
      // to the client's status just because it isn't tagged with client_id.
      const clientProjectIds = new Set(clientProjects.map((p) => p.id));
      const allClientTasks = tasks.filter(
        (t) => t.client_id === c.id || clientProjectIds.has(t.project_id)
      );
      const health = clientHealthStatus(allClientTasks);
      const healthTitles = {
        green: "בשליטה — אין משימות באיחור או קרובות מאוד",
        yellow: "יש משימה שמתקרבת לתאריך היעד",
        red: "יש משימה באיחור",
      };
      const healthDot = document.createElement("span");
      healthDot.className = `client-card-health client-card-health--${health}`;
      healthDot.title = healthTitles[health];
      card.appendChild(healthDot);

      const rest = document.createElement("div");
      rest.className = "client-card-body";
      rest.innerHTML = `
        ${clientAvatarHtml(c, "client-card-logo")}
        <div class="client-card-name">${escapeHtml(c.name)}</div>
        ${typesHtml}
        ${tasksHtml}
      `;
      card.appendChild(rest);
      card.addEventListener("click", () => openClientModal(c.id));
      return card;
    };
    renderWithShowAll(els.clientsGrid, clientsList, buildCard, {
      showAllBtn: els.clientsShowAllBtn,
      title: "כל הלקוחות",
      emptyText: "עדיין אין לקוחות.",
    });
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
    const start = new Date();
    const end = new Date(start.getTime() + 5 * 3600000);
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

function formatCurrency(amount, currency) {
  return `${amount.toLocaleString("he-IL", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${currency}`;
}

async function loadCashFlow() {
  try {
    const snapshot = await apiFetch("/finance/cash-flow");
    if (!snapshot) {
      els.cashFlowCard.hidden = true;
      els.cashFlowEmpty.hidden = false;
      return;
    }
    els.cashFlowEmpty.hidden = true;
    els.cashFlowCard.hidden = false;
    els.cashFlowBalance.textContent = formatCurrency(snapshot.current_balance, "₪");
    els.cashFlowFixedExpenses.textContent = formatCurrency(snapshot.fixed_expenses_this_month, "₪");
    els.cashFlowDues.textContent = formatCurrency(snapshot.dues_this_month, "₪");
    els.cashFlowProjected.textContent = formatCurrency(snapshot.projected_end_of_month_balance, "₪");
  } catch {
    els.cashFlowCard.hidden = true;
    els.cashFlowEmpty.hidden = false;
  }
}

async function loadFinance() {
  try {
    const [overview, clients] = await Promise.all([
      apiFetch("/finance/overview"),
      apiFetch("/clients"),
    ]);
    els.financeEmpty.hidden = true;
    els.financeContent.hidden = false;

    els.financeSummary.innerHTML = "";
    const summaryRows = [
      { label: "הכנסות", value: overview.total_income, cls: "finance-stat--income" },
      { label: "הוצאות", value: overview.total_expenses, cls: "finance-stat--expense" },
      { label: "נטו", value: overview.net, cls: overview.net >= 0 ? "finance-stat--income" : "finance-stat--expense" },
    ];
    for (const stat of summaryRows) {
      const box = document.createElement("div");
      box.className = `finance-stat ${stat.cls}`;
      const label = document.createElement("div");
      label.className = "finance-stat-label";
      label.textContent = stat.label;
      const value = document.createElement("div");
      value.className = "finance-stat-value";
      value.textContent = formatCurrency(stat.value, "₪");
      box.appendChild(label);
      box.appendChild(value);
      els.financeSummary.appendChild(box);
    }

    els.financeIncomeEmpty.hidden = overview.income.length > 0;
    renderWithShowAll(
      els.financeIncomeList,
      overview.income,
      (record) => buildFinanceRecordRow(record, "income", clients),
      {
        showAllBtn: els.financeIncomeShowAllBtn,
        title: "כל ההכנסות",
        emptyText: "אין הכנסות בטווח התאריכים הזה.",
      }
    );

    els.financeExpensesEmpty.hidden = overview.expenses.length > 0;
    renderWithShowAll(
      els.financeExpensesList,
      overview.expenses,
      (record) => buildFinanceRecordRow(record, "expense"),
      {
        showAllBtn: els.financeExpensesShowAllBtn,
        title: "כל ההוצאות",
        emptyText: "אין הוצאות בטווח התאריכים הזה.",
      }
    );
  } catch {
    els.financeContent.hidden = true;
    els.financeEmpty.hidden = false;
  }
}

function buildFinanceRecordRow(record, kind, clients) {
  const row = document.createElement("div");
  row.className = "finance-item";

  const date = document.createElement("span");
  date.className = "finance-item-date";
  date.textContent = record.date;
  row.appendChild(date);

  const desc = document.createElement("span");
  desc.className = "finance-item-desc";
  if (kind === "income") {
    const parts = [record.client_name, record.description].filter(Boolean);
    desc.textContent = parts.length > 0 ? parts.join(" — ") : "—";
  } else {
    desc.textContent = record.description || record.category || "—";
  }
  row.appendChild(desc);

  if (kind === "income" && record.client_name && !record.matched_client_id) {
    if (record.green_invoice_client_id && clients && clients.length > 0) {
      const select = document.createElement("select");
      select.className = "finance-item-link-select";
      select.innerHTML =
        '<option value="" selected disabled>לא משויך — שייך ללקוח</option>' +
        clients.map((c) => `<option value="${c.id}">${escapeHtml(c.name)}</option>`).join("");
      select.addEventListener("change", () => linkIncomeClientAndReload(record, select.value));
      row.appendChild(select);
    } else {
      const badge = document.createElement("span");
      badge.className = "finance-item-badge";
      badge.textContent = "לא משויך ללקוח קיים";
      row.appendChild(badge);
    }
  }

  const amount = document.createElement("span");
  amount.className = "finance-item-amount";
  amount.textContent = formatCurrency(record.amount, record.currency);
  row.appendChild(amount);

  return row;
}

async function linkIncomeClientAndReload(record, clientId) {
  try {
    await apiFetch("/finance/link-client", {
      method: "POST",
      body: JSON.stringify({
        green_invoice_client_id: record.green_invoice_client_id,
        green_invoice_client_name: record.client_name,
        client_id: clientId,
      }),
    });
    await loadFinance();
  } catch (err) {
    alert(err.message);
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

function formatEmailSender(sender) {
  // Gmail's "From" header is usually `"Display Name" <addr@example.com>` —
  // show just the name (or the raw address if there isn't one).
  const match = sender.match(/^"?([^"<]*)"?\s*<.*>$/);
  const name = match ? match[1].trim() : "";
  return name || sender;
}

function buildEmailRow(email) {
  const row = document.createElement("a");
  row.className = "email-item";
  row.href = `https://mail.google.com/mail/?authuser=${encodeURIComponent(
    currentUserEmail
  )}#all/${encodeURIComponent(email.id)}`;
  row.target = "_blank";
  row.rel = "noopener";

  const main = document.createElement("div");
  main.className = "email-item-main";
  const sender = document.createElement("span");
  sender.className = "email-item-sender";
  sender.textContent = formatEmailSender(email.sender);
  const subject = document.createElement("span");
  subject.className = "email-item-subject";
  subject.textContent = email.subject || "(ללא נושא)";
  const snippet = document.createElement("span");
  snippet.className = "email-item-snippet";
  snippet.textContent = email.snippet;
  main.appendChild(sender);
  main.appendChild(subject);
  main.appendChild(snippet);

  const date = document.createElement("span");
  date.className = "email-item-date";
  date.textContent = email.date ? new Date(email.date).toLocaleDateString("he-IL") : "";

  row.appendChild(main);
  row.appendChild(date);
  return row;
}

async function loadEmails() {
  try {
    const emails = await apiFetch("/emails?max_results=30");
    els.gmailEmpty.hidden = emails.length > 0;
    renderWithShowAll(els.gmailList, emails, buildEmailRow, {
      showAllBtn: els.gmailShowAllBtn,
      title: "כל המיילים האחרונים",
      emptyText: "אין מיילים להצגה.",
    });
  } catch {
    // not authenticated yet
  }
}

const FILES_TABLE_THEAD = "<tr><th>שם</th><th>סוג</th><th>עודכן</th><th></th></tr>";

function buildFileRow(file) {
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
  return tr;
}

async function loadFiles() {
  try {
    const files = await apiFetch("/files?max_results=30&order_by=viewedByMeTime%20desc");
    els.filesEmpty.hidden = files.length > 0;
    renderWithShowAll(els.filesTbody, files, buildFileRow, {
      showAllBtn: els.filesShowAllBtn,
      title: "כל הקבצים האחרונים",
      emptyText: "אין קבצים להצגה.",
      theadHtml: FILES_TABLE_THEAD,
    });
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

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

let myDayGoalsCache = [];
let myDayPlanCache = null;
let myDayPickerSlots = null;
let pendingUrgentTaskId = null;
let activeFocusSession = null;
let focusCurrentTask = null;
let focusDeadlineMs = null;
let focusTickInterval = null;

async function loadGoals() {
  try {
    myDayGoalsCache = await apiFetch("/my-day/goals");
  } catch {
    myDayGoalsCache = [];
  }
  renderGoalsList();
}

function renderGoalsList() {
  els.myDayGoalsList.innerHTML = "";
  for (const goal of myDayGoalsCache) {
    const row = document.createElement("div");
    row.className = "my-day-goal-row";
    const name = document.createElement("span");
    name.textContent = goal.name;
    row.appendChild(name);
    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "task-delete-btn";
    deleteBtn.textContent = "✕";
    deleteBtn.addEventListener("click", async () => {
      if (!confirm(`למחוק את היעד "${goal.name}"?`)) return;
      try {
        await apiFetch(`/my-day/goals/${goal.id}`, { method: "DELETE" });
        await loadGoals();
      } catch (err) {
        alert(err.message);
      }
    });
    row.appendChild(deleteBtn);
    els.myDayGoalsList.appendChild(row);
  }
}

els.myDayGoalAdd.addEventListener("click", async () => {
  const name = els.myDayGoalInput.value.trim();
  if (!name) return;
  try {
    await apiFetch("/my-day/goals", { method: "POST", body: JSON.stringify({ name }) });
    els.myDayGoalInput.value = "";
    await loadGoals();
  } catch (err) {
    alert(err.message);
  }
});

function buildTaskPickSlot(label, selectedTaskId) {
  const wrapper = document.createElement("div");
  wrapper.className = "my-day-slot-card";

  if (label) {
    const heading = document.createElement("div");
    heading.className = "my-day-slot-heading";
    heading.textContent = label;
    wrapper.appendChild(heading);
  }

  const openTasks = currentTasks.filter((t) => t.status !== "done");
  const taskSelect = document.createElement("select");
  taskSelect.className = "my-day-slot-field";
  taskSelect.innerHTML =
    '<option value="">בחר משימה...</option>' +
    openTasks
      .map(
        (t) =>
          `<option value="${t.id}" ${t.id === selectedTaskId ? "selected" : ""}>${escapeHtml(t.title)}</option>`
      )
      .join("");
  wrapper.appendChild(taskSelect);

  const deliverable = document.createElement("textarea");
  deliverable.className = "my-day-slot-field";
  deliverable.rows = 2;
  deliverable.placeholder = "תוצר סופי — איך ייראה שהמשימה בוצעה?";
  wrapper.appendChild(deliverable);

  const nextStep = document.createElement("textarea");
  nextStep.className = "my-day-slot-field";
  nextStep.rows = 2;
  nextStep.placeholder = "הצעד הראשון הקטן ביותר — למשל \"לפתוח את הקובץ ולכתוב שורה אחת\"";
  wrapper.appendChild(nextStep);

  const minutes = document.createElement("input");
  minutes.type = "number";
  minutes.min = "1";
  minutes.className = "my-day-slot-field";
  minutes.placeholder = "משך משוער (דקות)";
  minutes.value = "30";
  wrapper.appendChild(minutes);

  const importance = document.createElement("select");
  importance.className = "my-day-slot-field";
  importance.innerHTML = `
    <option value="high">חשיבות גבוהה</option>
    <option value="medium">חשיבות בינונית</option>
    <option value="low">חשיבות נמוכה</option>
  `;
  wrapper.appendChild(importance);

  const goalSelect = document.createElement("select");
  goalSelect.className = "my-day-slot-field";
  goalSelect.innerHTML =
    '<option value="">ללא יעד עסקי</option>' +
    myDayGoalsCache.map((g) => `<option value="${g.id}">${escapeHtml(g.name)}</option>`).join("");
  wrapper.appendChild(goalSelect);

  return { wrapper, taskSelect, deliverable, nextStep, minutes, importance, goalSelect };
}

function renderDailyTaskPicker(plan) {
  els.myDayPicker.innerHTML = "";
  const main = buildTaskPickSlot("המשימה המרכזית (חובה לסיים)", plan.main_task_id);
  const secondary1 = buildTaskPickSlot("משימה נוספת 1", plan.secondary_task_id_1);
  const secondary2 = buildTaskPickSlot("משימה נוספת 2", plan.secondary_task_id_2);
  els.myDayPicker.appendChild(main.wrapper);
  els.myDayPicker.appendChild(secondary1.wrapper);
  els.myDayPicker.appendChild(secondary2.wrapper);
  myDayPickerSlots = { main, secondary: [secondary1, secondary2] };
}

function buildDailyPickPayload(slot) {
  return {
    task_id: slot.taskSelect.value,
    deliverable: slot.deliverable.value.trim() || "בוצע",
    estimated_minutes: Number(slot.minutes.value) || 30,
    importance: slot.importance.value,
    goal_id: slot.goalSelect.value || null,
    next_step: slot.nextStep.value.trim(),
  };
}

function assertSlotHasNextStep(slot, label) {
  if (!slot.nextStep.value.trim()) {
    throw new Error(`צריך להגדיר צעד ראשון קטן ל${label}.`);
  }
}

async function saveDailyTaskSelection() {
  if (!myDayPickerSlots) throw new Error("אין בחירה להצגה.");
  const { main, secondary } = myDayPickerSlots;
  if (!main.taskSelect.value) {
    throw new Error("צריך לבחור משימה מרכזית.");
  }
  assertSlotHasNextStep(main, "משימה המרכזית");
  const usedSecondary = secondary.filter((s) => s.taskSelect.value);
  usedSecondary.forEach((s) => assertSlotHasNextStep(s, "משימה נוספת"));

  const mainPick = buildDailyPickPayload(main);
  const secondaryPicks = usedSecondary.map(buildDailyPickPayload);
  return apiFetch("/my-day/plan/today/select", {
    method: "POST",
    body: JSON.stringify({ main: mainPick, secondary: secondaryPicks }),
  });
}

els.myDayLockBtn.addEventListener("click", async () => {
  try {
    await saveDailyTaskSelection();
    const locked = await apiFetch("/my-day/plan/today/lock", { method: "POST" });
    await loadTasks(); // picks were just saved server-side — refresh the stale local cache
    renderMyDayPlanView(locked);
  } catch (err) {
    alert(err.message);
  }
});

function renderMyDayPlanView(plan) {
  myDayPlanCache = plan;
  if (plan.is_locked) {
    els.myDayPickerSection.hidden = true;
    els.myDayLockedSection.hidden = false;
    renderLockedTasks(plan);
  } else {
    els.myDayPickerSection.hidden = false;
    els.myDayLockedSection.hidden = true;
    renderDailyTaskPicker(plan);
  }
}

function renderLockedTasks(plan) {
  els.myDayLockedTasks.innerHTML = "";
  const taskById = new Map(currentTasks.map((t) => [t.id, t]));
  const slots = [
    { id: plan.main_task_id, label: "משימה מרכזית" },
    { id: plan.secondary_task_id_1, label: "משימה נוספת" },
    { id: plan.secondary_task_id_2, label: "משימה נוספת" },
  ].filter((s) => s.id);

  for (const slot of slots) {
    const task = taskById.get(slot.id);
    if (!task) continue;
    const card = document.createElement("div");
    card.className = "my-day-slot-card";
    const heading = document.createElement("div");
    heading.className = "my-day-slot-heading";
    heading.textContent = `${slot.label}${task.status === "done" ? " — הושלם ✔" : ""}`;
    card.appendChild(heading);
    const title = document.createElement("div");
    title.className = "my-day-locked-task-title";
    title.textContent = task.title;
    card.appendChild(title);
    if (task.deliverable) {
      const deliverable = document.createElement("div");
      deliverable.className = "my-day-locked-task-deliverable";
      deliverable.textContent = task.deliverable;
      card.appendChild(deliverable);
    }
    if (task.status !== "done") {
      const focusBtn = document.createElement("button");
      focusBtn.type = "button";
      focusBtn.className = "btn btn--primary";
      focusBtn.textContent = "כניסה ל-Focus";
      focusBtn.addEventListener("click", () => enterFocusMode(task.id));
      card.appendChild(focusBtn);
    }
    els.myDayLockedTasks.appendChild(card);
  }
}

els.myDayInboxAdd.addEventListener("click", async () => {
  const title = els.myDayInboxInput.value.trim();
  if (!title) return;
  try {
    const task = await apiFetch("/my-day/inbox", {
      method: "POST",
      body: JSON.stringify({ title }),
    });
    els.myDayInboxInput.value = "";
    const isUrgent = els.myDayInboxUrgent.checked;
    els.myDayInboxUrgent.checked = false;
    await loadTasks();
    if (isUrgent && myDayPlanCache && myDayPlanCache.is_locked) {
      openUrgentSwapModal(task.id);
    } else {
      await refreshMyDay();
    }
  } catch (err) {
    alert(err.message);
  }
});

function openUrgentSwapModal(newTaskId) {
  pendingUrgentTaskId = newTaskId;
  const slots = [
    { id: myDayPlanCache.main_task_id, label: "משימה מרכזית" },
    { id: myDayPlanCache.secondary_task_id_1, label: "משימה נוספת 1" },
    { id: myDayPlanCache.secondary_task_id_2, label: "משימה נוספת 2" },
  ].filter((s) => s.id);
  const taskNameById = new Map(currentTasks.map((t) => [t.id, t.title]));
  els.urgentSwapBumpedSelect.innerHTML = slots
    .map(
      (s) =>
        `<option value="${s.id}">${escapeHtml(s.label)}: ${escapeHtml(taskNameById.get(s.id) || "")}</option>`
    )
    .join("");
  els.urgentSwapDeliverable.value = "";
  els.urgentSwapNextStep.value = "";
  els.urgentSwapMinutes.value = "30";
  els.urgentSwapImportance.value = "high";
  els.urgentSwapGoal.innerHTML =
    '<option value="">ללא יעד</option>' +
    myDayGoalsCache.map((g) => `<option value="${g.id}">${escapeHtml(g.name)}</option>`).join("");
  els.urgentSwapModal.hidden = false;
}

els.urgentSwapCancel.addEventListener("click", () => {
  els.urgentSwapModal.hidden = true;
  pendingUrgentTaskId = null;
});

els.urgentSwapSave.addEventListener("click", async () => {
  if (!pendingUrgentTaskId) return;
  const bumpedTaskId = els.urgentSwapBumpedSelect.value;
  if (!bumpedTaskId) {
    alert("צריך לבחור משימה לדחות.");
    return;
  }
  if (!els.urgentSwapNextStep.value.trim()) {
    alert("צריך להגדיר צעד ראשון קטן למשימה הדחופה.");
    return;
  }
  try {
    const plan = await apiFetch("/my-day/plan/today/swap", {
      method: "POST",
      body: JSON.stringify({
        bumped_task_id: bumpedTaskId,
        pick: {
          task_id: pendingUrgentTaskId,
          deliverable: els.urgentSwapDeliverable.value.trim() || "בוצע",
          estimated_minutes: Number(els.urgentSwapMinutes.value) || 30,
          importance: els.urgentSwapImportance.value,
          goal_id: els.urgentSwapGoal.value || null,
          next_step: els.urgentSwapNextStep.value.trim(),
        },
      }),
    });
    els.urgentSwapModal.hidden = true;
    pendingUrgentTaskId = null;
    await loadTasks();
    renderMyDayPlanView(plan);
  } catch (err) {
    alert(err.message);
  }
});

async function refreshMyDay() {
  await loadTasks();
  await loadGoals();
  try {
    const plan = await apiFetch("/my-day/plan/today");
    renderMyDayPlanView(plan);
  } catch (err) {
    alert(err.message);
  }
}

async function enterFocusMode(taskId) {
  try {
    const session = await apiFetch("/my-day/focus/start", {
      method: "POST",
      body: JSON.stringify({ task_id: taskId }),
    });
    startFocusUI(session);
  } catch (err) {
    alert(err.message);
  }
}

function startFocusUI(session) {
  activeFocusSession = session;
  focusCurrentTask = currentTasks.find((t) => t.id === session.task_id) || null;
  setAppMode("focus");
  renderFocusScreen(session, focusCurrentTask);
}

function renderFocusScreen(session, task) {
  els.focusTaskTitle.textContent = task ? task.title : "";
  els.focusDeliverable.textContent = task && task.deliverable ? task.deliverable : "";
  els.focusNextStepInput.value = (task && task.next_step) || "";
  els.focusTimer.classList.remove("focus-timer--expired");

  const durationMinutes = (task && task.estimated_minutes) || 30;
  focusDeadlineMs = new Date(session.started_at).getTime() + durationMinutes * 60000;
  tickFocusTimer();
  if (focusTickInterval) clearInterval(focusTickInterval);
  focusTickInterval = setInterval(tickFocusTimer, 1000);
}

function tickFocusTimer() {
  if (focusDeadlineMs === null) return;
  const remaining = focusDeadlineMs - Date.now();
  els.focusTimer.textContent = formatCountdown(remaining);
  if (remaining <= 0 && !els.focusTimer.classList.contains("focus-timer--expired")) {
    els.focusTimer.classList.add("focus-timer--expired");
    playTimerExpiredSound();
    showTimerExpiredNotification(focusCurrentTask ? focusCurrentTask.title : "");
  }
}

function stopFocusTimerLoop() {
  if (focusTickInterval) {
    clearInterval(focusTickInterval);
    focusTickInterval = null;
  }
  focusDeadlineMs = null;
}

els.focusNextStepInput.addEventListener("change", async () => {
  if (!focusCurrentTask) return;
  try {
    await apiFetch(`/my-day/tasks/${focusCurrentTask.id}/next-step`, {
      method: "PATCH",
      body: JSON.stringify({ next_step: els.focusNextStepInput.value.trim() || null }),
    });
  } catch (err) {
    alert(err.message);
  }
});

async function endFocusSession(exitReason, stuckReason) {
  if (!activeFocusSession) return;
  try {
    await apiFetch(`/my-day/focus/${activeFocusSession.id}/end`, {
      method: "POST",
      body: JSON.stringify({ exit_reason: exitReason, stuck_reason: stuckReason || null }),
    });
    stopFocusTimerLoop();
    activeFocusSession = null;
    focusCurrentTask = null;
    setAppMode("my-day");
    await refreshMyDay();
  } catch (err) {
    alert(err.message);
  }
}

els.focusDoneBtn.addEventListener("click", () => endFocusSession("done", null));
els.focusBreakBtn.addEventListener("click", () => endFocusSession("break", null));

els.focusStuckBtn.addEventListener("click", () => {
  els.stuckReasonModal.hidden = false;
});

els.stuckReasonCancel.addEventListener("click", () => {
  els.stuckReasonModal.hidden = true;
});

document.querySelectorAll(".stuck-reason-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    els.stuckReasonModal.hidden = true;
    endFocusSession("stuck", btn.dataset.reason);
  });
});

async function checkForActiveFocusSessionOnLoad() {
  try {
    const session = await apiFetch("/my-day/focus/active");
    if (session) {
      await loadTasks();
      startFocusUI(session);
      return true;
    }
  } catch {
    // not authenticated yet
  }
  return false;
}

async function autoStartLockedMainTaskOnLoad() {
  try {
    const plan = await apiFetch("/my-day/plan/today");
    if (!plan.is_locked || !plan.main_task_id) return;
    await loadTasks();
    const mainTask = currentTasks.find((t) => t.id === plan.main_task_id);
    if (!mainTask || mainTask.status === "done") return;
    const session = await apiFetch("/my-day/focus/start", {
      method: "POST",
      body: JSON.stringify({ task_id: plan.main_task_id }),
    });
    startFocusUI(session);
  } catch {
    // no locked plan yet, not authenticated, or a race with another session —
    // fail silently into the normal dashboard, this is an unprompted auto-action.
  }
}

els.myDaySummaryBtn.addEventListener("click", async () => {
  try {
    const summary = await apiFetch("/my-day/plan/today/summary");
    renderMyDaySummary(summary);
  } catch (err) {
    alert(err.message);
  }
});

function renderMyDaySummary(summary) {
  const el = els.myDaySummaryContent;
  el.hidden = false;
  const stuckLabels = {
    unclear: "לא ברור מה לעשות",
    too_big: "המשימה גדולה מדי",
    blocked: "חסר מידע או אדם אחר",
    distracted: "הוסחתי",
  };
  const stuckEntries = Object.entries(summary.stuck_reason_counts || {});
  el.innerHTML = `
    <div class="eod-summary-card">
      <div class="eod-stat-row"><strong>המשימה המרכזית הושלמה:</strong> ${summary.main_task_completed ? "כן ✔" : "לא"}</div>
      <div class="eod-stat-row"><strong>הושלם:</strong> ${summary.completed_tasks.length ? summary.completed_tasks.map(escapeHtml).join(", ") : "—"}</div>
      <div class="eod-stat-row"><strong>לא הושלם:</strong> ${summary.incomplete_tasks.length ? summary.incomplete_tasks.map(escapeHtml).join(", ") : "—"}</div>
      <div class="eod-stat-row"><strong>מה הפריע:</strong> ${stuckEntries.length ? stuckEntries.map(([k, v]) => `${escapeHtml(stuckLabels[k] || k)} (${v})`).join(", ") : "—"}</div>
      <div class="eod-stat-row"><strong>משימות דחופות שנכנסו:</strong> ${summary.swap_count}</div>
      <div class="eod-stat-row">
        <strong>המשימה הראשונה למחר — נועלים עכשיו, כדי שמחר לא תצטרך להחליט כלום:</strong>
      </div>
      <div id="eod-first-task-slot"></div>
      <button type="button" id="eod-first-task-save" class="btn btn--primary btn--small">לנעול את המשימה הראשונה למחר</button>
    </div>
  `;

  const slotContainer = document.getElementById("eod-first-task-slot");
  const slot = buildTaskPickSlot("", summary.carry_over_task_id);
  slotContainer.appendChild(slot.wrapper);

  document.getElementById("eod-first-task-save").addEventListener("click", async () => {
    if (!slot.taskSelect.value) {
      alert("צריך לבחור משימה.");
      return;
    }
    try {
      assertSlotHasNextStep(slot, "משימה הראשונה למחר");
    } catch (err) {
      alert(err.message);
      return;
    }
    try {
      await apiFetch("/my-day/plan/tomorrow/first-task", {
        method: "POST",
        body: JSON.stringify(buildDailyPickPayload(slot)),
      });
      alert("המשימה הראשונה למחר ננעלה. כשתפתח את האפליקציה מחר, היא תיפתח ישר אליה.");
    } catch (err) {
      alert(err.message);
    }
  });
}

function refreshWorkspace() {
  loadDashboardSummary();
  loadTasks();
  loadClients();
  loadCalendar();
  loadEmails();
  loadFiles();
  loadNotifications();
  loadThoughts();
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
  setAppMode("dashboard");
  await checkAuth();
  refreshWorkspace();
  setInterval(tickTaskTimers, 1000);
  const resumedActiveSession = await checkForActiveFocusSessionOnLoad();
  if (!resumedActiveSession) {
    await autoStartLockedMainTaskOnLoad();
  }
})();
