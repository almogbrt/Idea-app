import styles from './ConfirmModal.module.css';
import buttons from '../styles/buttons.module.css';

export default function ConfirmModal({ title, body, confirmLabel, cancelLabel, onConfirm, onCancel }) {
  return (
    <div className={styles.overlay} role="dialog" aria-modal="true">
      <div className={styles.dialog}>
        <h2 className={styles.title}>{title}</h2>
        <p className={styles.body}>{body}</p>
        <div className={styles.actions}>
          <button className={buttons.secondary} onClick={onCancel}>
            {cancelLabel}
          </button>
          <button className={buttons.primary} onClick={onConfirm}>
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
