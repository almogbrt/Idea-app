import { getState, setState, goToStep } from '../state.js';
import { missionHeader } from '../ui.js';
import { playSuccess } from '../audio.js';

const APPROVERS = [
  { key: 'noam', label: 'נועם' },
  { key: 'rom', label: 'רום' },
  { key: 'niv', label: 'ניב' }
];

const MAX_DIMENSION = 1280;

function compressImage(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = reject;
    reader.onload = () => {
      const img = new Image();
      img.onerror = reject;
      img.onload = () => {
        let { width, height } = img;
        if (width > height && width > MAX_DIMENSION) {
          height = Math.round((height * MAX_DIMENSION) / width);
          width = MAX_DIMENSION;
        } else if (height > MAX_DIMENSION) {
          width = Math.round((width * MAX_DIMENSION) / height);
          height = MAX_DIMENSION;
        }
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d').drawImage(img, 0, 0, width, height);
        resolve(canvas.toDataURL('image/jpeg', 0.82));
      };
      img.src = reader.result;
    };
    reader.readAsDataURL(file);
  });
}

function allApproved(approvals) {
  return APPROVERS.every((a) => approvals[a.key]);
}

export default function renderMission4(container) {
  const draw = () => {
    const state = getState().m4;
    const complete = state.photo && allApproved(state.approvals);

    container.innerHTML = `
      <div class="screen">
        <div class="content">
          ${missionHeader('m4')}
          <div class="eyebrow">בעצירה הראשונה בדרך</div>
          <h1 class="title-xl">התמונה שלנו</h1>
          <p class="body-text">צרו תמונה אחת שמייצגת את שלושתכם.</p>

          <div class="card">
            <div class="role-card"><div class="role-name">בוחר מקום</div><div class="role-desc">אחד בוחר את המקום.</div></div>
            <div class="role-card"><div class="role-name">בוחר תנוחה</div><div class="role-desc">השני מחליט איך תעמדו ומה תעשו.</div></div>
            <div class="role-card"><div class="role-name">הצלם</div><div class="role-desc">השלישי מצלם ומביים.</div></div>
          </div>

          ${state.photo ? `
            <div class="photo-preview"><img src="${state.photo}" alt="התמונה של מבצע 3" /></div>
            <p class="small-note">התמונה של מבצע 3</p>
            <button class="btn btn-ghost btn-sm" id="m4-retake">צלמו/העלו תמונה אחרת</button>
          ` : `
            <label class="photo-drop" for="m4-file-input">
              <span style="font-size:30px;">📷</span>
              <span>הקישו כדי לצלם או להעלות תמונה</span>
            </label>
            <input type="file" id="m4-file-input" accept="image/*" capture="environment" style="display:none" />
          `}

          ${state.photo ? `
            <div class="card-title" style="margin-top:6px;">אישור התמונה</div>
            <div class="approval-grid">
              ${APPROVERS.map((a) => `
                <button class="approval-btn ${state.approvals[a.key] ? 'approved' : ''}" data-key="${a.key}">
                  <span class="dot"></span>
                  <span>${a.label}</span>
                </button>
              `).join('')}
            </div>
          ` : ''}

          <div class="spacer"></div>
          <button class="btn btn-primary" id="m4-cta" ${complete ? '' : 'disabled'}>זאת התמונה שלנו</button>
        </div>
      </div>
    `;

    const fileInput = container.querySelector('#m4-file-input');
    if (fileInput) {
      fileInput.addEventListener('change', async (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;
        try {
          const dataUrl = await compressImage(file);
          setState({ m4: { photo: dataUrl, approvals: { noam: false, rom: false, niv: false } } });
          draw();
        } catch (err) {
          console.warn('מבצע 3: כשל בטעינת התמונה', err);
        }
      });
    }

    const retake = container.querySelector('#m4-retake');
    if (retake) {
      retake.addEventListener('click', () => {
        setState({ m4: { photo: null, approvals: { noam: false, rom: false, niv: false } } });
        draw();
      });
    }

    container.querySelectorAll('.approval-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.key;
        const current = getState().m4.approvals[key];
        setState({ m4: { approvals: { [key]: !current } } });
        const wasComplete = complete;
        draw();
        if (!wasComplete && allApproved(getState().m4.approvals)) playSuccess();
      });
    });

    container.querySelector('#m4-cta').addEventListener('click', () => {
      if (!complete) return;
      goToStep('t4');
    });
  };

  draw();
}
