import { useCallback, useEffect, useMemo, useReducer } from 'react';
import { envelopes as ENVELOPES } from '../data/content';
import { pickNextEnvelope, shouldTriggerClimax } from '../game/engine';
import { loadState, saveState, clearState } from '../utils/storage';

const initialState = {
  screen: 'intro', // intro | rules | game | breaking | final | loser
  openedIds: [],
  recentTypes: [],
  flags: { almostBroke: false, dangerHigh: false },
  climaxTriggered: false,
  current: null, // { id, revealed }
  choiceModal: null, // { source: 'pick-one' | 'loser', selectedId }
  loserSelectedId: null,
};

function reducer(state, action) {
  switch (action.type) {
    case 'GO_RULES':
      return { ...state, screen: 'rules' };

    case 'START_GAME':
      return { ...state, screen: 'game' };

    case 'DRAW_ENVELOPE': {
      const envelope = pickNextEnvelope({
        envelopes: ENVELOPES,
        openedIds: state.openedIds,
        flags: state.flags,
        recentTypes: state.recentTypes,
      });
      if (!envelope) return state;
      return {
        ...state,
        current: { id: envelope.id, revealed: false },
      };
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
      return { ...state, choiceModal: null, current: null };

    case 'SKIP_CURRENT':
      return { ...state, current: null, choiceModal: null };

    case 'BREAK':
      return { ...state, screen: 'breaking' };

    case 'BREAKING_DONE':
      return { ...state, screen: 'final' };

    case 'FINAL_DONE':
      return { ...state, screen: 'loser' };

    case 'OPEN_LOSER_CARD':
      return { ...state, loserSelectedId: action.cardId };

    case 'RESTORE':
      return { ...initialState, ...action.state };

    case 'RESET':
      return { ...initialState };

    default:
      return state;
  }
}

function init() {
  const saved = loadState();
  if (!saved) return initialState;
  // אם היה מצב ביניים לא-נחשף באמצע אנימציה בזמן רענון — נחשוף ישירות
  const current = saved.current && !saved.current.revealed ? { ...saved.current, revealed: true } : saved.current;
  return { ...initialState, ...saved, current };
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

  const resetGame = useCallback(() => {
    clearState();
    dispatch({ type: 'RESET' });
  }, []);

  return {
    state,
    dispatch,
    currentEnvelope,
    remainingCount,
    totalCount,
    resetGame,
  };
}
