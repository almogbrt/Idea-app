import { getState, setState, goToStep, SIBLING_LABELS } from '../state.js';
import { missionHeader, formatTime, startCountdown } from '../ui.js';
import { playAlert } from '../audio.js';

const CLUES = {
  noam: 'הדבר שאתם מחפשים נמצא במקום שאליו נכנסים לפני שמתחילים נסיעה ארוכה.',
  rom: 'חפשו באזור שבו אבא יושב.',
  niv: 'חפשו מתחת למשהו שחוגרים לפני שנוסעים.'
};

const TIMER_MS = 3 * 60 * 1000;

// step map: 1 pass->noam, 2 noam clue, 3 pass->rom, 4 rom clue, 5 pass->niv, 6 niv clue, 7 put-down+timer

function passScreen(container, sibling, onReady) {
  container.innerHTML = `
    <div class="screen">
      <div class="content">
        ${missionHeader('m3')}
        <div class="pass-screen">
          <div class="pass-icon">📱</div>
          <h1 class="title-lg">העבירו את הטלפון ל${sibling}</h1>
          <button class="btn btn-primary" id="pass-ready">אני מוכן</button>
        </div>
      </div>
    </div>
  `;
  container.querySelector('#pass-ready').addEventListener('click', onReady);
}

function clueScreen(container, siblingKey, onDone) {
  container.innerHTML = `
    <div class="screen">
      <div class="content">
        ${missionHeader('m3')}
        <div class="pass-screen">
          <div class="eyebrow">הרמז שלך, ${SIBLING_LABELS[siblingKey]}</div>
          <div class="clue-box">${CLUES[siblingKey]}</div>
          <p class="warning-text">זכור את הרמז. אל תראה לאחרים.</p>
          <button class="btn btn-primary" id="clue-done">סיימתי</button>
        </div>
      </div>
    </div>
  `;
  container.querySelector('#clue-done').addEventListener('click', onDone);
}

export default function renderMission3(container) {
  let stopFn = null;

  function show(step) {
    if (stopFn) { stopFn(); stopFn = null; }
    const go = (n) => { setState({ m3: { step: n } }); show(n); };

    if (step === 1) return passScreen(container, 'נועם', () => go(2));
    if (step === 2) return clueScreen(container, 'noam', () => go(3));
    if (step === 3) return passScreen(container, 'רום', () => go(4));
    if (step === 4) return clueScreen(container, 'rom', () => go(5));
    if (step === 5) return passScreen(container, 'ניב', () => go(6));
    if (step === 6) return clueScreen(container, 'niv', () => go(7));

    // step 7: put phone down + timer
    if (!getState().m3.timerDeadline) {
      setState({ m3: { timerDeadline: Date.now() + TIMER_MS } });
    }

    container.innerHTML = `
      <div class="screen">
        <div class="content">
          ${missionHeader('m3')}
          <div class="pass-screen">
            <div class="pass-icon">🤝</div>
            <h1 class="title-lg">עכשיו הניחו את הטלפון.</h1>
            <p class="body-text">לכל אחד יש חלק אחר מהמידע.
רק אם תחברו את שלושת הרמזים תוכלו למצוא את המקום.</p>
            <div class="timer-wrap">
              <span class="timer-label">זמן שנותר</span>
              <span class="timer" id="m3-timer">03:00</span>
            </div>
            <button class="btn btn-primary" id="m3-found">מצאנו</button>
          </div>
        </div>
      </div>
    `;

    const timerEl = container.querySelector('#m3-timer');
    let alerted = false;
    stopFn = startCountdown(
      getState().m3.timerDeadline,
      (remaining) => {
        timerEl.textContent = formatTime(remaining);
        timerEl.classList.toggle('urgent', remaining <= 30000 && remaining > 0);
      },
      () => { if (!alerted) { alerted = true; playAlert(); } }
    );

    container.querySelector('#m3-found').addEventListener('click', () => {
      goToStep('m4');
    });
  }

  show(getState().m3.step);

  return () => { if (stopFn) stopFn(); };
}
