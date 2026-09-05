import { SealIcon } from './icons';
import Timer from './Timer';
import { ui } from '../data/content';
import { vibrate } from '../utils/vibrate';
import styles from './CardChooser.module.css';

export default function CardChooser({ cards, selectedId, onSelect }) {
  const chosen = cards.find((c) => c.id === selectedId);

  const handlePick = (id) => {
    vibrate(25);
    onSelect(id);
  };

  if (chosen) {
    return (
      <div className={`${styles.grid} ${cards.length > 3 ? styles.gridFour : ''}`}>
        <div className={`${styles.card} ${styles.chosen}`}>
          <h3 className={styles.chosenTitle}>{chosen.title}</h3>
          <p className={styles.chosenBody}>{chosen.body}</p>
          {chosen.duration ? <Timer durationSeconds={chosen.duration} /> : null}
        </div>
      </div>
    );
  }

  return (
    <>
      <p className={styles.hint}>{ui.chooseCardHint}</p>
      <div className={`${styles.grid} ${cards.length > 3 ? styles.gridFour : ''}`}>
        {cards.map((card) => (
          <button key={card.id} className={styles.card} onClick={() => handlePick(card.id)} aria-label={ui.chooseCardHint}>
            <SealIcon size={28} />
          </button>
        ))}
      </div>
    </>
  );
}
