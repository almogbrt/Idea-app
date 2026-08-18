import { getState, setState, goToStep, SIBLING_LABELS } from '../state.js';
import { missionHeader, formatTime } from '../ui.js';
import { playAlert } from '../audio.js';

const HOLD_MS = 3 * 60 * 1000;
const HOLDERS = [
  { key: 'noam', label: 'נועם' },
  { key: 'rom', label: 'רום' },
  { key: 'niv', label: 'ניב' }
];

export default function renderMission6(container) {
  const draw = () => {
    const m6 = getState().m6;
    container.innerHTML = `
      <div class="screen">
        <div class="content">
          ${missionHeader('m6')}
          <div class="eyebrow">באמצע המסלול</div>
          <h1 class="title-xl">המטען</h1>
          <p class="body-text">לכו לאבא ואמרו:
אנחנו מוכנים לקבל את המטען.</p>

          <div class="card">
            <div class="body-text">1. אסור להכניס את המטען לתיק.</div>
            <div class="body-text">2. אסור לאותו אדם להחזיק אותו יותר משלוש דקות.</div>
            <div class="body-text">3. אם המטען נופל — כל הצוות חוזר לנקודת הבדיקה האחרונה.</div>
          </div>

          <div class="card-title">מי מחזיק עכשיו?</div>
          <div class="approval-grid">
            ${HOLDERS.map((h) => `
              <button class="approval-btn ${m6.holder === h.key ? 'approved' : ''}" data-key="${h.key}">
                <span class="dot"></span>
                <span>${h.label}</span>
              </button>
            `).join('')}
          </div>

          <div class="timer-wrap" id="m6-timer-wrap" style="${m6.holder ? '' : 'display:none'}">
            <span class="timer-label">זמן החזקה</span>
            <span class="timer" id="m6-timer">03:00</span>
          </div>
          <div class="highlight-line" id="m6-warning" style="display:none;">העבירו את המטען לחבר צוות אחר.</div>

          <div class="spacer"></div>
          <button class="btn btn-primary" id="m6-cta">המטען הגיע לסוף</button>
        </div>
      </div>
    `;

    container.querySelectorAll('.approval-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.key;
        setState({ m6: { holder: key, deadline: Date.now() + HOLD_MS } });
        draw();
      });
    });

    container.querySelector('#m6-cta').addEventListener('click', () => {
      goToStep('t6');
    });
  };

  draw();

  // custom interval (not startCountdown) because the deadline itself changes
  // whenever a new holder is picked, and we need to re-read it live from state.
  let alertedFor = null;
  const intervalId = setInterval(() => {
    const m6 = getState().m6;
    if (!m6.holder || !m6.deadline) return;
    const remaining = Math.max(0, m6.deadline - Date.now());
    const timerEl = container.querySelector('#m6-timer');
    const warnEl = container.querySelector('#m6-warning');
    if (timerEl) {
      timerEl.textContent = formatTime(remaining);
      timerEl.classList.toggle('urgent', remaining <= 20000 && remaining > 0);
    }
    if (warnEl) warnEl.style.display = remaining <= 0 ? 'block' : 'none';
    if (remaining <= 0 && alertedFor !== m6.deadline) {
      alertedFor = m6.deadline;
      playAlert();
    }
  }, 250);

  return () => clearInterval(intervalId);
}
