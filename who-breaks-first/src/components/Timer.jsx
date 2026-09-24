import { useTimer } from '../hooks/useTimer';
import { ui } from '../data/content';
import styles from './Timer.module.css';
import buttons from '../styles/buttons.module.css';

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

const RING_RADIUS = 42;
const RING_CIRCUMFERENCE = 2 * Math.PI * RING_RADIUS;

export default function Timer({ durationSeconds, mode = 'exact' }) {
  const { secondsLeft, status, start } = useTimer(durationSeconds);

  if (mode === 'ambient') {
    const fraction = durationSeconds > 0 ? secondsLeft / durationSeconds : 0;
    const offset = RING_CIRCUMFERENCE * (1 - fraction);

    return (
      <div className={styles.wrap}>
        <div className={styles.ringWrap}>
          <svg width="100" height="100" viewBox="0 0 100 100" className={styles.ring}>
            <circle cx="50" cy="50" r={RING_RADIUS} className={styles.ringTrack} />
            <circle
              cx="50"
              cy="50"
              r={RING_RADIUS}
              className={`${styles.ringProgress} ${status === 'done' ? styles.ringDone : ''}`}
              style={{ strokeDasharray: RING_CIRCUMFERENCE, strokeDashoffset: offset }}
            />
          </svg>
        </div>
        {status === 'idle' && (
          <button className={buttons.secondary} onClick={start}>
            {ui.startTimer}
          </button>
        )}
        {status === 'running' && <span className={styles.label}>{ui.timerRunning}</span>}
        {status === 'done' && <span className={styles.label}>{ui.timerDoneAmbient}</span>}
      </div>
    );
  }

  return (
    <div className={styles.wrap}>
      <div className={`${styles.clock} ${status === 'done' ? styles.clockDone : ''}`}>
        {formatTime(secondsLeft)}
      </div>
      {status === 'idle' && (
        <button className={buttons.secondary} onClick={start}>
          {ui.startTimer}
        </button>
      )}
      {status === 'running' && <span className={styles.label}>{ui.timerRunning}</span>}
      {status === 'done' && <span className={styles.label}>{ui.timerDone}</span>}
    </div>
  );
}
