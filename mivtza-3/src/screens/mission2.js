import { getState, setState, goToStep, SIBLING_LABELS, GEAR_ITEMS_LIST } from '../state.js';
import { missionHeader } from '../ui.js';
import { playSuccess } from '../audio.js';

function allChecked(m2) {
  return ['noam', 'rom', 'niv'].every((checker) =>
    GEAR_ITEMS_LIST.every((item) => m2[checker].list[item])
  );
}

function sectionHTML(checkerKey, m2) {
  const checker = SIBLING_LABELS[checkerKey];
  const target = SIBLING_LABELS[m2[checkerKey].checks];
  const list = m2[checkerKey].list;
  const doneCount = GEAR_ITEMS_LIST.filter((i) => list[i]).length;
  const done = doneCount === GEAR_ITEMS_LIST.length;
  return `
    <div class="card">
      <div class="card-title">
        <span>${checker} בודק את ${target}</span>
        <span class="tag ${done ? 'done' : ''}">${doneCount}/${GEAR_ITEMS_LIST.length}</span>
      </div>
      <div class="checklist" data-checker="${checkerKey}">
        ${GEAR_ITEMS_LIST.map((item) => `
          <div class="check-item ${list[item] ? 'checked' : ''}" data-item="${item}">
            <span class="box">${list[item] ? '✓' : ''}</span>
            <span class="label">${item}</span>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

export default function renderMission2(container) {
  const render = () => {
    const state = getState();
    const complete = allChecked(state.m2);
    container.innerHTML = `
      <div class="screen">
        <div class="content">
          ${missionHeader('m2')}
          <div class="eyebrow">בדיקת ציוד</div>
          <h1 class="title-xl">שלושה תיקים, צוות אחד</h1>
          <div class="rule-banner">לא אומרים "אתה שכחת".<br/>אומרים: "חסר לנו".</div>
          ${sectionHTML('noam', state.m2)}
          ${sectionHTML('rom', state.m2)}
          ${sectionHTML('niv', state.m2)}
          <button class="btn btn-primary" id="m2-cta" ${complete ? '' : 'disabled'}>כל התיקים מוכנים</button>
        </div>
      </div>
    `;

    container.querySelectorAll('.check-item').forEach((el) => {
      el.addEventListener('click', () => {
        const checker = el.closest('.checklist').dataset.checker;
        const item = el.dataset.item;
        const current = getState().m2[checker].list[item];
        setState({ m2: { [checker]: { list: { [item]: !current } } } });
        const wasComplete = complete;
        render();
        if (!wasComplete && allChecked(getState().m2)) playSuccess();
      });
    });

    container.querySelector('#m2-cta').addEventListener('click', () => {
      if (!allChecked(getState().m2)) return;
      goToStep('t2');
    });
  };

  render();
}
