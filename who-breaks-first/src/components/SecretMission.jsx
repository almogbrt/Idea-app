import { useEffect, useRef, useState } from 'react';
import { secretMissionCopy } from '../data/secretMissions';
import { MaskIcon } from './icons';
import styles from './SecretMission.module.css';
import buttons from '../styles/buttons.module.css';

const HOLD_MS = 700;

/**
 * "משימה סודית" — נראית רק לשחקן/ית אחד/ת. אחרי "הבנתי" הטקסט מוסר לגמרי
 * מה-DOM (לא רק opacity:0) ואין דרך לחזור אליו — onAck מנקה את המצב הגלובלי.
 */
export default function SecretMission({ mission, playerName, onAck }) {
  const [phase, setPhase] = useState('handoff'); // handoff -> ready -> revealed -> return
  const [holding, setHolding] = useState(false);
  const holdTimer = useRef(null);

  useEffect(() => () => clearTimeout(holdTimer.current), []);

  const startHold = () => {
    setHolding(true);
    holdTimer.current = setTimeout(() => setPhase('revealed'), HOLD_MS);
  };

  const cancelHold = () => {
    setHolding(false);
    clearTimeout(holdTimer.current);
  };

  if (phase === 'handoff') {
    return (
      <div className={styles.overlay}>
        <MaskIcon size={30} className={styles.icon} />
        <p className={styles.name}>{playerName}</p>
        <p className={styles.instruction}>{secretMissionCopy.nextScreenNote}</p>
        <button className={buttons.gold} onClick={() => setPhase('ready')}>
          {secretMissionCopy.aloneWithPhoneCta}
        </button>
      </div>
    );
  }

  if (phase === 'ready') {
    return (
      <div className={styles.overlay}>
        <button
          className={`${styles.holdButton} ${holding ? styles.holding : ''}`}
          onPointerDown={startHold}
          onPointerUp={cancelHold}
          onPointerLeave={cancelHold}
          onPointerCancel={cancelHold}
        >
          {secretMissionCopy.pressAndHold}
        </button>
      </div>
    );
  }

  if (phase === 'revealed') {
    return (
      <div className={styles.overlay}>
        <p className={styles.missionBody}>{mission.body}</p>
        <button className={buttons.primary} onClick={() => setPhase('return')}>
          {secretMissionCopy.understood}
        </button>
      </div>
    );
  }

  return (
    <div className={styles.overlay}>
      <p className={styles.returnLine}>{secretMissionCopy.returnPhone}</p>
      <button className={buttons.secondary} onClick={onAck}>
        {secretMissionCopy.continueCta}
      </button>
    </div>
  );
}
