import CardChooser from './CardChooser';
import RestartLink from './RestartLink';
import { CardIcon } from './icons';
import { loserCards, ui } from '../data/content';
import styles from './LoserEnvelope.module.css';
import buttons from '../styles/buttons.module.css';

export default function LoserEnvelope({ selectedId, onSelect, onRestart }) {
  return (
    <div className={styles.wrap}>
      {!selectedId && (
        <div className={styles.topBar}>
          <RestartLink onRestart={onRestart} />
        </div>
      )}

      <div className={styles.iconRow}>
        <CardIcon size={30} />
      </div>

      <h1 className={styles.title}>מעטפת המפסיד</h1>

      <CardChooser cards={loserCards} selectedId={selectedId} onSelect={onSelect} />

      {selectedId && (
        <div className={styles.footer}>
          <p className={styles.note}>{ui.playAgainNote}</p>
          <button className={buttons.primary} onClick={onRestart}>
            {ui.restart}
          </button>
        </div>
      )}
    </div>
  );
}
