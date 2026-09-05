import { EnvelopeIcon } from './icons';
import { intro } from '../data/content';
import styles from './IntroScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function IntroScreen({ onStart }) {
  return (
    <div className={styles.wrap}>
      <div className={styles.iconRow}>
        <EnvelopeIcon size={36} />
      </div>
      <h1 className={`${styles.title} serifTitle`}>{intro.title}</h1>
      <div className={styles.divider} />
      <p className={styles.subtitle}>{intro.subtitle}</p>
      <p className={styles.body}>{intro.body}</p>
      <button className={`${buttons.primary} ${styles.cta}`} onClick={onStart}>
        {intro.cta}
      </button>
    </div>
  );
}
