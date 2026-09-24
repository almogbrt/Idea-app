// התמונות נשמרות רק בדפדפן של המכשיר הזה (IndexedDB) — לא עולות לשום שרת,
// לא נכנסות לקוד ולא ל-localStorage של מצב המשחק. "התחל מחדש" לא נוגע בהן.

const DB_NAME = 'who-breaks-first-photos';
const STORE = 'photos';
export const PHOTOS_CHANGED = 'wbf-photos-changed';

function openDb() {
  return new Promise((resolve, reject) => {
    if (typeof indexedDB === 'undefined') {
      reject(new Error('IndexedDB unavailable'));
      return;
    }
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => req.result.createObjectStore(STORE);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function run(mode, fn) {
  const db = await openDb();
  try {
    return await new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, mode);
      const req = fn(tx.objectStore(STORE));
      tx.oncomplete = () => resolve(req?.result);
      tx.onerror = () => reject(tx.error);
      tx.onabort = () => reject(tx.error);
    });
  } finally {
    db.close();
  }
}

function notify() {
  window.dispatchEvent(new Event(PHOTOS_CHANGED));
}

export async function getPhoto(slot) {
  try {
    const blob = await run('readonly', (store) => store.get(slot));
    return blob instanceof Blob ? blob : null;
  } catch {
    return null;
  }
}

export async function savePhoto(slot, blob) {
  await run('readwrite', (store) => store.put(blob, slot));
  notify();
}

export async function deletePhoto(slot) {
  await run('readwrite', (store) => store.delete(slot));
  notify();
}

export async function deleteAllPhotos() {
  await run('readwrite', (store) => store.clear());
  notify();
}

/**
 * מקטין תמונה על המכשיר לפני שמירה — תמונת מצלמה של 5–12MB הופכת ל-~200KB,
 * כך שהאחסון לא מתמלא והטעינה במשחק מיידית.
 */
export function downscaleImage(file, maxSide = 1400, quality = 0.84) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      const scale = Math.min(1, maxSide / Math.max(img.naturalWidth, img.naturalHeight));
      const canvas = document.createElement('canvas');
      canvas.width = Math.round(img.naturalWidth * scale);
      canvas.height = Math.round(img.naturalHeight * scale);
      canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
      URL.revokeObjectURL(url);
      canvas.toBlob((blob) => (blob ? resolve(blob) : reject(new Error('encode failed'))), 'image/jpeg', quality);
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error('unreadable image'));
    };
    img.src = url;
  });
}
