import { goToStep } from '../state.js';
import { missionHeader } from '../ui.js';
import { memoryPath } from '../photos.js';

export default function renderIntro(container) {
  container.innerHTML = `
    <div class="screen">
      <div class="hero">
        <img src="${memoryPath(1)}" alt="נועם, רום וניב" loading="eager" />
        <div class="hero-fallback" style="display:none">
          <span style="font-size:34px;opacity:.5">🖤</span>
          <span>מקום לתמונת הגיבורים — memory-01.jpg</span>
        </div>
        <div class="hero-overlay">
          <div class="hero-title">מבצע 3</div>
          <div class="hero-subtitle">נועם • רום • ניב</div>
        </div>
      </div>
      <div class="content">
        ${missionHeader(null)}
        <div class="center-col content-tight">
          <p class="body-text" style="text-align:center;font-size:19px;font-weight:700;">שלושה אחים. צוות אחד.</p>
          <p class="body-text" style="text-align:center;">מהרגע הזה אתם צוות אחד.</p>
          <div class="highlight-line accent">או ששלושתכם מצליחים — או שאף אחד לא מצליח.</div>
          <p class="body-text" style="text-align:center;">אין מקום ראשון. אין מקום שני. אין מקום שלישי.</p>
        </div>
        <button class="btn btn-primary" id="start-btn">התחלנו</button>
      </div>
    </div>
  `;

  const heroImg = container.querySelector('.hero img');
  const fallback = container.querySelector('.hero-fallback');
  if (heroImg) {
    heroImg.addEventListener('error', () => {
      heroImg.style.display = 'none';
      fallback.style.display = 'flex';
    }, { once: true });
  }

  container.querySelector('#start-btn').addEventListener('click', () => {
    goToStep('m1');
  });
}
