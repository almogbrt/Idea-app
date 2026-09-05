export function vibrate(pattern = 20) {
  if (typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function') {
    try {
      navigator.vibrate(pattern);
    } catch {
      // מכשירים מסוימים חוסמים רטט — לא קריטי להמשך המשחק
    }
  }
}
