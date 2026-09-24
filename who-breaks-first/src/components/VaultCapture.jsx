import { useState } from 'react';
import { VAULT_PROMPTS, VAULT_TEXT_MAX, vaultCopy } from '../data/vault';
import styles from './VaultCapture.module.css';
import buttons from '../styles/buttons.module.css';

/** אופציונלי לגמרי — מקופל כברירת מחדל, ולעולם לא חוסם את המשך המשחק. */
export default function VaultCapture({ source, players, alreadySaved, onSave }) {
  const [phase, setPhase] = useState(alreadySaved ? 'saved' : 'closed'); // closed -> open -> saved
  const [playerId, setPlayerId] = useState('p1');
  const [text, setText] = useState('');

  if (phase === 'saved') {
    return <p className={styles.saved}>{vaultCopy.saved}</p>;
  }

  if (phase === 'closed') {
    return (
      <button className={styles.openLink} onClick={() => setPhase('open')}>
        {vaultCopy.open}
      </button>
    );
  }

  const handleSave = () => {
    if (!text.trim()) return;
    onSave({ source, playerId, text });
    setPhase('saved');
  };

  return (
    <div className={styles.panel}>
      <p className={styles.prompt}>{VAULT_PROMPTS[source]}</p>

      <div className={styles.whose} role="radiogroup" aria-label={vaultCopy.whose}>
        {['p1', 'p2'].map((id) => (
          <button
            key={id}
            role="radio"
            aria-checked={playerId === id}
            className={`${styles.chip} ${playerId === id ? styles.chipActive : ''}`}
            onClick={() => setPlayerId(id)}
          >
            {players[id]}
          </button>
        ))}
      </div>

      <textarea
        className={styles.input}
        value={text}
        maxLength={VAULT_TEXT_MAX}
        rows={2}
        placeholder={vaultCopy.placeholder}
        onChange={(e) => setText(e.target.value)}
      />

      <div className={styles.row}>
        <button className={buttons.ghost} onClick={() => setPhase('closed')}>
          {vaultCopy.cancel}
        </button>
        <button className={buttons.secondary} onClick={handleSave} disabled={!text.trim()}>
          {vaultCopy.save}
        </button>
      </div>
    </div>
  );
}
