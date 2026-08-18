// עזרי תמונות זיכרון (memory-01.jpg ... memory-09.jpg).
// אם קובץ חסר — נופלים בחן לכרטיס placeholder כהה, בלי לשבור את החוויה.

export const MEMORY_COUNT = 9;

export function memoryPath(n) {
  const idx = String(n).padStart(2, '0');
  return `./images/memories/memory-${idx}.jpg`;
}

// מחזיר HTML למחרוזת <div> עטיפה עם <img> + נפילה חיננית אם התמונה חסרה.
export function memoryImgHTML(n, altText, extraClass = '') {
  const src = memoryPath(n);
  return `
    <div class="memory-photo-wrap ${extraClass}" data-memory-index="${n}">
      <img src="${src}" alt="${altText}" loading="lazy"
        onerror="this.closest('.memory-photo-wrap').classList.add('img-missing'); this.style.display='none';" />
      <div class="img-missing-fallback">
        <span class="img-missing-icon">🖼</span>
        <span>הוסיפו כאן תמונה</span>
        <code>memory-${String(n).padStart(2, '0')}.jpg</code>
      </div>
    </div>`;
}

export function checkImageExists(src) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => resolve(true);
    img.onerror = () => resolve(false);
    img.src = src;
  });
}
