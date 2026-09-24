import { useRef, useState } from 'react';
import ConfirmModal from './ConfirmModal';
import { usePhoto } from '../hooks/usePhoto';
import { savePhoto, deletePhoto, deleteAllPhotos, downscaleImage } from '../utils/photoStore';
import { PHOTO_SLOTS, photosCopy } from '../data/photos';
import styles from './PhotosScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function PhotosScreen({ onDone }) {
  const [confirmDelete, setConfirmDelete] = useState(false);

  return (
    <div className={styles.wrap}>
      <h1 className={styles.title}>{photosCopy.title}</h1>
      <p className={styles.privacy}>{photosCopy.privacy}</p>

      <div className={styles.slots}>
        {PHOTO_SLOTS.map((slot) => (
          <PhotoSlot key={slot.id} slot={slot} />
        ))}
      </div>

      <div className={styles.footer}>
        <button className={buttons.primary} onClick={onDone}>
          {photosCopy.done}
        </button>
        <button className={buttons.ghost} onClick={() => setConfirmDelete(true)}>
          {photosCopy.deleteAll}
        </button>
      </div>

      {confirmDelete && (
        <ConfirmModal
          title={photosCopy.confirmDeleteTitle}
          body={photosCopy.confirmDeleteBody}
          confirmLabel={photosCopy.confirmDeleteYes}
          cancelLabel={photosCopy.confirmDeleteNo}
          onConfirm={async () => {
            setConfirmDelete(false);
            await deleteAllPhotos();
          }}
          onCancel={() => setConfirmDelete(false)}
        />
      )}
    </div>
  );
}

function PhotoSlot({ slot }) {
  const url = usePhoto(slot.id);
  const inputRef = useRef(null);
  const [status, setStatus] = useState('idle'); // idle | saving | error

  const handleFile = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = '';
    if (!file) return;
    setStatus('saving');
    try {
      await savePhoto(slot.id, await downscaleImage(file));
      setStatus('idle');
    } catch {
      setStatus('error');
    }
  };

  return (
    <div className={styles.slot}>
      <div className={styles.thumb}>
        {url ? <img src={url} alt={slot.label} /> : <span className={styles.empty}>{slot.label}</span>}
      </div>
      <div className={styles.meta}>
        <span className={styles.label}>{slot.label}</span>
        <span className={styles.hint}>{status === 'error' ? photosCopy.error : slot.hint}</span>
        <div className={styles.actions}>
          <button className={buttons.secondary} onClick={() => inputRef.current?.click()} disabled={status === 'saving'}>
            {status === 'saving' ? photosCopy.saving : url ? photosCopy.replace : photosCopy.choose}
          </button>
          {url && (
            <button className={buttons.ghost} onClick={() => deletePhoto(slot.id)}>
              {photosCopy.remove}
            </button>
          )}
        </div>
      </div>
      <input ref={inputRef} type="file" accept="image/*" hidden onChange={handleFile} />
    </div>
  );
}
