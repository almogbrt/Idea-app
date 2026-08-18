import { getState, setState } from '../state.js';
import { missionHeader } from '../ui.js';
import { memoryPath } from '../photos.js';
import { playSuccess } from '../audio.js';
import { fireConfetti } from '../confetti.js';
import renderGallery from './gallery.js';

const CINEMA_SLIDES = [
  { photo: 3, caption: 'עברתם כבר לא מעט ביחד.' },
  { photo: 5, caption: 'גדלתם.' },
  { photo: 6, caption: 'רבתם.' },
  { photo: 7, caption: 'צחקתם.' },
  { photo: 8, caption: 'עזרתם אחד לשני.' },
  { photo: 9, caption: 'והיום הוכחתם משהו.' }
];

const SLIDE_MS = 3200;

function card(container, { eyebrow, titleHTML, bodyHTML, buttonLabel, onNext, extraHTML = '' }) {
  container.innerHTML = `
    <div class="screen">
      <div class="content">
        ${missionHeader('m9')}
        <div class="center-col content-tight">
          ${eyebrow ? `<div class="eyebrow" style="text-align:center;">${eyebrow}</div>` : ''}
          ${titleHTML || ''}
          ${bodyHTML || ''}
          ${extraHTML}
        </div>
        <button class="btn btn-primary" id="m9-next">${buttonLabel}</button>
      </div>
    </div>
  `;
  container.querySelector('#m9-next').addEventListener('click', onNext);
}

function runCinematicSequence(onFinish) {
  const overlay = document.createElement('div');
  overlay.className = 'cinema';
  overlay.innerHTML = `
    <button class="cinema-skip" id="cinema-skip">דלגו</button>
  `;
  document.body.appendChild(overlay);

  let index = 0;
  let timeoutId = null;

  function showSlide(i) {
    const old = overlay.querySelector('.cinema-slide');
    if (old) old.remove();
    const slide = CINEMA_SLIDES[i];
    const el = document.createElement('div');
    el.className = 'cinema-slide';
    el.innerHTML = `
      <img src="${memoryPath(slide.photo)}" alt="" />
      <div class="cinema-fallback" style="display:none"></div>
      <div class="cinema-caption">${slide.caption}</div>
    `;
    overlay.insertBefore(el, overlay.firstChild);
    const img = el.querySelector('img');
    const fallback = el.querySelector('.cinema-fallback');
    img.addEventListener('error', () => {
      img.style.display = 'none';
      fallback.style.display = 'block';
    }, { once: true });
  }

  function next() {
    if (index >= CINEMA_SLIDES.length) {
      finish();
      return;
    }
    showSlide(index);
    index += 1;
    timeoutId = setTimeout(next, SLIDE_MS);
  }

  function finish() {
    clearTimeout(timeoutId);
    overlay.remove();
    onFinish();
  }

  overlay.querySelector('#cinema-skip').addEventListener('click', finish);
  next();
}

export default function renderMission9(container) {
  const goPhase = (n) => { setState({ m9: { phase: n } }); render(); };

  function render() {
    const phase = getState().m9.phase || 1;

    if (phase === 1) {
      return card(container, {
        eyebrow: 'בלילה אחרי ארוחת הערב',
        titleHTML: '<h1 class="title-xl" style="text-align:center;">המשימה האחרונה</h1>',
        bodyHTML: `<p class="body-text" style="text-align:center;">עכשיו הגיע הזמן לגלות מה באמת היה מבצע 3.
המשימה לא הייתה להגיע לגני חוגה.
היא לא הייתה לסיים את המסלול.
היא לא הייתה להקים אוהל.
והיא אפילו לא הייתה לפתוח את כל המשימות.</p>`,
        buttonLabel: 'המשך',
        onNext: () => goPhase(2)
      });
    }

    if (phase === 2) {
      return card(container, {
        bodyHTML: `<div class="highlight-line accent">הייתה לכם משימה אחת במשך כל היום:<br/>להצליח ביחד.</div>`,
        buttonLabel: 'המשך',
        onNext: () => goPhase(3)
      });
    }

    if (phase === 3) {
      return card(container, {
        bodyHTML: `<p class="body-text" style="text-align:center;">בבוקר דאגתם שכולם מוכנים.
בתיקים דאגתם אחד לשני.
בחידה לכל אחד היה חלק מהתשובה.
במסלול אף אחד לא נשאר מאחור.
את המטען הייתם חייבים להעביר ביניכם.
אפילו 50 ₪ לא יכולתם להוציא בלי להגיע להסכמה.</p>`,
        buttonLabel: 'המשך',
        onNext: () => goPhase(4)
      });
    }

    if (phase === 4) {
      return card(container, {
        bodyHTML: `<p class="body-text" style="text-align:center;font-size:19px;font-weight:700;">עכשיו מותר לפתוח את המטען.</p>`,
        buttonLabel: 'פתחו את המטען',
        onNext: () => {
          setState({ m9: { phase: 5 } });
          runCinematicSequence(() => {
            setState({ m9: { phase: 6 } });
            render();
          });
        }
      });
    }

    if (phase === 5) {
      // mid-cinematic (e.g. reload happened during sequence) — just replay it
      return card(container, {
        bodyHTML: `<p class="body-text" style="text-align:center;">רגע של זיכרונות...</p>`,
        buttonLabel: 'המשך',
        onNext: () => {
          runCinematicSequence(() => {
            setState({ m9: { phase: 6 } });
            render();
          });
        }
      });
    }

    if (phase === 6) {
      return card(container, {
        bodyHTML: `<div class="highlight-line accent" style="font-size:24px;">תמיד יש לכם אחד את השני.</div>`,
        buttonLabel: 'המשך',
        onNext: () => goPhase(7)
      });
    }

    if (phase === 7) {
      const photo = getState().m4.photo;
      return card(container, {
        bodyHTML: photo
          ? `<div class="photo-preview"><img src="${photo}" alt="התמונה של מבצע 3" /></div><p class="small-note">התמונה של מבצע 3</p>`
          : `<p class="body-text" style="text-align:center;">התמונה של מבצע 3</p>`,
        buttonLabel: 'המשך',
        onNext: () => goPhase(8)
      });
    }

    if (phase === 8) {
      return card(container, {
        bodyHTML: `<p class="body-text" style="text-align:center;">אתם אחים.
לא תמיד תסכימו.
אתם תריבו.
אתם תעצבנו אחד את השני.
לפעמים אחד יהיה טוב במשהו שהאחר פחות טוב בו.
לפעמים אחד יצטרך עזרה.
יום אחד תהיו גדולים.
לכל אחד יהיו החיים שלו.
ואבא לא תמיד יהיה לידכם כדי לפתור דברים.
אבל תמיד יהיה לכם אחד את השני.
לא משנה בני כמה תהיו.
לא משנה איפה תהיו.
ולא משנה על מה רבתם אתמול.
אתם שלושה אחים —
ואתם תמיד באותו צוות.</p>`,
        buttonLabel: 'סיום המבצע',
        onNext: () => {
          setState({ m9: { phase: 9 }, completed: true });
          render();
        }
      });
    }

    // phase 9: MISSION COMPLETE
    renderComplete();
  }

  function renderComplete() {
    const photo = getState().m4.photo;
    container.innerHTML = `
      <div class="screen">
        <div class="content center-col">
          ${missionHeader(null)}
          <div class="complete-title">MISSION COMPLETE</div>
          <div class="complete-sub">מבצע 3 הושלם</div>
          ${photo ? `<div class="photo-preview" style="max-width:320px;margin:0 auto;"><img src="${photo}" alt="התמונה של מבצע 3" /></div>` : ''}
          <div class="dad-heart">אבא ♥</div>
          <div class="spacer"></div>
          <button class="btn btn-primary" id="m9-gallery-btn">הזיכרונות שלנו</button>
        </div>
      </div>
    `;
    container.querySelector('#m9-gallery-btn').addEventListener('click', () => {
      renderGallery(container, () => render());
    });

    if (!getState().m9.celebrated) {
      setState({ m9: { celebrated: true } });
      fireConfetti();
      playSuccess();
    }
  }

  render();
}
