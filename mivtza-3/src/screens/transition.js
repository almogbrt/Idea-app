import { goToStep } from '../state.js';
import { memoryImgHTML } from '../photos.js';

const CONFIG = {
  t2: { photo: 2, next: 'm3' },
  t4: { photo: 4, next: 'm5' },
  t6: { photo: 6, next: 'm7' }
};

export default function renderTransition(container, step) {
  const cfg = CONFIG[step];
  container.innerHTML = `
    <div class="screen">
      <div class="content center-col">
        ${memoryImgHTML(cfg.photo, 'זיכרון משפחתי')}
        <p class="body-text" style="text-align:center;font-size:19px;font-weight:700;">
          זוכרים? אתם כבר עושים דברים ביחד הרבה זמן.
        </p>
        <button class="btn btn-primary" id="transition-next">המשך למשימה הבאה</button>
      </div>
    </div>
  `;

  container.querySelector('#transition-next').addEventListener('click', () => {
    goToStep(cfg.next);
  });
}
