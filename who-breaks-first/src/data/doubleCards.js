// משימות "דאבל או כלום" — מערבות את שני המשתתפים בו-זמנית.
// עריכת נוסח נעשית רק כאן, באותה רוח כמו src/data/content.js.

import { HER, HIM } from './content';

export const doubleCards = [
  {
    id: 'who-blinks-first',
    title: 'מי ימצמץ ראשון?',
    level: 2,
    timerSeconds: null,
    desireTags: ['eyeContact', 'anticipation', 'teasing'],
    body: `שבו קרוב.\n\nהסתכלו זה לזו בעיניים.\n\nאסור לדבר.\n\nאסור להתנשק.\n\n${HER} מסיטה את המבט ראשונה? ${HIM} ניצח.\n${HIM} מסיט ראשון? ${HER} ניצחה.`,
  },
  {
    id: 'double-duel',
    title: 'הדו-קרב',
    level: 4,
    timerSeconds: 180,
    desireTags: ['teasing', 'seduction', 'surprise'],
    body: `3 דקות.\n\nשניכם משחקים בו-זמנית.\n\nאין תורות.\n\n${HER} מנסה לגרום ל${HIM} לרצות להגיד "נשברתי".\n${HIM} מנסה לגרום לזה ל${HER}.\n\nהשתמשו במה שלמדתם זה על זו הערב.\n\nאין נשיקה בשפתיים.`,
  },
  {
    id: 'close-not-enough',
    title: 'קרוב. לא מספיק.',
    level: 3,
    timerSeconds: 90,
    desireTags: ['proximity', 'teasing', 'anticipation'],
    body: `עמדו קרוב מאוד.\n\nמותר לדבר.\n\nמותר ללחוש.\n\nמותר להתקרב.\n\nאבל למשך 90 שניות אסור לגעת — לא ${HER} ב${HIM}, ולא ${HIM} ב${HER}.\n\nבסיום:\n\nשניכם אומרים מה היה הכי קשה לא לעשות.`,
  },
  {
    id: 'who-knows-weakness',
    title: 'מי מכיר את החולשה?',
    level: 3,
    timerSeconds: null,
    desireTags: ['words', 'anticipation'],
    body: 'שניכם כותבים בסתר:\n\n"נראה לי שהדבר שהכי משפיע עליך הערב הוא..."\n\nחשפו יחד.\n\nאם צדקתם — מותר להשתמש במידע במשימה הבאה.',
  },
  {
    id: 'one-more-minute',
    title: 'עוד דקה',
    level: 2,
    timerSeconds: 60,
    desireTags: ['anticipation', 'slowBuild', 'spontaneous'],
    body: 'הפעילו טיימר של 60 שניות.\n\nשניכם מנסים לגרום לדקה הזאת להרגיש קצרה מדי.\n\nאין מנצח רשמי.\n\nכשהטיימר נגמר — עוצרים מיד.',
  },
];
