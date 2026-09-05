import { rules } from '../data/content';
import RestartLink from './RestartLink';
import styles from './RulesScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function RulesScreen({ onContinue, onRestart }) {
  return (
    <div className={styles.wrap}>
      <div className={styles.topBar}>
        <RestartLink onRestart={onRestart} />
      </div>

      <h1 className={styles.title}>{rules.title}</h1>

      <ul className={styles.list}>
        {rules.list.map((rule) => (
          <li key={rule}>{rule}</li>
        ))}
      </ul>

      <div className={styles.section}>
        <span className={styles.sectionLabel}>{rules.openingTaskLabel}</span>
        <p className={styles.taskText}>{rules.openingTask}</p>
        {rules.openingPrompts.map((prompt) => (
          <p key={prompt} className={styles.prompt}>
            {prompt}
          </p>
        ))}
      </div>

      <div className={styles.footer}>
        <button className={buttons.primary} onClick={onContinue}>
          {rules.cta}
        </button>
      </div>
    </div>
  );
}
