import { getState, setState, goToStep, CAMP_ITEMS_LIST } from '../state.js';
import { missionHeader, formatTime, startCountdown } from '../ui.js';
import { playSuccess, playAlert } from '../audio.js';

const DURATION_MS = 20 * 60 * 1000;

function allChecked(list) {
  return CAMP_ITEMS_LIST.every((item) => list[item]);
}

export default function renderMission8(container) {
  if (!getState().m8.deadline) {
    setState({ m8: { deadline: Date.now() + DURATION_MS } });
  }

  const draw = () => {
    const list = getState().m8.list;
    const complete = allChecked(list);
    const doneCount = CAMP_ITEMS_LIST.filter((i) => list[i]).length;

    container.innerHTML = `
      <div class="screen">
        <div class="content">
          ${missionHeader('m8')}
          <div class="eyebrow">הגענו לגני חוגה</div>
          <h1 class="title-xl">בונים את המחנה</h1>
          <p class="body-text">לפני מים, אוכל ומנוחה — בונים בסיס למבצע.</p>

          <div class="timer-wrap">
            <span class="timer-label">זמן שנותר</span>
            <span class="timer" id="m8-timer">20:00</span>
          </div>

          <div class="card">
            <div class="card-title"><span>רשימת הקמה</span><span class="tag ${complete ? 'done' : ''}">${doneCount}/${CAMP_ITEMS_LIST.length}</span></div>
            <div class="checklist">
              ${CAMP_ITEMS_LIST.map((item) => `
                <div class="check-item ${list[item] ? 'checked' : ''}" data-item="${item}">
                  <span class="box">${list[item] ? '✓' : ''}</span>
                  <span class="label">${item}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="highlight-line">סיימת את שלך? שאל: מי צריך עזרה?</div>

          <div class="spacer"></div>
          <button class="btn btn-primary" id="m8-cta" ${complete ? '' : 'disabled'}>המחנה מוכן — כולם למים</button>
        </div>
      </div>
    `;

    container.querySelectorAll('.check-item').forEach((el) => {
      el.addEventListener('click', () => {
        const item = el.dataset.item;
        const current = getState().m8.list[item];
        setState({ m8: { list: { [item]: !current } } });
        const wasComplete = complete;
        draw();
        if (!wasComplete && allChecked(getState().m8.list)) playSuccess();
      });
    });

    container.querySelector('#m8-cta').addEventListener('click', () => {
      if (!allChecked(getState().m8.list)) return;
      goToStep('m9');
    });
  };

  draw();

  let alerted = false;
  const stop = startCountdown(
    getState().m8.deadline,
    (remaining) => {
      const el = container.querySelector('#m8-timer');
      if (!el) return;
      el.textContent = formatTime(remaining);
      el.classList.toggle('urgent', remaining <= 60000 && remaining > 0);
    },
    () => { if (!alerted) { alerted = true; playAlert(); } }
  );

  return stop;
}
