import { useGameState } from './hooks/useGameState';
import IntroScreen from './components/IntroScreen';
import RulesScreen from './components/RulesScreen';
import GameScreen from './components/GameScreen';
import BreakingTransition from './components/BreakingTransition';
import FinalScreen from './components/FinalScreen';
import LoserEnvelope from './components/LoserEnvelope';

export default function App() {
  const { state, dispatch, currentEnvelope, remainingCount, totalCount, resetGame } = useGameState();

  return (
    <div className="app-shell">
      {state.screen === 'intro' && <IntroScreen onStart={() => dispatch({ type: 'GO_RULES' })} />}

      {state.screen === 'rules' && <RulesScreen onContinue={() => dispatch({ type: 'START_GAME' })} />}

      {state.screen === 'game' && (
        <GameScreen
          state={state}
          dispatch={dispatch}
          currentEnvelope={currentEnvelope}
          remainingCount={remainingCount}
          totalCount={totalCount}
          resetGame={resetGame}
        />
      )}

      {state.screen === 'breaking' && <BreakingTransition onContinue={() => dispatch({ type: 'BREAKING_DONE' })} />}

      {state.screen === 'final' && <FinalScreen onContinue={() => dispatch({ type: 'FINAL_DONE' })} />}

      {state.screen === 'loser' && (
        <LoserEnvelope
          selectedId={state.loserSelectedId}
          onSelect={(cardId) => dispatch({ type: 'OPEN_LOSER_CARD', cardId })}
          onRestart={resetGame}
        />
      )}
    </div>
  );
}
