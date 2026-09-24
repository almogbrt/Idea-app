import { useEffect, useRef, useState } from 'react';
import Timer from './Timer';
import ProgressiveReveal from './ProgressiveReveal';
import OurPhoto from './OurPhoto';
import { ENVELOPE_PHOTO } from '../data/photos';
import { useReducedMotion } from '../hooks/useReducedMotion';
import { ui } from '../data/content';
import { vibrate } from '../utils/vibrate';
import styles from './EnvelopeCard.module.css';
import buttons from '../styles/buttons.module.css';

export default function EnvelopeCard({ envelope, revealed, onRevealed, onSkip }) {
  const reducedMotion = useReducedMotion();
  const [phase, setPhase] = useState(revealed ? 'revealed' : 'shaking');
  const [bodyVisible, setBodyVisible] = useState(revealed || reducedMotion);
  const timeouts = useRef([]);

  useEffect(() => {
    timeouts.current.forEach(clearTimeout);
    timeouts.current = [];

    if (revealed) {
      setPhase('revealed');
      setBodyVisible(true);
      return undefined;
    }

    if (reducedMotion) {
      setPhase('revealed');
      setBodyVisible(true);
      onRevealed();
      return undefined;
    }

    setPhase('shaking');
    setBodyVisible(false);
    vibrate(15);

    timeouts.current.push(
      setTimeout(() => setPhase('opening'), 450),
      setTimeout(() => setPhase('pause'), 1050),
      setTimeout(() => {
        setPhase('revealed');
        onRevealed();
      }, 1800),
      setTimeout(() => setBodyVisible(true), 2150)
    );

    return () => timeouts.current.forEach(clearTimeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [envelope.id, reducedMotion]);

  if (phase !== 'revealed') {
    return (
      <div className={styles.stage}>
        <div>
          <div className={`${styles.envelope} ${styles[phase] || ''}`}>
            <div className={styles.envelopeBody} />
            <div className={styles.seal} />
            <div className={styles.envelopeFlap} />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.card}>
      <h2 className={styles.cardTitle}>{envelope.title}</h2>
      {ENVELOPE_PHOTO[envelope.id] && <OurPhoto slot={ENVELOPE_PHOTO[envelope.id]} variant="card" />}
      {bodyVisible && (
        <div className={reducedMotion ? '' : styles.bodyIn}>
          {envelope.revealSteps ? (
            <ProgressiveReveal steps={envelope.revealSteps} />
          ) : (
            <>
              {envelope.body && <p className={styles.cardBody}>{envelope.body}</p>}
              {envelope.instruction && <p className={styles.cardBody}>{envelope.instruction}</p>}
            </>
          )}
          {envelope.duration ? <Timer durationSeconds={envelope.duration} mode={envelope.timerMode || 'exact'} /> : null}
          {envelope.special !== 'choice' && envelope.special !== 'danger-check' && (
            <div className={styles.skipRow}>
              <button className={buttons.ghost} onClick={onSkip}>
                {ui.skip}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
