const API_BASE = "/api/v1";

const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const authStatus = document.getElementById("auth-status");

let conversationId = null;

function addBubble(role, text) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  chatWindow.appendChild(bubble);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return bubble;
}

function addToolTrace(toolCalls) {
  if (!toolCalls || toolCalls.length === 0) return;
  const trace = document.createElement("div");
  trace.className = "tool-trace";
  trace.textContent = `Used: ${toolCalls.map((t) => t.tool_name).join(", ")}`;
  chatWindow.appendChild(trace);
}

async function checkAuth() {
  try {
    const response = await fetch(`${API_BASE}/auth/google/me`, { credentials: "include" });
    if (!response.ok) throw new Error("not authenticated");
    const user = await response.json();
    authStatus.innerHTML = `Signed in as ${user.name}`;
    chatForm.querySelector("button").disabled = false;
  } catch {
    authStatus.innerHTML = `<a href="${API_BASE}/auth/google/login">Sign in with Google</a>`;
    chatForm.querySelector("button").disabled = true;
    addBubble("assistant", "Please sign in with Google to talk to Edith.");
  }
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = chatInput.value.trim();
  if (!text) return;

  addBubble("user", text);
  chatInput.value = "";

  try {
    const response = await fetch(`${API_BASE}/chat/commands`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ text, conversation_id: conversationId }),
    });

    if (!response.ok) {
      const error = await response.json();
      addBubble("error", error.message || "Something went wrong.");
      return;
    }

    const data = await response.json();
    conversationId = data.conversation_id;
    addBubble("assistant", data.reply);
    addToolTrace(data.tool_calls_made);
  } catch (err) {
    addBubble("error", `Network error: ${err.message}`);
  }
});

checkAuth();
