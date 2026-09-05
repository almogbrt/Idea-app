import { useState } from 'react';
import ConfirmModal from './ConfirmModal';
import { ui } from '../data/content';
import styles from './RestartLink.module.css';

export default function RestartLink({ onRestart, className = '' }) {
  const [showConfirm, setShowConfirm] = useState(false);

  return (
    <>
      <button className={`${styles.link} ${className}`} onClick={() => setShowConfirm(true)}>
        {ui.restart}
      </button>
      {showConfirm && (
        <ConfirmModal
          title={ui.confirmRestartTitle}
          body={ui.confirmRestartBody}
          confirmLabel={ui.confirmRestartYes}
          cancelLabel={ui.confirmRestartNo}
          onConfirm={() => {
            setShowConfirm(false);
            onRestart();
          }}
          onCancel={() => setShowConfirm(false)}
        />
      )}
    </>
  );
}
