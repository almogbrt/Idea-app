import CardChooser from './CardChooser';
import { choiceCards, envelopes } from '../data/content';
import styles from './ChoiceModal.module.css';
import buttons from '../styles/buttons.module.css';

const pickOneEnvelope = envelopes.find((e) => e.id === 'pick-one');

export default function ChoiceModal({ selectedId, onSelect, onClose }) {
  return (
    <div className={styles.overlay} role="dialog" aria-modal="true">
      <div className={styles.dialog}>
        <h2 className={styles.title}>{pickOneEnvelope.title}</h2>
        <p className={styles.subtitle}>{pickOneEnvelope.instruction}</p>
        <CardChooser cards={choiceCards} selectedId={selectedId} onSelect={onSelect} />
        {selectedId && (
          <div className={styles.footer}>
            <button className={buttons.primary} onClick={onClose}>
              המשך
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
