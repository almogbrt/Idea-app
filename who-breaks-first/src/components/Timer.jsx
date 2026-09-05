import { useTimer } from '../hooks/useTimer';
import { ui } from '../data/content';
import styles from './Timer.module.css';
import buttons from '../styles/buttons.module.css';

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

export default function Timer({ durationSeconds }) {
  const { secondsLeft, status, start } = useTimer(durationSeconds);

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
