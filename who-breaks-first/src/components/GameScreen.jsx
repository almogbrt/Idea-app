import { useEffect, useState } from 'react';
import EnvelopeCard from './EnvelopeCard';
import ChoiceModal from './ChoiceModal';
import ConfirmModal from './ConfirmModal';
import RestartLink from './RestartLink';
import DoubleOrNothing from './DoubleOrNothing';
import FakeOut from './FakeOut';
import PrivateTransition from './PrivateTransition';
import SecretMission from './SecretMission';
import VaultCapture from './VaultCapture';
import CallbackScreen from './CallbackScreen';
import { EnvelopeIcon, WineIcon } from './icons';
import { ui, riskChoice, feedbackPrompt } from '../data/content';
import { secretMissions } from '../data/secretMissions';
import { VAULT_PROMPTS, anticipationCopy } from '../data/vault';
import { giveUpCaption } from '../game/engine';
import { vibrate } from '../utils/vibrate';
import styles from './GameScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function GameScreen({
  state,
  dispatch,
  currentEnvelope,
  currentDoubleCard,
  remainingCount,
  resetGame,
  visualIntensity,
}) {
  const openedCount = state.openedIds.length;
  const caption = giveUpCaption(openedCount, ui, visualIntensity);

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
  const [showPrivateConfirm, setShowPrivateConfirm] = useState(false);

  // הכיוון PUBLIC→PRIVATE (כיבוי מצב מסעדה) עובר דרך אישור וטרנזישן דרמטי;
  // הכיוון ההפוך (יציאה למסעדה) נשאר מיידי, בלי טקס.
  const handleToggleRestaurantMode = () => {
    if (state.restaurantMode) setShowPrivateConfirm(true);
    else dispatch({ type: 'TOGGLE_RESTAURANT_MODE' });
  };
  const handleConfirmPrivate = () => {
    setShowPrivateConfirm(false);
    dispatch({ type: 'START_PRIVATE_TRANSITION' });
  };
  const handlePrivateTransitionDone = () => dispatch({ type: 'PRIVATE_TRANSITION_DONE' });
  const handleSecretMissionAck = () => dispatch({ type: 'SECRET_MISSION_ACK' });
  const handleFakeOutDone = () => dispatch({ type: 'FAKE_OUT_DONE' });
  const handleVaultSave = ({ source, playerId, text }) => dispatch({ type: 'VAULT_ADD', source, playerId, text });
  const handleCallbackDone = () => dispatch({ type: 'CALLBACK_DONE' });

  const callbackItem = state.callbackActive
    ? state.anticipationQueue.find((q) => q.id === state.callbackActive.id)
    : null;

  // "משהו מחכה לכם" — רק כמות, לעולם לא התוכן. הניסוח מתחלף לפי מספר המעטפות (לא אקראי, כדי שלא יהבהב).
  const pendingCount = state.anticipationQueue.filter((q) => !q.revealed).length;
  const anticipationLine =
    pendingCount === 0
      ? null
      : openedCount % 3 === 2
        ? anticipationCopy.unreturned
        : pendingCount === 1
          ? anticipationCopy.one
          : anticipationCopy.many(pendingCount);

  const canVault = Boolean(currentEnvelope && state.current?.revealed && VAULT_PROMPTS[currentEnvelope.id]);

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

  const doubleCardForView = currentDoubleCard ? { ...currentDoubleCard, duration: currentDoubleCard.timerSeconds } : null;

  return (
    <div className={styles.wrap} data-intensity={visualIntensity}>
      <div className={styles.header}>
        <span className={styles.progress}>{progressText}</span>
        <RestartLink onRestart={resetGame} />
      </div>

      <div className={styles.restaurantRow}>
        <button
          className={`${styles.restaurantToggle} ${state.restaurantMode ? styles.restaurantToggleActive : ''}`}
          onClick={handleToggleRestaurantMode}
          disabled={state.privateTransitionPending || Boolean(state.secretMissionActive) || Boolean(callbackItem)}
        >
          {state.restaurantMode ? ui.restaurantModeOff : ui.restaurantModeOn}
        </button>
        {state.restaurantMode && (
          <span className={styles.restaurantBadge}>
            <WineIcon size={16} plain />
            {ui.restaurantModeBadge}
          </span>
        )}
      </div>

      {anticipationLine && !callbackItem && <p className={styles.anticipation}>{anticipationLine}</p>}

      <div className={styles.stage}>
        {state.privateTransitionPending ? (
          <PrivateTransition onDone={handlePrivateTransitionDone} />
        ) : callbackItem ? (
          <CallbackScreen
            item={callbackItem}
            speakerName={state.players[callbackItem.playerId]}
            onDone={handleCallbackDone}
          />
        ) : state.secretMissionActive ? (
          <SecretMission
            mission={secretMissions.find((m) => m.id === state.secretMissionActive.id)}
            playerName={state.players[state.secretMissionActive.forPlayer]}
            onAck={handleSecretMissionAck}
          />
        ) : doubleCardForView ? (
          <EnvelopeCard
            envelope={doubleCardForView}
            revealed={Boolean(state.doubleCurrent?.revealed)}
            onRevealed={handleDoubleRevealed}
            onSkip={handleDoubleDone}
          />
        ) : state.fakeOutPending ? (
          <FakeOut onDone={handleFakeOutDone} />
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
            <h2 className={`${styles.climaxTitle} serifTitle`}>{ui.climaxTitle}</h2>
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
        ) : state.restaurantModeExhausted ? (
          <div className={styles.idleTile}>
            <EnvelopeIcon size={26} />
            <span>{ui.restaurantModeEmptyTitle}</span>
            <span className={styles.restaurantEmptyBody}>{ui.restaurantModeEmptyBody}</span>
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
          {canVault && (
            <VaultCapture
              key={currentEnvelope.id}
              source={currentEnvelope.id}
              players={state.players}
              alreadySaved={state.vaultedSources.includes(currentEnvelope.id)}
              onSave={handleVaultSave}
            />
          )}
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
        !state.feedbackPending &&
        !state.restaurantModeExhausted &&
        !state.privateTransitionPending &&
        !state.secretMissionActive &&
        !callbackItem && (
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

      {showPrivateConfirm && (
        <ConfirmModal
          title={ui.privateModeConfirmTitle}
          body={ui.privateModeConfirmBody}
          confirmLabel={ui.privateModeConfirmYes}
          cancelLabel={ui.privateModeConfirmNo}
          onConfirm={handleConfirmPrivate}
          onCancel={() => setShowPrivateConfirm(false)}
        />
      )}
    </div>
  );
}
