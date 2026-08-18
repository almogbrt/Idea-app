import { getState, subscribe } from './state.js';
import { initDadMode, renderDadBar } from './dadmode.js';
import { isMuted, toggleMute } from './audio.js';

import renderIntro from './screens/intro.js';
import renderMission1 from './screens/mission1.js';
import renderMission2 from './screens/mission2.js';
import renderTransition from './screens/transition.js';
import renderMission3 from './screens/mission3.js';
import renderMission4 from './screens/mission4.js';
import renderMission5 from './screens/mission5.js';
import renderMission6 from './screens/mission6.js';
import renderMission7 from './screens/mission7.js';
import renderMission8 from './screens/mission8.js';
import renderMission9 from './screens/mission9.js';

const appEl = document.getElementById('app');
const screenRoot = document.createElement('div');
screenRoot.id = 'screen-root';
appEl.appendChild(screenRoot);

let currentCleanup = null;
let currentStep = null;

function dispatch(step) {
  if (step === 'intro') return renderIntro(screenRoot);
  if (step === 'm1') return renderMission1(screenRoot);
  if (step === 'm2') return renderMission2(screenRoot);
  if (step === 't2' || step === 't4' || step === 't6') return renderTransition(screenRoot, step);
  if (step === 'm3') return renderMission3(screenRoot);
  if (step === 'm4') return renderMission4(screenRoot);
  if (step === 'm5') return renderMission5(screenRoot);
  if (step === 'm6') return renderMission6(screenRoot);
  if (step === 'm7') return renderMission7(screenRoot);
  if (step === 'm8') return renderMission8(screenRoot);
  if (step === 'm9') return renderMission9(screenRoot);
  return renderIntro(screenRoot);
}

function renderMute() {
  let btn = document.getElementById('mute-toggle');
  if (!btn) {
    btn = document.createElement('button');
    btn.id = 'mute-toggle';
    btn.className = 'mute-toggle';
    btn.addEventListener('click', () => {
      toggleMute();
      renderMute();
    });
    document.body.appendChild(btn);
  }
  btn.textContent = isMuted() ? '🔇' : '🔊';
  btn.setAttribute('aria-label', isMuted() ? 'הפעל צלילים' : 'השתק צלילים');
}

function renderAll() {
  const step = getState().step;
  if (typeof currentCleanup === 'function') {
    currentCleanup();
    currentCleanup = null;
  }
  // safety net: dad-mode can jump away mid-cinematic sequence (mission 9);
  // that overlay lives on document.body, not inside screenRoot, so clear it explicitly.
  const strandedCinema = document.querySelector('.cinema');
  if (strandedCinema) strandedCinema.remove();
  currentStep = step;
  currentCleanup = dispatch(step);
  renderMute();
  renderDadBar();
}

subscribe(() => {
  // Only a full screen rebuild when the top-level step actually changed;
  // in-mission state changes are handled locally by each screen module.
  if (getState().step !== currentStep) {
    renderAll();
  } else {
    renderDadBar();
  }
});

initDadMode(renderAll);
renderAll();

// ---------- PWA: service worker registration ----------
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(() => {
      /* offline support is a bonus — fail silently if unsupported */
    });
  });
}
