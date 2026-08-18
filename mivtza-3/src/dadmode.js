import { getState, setState, nextStep, prevStep, resetStep, resetAll } from './state.js';
import { h, toast } from './ui.js';

const PIN = '314';
const LONG_PRESS_MS = 1200;

let pressTimer = null;
let rerenderCallback = () => {};

export function initDadMode(onRerender) {
  rerenderCallback = onRerender;

  document.addEventListener('pointerdown', (e) => {
    const target = e.target.closest && e.target.closest('#logo-longpress');
    if (!target) return;
    clearTimeout(pressTimer);
    pressTimer = setTimeout(() => {
      openPinPrompt();
    }, LONG_PRESS_MS);
  });

  const cancel = () => clearTimeout(pressTimer);
  document.addEventListener('pointerup', cancel);
  document.addEventListener('pointercancel', cancel);
  document.addEventListener('pointerleave', cancel);

  renderDadBar();
}

function openPinPrompt() {
  if (getState().dadMode.unlocked) return;
  const backdrop = h(`
    <div class="modal-backdrop">
      <div class="modal-box">
        <div class="title-lg">מצב אבא</div>
        <div class="body-text">הזינו קוד גישה</div>
        <div class="dad-pin-box">
          <input id="dad-pin-input" type="tel" inputmode="numeric" maxlength="3" autofocus />
        </div>
        <div class="btn-row">
          <button class="btn btn-ghost" id="dad-pin-cancel">ביטול</button>
          <button class="btn btn-primary" id="dad-pin-submit">אישור</button>
        </div>
      </div>
    </div>
  `);
  document.body.appendChild(backdrop);
  const input = backdrop.querySelector('#dad-pin-input');
  setTimeout(() => input.focus(), 50);

  const close = () => backdrop.remove();
  backdrop.querySelector('#dad-pin-cancel').addEventListener('click', close);
  backdrop.addEventListener('click', (e) => { if (e.target === backdrop) close(); });

  const submit = () => {
    if (input.value === PIN) {
      setState({ dadMode: { unlocked: true } });
      close();
      toast('מצב אבא פעיל');
      renderDadBar();
    } else {
      input.value = '';
      input.classList.add('shake');
      toast('קוד שגוי');
    }
  };
  backdrop.querySelector('#dad-pin-submit').addEventListener('click', submit);
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter') submit(); });
}

export function renderDadBar() {
  const existing = document.getElementById('dad-admin-bar');
  if (existing) existing.remove();
  if (!getState().dadMode.unlocked) return;

  const bar = h(`
    <div class="dad-bar" id="dad-admin-bar">
      <button class="btn btn-sm" id="dad-prev">קודם</button>
      <button class="btn btn-sm" id="dad-reset-step">איפוס משימה</button>
      <button class="btn btn-sm" id="dad-next">הבא</button>
      <button class="btn btn-sm btn-ghost" id="dad-reset-all">איפוס הכל</button>
      <button class="btn btn-sm btn-ghost" id="dad-lock">נעילה</button>
    </div>
  `);
  document.body.appendChild(bar);

  bar.querySelector('#dad-prev').addEventListener('click', () => {
    prevStep();
    rerenderCallback();
  });
  bar.querySelector('#dad-next').addEventListener('click', () => {
    nextStep();
    rerenderCallback();
  });
  bar.querySelector('#dad-reset-step').addEventListener('click', () => {
    resetStep();
    toast('המשימה אופסה');
    rerenderCallback();
  });
  bar.querySelector('#dad-reset-all').addEventListener('click', () => {
    if (confirm('לאפס את כל המבצע מההתחלה?')) {
      resetAll();
      rerenderCallback();
    }
  });
  bar.querySelector('#dad-lock').addEventListener('click', () => {
    setState({ dadMode: { unlocked: false } });
    renderDadBar();
    toast('מצב אבא ננעל');
  });
}
