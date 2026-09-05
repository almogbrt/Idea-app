// מנוע הבחירה של המעטפה הבאה — מנהל עקומת מתח נסתרת של 4 רמות,
// ומשלב עליה שכבת התאמה אישית (Desire Profile) בלי לחשוף את הלוגיקה למשתמש.
//
// שכבות, מהחיצונית לפנימית:
// 1. עקומת מתח לפי מספר מעטפות שנפתחו (בחירת רמה).
// 2. SAFE/RISK ו-DOUBLE יכולים לכפות רמה ספציפית במקום זו שנבחרה בשכבה 1.
// 3. בתוך הרמה שנבחרה — ניקוד משוקלל לכל קלף (baseWeight + desireMatch +
//    varietyBonus + contextBonus) ואז weighted random — לא תמיד הניקוד הגבוה ביותר.

export const ALL_TAGS = [
  'words',
  'touch',
  'eyeContact',
  'proximity',
  'leading',
  'beingLed',
  'surprise',
  'anticipation',
  'slowBuild',
  'spontaneous',
  'pampering',
  'seduction',
  'teasing',
];

export function createDefaultDesireProfile() {
  return Object.fromEntries(ALL_TAGS.map((tag) => [tag, 1]));
}

export function createDefaultTagWeights() {
  return Object.fromEntries(ALL_TAGS.map((tag) => [tag, 1]));
}

function bandForOpenedCount(openedCount) {
  if (openedCount < 4) return { 1: 0.8, 2: 0.2, 3: 0, 4: 0 };
  if (openedCount < 9) return { 1: 0.4, 2: 0.6, 3: 0, 4: 0 };
  if (openedCount < 15) return { 1: 0.05, 2: 0.45, 3: 0.5, 4: 0 };
  return { 1: 0, 2: 0.1, 3: 0.45, 4: 0.45 };
}

/** הרמה ה"רשמית" הנוכחית של המשחק — משמשת את SAFE/RISK ואת DOUBLE כדי לדעת מה זה "רמה אחת מעל". */
export function currentStageLevel(openedCount) {
  if (openedCount < 4) return 1;
  if (openedCount < 9) return 2;
  if (openedCount < 15) return 3;
  return 4;
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

function nearestAvailableLevel(unopened, level, { capAt4 = true } = {}) {
  const order = [level, level - 1, level + 1, level - 2, level + 2, level - 3, level + 3]
    .filter((l) => l >= 1 && l <= 4 && !(capAt4 && l > 4));
  for (const l of order) {
    const pool = poolForLevel(unopened, l);
    if (pool.length > 0) return { level: l, pool };
  }
  return { level, pool: unopened };
}

function combinedDesireWeight(tag, desireProfiles, tagWeights) {
  const p1 = desireProfiles?.p1?.[tag] ?? 1;
  const p2 = desireProfiles?.p2?.[tag] ?? 1;
  const multiplier = tagWeights?.[tag] ?? 1;
  return ((p1 + p2) / 2) * multiplier;
}

function desireMatchScore(card, desireProfiles, tagWeights) {
  if (!card.desireTags || card.desireTags.length === 0) return 0;
  const sum = card.desireTags.reduce((acc, tag) => acc + combinedDesireWeight(tag, desireProfiles, tagWeights), 0);
  return sum / card.desireTags.length;
}

function varietyBonus(card, recentTypes) {
  const lastType = recentTypes[recentTypes.length - 1];
  const secondLastType = recentTypes[recentTypes.length - 2];
  if (!lastType) return 0;
  if (card.type === lastType && lastType === secondLastType) return -0.6;
  if (card.type === lastType) return -0.3;
  return 0.3;
}

function contextBonus(card, flags) {
  let bonus = 0;
  if (flags?.almostBroke && card.level === 3) bonus += 0.4;
  if (flags?.dangerHigh && card.level === 4) bonus += 0.4;
  return bonus;
}

function scoreCard(card, { flags, recentTypes, desireProfiles, tagWeights }) {
  const base = 1;
  const desire = desireMatchScore(card, desireProfiles, tagWeights);
  const variety = varietyBonus(card, recentTypes);
  const context = contextBonus(card, flags);
  return Math.max(base + desire + variety + context, 0.05);
}

function weightedPickCard(pool, ctx) {
  const scored = pool.map((card) => ({ card, score: scoreCard(card, ctx) }));
  const total = scored.reduce((sum, s) => sum + s.score, 0);
  let roll = Math.random() * total;
  for (const { card, score } of scored) {
    if (roll < score) return card;
    roll -= score;
  }
  return scored[scored.length - 1].card;
}

/**
 * בוחר את המעטפה הבאה. אם forcedLevel מסופק (SAFE/RISK), הבחירה מוגבלת
 * לרמה הזו (עם נפילה חכמה לרמה הקרובה הזמינה). אחרת — עקומת המתח הרגילה.
 */
export function pickNextEnvelope({
  envelopes,
  openedIds,
  flags,
  recentTypes,
  desireProfiles,
  tagWeights,
  forcedLevel,
  restaurantMode,
}) {
  let unopened = envelopes.filter((e) => !openedIds.includes(e.id));
  if (restaurantMode) unopened = unopened.filter((e) => e.restaurantSafe);
  if (unopened.length === 0) return null;

  const openedCount = openedIds.length;
  let pool;

  if (forcedLevel) {
    const capped = Math.min(forcedLevel, 4);
    ({ pool } = nearestAvailableLevel(unopened, capped));
  } else {
    let weights = bandForOpenedCount(openedCount);
    if (flags?.dangerHigh) {
      weights = { 1: 0, 2: 0, 3: 0.3, 4: 0.7 };
    } else if (flags?.almostBroke) {
      weights = { ...weights, 3: (weights[3] || 0) + 0.25 };
    }
    const level = weightedPickLevel(weights);
    pool = poolForLevel(unopened, level);
    if (pool.length === 0) ({ pool } = nearestAvailableLevel(unopened, level, { capAt4: false }));
  }

  if (pool.length === 0) pool = unopened;

  return weightedPickCard(pool, { flags, recentTypes, desireProfiles, tagWeights });
}

/** אותה לוגיקת ניקוד, על מאגר משימות ה-Double — בלי הגבלת רמה. */
export function pickDoubleCard({ doubleCards, usedIds = [], desireProfiles, tagWeights }) {
  const available = doubleCards.filter((c) => !usedIds.includes(c.id));
  const pool = available.length > 0 ? available : doubleCards;
  return weightedPickCard(pool, { flags: {}, recentTypes: [], desireProfiles, tagWeights });
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

// חלונות מוגדרים-מראש שבהם SAFE/RISK רשאי להופיע (אינדקס מעטפה, 1-מבוסס)
const RISK_WINDOWS = [
  { min: 4, max: 4, chance: 0.6 },
  { min: 7, max: 9, chance: 0.55 },
  { min: 11, max: 14, chance: 0.5 },
  { min: 15, max: 99, chance: 0.3 },
];

/**
 * קובע אם להציע SAFE/RISK לפני פתיחת המעטפה הבאה (openedCount = כמה כבר נפתחו).
 * לעולם לא פעמיים ברצף, כדי שהבחירה "מסוכן" תרגיש מיוחדת ולא שגרתית.
 */
export function shouldOfferRiskChoice({ openedCount, lastWasRiskChoice, restaurantMode }) {
  if (restaurantMode) return false;
  if (lastWasRiskChoice) return false;
  const nextEnvelopeNumber = openedCount + 1;
  const window = RISK_WINDOWS.find((w) => nextEnvelopeNumber >= w.min && nextEnvelopeNumber <= w.max);
  if (!window) return false;
  return Math.random() < window.chance;
}

/**
 * קובע אם להפעיל "דאבל או כלום". רק אחרי מתח מספק, לא יותר מפעמיים במשחק,
 * והסיכוי גדל ככל שנפתחו יותר מעטפות.
 */
export function shouldTriggerDoubleOrNothing({ openedCount, doubleEventsUsed, restaurantMode }) {
  if (restaurantMode) return false;
  if (doubleEventsUsed >= 2) return false;
  if (openedCount < 8) return false;
  const chance = Math.min(0.08 + (openedCount - 8) * 0.03, 0.35);
  return Math.random() < chance;
}

/** מעדכן משקל תגית בעקבות משוב "זה עבד?" — לעולם לא מסיר קטגוריה לגמרי. */
export function applyFeedback(tagWeights, tags, delta) {
  const next = { ...tagWeights };
  for (const tag of tags) {
    const current = next[tag] ?? 1;
    next[tag] = Math.min(1.8, Math.max(0.5, current + delta));
  }
  return next;
}
