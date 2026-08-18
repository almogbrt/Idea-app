import { MISSION_NUMBER } from './state.js';

export function h(html) {
  const tpl = document.createElement('template');
  tpl.innerHTML = html.trim();
  return tpl.content.firstElementChild;
}

export function formatTime(ms) {
  const total = Math.max(0, Math.ceil(ms / 1000));
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

// deadline-based countdown: caller supplies onTick(remainingMs) and onDone()
export function startCountdown(deadline, onTick, onDone) {
  let done = false;
  const tick = () => {
    const remaining = deadline - Date.now();
    onTick(Math.max(0, remaining));
    if (remaining <= 0 && !done) {
      done = true;
      onDone && onDone();
    }
  };
  tick();
  const id = setInterval(tick, 250);
  return () => clearInterval(id);
}

export function missionHeader(missionKey, extra = '') {
  const num = MISSION_NUMBER[missionKey];
  const badge = num ? `${String(num).padStart(2, '0')} / 09` : '';
  const pct = num ? Math.round((num / 9) * 100) : 0;
  return `
    <div class="mission-header">
      <span class="logo-mark" id="logo-longpress">מבצע 3</span>
      ${badge ? `<span class="mission-badge">${badge}</span>` : '<span></span>'}
    </div>
    ${num ? `<div class="progress-track"><div class="progress-fill" style="width:${pct}%"></div></div>` : ''}
    ${extra}
  `;
}

export function toast(message, duration = 2400) {
  const el = h(`<div class="toast">${message}</div>`);
  document.body.appendChild(el);
  setTimeout(() => el.remove(), duration);
}

export function modal({ title, body, buttonText = 'הבנתי', onClose } = {}) {
  const backdrop = h(`
    <div class="modal-backdrop">
      <div class="modal-box">
        ${title ? `<div class="title-lg">${title}</div>` : ''}
        ${body ? `<div class="body-text">${body}</div>` : ''}
        <button class="btn btn-primary" id="modal-close-btn">${buttonText}</button>
      </div>
    </div>
  `);
  document.body.appendChild(backdrop);
  const close = () => {
    backdrop.remove();
    onClose && onClose();
  };
  backdrop.querySelector('#modal-close-btn').addEventListener('click', close);
  backdrop.addEventListener('click', (e) => {
    if (e.target === backdrop) close();
  });
  return close;
}
