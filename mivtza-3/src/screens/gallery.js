import { getState } from '../state.js';
import { memoryImgHTML, MEMORY_COUNT } from '../photos.js';

export default function renderGallery(container, onBack) {
  const photo = getState().m4.photo;

  container.innerHTML = `
    <div class="screen">
      <div class="content content-tight">
        <div class="mission-header">
          <span class="logo-mark" id="logo-longpress">מבצע 3</span>
          <button class="btn btn-sm btn-ghost" id="gallery-back">חזרה</button>
        </div>
        <h1 class="title-lg" style="text-align:center;">הזיכרונות שלנו</h1>
        ${photo ? `
          <div class="photo-preview" style="max-width:280px;margin:0 auto;"><img src="${photo}" alt="התמונה של מבצע 3" /></div>
          <p class="small-note">התמונה של מבצע 3</p>
        ` : ''}
        <div class="gallery-grid">
          ${Array.from({ length: MEMORY_COUNT }, (_, i) => memoryImgHTML(i + 1, `זיכרון ${i + 1}`)).join('')}
        </div>
      </div>
    </div>
  `;

  container.querySelector('#gallery-back').addEventListener('click', onBack);
}
