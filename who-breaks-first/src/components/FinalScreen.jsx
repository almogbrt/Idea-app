import { finalScreen } from '../data/content';
import styles from './FinalScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function FinalScreen({ onContinue }) {
  return (
    <div className={styles.wrap}>
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
