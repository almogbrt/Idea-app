import { getState, setState, goToStep, SIBLING_LABELS, SIBLINGS } from '../state.js';
import { missionHeader, formatTime, startCountdown, toast, modal } from '../ui.js';
import { playAlert } from '../audio.js';

const DURATION_MS = 10 * 60 * 1000;
const ROLES = [
  { name: 'המוביל', desc: 'אחראי על הדרך והכיוון.' },
  { name: 'שומר הקצב', desc: 'דואג שהקצב מתאים לכולם.' },
  { name: 'שומר הצוות', desc: 'דואג שאף אחד לא נשאר מאחור.' }
];

export default function renderMission5(container) {
  if (!getState().m5.deadline) {
    setState({ m5: { deadline: Date.now() + DURATION_MS } });
  }

  const draw = () => {
    const roleIndex = getState().m5.roleIndex;

    container.innerHTML = `
      <div class="screen">
        <div class="content">
          ${missionHeader('m5')}
          <div class="eyebrow">בתחילת המסלול</div>
          <h1 class="title-xl">המשימה הגדולה</h1>
          <p class="body-text">המטרה: להגיע שלושתכם לסוף המסלול.</p>

          ${ROLES.map((r) => `<div class="role-card"><div class="role-name">${r.name}</div><div class="role-desc">${r.desc}</div></div>`).join('')}

          <div class="card">
            <div class="card-title">חלוקה נוכחית</div>
            ${SIBLINGS.map((s, i) => `<div class="body-text">${SIBLING_LABELS[s]} — ${ROLES[(roleIndex + i) % 3].name}</div>`).join('')}
          </div>

          <div class="timer-wrap">
            <span class="timer-label">זמן שנותר</span>
            <span class="timer" id="m5-timer">10:00</span>
          </div>

          <button class="btn" id="m5-swap">🔄 החלפה</button>
          <button class="btn btn-danger" id="m5-help">אני צריך עזרה</button>

          <div class="spacer"></div>
          <button class="btn btn-primary" id="m5-cta">שלושתנו סיימנו את המסלול</button>
        </div>
      </div>
    `;

    container.querySelector('#m5-swap').addEventListener('click', () => {
      setState({ m5: { roleIndex: (getState().m5.roleIndex + 1) % 3 } });
      toast('החלפה! כל אחד עובר לתפקיד הבא.');
      draw();
    });

    container.querySelector('#m5-help').addEventListener('click', () => {
      modal({
        body: 'צוות 3 עוצר. מישהו ביקש עזרה. ממשיכים רק כשכולם מוכנים.',
        buttonText: 'ממשיכים'
      });
    });

    container.querySelector('#m5-cta').addEventListener('click', () => {
      goToStep('m6');
    });
  };

  draw();

  const timerEl = container.querySelector('#m5-timer');
  let alerted = false;
  const stop = startCountdown(
    getState().m5.deadline,
    (remaining) => {
      const el = container.querySelector('#m5-timer');
      if (!el) return;
      el.textContent = formatTime(remaining);
      el.classList.toggle('urgent', remaining <= 60000 && remaining > 0);
    },
    () => { if (!alerted) { alerted = true; playAlert(); } }
  );

  return stop;
}
