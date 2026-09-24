import { EnvelopeIcon, MaskIcon, WineIcon } from './icons';
import OurPhoto from './OurPhoto';
import { intro } from '../data/content';
import styles from './IntroScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function IntroScreen({ onStart }) {
  return (
    <div className={styles.wrap}>
      <OurPhoto slot="intro" variant="intro" />
      <div className={styles.iconRow}>
        <MaskIcon size={26} className={styles.sideIcon} />
        <EnvelopeIcon size={36} />
        <WineIcon size={26} className={styles.sideIcon} />
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
