import { useGameState } from './hooks/useGameState';
import IntroScreen from './components/IntroScreen';
import PlayersScreen from './components/PlayersScreen';
import PhotosScreen from './components/PhotosScreen';
import DesireQuizScreen from './components/DesireQuizScreen';
import RulesScreen from './components/RulesScreen';
import GameScreen from './components/GameScreen';
import BreakingTransition from './components/BreakingTransition';
import FinalScreen from './components/FinalScreen';
import LoserEnvelope from './components/LoserEnvelope';
import { ChalkFilterDefs } from './components/icons';

export default function App() {
  const { state, dispatch, currentEnvelope, currentDoubleCard, remainingCount, totalCount, resetGame, visualIntensity } =
    useGameState();

  return (
    <div className="app-shell">
      <ChalkFilterDefs />
      {state.screen === 'intro' && <IntroScreen onStart={() => dispatch({ type: 'GO_PLAYERS' })} />}

      {state.screen === 'players' && (
        <PlayersScreen
          players={state.players}
          onSetName={(player, name) => dispatch({ type: 'SET_PLAYER_NAME', player, name })}
          onContinue={() => dispatch({ type: 'GO_QUIZ' })}
          onPhotos={() => dispatch({ type: 'GO_PHOTOS' })}
          onRestart={resetGame}
        />
      )}

      {state.screen === 'photos' && <PhotosScreen onDone={() => dispatch({ type: 'PHOTOS_DONE' })} />}

      {state.screen === 'quiz' && (
        <DesireQuizScreen
          quiz={state.quiz}
          players={state.players}
          onAnswer={(side) => dispatch({ type: 'ANSWER_QUIZ', side })}
          onHandoffContinue={() => dispatch({ type: 'QUIZ_HANDOFF_CONTINUE' })}
          onDone={() => dispatch({ type: 'QUIZ_DONE' })}
          onRestart={resetGame}
        />
      )}

      {state.screen === 'rules' && (
        <RulesScreen onContinue={() => dispatch({ type: 'START_GAME' })} onRestart={resetGame} />
      )}

      {state.screen === 'game' && (
        <GameScreen
          state={state}
          dispatch={dispatch}
          currentEnvelope={currentEnvelope}
          currentDoubleCard={currentDoubleCard}
          remainingCount={remainingCount}
          totalCount={totalCount}
          resetGame={resetGame}
          visualIntensity={visualIntensity}
        />
      )}

      {state.screen === 'breaking' && (
        <BreakingTransition onContinue={() => dispatch({ type: 'BREAKING_DONE' })} onRestart={resetGame} />
      )}

      {state.screen === 'final' && (
        <FinalScreen onContinue={() => dispatch({ type: 'FINAL_DONE' })} onRestart={resetGame} />
      )}

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
