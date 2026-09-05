import { useEffect } from 'react';
import EnvelopeCard from './EnvelopeCard';
import ChoiceModal from './ChoiceModal';
import RestartLink from './RestartLink';
import DoubleOrNothing from './DoubleOrNothing';
import { EnvelopeIcon } from './icons';
import { ui, riskChoice, feedbackPrompt } from '../data/content';
import { giveUpCaption } from '../game/engine';
import { vibrate } from '../utils/vibrate';
import styles from './GameScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function GameScreen({ state, dispatch, currentEnvelope, currentDoubleCard, remainingCount, resetGame }) {
  const openedCount = state.openedIds.length;
  const caption = giveUpCaption(openedCount, ui);

  const progressText =
    remainingCount === 0 ? ui.noEnvelopesLeft : remainingCount === 1 ? ui.oneEnvelopeLeft : ui.envelopesLeft(remainingCount);

  const handleDraw = () => dispatch({ type: 'DRAW_ENVELOPE' });
  const handleBreak = () => dispatch({ type: 'BREAK' });
  const handleRevealed = () => dispatch({ type: 'MARK_REVEALED' });
  const handleSkip = () => dispatch({ type: 'SKIP_CURRENT' });
  const handleNext = () => dispatch({ type: 'SKIP_CURRENT' });
  const handleChooseSafe = () => dispatch({ type: 'CHOOSE_SAFE' });
  const handleChooseRisk = () => {
    vibrate(25);
    dispatch({ type: 'CHOOSE_RISK' });
  };
  const handleDoubleAccept = () => {
    vibrate([20, 40, 20]);
    dispatch({ type: 'DOUBLE_ACCEPT' });
  };
  const handleDoubleDecline = () => dispatch({ type: 'DOUBLE_DECLINE' });
  const handleDoubleRevealed = () => dispatch({ type: 'MARK_DOUBLE_REVEALED' });
  const handleDoubleDone = () => dispatch({ type: 'DOUBLE_DONE' });
  const handleFeedback = (option) => dispatch({ type: 'GIVE_FEEDBACK', optionId: option.id, delta: option.delta });

  // רטט קצר כשמופיע "דאבל או כלום" — רגע נבדל מפתיחת מעטפה רגילה
  useEffect(() => {
    if (state.doublePending) vibrate([30, 50, 30]);
  }, [state.doublePending]);

  // "אתם ביקשתם את זה" — השהיה קצרה לפני שהמעטפה שנבחרה ב-RISK נחשפת
  useEffect(() => {
    if (!state.riskConfirmPendingId) return undefined;
    const timer = setTimeout(() => dispatch({ type: 'RISK_CONFIRM_DONE' }), 900);
    return () => clearTimeout(timer);
  }, [state.riskConfirmPendingId, dispatch]);

  const isDangerCard = currentEnvelope?.special === 'danger-check' && state.current?.revealed;
  const isChoiceCard = currentEnvelope?.special === 'choice';

  const tensionClass = state.climaxTriggered
    ? styles.tensionDeep
    : openedCount >= 5
      ? styles.tensionWarm
      : '';

  const doubleCardForView = currentDoubleCard ? { ...currentDoubleCard, duration: currentDoubleCard.timerSeconds } : null;

  return (
    <div className={`${styles.wrap} ${tensionClass}`}>
      <div className={styles.header}>
        <span className={styles.progress}>{progressText}</span>
        <RestartLink onRestart={resetGame} />
      </div>

      <div className={styles.stage}>
        {doubleCardForView ? (
          <EnvelopeCard
            envelope={doubleCardForView}
            revealed={Boolean(state.doubleCurrent?.revealed)}
            onRevealed={handleDoubleRevealed}
            onSkip={handleDoubleDone}
          />
        ) : currentEnvelope ? (
          <EnvelopeCard
            envelope={currentEnvelope}
            revealed={Boolean(state.current?.revealed)}
            onRevealed={handleRevealed}
            onSkip={handleSkip}
          />
        ) : state.riskConfirmPendingId ? (
          <div className={styles.riskConfirm}>{riskChoice.confirmLine}</div>
        ) : state.feedbackPending ? (
          <div className={styles.feedbackPanel}>
            <p className={styles.feedbackQuestion}>{feedbackPrompt.question}</p>
            <div className={styles.feedbackOptions}>
              {feedbackPrompt.options.map((option) => (
                <button key={option.id} className={buttons.secondary} onClick={() => handleFeedback(option)}>
                  {option.label}
                </button>
              ))}
            </div>
          </div>
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
        ) : state.riskOfferPending ? (
          <div className={styles.riskPanel}>
            <p className={styles.riskPrompt}>{riskChoice.prompt}</p>
            <div className={styles.riskCards}>
              <button className={styles.safeCard} onClick={handleChooseSafe}>
                <span className={styles.riskCardBody}>{riskChoice.safeBody}</span>
                <span className={styles.safeCardLabel}>{riskChoice.safeLabel}</span>
              </button>
              <button className={styles.riskCard} onClick={handleChooseRisk}>
                <span className={styles.riskCardBody}>{riskChoice.riskBody}</span>
                <span className={styles.riskCardLabel}>{riskChoice.riskLabel}</span>
              </button>
            </div>
          </div>
        ) : (
          <div className={styles.idleTile}>
            <EnvelopeIcon size={26} />
            <span>{ui.closedEnvelopeHint}</span>
          </div>
        )}

        {state.doublePending && (
          <DoubleOrNothing onAccept={handleDoubleAccept} onDecline={handleDoubleDecline} />
        )}

        {isChoiceCard && state.choiceModal && (
          <ChoiceModal
            selectedId={state.choiceModal.selectedId}
            onSelect={(cardId) => dispatch({ type: 'CHOOSE_PICK_ONE_CARD', cardId })}
            onClose={() => dispatch({ type: 'CLOSE_PICK_ONE_MODAL' })}
          />
        )}
      </div>

      {doubleCardForView && state.doubleCurrent?.revealed && (
        <div className={styles.actions}>
          <button className={buttons.primary} onClick={handleDoubleDone}>
            {ui.doubleDone}
          </button>
        </div>
      )}

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

      {!currentEnvelope &&
        !doubleCardForView &&
        !state.climaxTriggered &&
        !state.riskOfferPending &&
        !state.riskConfirmPendingId &&
        !state.feedbackPending && (
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
    </div>
  );
}
