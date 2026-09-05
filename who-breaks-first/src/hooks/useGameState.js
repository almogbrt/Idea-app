import { useCallback, useEffect, useMemo, useReducer } from 'react';
import { envelopes as ENVELOPES, defaultPlayers, desireQuiz } from '../data/content';
import { doubleCards as DOUBLE_CARDS } from '../data/doubleCards';
import {
  pickNextEnvelope,
  pickDoubleCard,
  shouldTriggerClimax,
  shouldOfferRiskChoice,
  shouldTriggerDoubleOrNothing,
  currentStageLevel,
  createDefaultDesireProfile,
  createDefaultTagWeights,
  applyFeedback,
} from '../game/engine';
import { loadState, saveState, clearState } from '../utils/storage';

const VALID_SCREENS = ['intro', 'players', 'quiz', 'rules', 'game', 'breaking', 'final', 'loser'];
const FEEDBACK_CHANCE = 0.3;

function freshInitialState() {
  return {
    screen: 'intro',
    players: { ...defaultPlayers },
    desireProfiles: { p1: createDefaultDesireProfile(), p2: createDefaultDesireProfile() },
    tagWeights: createDefaultTagWeights(),
    quiz: { phase: 'p1', questionIndex: 0 },
    openedIds: [],
    recentTypes: [],
    flags: { almostBroke: false, dangerHigh: false },
    climaxTriggered: false,
    current: null,
    choiceModal: null,
    loserSelectedId: null,
    riskOfferPending: false,
    riskConfirmPendingId: null,
    lastWasRiskChoice: false,
    riskHistory: [],
    doublePending: false,
    doubleEventsUsed: 0,
    doubleCurrent: null,
    usedDoubleIds: [],
    advantageAvailable: false,
    feedbackPending: null,
    feedbackHistory: [],
  };
}

/** מחליט מה להציג במסך ההמתנה (idle) הבא: דאבל, סיכון, או כלום מיוחד. */
function computeIdleFlags(state) {
  if (state.climaxTriggered) {
    return { doublePending: false, riskOfferPending: false, advantageAvailable: state.advantageAvailable };
  }

  const openedCount = state.openedIds.length;

  if (state.advantageAvailable) {
    return { doublePending: false, riskOfferPending: true, advantageAvailable: false };
  }

  const offerDouble = shouldTriggerDoubleOrNothing({ openedCount, doubleEventsUsed: state.doubleEventsUsed });
  if (offerDouble) {
    return { doublePending: true, riskOfferPending: false, advantageAvailable: false, doubleEventsUsed: state.doubleEventsUsed + 1 };
  }

  const offerRisk = shouldOfferRiskChoice({ openedCount, lastWasRiskChoice: state.lastWasRiskChoice });
  return { doublePending: false, riskOfferPending: offerRisk, advantageAvailable: false };
}

function drawEnvelopeId(state, forcedLevel) {
  const envelope = pickNextEnvelope({
    envelopes: ENVELOPES,
    openedIds: state.openedIds,
    flags: state.flags,
    recentTypes: state.recentTypes,
    desireProfiles: state.desireProfiles,
    tagWeights: state.tagWeights,
    forcedLevel,
  });
  return envelope ?? null;
}

function reducer(state, action) {
  switch (action.type) {
    case 'GO_PLAYERS':
      return { ...state, screen: 'players' };

    case 'SET_PLAYER_NAME': {
      const name = (action.name || '').trim();
      return { ...state, players: { ...state.players, [action.player]: name || defaultPlayers[action.player] } };
    }

    case 'GO_QUIZ':
      return { ...state, screen: 'quiz', quiz: { phase: 'p1', questionIndex: 0 } };

    case 'ANSWER_QUIZ': {
      const { phase, questionIndex } = state.quiz;
      const question = desireQuiz.questions[questionIndex];
      const chosenTag = action.side === 'a' ? question.tagA : question.tagB;
      const profileKey = phase === 'p1' ? 'p1' : 'p2';
      const profile = { ...state.desireProfiles[profileKey] };
      profile[chosenTag] = (profile[chosenTag] ?? 1) + 1;
      const desireProfiles = { ...state.desireProfiles, [profileKey]: profile };

      const isLastQuestion = questionIndex >= desireQuiz.questions.length - 1;
      if (!isLastQuestion) {
        return { ...state, desireProfiles, quiz: { phase, questionIndex: questionIndex + 1 } };
      }
      if (phase === 'p1') {
        return { ...state, desireProfiles, quiz: { phase: 'handoff', questionIndex: 0 } };
      }
      return { ...state, desireProfiles, quiz: { phase: 'done', questionIndex: 0 } };
    }

    case 'QUIZ_HANDOFF_CONTINUE':
      return { ...state, quiz: { phase: 'p2', questionIndex: 0 } };

    case 'QUIZ_DONE':
      return { ...state, screen: 'rules' };

    case 'START_GAME':
      return { ...state, screen: 'game', ...computeIdleFlags(state) };

    case 'DRAW_ENVELOPE': {
      const envelope = drawEnvelopeId(state);
      if (!envelope) return state;
      return { ...state, current: { id: envelope.id, revealed: false } };
    }

    case 'CHOOSE_SAFE': {
      const level = currentStageLevel(state.openedIds.length);
      const envelope = drawEnvelopeId(state, level);
      if (!envelope) return state;
      return {
        ...state,
        current: { id: envelope.id, revealed: false },
        riskOfferPending: false,
        lastWasRiskChoice: false,
        riskHistory: [...state.riskHistory, { choice: 'safe', level }],
      };
    }

    case 'CHOOSE_RISK': {
      const level = Math.min(currentStageLevel(state.openedIds.length) + 1, 4);
      const envelope = drawEnvelopeId(state, level);
      if (!envelope) return state;
      return {
        ...state,
        riskConfirmPendingId: envelope.id,
        riskOfferPending: false,
        lastWasRiskChoice: true,
        riskHistory: [...state.riskHistory, { choice: 'risk', level }],
      };
    }

    case 'RISK_CONFIRM_DONE': {
      if (!state.riskConfirmPendingId) return state;
      return { ...state, current: { id: state.riskConfirmPendingId, revealed: false }, riskConfirmPendingId: null };
    }

    case 'MARK_REVEALED': {
      if (!state.current || state.current.revealed) return state;
      const envelope = ENVELOPES.find((e) => e.id === state.current.id);
      const openedIds = [...state.openedIds, envelope.id];
      const recentTypes = [...state.recentTypes, envelope.type].slice(-3);
      const flags = {
        almostBroke: state.flags.almostBroke || envelope.special === 'almost-broke',
        dangerHigh: state.flags.dangerHigh || envelope.special === 'danger-check',
      };
      const climaxTriggered =
        state.climaxTriggered ||
        shouldTriggerClimax({
          openedCount: openedIds.length,
          totalCount: ENVELOPES.length,
          flags,
          lastLevel: envelope.level,
        });

      const autoOpenChoice = envelope.special === 'choice';

      return {
        ...state,
        openedIds,
        recentTypes,
        flags,
        climaxTriggered,
        current: { ...state.current, revealed: true },
        choiceModal: autoOpenChoice ? { source: 'pick-one', selectedId: null } : state.choiceModal,
      };
    }

    case 'OPEN_PICK_ONE_MODAL':
      return { ...state, choiceModal: { source: 'pick-one', selectedId: null } };

    case 'CHOOSE_PICK_ONE_CARD':
      if (!state.choiceModal) return state;
      return { ...state, choiceModal: { ...state.choiceModal, selectedId: action.cardId } };

    case 'CLOSE_PICK_ONE_MODAL':
      return { ...state, choiceModal: null, current: null, ...computeIdleFlags(state) };

    case 'SKIP_CURRENT': {
      if (!state.current) return state;
      const envelope = ENVELOPES.find((e) => e.id === state.current.id);
      const shouldAskFeedback =
        state.current.revealed &&
        envelope &&
        envelope.desireTags &&
        envelope.desireTags.length > 0 &&
        !envelope.special &&
        Math.random() < FEEDBACK_CHANCE;

      if (shouldAskFeedback) {
        return {
          ...state,
          current: null,
          choiceModal: null,
          feedbackPending: { cardId: envelope.id, tags: envelope.desireTags },
        };
      }

      return { ...state, current: null, choiceModal: null, ...computeIdleFlags(state) };
    }

    case 'GIVE_FEEDBACK': {
      if (!state.feedbackPending) return state;
      const tagWeights = applyFeedback(state.tagWeights, state.feedbackPending.tags, action.delta);
      const feedbackHistory = [
        ...state.feedbackHistory,
        { cardId: state.feedbackPending.cardId, tags: state.feedbackPending.tags, optionId: action.optionId },
      ];
      const nextState = { ...state, tagWeights, feedbackHistory, feedbackPending: null };
      return { ...nextState, ...computeIdleFlags(nextState) };
    }

    case 'DOUBLE_DECLINE':
      return { ...state, doublePending: false };

    case 'DOUBLE_ACCEPT': {
      const card = pickDoubleCard({
        doubleCards: DOUBLE_CARDS,
        usedIds: state.usedDoubleIds,
        desireProfiles: state.desireProfiles,
        tagWeights: state.tagWeights,
      });
      if (!card) return { ...state, doublePending: false };
      return {
        ...state,
        doublePending: false,
        doubleCurrent: { id: card.id, revealed: false },
        usedDoubleIds: [...state.usedDoubleIds, card.id],
      };
    }

    case 'MARK_DOUBLE_REVEALED':
      if (!state.doubleCurrent || state.doubleCurrent.revealed) return state;
      return { ...state, doubleCurrent: { ...state.doubleCurrent, revealed: true } };

    case 'DOUBLE_DONE': {
      const nextState = { ...state, doubleCurrent: null, advantageAvailable: true };
      return { ...nextState, ...computeIdleFlags(nextState) };
    }

    case 'BREAK':
      return { ...state, screen: 'breaking' };

    case 'BREAKING_DONE':
      return { ...state, screen: 'final' };

    case 'FINAL_DONE':
      return { ...state, screen: 'loser' };

    case 'OPEN_LOSER_CARD':
      return { ...state, loserSelectedId: action.cardId };

    case 'RESET':
      return freshInitialState();

    default:
      return state;
  }
}

function sanitizeTagMap(value) {
  const defaults = createDefaultTagWeights();
  if (!value || typeof value !== 'object') return defaults;
  const merged = { ...defaults };
  for (const key of Object.keys(defaults)) {
    if (typeof value[key] === 'number' && Number.isFinite(value[key])) merged[key] = value[key];
  }
  return merged;
}

/** מוודא שמצב שנטען מ-localStorage תקין, גם אם הוא ישן/חלקי/פגום — אף פעם לא קורס. */
function sanitizeState(saved) {
  const fresh = freshInitialState();
  if (!saved || typeof saved !== 'object') return fresh;

  try {
    const validEnvelopeIds = new Set(ENVELOPES.map((e) => e.id));
    const openedIds = Array.isArray(saved.openedIds) ? saved.openedIds.filter((id) => validEnvelopeIds.has(id)) : [];

    const screen = VALID_SCREENS.includes(saved.screen) ? saved.screen : 'intro';

    const players = {
      p1: typeof saved.players?.p1 === 'string' && saved.players.p1.trim() ? saved.players.p1 : fresh.players.p1,
      p2: typeof saved.players?.p2 === 'string' && saved.players.p2.trim() ? saved.players.p2 : fresh.players.p2,
    };

    const desireProfiles = {
      p1: sanitizeTagMap(saved.desireProfiles?.p1),
      p2: sanitizeTagMap(saved.desireProfiles?.p2),
    };

    const tagWeights = sanitizeTagMap(saved.tagWeights);

    const current =
      saved.current && typeof saved.current === 'object' && validEnvelopeIds.has(saved.current.id)
        ? { id: saved.current.id, revealed: true }
        : null;

    const validDoubleIds = new Set(DOUBLE_CARDS.map((c) => c.id));
    const doubleCurrent =
      saved.doubleCurrent && typeof saved.doubleCurrent === 'object' && validDoubleIds.has(saved.doubleCurrent.id)
        ? { id: saved.doubleCurrent.id, revealed: true }
        : null;

    return {
      ...fresh,
      ...saved,
      screen,
      players,
      desireProfiles,
      tagWeights,
      openedIds,
      current,
      doubleCurrent,
      recentTypes: Array.isArray(saved.recentTypes) ? saved.recentTypes : [],
      flags: {
        almostBroke: Boolean(saved.flags?.almostBroke),
        dangerHigh: Boolean(saved.flags?.dangerHigh),
      },
      riskHistory: Array.isArray(saved.riskHistory) ? saved.riskHistory : [],
      feedbackHistory: Array.isArray(saved.feedbackHistory) ? saved.feedbackHistory : [],
      usedDoubleIds: Array.isArray(saved.usedDoubleIds) ? saved.usedDoubleIds : [],
      doubleEventsUsed: typeof saved.doubleEventsUsed === 'number' ? saved.doubleEventsUsed : 0,
      quiz:
        saved.quiz && typeof saved.quiz === 'object'
          ? { phase: saved.quiz.phase || 'p1', questionIndex: Number(saved.quiz.questionIndex) || 0 }
          : fresh.quiz,
    };
  } catch {
    return fresh;
  }
}

function init() {
  const saved = loadState();
  return sanitizeState(saved);
}

export function useGameState() {
  const [state, dispatch] = useReducer(reducer, undefined, init);

  useEffect(() => {
    saveState(state);
  }, [state]);

  const totalCount = ENVELOPES.length;
  const remainingCount = totalCount - state.openedIds.length;

  const currentEnvelope = useMemo(
    () => (state.current ? ENVELOPES.find((e) => e.id === state.current.id) : null),
    [state.current]
  );

  const currentDoubleCard = useMemo(
    () => (state.doubleCurrent ? DOUBLE_CARDS.find((c) => c.id === state.doubleCurrent.id) : null),
    [state.doubleCurrent]
  );

  const resetGame = useCallback(() => {
    clearState();
    dispatch({ type: 'RESET' });
  }, []);

  return {
    state,
    dispatch,
    currentEnvelope,
    currentDoubleCard,
    remainingCount,
    totalCount,
    resetGame,
  };
}
