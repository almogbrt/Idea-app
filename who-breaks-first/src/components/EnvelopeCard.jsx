import { useEffect, useRef, useState } from 'react';
import Timer from './Timer';
import { ui } from '../data/content';
import { vibrate } from '../utils/vibrate';
import styles from './EnvelopeCard.module.css';
import buttons from '../styles/buttons.module.css';

export default function EnvelopeCard({ envelope, revealed, onRevealed, onSkip }) {
  const [phase, setPhase] = useState(revealed ? 'revealed' : 'shaking');
  const timeouts = useRef([]);

  useEffect(() => {
    timeouts.current.forEach(clearTimeout);
    timeouts.current = [];

    if (revealed) {
      setPhase('revealed');
      return;
    }

    setPhase('shaking');
    vibrate(15);

    timeouts.current.push(
      setTimeout(() => setPhase('opening'), 450),
      setTimeout(() => setPhase('pause'), 1050),
      setTimeout(() => {
        setPhase('revealed');
        onRevealed();
      }, 1750)
    );

    return () => timeouts.current.forEach(clearTimeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [envelope.id]);

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
      {envelope.body && <p className={styles.cardBody}>{envelope.body}</p>}
      {envelope.instruction && <p className={styles.cardBody}>{envelope.instruction}</p>}
      {envelope.duration ? <Timer durationSeconds={envelope.duration} /> : null}
      {envelope.special !== 'choice' && envelope.special !== 'danger-check' && (
        <div className={styles.skipRow}>
          <button className={buttons.ghost} onClick={onSkip}>
            {ui.skip}
          </button>
        </div>
      )}
    </div>
  );
}
