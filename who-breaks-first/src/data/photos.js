// שלושה רגעים שבהם המשחק יכול להציג תמונה שלכם. כל אחד אופציונלי.

export const PHOTO_SLOTS = [
  { id: 'intro', label: 'פתיחה', hint: 'מופיעה במסך הראשון של הערב.' },
  { id: 'memory', label: 'זיכרון', hint: 'מופיעה כשנפתחת מעטפת "זיכרון".' },
  { id: 'final', label: 'סיום', hint: 'מופיעה במעטפת הסיום, רגע לפני הנשיקה.' },
];

// מעטפה → סלוט התמונה שלה
export const ENVELOPE_PHOTO = {
  memory: 'memory',
};

export const photosCopy = {
  entry: 'להוסיף תמונות שלנו',
  title: 'התמונות שלנו',
  privacy: 'התמונות נשמרות רק בטלפון הזה. הן לא עולות לשום מקום ולא נמחקות כשמתחילים משחק חדש.',
  choose: 'לבחור תמונה',
  replace: 'להחליף',
  remove: 'להסיר',
  saving: 'שומר...',
  error: 'לא הצלחנו לקרוא את התמונה. נסו תמונה אחרת.',
  deleteAll: 'למחוק את כל התמונות',
  confirmDeleteTitle: 'למחוק את כל התמונות?',
  confirmDeleteBody: 'הן יימחקו מהטלפון הזה ולא יהיה אפשר לשחזר אותן מכאן.',
  confirmDeleteYes: 'כן, למחוק',
  confirmDeleteNo: 'ביטול',
  done: 'סיימנו',
  alt: 'שנינו',
};
