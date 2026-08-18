import { getState, setState, goToStep } from '../state.js';
import { missionHeader } from '../ui.js';
import { playSuccess } from '../audio.js';

const APPROVERS = [
  { key: 'noam', label: 'נועם' },
  { key: 'rom', label: 'רום' },
  { key: 'niv', label: 'ניב' }
];

function allApproved(approvals) {
  return APPROVERS.every((a) => approvals[a.key]);
}

export default function renderMission7(container) {
  const draw = () => {
    const approvals = getState().m7.approvals;
    const complete = allApproved(approvals);

    container.innerHTML = `
      <div class="screen">
        <div class="content">
          ${missionHeader('m7')}
          <div class="eyebrow">אחרי המסלול</div>
          <h1 class="title-xl">50 שקלים</h1>
          <div class="highlight-line accent" style="font-size:40px;">₪50</div>
          <p class="body-text">קנו דבר אחד שיהפוך את הערב של כולנו בקמפינג ליותר כיפי.</p>

          <div class="card">
            <div class="body-text">לא קונים שלושה דברים נפרדים.</div>
            <div class="body-text">לא מחלקים את הכסף.</div>
            <div class="body-text">אסור לעבור את התקציב.</div>
            <div class="body-text">שניים נגד אחד? אין החלטה.</div>
          </div>

          <div class="card-title">אישור ההחלטה</div>
          <div class="approval-grid">
            ${APPROVERS.map((a) => `
              <button class="approval-btn ${approvals[a.key] ? 'approved' : ''}" data-key="${a.key}">
                <span class="dot"></span>
                <span>${a.label}</span>
              </button>
            `).join('')}
          </div>

          <div class="spacer"></div>
          <button class="btn btn-primary" id="m7-cta" ${complete ? '' : 'disabled'}>3 מתוך 3 — ממשיכים</button>
        </div>
      </div>
    `;

    container.querySelectorAll('.approval-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.key;
        const current = getState().m7.approvals[key];
        setState({ m7: { approvals: { [key]: !current } } });
        const wasComplete = complete;
        draw();
        if (!wasComplete && allApproved(getState().m7.approvals)) playSuccess();
      });
    });

    container.querySelector('#m7-cta').addEventListener('click', () => {
      if (!allApproved(getState().m7.approvals)) return;
      goToStep('m8');
    });
  };

  draw();
}
