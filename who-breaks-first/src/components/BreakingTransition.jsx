import { useEffect, useState } from 'react';
import { breaking } from '../data/content';
import { vibrate } from '../utils/vibrate';
import RestartLink from './RestartLink';
import { SealIcon } from './icons';
import styles from './BreakingTransition.module.css';
import buttons from '../styles/buttons.module.css';

export default function BreakingTransition({ onContinue, onRestart }) {
  const [step, setStep] = useState(0);

  useEffect(() => {
    vibrate(breaking.vibrationPattern);
    const timers = [
      setTimeout(() => setStep(1), 700),
      setTimeout(() => setStep(2), 2200),
      setTimeout(() => setStep(3), 3200),
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <div className={styles.wrap}>
      <div className={styles.content}>
        {step >= 1 && (
          <div className={styles.icon}>
            <SealIcon size={28} />
          </div>
        )}
        {step >= 1 && <p className={styles.line}>{breaking.lines[0]}</p>}
        {step >= 2 && <p className={`${styles.line} ${styles.gold}`}>{breaking.lines[1]}</p>}
        {step >= 3 && (
          <button className={`${buttons.gold} ${styles.cta}`} onClick={onContinue}>
            {breaking.cta}
          </button>
        )}
      </div>
      {step >= 1 && <RestartLink onRestart={onRestart} className={styles.restartDark} />}
    </div>
  );
}
