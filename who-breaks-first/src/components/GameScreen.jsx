import { useState } from 'react';
import EnvelopeCard from './EnvelopeCard';
import ChoiceModal from './ChoiceModal';
import ConfirmModal from './ConfirmModal';
import { ui } from '../data/content';
import { giveUpCaption } from '../game/engine';
import styles from './GameScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function GameScreen({ state, dispatch, currentEnvelope, remainingCount, resetGame }) {
  const [showRestart, setShowRestart] = useState(false);

  const openedCount = state.openedIds.length;
  const caption = giveUpCaption(openedCount, ui);

  const progressText =
    remainingCount === 0 ? ui.noEnvelopesLeft : remainingCount === 1 ? ui.oneEnvelopeLeft : ui.envelopesLeft(remainingCount);

  const handleDraw = () => dispatch({ type: 'DRAW_ENVELOPE' });
  const handleBreak = () => dispatch({ type: 'BREAK' });
  const handleRevealed = () => dispatch({ type: 'MARK_REVEALED' });
  const handleSkip = () => dispatch({ type: 'SKIP_CURRENT' });
  const handleNext = () => dispatch({ type: 'SKIP_CURRENT' });

  const isDangerCard = currentEnvelope?.special === 'danger-check' && state.current?.revealed;
  const isChoiceCard = currentEnvelope?.special === 'choice';

  const tensionClass = state.climaxTriggered
    ? styles.tensionDeep
    : openedCount >= 5
      ? styles.tensionWarm
      : '';

  return (
    <div className={`${styles.wrap} ${tensionClass}`}>
      <div className={styles.header}>
        <span className={styles.progress}>{progressText}</span>
        <button className={styles.restartBtn} onClick={() => setShowRestart(true)}>
          {ui.restart}
        </button>
      </div>

      <div className={styles.stage}>
        {currentEnvelope ? (
          <EnvelopeCard
            envelope={currentEnvelope}
            revealed={Boolean(state.current?.revealed)}
            onRevealed={handleRevealed}
            onSkip={handleSkip}
          />
        ) : state.climaxTriggered ? (
          <div className={styles.climaxPanel}>
            <h2 className={styles.climaxTitle}>{ui.climaxTitle}</h2>
            <p className={styles.climaxSubtitle}>{ui.climaxSubtitle}</p>
            <div className={styles.climaxButtons}>
              {remainingCount > 0 && (
                <button className={buttons.gold} onClick={handleDraw}>
                  {ui.climaxContinue}
                </button>
              )}
              <button className={buttons.secondary} onClick={handleBreak}>
                {ui.giveUp}
              </button>
            </div>
          </div>
        ) : (
          <div className={styles.idleTile}>{ui.closedEnvelopeHint}</div>
        )}

        {isChoiceCard && state.choiceModal && (
          <ChoiceModal
            selectedId={state.choiceModal.selectedId}
            onSelect={(cardId) => dispatch({ type: 'CHOOSE_PICK_ONE_CARD', cardId })}
            onClose={() => dispatch({ type: 'CLOSE_PICK_ONE_MODAL' })}
          />
        )}
      </div>

      {currentEnvelope && state.current?.revealed && !isChoiceCard && (
        <div className={styles.actions}>
          {isDangerCard ? (
            <div className={styles.dangerButtons}>
              <button className={buttons.primary} onClick={handleNext}>
                {ui.dangerContinue}
              </button>
              <button className={buttons.secondary} onClick={handleBreak}>
                {ui.dangerBreak}
              </button>
            </div>
          ) : (
            <button className={buttons.primary} onClick={handleNext}>
              {ui.nextEnvelopeAfterSkip}
            </button>
          )}
        </div>
      )}

      {!currentEnvelope && !state.climaxTriggered && (
        <div className={styles.actions}>
          <button className={buttons.primary} onClick={handleDraw} disabled={remainingCount === 0}>
            {ui.openEnvelope}
          </button>
        </div>
      )}

      <div className={styles.footerBar}>
        <button className={`${buttons.secondary} ${styles.breakBtn}`} onClick={handleBreak}>
          {ui.giveUp}
        </button>
        {caption && <span className={styles.breakCaption}>{caption}</span>}
      </div>

      {showRestart && (
        <ConfirmModal
          title={ui.confirmRestartTitle}
          body={ui.confirmRestartBody}
          confirmLabel={ui.confirmRestartYes}
          cancelLabel={ui.confirmRestartNo}
          onConfirm={() => {
            setShowRestart(false);
            resetGame();
          }}
          onCancel={() => setShowRestart(false)}
        />
      )}
    </div>
  );
}
