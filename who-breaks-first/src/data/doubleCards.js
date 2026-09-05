// משימות "דאבל או כלום" — מערבות את שני המשתתפים בו-זמנית.
// עריכת נוסח נעשית רק כאן, באותה רוח כמו src/data/content.js.

export const doubleCards = [
  {
    id: 'who-blinks-first',
    title: 'מי ימצמץ ראשון?',
    level: 2,
    timerSeconds: null,
    desireTags: ['eyeContact', 'anticipation', 'teasing'],
    body: 'שבו קרוב.\n\nהסתכלו אחד לשנייה בעיניים.\n\nאסור לדבר.\n\nאסור להתנשק.\n\nהראשון שמסיט את המבט מפסיד.',
  },
  {
    id: 'double-duel',
    title: 'הדו-קרב',
    level: 4,
    timerSeconds: 180,
    desireTags: ['teasing', 'seduction', 'surprise'],
    body: '3 דקות.\n\nשניכם משחקים בו-זמנית.\n\nאין תורות.\n\nכל אחד מנסה לגרום לשני לרצות להגיד:\n\n"נשברתי".\n\nהשתמשו במה שלמדתם אחד על השנייה הערב.\n\nאין נשיקה בשפתיים.',
  },
  {
    id: 'close-not-enough',
    title: 'קרוב. לא מספיק.',
    level: 3,
    timerSeconds: 90,
    desireTags: ['proximity', 'teasing', 'anticipation'],
    body: 'עמדו קרוב מאוד.\n\nמותר לדבר.\n\nמותר ללחוש.\n\nמותר להתקרב.\n\nאבל למשך 90 שניות אסור לאף אחד לגעת בשני.\n\nבסיום:\n\nכל אחד אומר מה היה לו הכי קשה לא לעשות.',
  },
  {
    id: 'who-knows-weakness',
    title: 'מי מכיר את החולשה?',
    level: 3,
    timerSeconds: null,
    desireTags: ['words', 'anticipation'],
    body: 'כל אחד כותב בסתר:\n\n"אני חושב/ת שהדבר שהכי משפיע עליך הערב הוא..."\n\nחשפו יחד.\n\nאם צדקתם — מותר להשתמש במידע במשימה הבאה.',
  },
  {
    id: 'one-more-minute',
    title: 'עוד דקה',
    level: 2,
    timerSeconds: 60,
    desireTags: ['anticipation', 'slowBuild', 'spontaneous'],
    body: 'הפעילו טיימר של 60 שניות.\n\nשניכם מנסים לגרום לשני לרצות שהדקה לא תיגמר.\n\nאין מנצח רשמי.\n\nכשהטיימר נגמר — עוצרים מיד.',
  },
];
