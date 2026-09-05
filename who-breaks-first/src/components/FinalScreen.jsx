import { finalScreen } from '../data/content';
import RestartLink from './RestartLink';
import { KeyIcon } from './icons';
import styles from './FinalScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function FinalScreen({ onContinue, onRestart }) {
  return (
    <div className={styles.wrap}>
      <div className={styles.topBar}>
        <RestartLink onRestart={onRestart} />
      </div>

      <div className={styles.iconRow}>
        <KeyIcon size={30} />
      </div>

      <h1 className={styles.title}>{finalScreen.title}</h1>

      <div className={styles.section}>
        {finalScreen.prompts.map((prompt) => (
          <p key={prompt} className={styles.prompt}>
            {prompt}
          </p>
        ))}
      </div>

      <p className={styles.kissLine}>{finalScreen.kissLine}</p>
      <p className={styles.closing}>{finalScreen.closingText}</p>

      <div className={styles.footer}>
        <button className={buttons.primary} onClick={onContinue}>
          {finalScreen.cta}
        </button>
      </div>
    </div>
  );
}
