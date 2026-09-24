import { useEffect, useMemo, useState } from 'react';
import { useReducedMotion } from '../hooks/useReducedMotion';
import { pickLine } from '../data/microcopy';
import { ui } from '../data/content';
import styles from './FakeOut.module.css';
import buttons from '../styles/buttons.module.css';

/**
 * מודיפייר תצוגה נדיר — לא קלף חדש. מוצג לפני חשיפת מעטפה שנבחרה,
 * ומעכב את הסיפוק המיידי בכמה שניות. הסתברות ההפעלה נקבעת במנוע (engine.js).
 */
export default function FakeOut({ onDone }) {
  const reducedMotion = useReducedMotion();
  const bridgeLine = useMemo(() => pickLine('fakeOut'), []);
  const [step, setStep] = useState(reducedMotion ? 2 : 0);

  useEffect(() => {
    if (reducedMotion) return undefined;
    const timers = [setTimeout(() => setStep(1), 900), setTimeout(() => setStep(2), 1800)];
    return () => timers.forEach(clearTimeout);
  }, [reducedMotion]);

  return (
    <div className={styles.overlay}>
      <p className={`${styles.line} ${step >= 0 ? styles.lineIn : ''}`}>לא.</p>
      {step >= 1 && <p className={`${styles.line} ${styles.lineIn}`}>עוד לא.</p>}
      {step >= 2 && (
        <>
          <p className={`${styles.bridge} ${styles.lineIn}`}>{bridgeLine}</p>
          <button className={`${buttons.gold} ${styles.cta}`} onClick={onDone}>
            {ui.continue}
          </button>
        </>
      )}
    </div>
  );
}
