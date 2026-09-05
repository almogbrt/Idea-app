import { desireQuiz } from '../data/content';
import RestartLink from './RestartLink';
import { LockIcon } from './icons';
import styles from './DesireQuizScreen.module.css';
import buttons from '../styles/buttons.module.css';

export default function DesireQuizScreen({ quiz, players, onAnswer, onHandoffContinue, onDone, onRestart }) {
  const { phase, questionIndex } = quiz;

  return (
    <div className={styles.wrap}>
      <div className={styles.topBar}>
        <RestartLink onRestart={onRestart} />
      </div>

      {(phase === 'p1' || phase === 'p2') && (
        <QuestionView
          phase={phase}
          questionIndex={questionIndex}
          playerName={phase === 'p1' ? players.p1 : players.p2}
          onAnswer={onAnswer}
        />
      )}

      {phase === 'handoff' && (
        <div className={styles.center}>
          <LockIcon size={28} />
          <p className={styles.instruction}>{desireQuiz.handoff(players.p2)}</p>
          <h2 className={styles.handoffName}>{desireQuiz.startInstruction}</h2>
          <button className={buttons.primary} onClick={onHandoffContinue}>
            {desireQuiz.done.cta}
          </button>
        </div>
      )}

      {phase === 'done' && (
        <div className={styles.center}>
          <h1 className={styles.handoffName}>{desireQuiz.done.text}</h1>
          <button className={buttons.primary} onClick={onDone}>
            {desireQuiz.done.cta}
          </button>
        </div>
      )}
    </div>
  );
}

function QuestionView({ phase, questionIndex, playerName, onAnswer }) {
  const question = desireQuiz.questions[questionIndex];
  const isFirstQuestion = questionIndex === 0;

  return (
    <div className={styles.center}>
      <span className={styles.progress}>
        {playerName} — שאלה {questionIndex + 1} מתוך {desireQuiz.questions.length}
      </span>

      {isFirstQuestion && (
        <>
          <h1>{desireQuiz.intro.title}</h1>
          <p className={styles.privacyNote}>{desireQuiz.intro.privacyNote}</p>
          <p className={styles.instruction}>{desireQuiz.startInstruction}</p>
        </>
      )}

      <div className={styles.options}>
        <button className={styles.option} onClick={() => onAnswer('a')}>
          {question.labelA}
        </button>
        <button className={styles.option} onClick={() => onAnswer('b')}>
          {question.labelB}
        </button>
      </div>
    </div>
  );
}
