// מנוע הבחירה של המעטפה הבאה — מנהל עקומת מתח נסתרת של 4 רמות
// ומאזן בין סוגי חוויה (push/pull) כדי שלא ייווצר רצף חד-גוני.

function bandForOpenedCount(openedCount) {
  if (openedCount < 4) return { 1: 0.8, 2: 0.2, 3: 0, 4: 0 };
  if (openedCount < 9) return { 1: 0.4, 2: 0.6, 3: 0, 4: 0 };
  if (openedCount < 15) return { 1: 0.05, 2: 0.45, 3: 0.5, 4: 0 };
  return { 1: 0, 2: 0.1, 3: 0.45, 4: 0.45 };
}

function weightedPickLevel(weights) {
  const entries = Object.entries(weights).filter(([, w]) => w > 0);
  const total = entries.reduce((sum, [, w]) => sum + w, 0);
  if (total <= 0) return 1;
  let roll = Math.random() * total;
  for (const [level, weight] of entries) {
    if (roll < weight) return Number(level);
    roll -= weight;
  }
  return Number(entries[entries.length - 1][0]);
}

function poolForLevel(unopened, level) {
  return unopened.filter((e) => e.level === level);
}

/**
 * בוחר את המעטפה הבאה מתוך אלו שטרם נפתחו, לפי עקומת המתח הנסתרת,
 * הדגלים שנצברו במשחק, ואיזון push/pull מול שני הסוגים האחרונים שנפתחו.
 */
export function pickNextEnvelope({ envelopes, openedIds, flags, recentTypes }) {
  const unopened = envelopes.filter((e) => !openedIds.includes(e.id));
  if (unopened.length === 0) return null;

  const openedCount = openedIds.length;
  let weights = bandForOpenedCount(openedCount);

  if (flags.dangerHigh) {
    weights = { 1: 0, 2: 0, 3: 0.3, 4: 0.7 };
  } else if (flags.almostBroke) {
    weights = { ...weights, 3: (weights[3] || 0) + 0.25 };
  }

  const level = weightedPickLevel(weights);
  let pool = poolForLevel(unopened, level);

  if (pool.length === 0) {
    const fallbackOrder = [level + 1, level - 1, level + 2, level - 2, level + 3, level - 3].filter(
      (l) => l >= 1 && l <= 4
    );
    for (const l of fallbackOrder) {
      pool = poolForLevel(unopened, l);
      if (pool.length > 0) break;
    }
  }
  if (pool.length === 0) pool = unopened;

  const lastType = recentTypes[recentTypes.length - 1];
  const secondLastType = recentTypes[recentTypes.length - 2];

  let filtered = pool.filter((e) => e.type !== lastType);
  if (filtered.length === 0) filtered = pool;

  const stricter = filtered.filter((e) => !(lastType && e.type === lastType && lastType === secondLastType));
  const finalPool = stricter.length > 0 ? stricter : filtered;

  return finalPool[Math.floor(Math.random() * finalPool.length)];
}

/**
 * קובע אם הגיע הרגע להציג את "רגע השיא" — פאנל שמזמין לבחור
 * בין עוד מעטפה לבין הכרזה על שבירה, בלי לחשוף את מספר השלב.
 */
export function shouldTriggerClimax({ openedCount, totalCount, flags, lastLevel }) {
  const remaining = totalCount - openedCount;
  return remaining <= 4 || lastLevel === 4 || flags.dangerHigh;
}

export function giveUpCaption(openedCount, texts) {
  if (openedCount >= 15) return texts.giveUpCaptionLate;
  if (openedCount >= 5) return texts.giveUpCaptionMid;
  return null;
}
