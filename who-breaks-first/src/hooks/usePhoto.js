import { useEffect, useState } from 'react';
import { getPhoto, PHOTOS_CHANGED } from '../utils/photoStore';

/** מחזיר object URL לתמונה בסלוט, או null. מתעדכן כשתמונה נוספת/נמחקת. */
export function usePhoto(slot) {
  const [url, setUrl] = useState(null);

  useEffect(() => {
    let current = null;
    let cancelled = false;

    const load = async () => {
      const blob = await getPhoto(slot);
      if (cancelled) return;
      if (current) URL.revokeObjectURL(current);
      current = blob ? URL.createObjectURL(blob) : null;
      setUrl(current);
    };

    load();
    window.addEventListener(PHOTOS_CHANGED, load);
    return () => {
      cancelled = true;
      window.removeEventListener(PHOTOS_CHANGED, load);
      if (current) URL.revokeObjectURL(current);
    };
  }, [slot]);

  return url;
}
