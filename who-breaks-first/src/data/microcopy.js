// ספריית מיקרוקופי — משפטים קצרים לרגעים חוזרים. משתמשים ב-pickLine כדי לגוון
// ולא לחזור על אותו משפט שוב ושוב. חלק מהקטגוריות ייכנסו לשימוש בשלבים הבאים
// של הרדיזיין (risk, pause, callback, privateTransition, lateGame, anticipation).

export const microcopy = {
  anticipation: ['עוד לא.', 'משהו מחכה לכם.', 'את זה נשמור לאחר כך.', 'המשחק זוכר.'],
  risk: ['בטוחים?', 'אפשר להישאר כאן.', 'אפשר גם שלא.'],
  pause: ['עצרו.', 'אל תמהרו.', 'לא לפתוח עדיין.'],
  callback: ['זוכרים?', 'זה חוזר.', 'לא שכחנו.'],
  privateTransition: ['מה שנאמר בחוץ...', 'נשאר איתנו.', 'המשחק זוכר.', 'ועכשיו — גם אתם לבד.'],
  lateGame: ['עוד מעטפה?', 'עדיין מחזיקים?', 'או שמישהו כבר מוכן להודות?'],
  fakeOut: ['קודם תסתכל/י עליו/ה.', 'לא ככה מהר.', 'תני לזה רגע.', 'תן לזה רגע.'],
};

/**
 * בוחר שורה אקראית מקטגוריה, עם העדפה שלא תהיה זהה לשורה האחרונה שנבחרה
 * (excludeText) — כדי שאותו משפט לא יחזור שוב ושוב ברצף.
 */
export function pickLine(category, excludeText) {
  const pool = microcopy[category] || [];
  if (pool.length === 0) return '';
  const options = excludeText ? pool.filter((line) => line !== excludeText) : pool;
  const list = options.length > 0 ? options : pool;
  return list[Math.floor(Math.random() * list.length)];
}
