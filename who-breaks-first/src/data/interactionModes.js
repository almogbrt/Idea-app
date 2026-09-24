// מיפוי מזהה-קלף → מצב אינטראקציה, עבור מנוע ה-Push/Pull.
// שכבת מטה-דאטה נפרדת מ-content.js כדי לא לגעת בתוכן/בנוסח הקיים.
//
// מצבים: approach (התקרבות) | hold (החזקת מתח) | distance (ריחוק מכוון) |
// emotion (רגש/שיתוף) | tease (משיכה שובבה) | release (שחרור/הפסקה)

export const INTERACTION_MODES = {
  // envelopes
  'too-close': 'approach',
  'ninety-seconds': 'hold',
  'no-hands': 'hold',
  'the-gaze': 'distance',
  'private-message': 'emotion',
  'pick-one': 'tease',
  ceasefire: 'release',
  'no-touching': 'distance',
  'stop-now': 'release',
  'surprise-me': 'tease',
  'who-knows-me': 'emotion',
  'no-shame': 'emotion',
  unasked: 'emotion',
  'still-want-you': 'emotion',
  'still-falling': 'emotion',
  'just-us': 'emotion',
  'afraid-to-lose': 'emotion',
  memory: 'emotion',
  'why-you': 'emotion',
  'the-director': 'approach',
  'closest-distance': 'hold',
  'almost-broke': 'emotion',
  'five-minutes-mine': 'hold',
  'the-duel': 'approach',
  'second-before': 'hold',
  'emotional-truth': 'emotion',
  'thanks-unsaid': 'emotion',
  'next-year': 'emotion',
  'dangerous-to-continue': 'release',
  'passing-glance': 'tease',
  'text-under-the-table': 'tease',
  'foot-under-the-table': 'approach',
  'secret-word': 'distance',
  'shared-plate': 'hold',
  'whispered-plan': 'emotion',

  // choiceCards
  'pamper-me': 'hold',
  'tempt-me': 'tease',
  'in-your-hands': 'approach',

  // doubleCards
  'who-blinks-first': 'hold',
  'double-duel': 'approach',
  'close-not-enough': 'distance',
  'who-knows-weakness': 'emotion',
  'one-more-minute': 'tease',
};

export function resolveInteractionMode(cardId) {
  return INTERACTION_MODES[cardId] || 'approach';
}
