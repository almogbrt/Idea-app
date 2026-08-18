// מבצע 3 — persistence & state machine
// Everything lives in localStorage so the app resumes exactly where it left off.

const STORAGE_KEY = 'mivtza3_state_v1';

export const STEPS = [
  'intro',
  'm1',
  'm2',
  't2',   // memory transition after mission 2
  'm3',
  'm4',
  't4',   // memory transition after mission 4
  'm5',
  'm6',
  't6',   // memory transition after mission 6
  'm7',
  'm8',
  'm9'
];

// mission number shown to the user ("01 / 09" etc) per step id
export const MISSION_NUMBER = {
  m1: 1, m2: 2, m3: 3, m4: 4, m5: 5, m6: 6, m7: 7, m8: 8, m9: 9
};

const SIBLINGS = ['noam', 'rom', 'niv'];
export const SIBLING_LABELS = { noam: 'נועם', rom: 'רום', niv: 'ניב' };

const GEAR_ITEMS = ['בגד ים', 'מגבת', 'בגדים להחלפה', 'כובע', 'בקבוק מים', 'פנס'];
export const GEAR_ITEMS_LIST = GEAR_ITEMS;

const CAMP_ITEMS = [
  'הציוד בחוץ',
  'האוהל מוקם',
  'המזרנים מסודרים',
  'פינת הישיבה מוכנה',
  'המים והציוד מאורגנים'
];
export const CAMP_ITEMS_LIST = CAMP_ITEMS;

function emptyChecklist() {
  const obj = {};
  GEAR_ITEMS.forEach((item) => { obj[item] = false; });
  return obj;
}

function emptyApprovals() {
  return { noam: false, rom: false, niv: false };
}

function defaultState() {
  return {
    version: 1,
    step: 'intro',
    muted: false,
    dadMode: { unlocked: false },
    m1: { deadline: null, ready: false },
    m2: {
      // checker -> checks-of -> checklist
      noam: { checks: 'rom', list: emptyChecklist() },
      rom: { checks: 'niv', list: emptyChecklist() },
      niv: { checks: 'noam', list: emptyChecklist() }
    },
    m3: { step: 1, timerDeadline: null, timerStarted: false },
    m4: { photo: null, approvals: emptyApprovals() },
    m5: { deadline: null, roleIndex: 0 },
    m6: { holder: null, deadline: null, dropped: false },
    m7: { approvals: emptyApprovals() },
    m8: { deadline: null, list: (() => {
      const obj = {};
      CAMP_ITEMS.forEach((item) => { obj[item] = false; });
      return obj;
    })() },
    m9: { phase: 1, celebrated: false },
    completed: false
  };
}

let state = load();
const listeners = new Set();

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultState();
    const parsed = JSON.parse(raw);
    // shallow-merge over defaults so new fields introduced later don't crash old saves
    const base = defaultState();
    return deepMerge(base, parsed);
  } catch (e) {
    console.warn('מבצע 3: לא ניתן לטעון מצב שמור, מתחילים מחדש', e);
    return defaultState();
  }
}

function deepMerge(base, patch) {
  if (typeof patch !== 'object' || patch === null) return base;
  const out = Array.isArray(base) ? base.slice() : { ...base };
  for (const key of Object.keys(patch)) {
    if (
      typeof patch[key] === 'object' &&
      patch[key] !== null &&
      !Array.isArray(patch[key]) &&
      typeof base[key] === 'object' &&
      base[key] !== null
    ) {
      out[key] = deepMerge(base[key], patch[key]);
    } else if (key in base) {
      out[key] = patch[key];
    }
  }
  return out;
}

function persist() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    console.warn('מבצע 3: שמירה נכשלה (ייתכן שהאחסון מלא)', e);
  }
  listeners.forEach((fn) => fn(state));
}

export function getState() {
  return state;
}

export function setState(patch) {
  state = deepMerge(state, patch);
  persist();
}

export function subscribe(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

export function goToStep(stepId) {
  if (!STEPS.includes(stepId)) return;
  setState({ step: stepId });
}

export function nextStep() {
  const idx = STEPS.indexOf(state.step);
  if (idx === -1 || idx === STEPS.length - 1) return;
  goToStep(STEPS[idx + 1]);
}

export function prevStep() {
  const idx = STEPS.indexOf(state.step);
  if (idx <= 0) return;
  goToStep(STEPS[idx - 1]);
}

export function resetStep(stepId) {
  const target = stepId || state.step;
  const fresh = defaultState();
  if (target in fresh) {
    setState({ [target]: fresh[target] });
  }
}

export function resetAll() {
  state = defaultState();
  persist();
}

export { SIBLINGS };
