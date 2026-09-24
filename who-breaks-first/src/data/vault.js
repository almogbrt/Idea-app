// The Vault — מעטפות שבסופן אפשר (לא חובה) לשמור משפט אחד שנאמר.
// מה שנשמר נכנס ל-Anticipation Queue ויחזור מאוחר יותר כ-Callback.
// המשחק לעולם לא ממציא תוכן — חוזר רק מה ששחקן/ית הקלידו בעצמם.

export const VAULT_PROMPTS = {
  'the-gaze': 'מה כל אחד אמר שהוא הכי היה רוצה?',
  'no-touching': 'מה הכי רציתם לעשות בשלוש הדקות האלה?',
  'stop-now': 'מה הכי קשה לא לעשות עכשיו?',
  unasked: 'מה הדבר שקשה לבקש?',
  'private-message': 'איך נגמר המשפט "כשנפסיק לשחק הלילה, אני רוצה..."?',
  'text-under-the-table': 'מה נכתב בהודעה?',
  'whispered-plan': 'מה נלחש?',
};

export const vaultCopy = {
  open: 'לשמור את זה לאחר כך',
  whose: 'מי אמר את זה?',
  placeholder: 'משפט אחד. רק אתם תראו אותו.',
  save: 'לשמור',
  cancel: 'לא עכשיו',
  saved: 'נשמר. המשחק זוכר.',
};

export const anticipationCopy = {
  one: 'משהו מחכה לכם.',
  many: (n) => `${n} דברים מחכים לכם.`,
  unreturned: 'יש משהו שהמשחק עדיין לא החזיר לכם.',
};

export const callbackCopy = {
  opener: 'הגיע הזמן.',
  leadPublic: 'זוכרים מה נאמר במסעדה?',
  leadPrivate: (name) => `מוקדם יותר הערב, ${name} אמר/ה...`,
  closer: 'עכשיו זה חוזר למשחק.',
  cta: 'להמשיך',
};

export const VAULT_TEXT_MAX = 140;
