import { useEffect, useState } from 'react';
import ProgressiveReveal from './ProgressiveReveal';
import { MaskIcon } from './icons';
import { useReducedMotion } from '../hooks/useReducedMotion';
import { ui } from '../data/content';
import { microcopy } from '../data/microcopy';
import styles from './PrivateTransition.module.css';
import buttons from '../styles/buttons.module.css';

// ההשהיה לפני השורה האחרונה ("ועכשיו — גם אתם לבד") ארוכה קצת יותר מהאחרות בכוונה.
const STEP_DELAYS = [0, 1400, 2800, 4600];
const STEPS = microcopy.privateTransition.map((text, i) => ({ text, delay: STEP_DELAYS[i] ?? i * 1400 }));
const LAST_STEP_DELAY = STEPS[STEPS.length - 1].delay;

export default function PrivateTransition({ onDone }) {
  const reducedMotion = useReducedMotion();
  const [ctaVisible, setCtaVisible] = useState(reducedMotion);

  useEffect(() => {
    if (reducedMotion) {
      setCtaVisible(true);
      return undefined;
    }
    const timer = setTimeout(() => setCtaVisible(true), LAST_STEP_DELAY + 900);
    return () => clearTimeout(timer);
  }, [reducedMotion]);

  return (
    <div className={styles.overlay}>
      <MaskIcon size={34} className={styles.mask} />
      <ProgressiveReveal steps={STEPS} stepClassName={styles.line} />
      {ctaVisible && (
        <button className={`${buttons.gold} ${styles.cta}`} onClick={onDone}>
          {ui.continue}
        </button>
      )}
    </div>
  );
}
