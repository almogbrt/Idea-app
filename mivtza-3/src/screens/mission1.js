import { getState, setState, goToStep } from '../state.js';
import { missionHeader, formatTime, startCountdown } from '../ui.js';
import { playSuccess, playAlert } from '../audio.js';

const DURATION_MS = 25 * 60 * 1000;

export default function renderMission1(container) {
  const state = getState();
  if (!state.m1.deadline) {
    setState({ m1: { deadline: Date.now() + DURATION_MS } });
  }

  container.innerHTML = `
    <div class="screen">
      <div class="content">
        ${missionHeader('m1')}
        <div class="eyebrow">לפתוח ברגע שמתעוררים</div>
        <h1 class="title-xl">המבצע מתחיל</h1>
        <p class="body-text">יש לכם 25 דקות להיות לבושים, מצוחצחים, עם תיק אישי מוכן וליד הדלת.
מותר לעזור אחד לשני.
אבא לא מזכיר דברים ששכחתם.</p>

        <div class="timer-wrap">
          <span class="timer-label">זמן שנותר</span>
          <span class="timer" id="m1-timer">25:00</span>
        </div>

        <div class="highlight-line">צוות 3 מוכן למשימה.</div>

        <div class="spacer"></div>
        <button class="btn btn-primary" id="m1-action-btn">
          ${getState().m1.ready ? 'למשימה 2' : 'שלושתנו מוכנים'}
        </button>
      </div>
    </div>
  `;

  const timerEl = container.querySelector('#m1-timer');
  let alerted = false;
  const stopTimer = startCountdown(
    getState().m1.deadline,
    (remaining) => {
      timerEl.textContent = formatTime(remaining);
      timerEl.classList.toggle('urgent', remaining <= 60000 && remaining > 0);
    },
    () => {
      if (!alerted) { alerted = true; playAlert(); }
    }
  );

  const btn = container.querySelector('#m1-action-btn');
  btn.addEventListener('click', () => {
    if (!getState().m1.ready) {
      setState({ m1: { ready: true } });
      playSuccess();
      btn.textContent = 'למשימה 2';
    } else {
      goToStep('m2');
    }
  });

  return stopTimer;
}
