import { doubleOrNothing } from '../data/content';
import styles from './DoubleOrNothing.module.css';
import buttons from '../styles/buttons.module.css';

export default function DoubleOrNothing({ onDecline, onAccept }) {
  return (
    <div className={styles.overlay}>
      <h2 className={styles.title}>{doubleOrNothing.title}</h2>
      <p className={styles.subtitle}>{doubleOrNothing.subtitle}</p>
      <div className={styles.buttons}>
        <button className={buttons.gold} onClick={onAccept}>
          {doubleOrNothing.acceptLabel}
        </button>
        <span className={styles.hint}>{doubleOrNothing.acceptHint}</span>
        <button className={buttons.ghost} onClick={onDecline}>
          {doubleOrNothing.declineLabel}
        </button>
      </div>
    </div>
  );
}
