import { usePhoto } from '../hooks/usePhoto';
import { photosCopy } from '../data/photos';
import styles from './OurPhoto.module.css';

/** מציג את התמונה של הסלוט אם הועלתה; אחרת לא מרנדר כלום — המסך נראה בדיוק כמו קודם. */
export default function OurPhoto({ slot, variant = 'card' }) {
  const url = usePhoto(slot);
  if (!url) return null;
  return (
    <div className={`${styles.frame} ${styles[variant] || ''}`}>
      <img className={styles.img} src={url} alt={photosCopy.alt} />
    </div>
  );
}
