import { useEffect, useState } from 'react';
import { useReducedMotion } from '../hooks/useReducedMotion';
import styles from './ProgressiveReveal.module.css';

/**
 * חושף שורות טקסט בהדרגה, אחת אחרי השנייה, לפי delay שמוגדר לכל שורה.
 * שמורה לרגעים נדירים ובוחרים בלבד — שימוש-יתר הורס את האפקט.
 *
 * steps: [{ text, delay }]
 */
export default function ProgressiveReveal({ steps, stepClassName = '' }) {
  const reducedMotion = useReducedMotion();
  const [visibleCount, setVisibleCount] = useState(reducedMotion ? steps.length : 0);

  useEffect(() => {
    if (reducedMotion) {
      setVisibleCount(steps.length);
      return undefined;
    }
    setVisibleCount(0);
    const timers = steps.map((step, i) => setTimeout(() => setVisibleCount((v) => Math.max(v, i + 1)), step.delay));
    return () => timers.forEach(clearTimeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [steps, reducedMotion]);

  return (
    <div className={styles.wrap}>
      {steps.slice(0, visibleCount).map((step, i) => (
        <p key={i} className={`${styles.step} ${stepClassName} ${reducedMotion ? '' : styles.stepIn}`}>
          {step.text}
        </p>
      ))}
    </div>
  );
}
