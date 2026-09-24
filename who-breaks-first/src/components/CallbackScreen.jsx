import { useEffect, useMemo, useState } from 'react';
import ProgressiveReveal from './ProgressiveReveal';
import { useReducedMotion } from '../hooks/useReducedMotion';
import { callbackCopy } from '../data/vault';
import { vibrate } from '../utils/vibrate';
import styles from './CallbackScreen.module.css';
import buttons from '../styles/buttons.module.css';

/** מחזיר למשחק משפט שנשמר מוקדם יותר — הטקסט מגיע תמיד מה-state, אף פעם לא ממוצא. */
export default function CallbackScreen({ item, speakerName, onDone }) {
  const reducedMotion = useReducedMotion();
  const [ctaVisible, setCtaVisible] = useState(reducedMotion);

  const steps = useMemo(
    () => [
      { text: callbackCopy.opener, delay: 0 },
      { text: item.publicMode ? callbackCopy.leadPublic : callbackCopy.leadPrivate(speakerName, item.playerId), delay: 1300 },
      { text: `"${item.text}"`, delay: 2900 },
      { text: callbackCopy.closer, delay: 4700 },
    ],
    [item, speakerName]
  );

  useEffect(() => {
    vibrate([15, 80, 15]);
    if (reducedMotion) {
      setCtaVisible(true);
      return undefined;
    }
    const timer = setTimeout(() => setCtaVisible(true), 5500);
    return () => clearTimeout(timer);
  }, [reducedMotion]);

  return (
    <div className={styles.overlay}>
      <ProgressiveReveal steps={steps} stepClassName={styles.line} />
      {ctaVisible && (
        <button className={`${buttons.gold} ${styles.cta}`} onClick={onDone}>
          {callbackCopy.cta}
        </button>
      )}
    </div>
  );
}
