import { playersScreen } from '../data/content';
import RestartLink from './RestartLink';
import styles from './PlayersScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function PlayersScreen({ players, onSetName, onContinue, onRestart }) {
  return (
    <div className={styles.wrap}>
      <div className={styles.topBar}>
        <RestartLink onRestart={onRestart} />
      </div>

      <h1 className={styles.title}>{playersScreen.title}</h1>

      <div className={styles.body}>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="player1-name">
            {playersScreen.label1}
          </label>
          <input
            id="player1-name"
            className={styles.input}
            type="text"
            value={players.p1}
            onChange={(e) => onSetName('p1', e.target.value)}
            maxLength={20}
          />
        </div>

        <div className={styles.field}>
          <label className={styles.label} htmlFor="player2-name">
            {playersScreen.label2}
          </label>
          <input
            id="player2-name"
            className={styles.input}
            type="text"
            value={players.p2}
            onChange={(e) => onSetName('p2', e.target.value)}
            maxLength={20}
          />
        </div>
      </div>

      <div className={styles.footer}>
        <button className={buttons.primary} onClick={onContinue}>
          {playersScreen.cta}
        </button>
      </div>
    </div>
  );
}
