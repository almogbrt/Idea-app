# מבצע 3

אפליקציית ווב לניידים, בעברית ו-RTL, לשלושה אחים (נועם, רום, ניב) שחולקים
טלפון אחד ביום קמפינג. תשע משימות רצופות, מצב "אבא" נסתר, שמירת התקדמות
מקומית (`localStorage`), טיימרים אמיתיים, העלאת/צילום תמונה, ואישורי
"שלושתנו" בין המשימות. אתר סטטי לחלוטין — בלי שרת, בלי התחברות.

## הרצה מקומית

```bash
cd mivtza-3
npm install
npm run dev
```

האפליקציה תיפתח על `http://localhost:5173`. פתחו בכרום בנייד (או ב-DevTools
במצב מובייל) לחוויה המיועדת.

## בנייה לפרודקשן

```bash
npm run build
```

הפלט ייכתב לתיקיית `dist/`. אפשר לבדוק אותו מקומית עם:

```bash
npm run preview
```

## הוספת תמונות המשפחה

התמונות **אינן** כלולות בריפו (ראו `public/images/memories/README.txt`).
כדי להפעיל את חוויית התמונות המלאה, הוסיפו לתיקיית
`public/images/memories/` תשעה קבצים בשמות:

```
memory-01.jpg ... memory-09.jpg
```

`memory-01.jpg` משמשת כתמונת הגיבור במסך הפתיחה. אין צורך בשינוי קוד —
כל עוד קובץ חסר, האפליקציה מציגה כרטיס placeholder כהה במקומו במקום
להישבר. גם התמונה החדשה שמצולמת/מועלית במשימה 4 נשמרת מקומית
ב-`localStorage` בלבד (לא מועלית לשום שירות חיצוני).

## מבנה הפרויקט

```
mivtza-3/
  index.html          נקודת הכניסה (RTL, meta viewport, manifest)
  vite.config.js
  package.json
  public/
    manifest.json      PWA manifest (theme-color שחור, ניתן להתקנה)
    sw.js               Service worker לתמיכה אופליין
    icons/              אייקוני PWA (192/512)
    images/memories/    תמונות המשפחה (לא כלולות — ראו למעלה)
  src/
    state.js            שכבת state + localStorage persistence
    ui.js                עזרי UI משותפים (טיימר, כותרת משימה, מודל, טוסט)
    audio.js             צלילי הצלחה/התראה דרך WebAudio + השתקה
    confetti.js          אנימציית קונפטי ל-MISSION COMPLETE
    photos.js            עזרי תמונות זיכרון + נפילה חיננית לתמונה חסרה
    dadmode.js           מצב אבא נסתר (לחיצה ארוכה על הלוגו, קוד 314)
    main.js              ראוטר המסכים
    screens/             כל אחת מ-9 המשימות + מסך פתיחה, מעברי זיכרון וגלריה
```

## שמירת התקדמות

כל מצב האפליקציה (משימה נוכחית, צ'קליסטים, טיימרים, שלב הרמז במשימה 3,
התמונה ממשימה 4, אישורי "שלושתנו", מחזיק המטען, מצב אבא) נשמר תחת מפתח
אחד ב-`localStorage`. סגירת הדפדפן ופתיחתו מחדש ממשיכה בדיוק מאותה נקודה.

## מצב אבא (Dad Mode)

לחיצה ארוכה (כ-1.2 שניות) על הלוגו "מבצע 3" בראש כל מסך פותחת בקשת קוד.
הקוד הוא `314`. לאחר אישור מופיע פס כלים קבוע בתחתית המסך עם:

- **קודם** — חזרה למשימה הקודמת
- **הבא** — דילוג למשימה הבאה (עוקף חסימות)
- **איפוס משימה** — איפוס המשימה הנוכחית בלבד
- **איפוס הכל** — איפוס מלא של כל המבצע (עם אישור)
- **נעילה** — יציאה ממצב אבא

מצב אבא אינו גלוי כלל למשתמש שלא יודע את הקוד.

## פריסה (Deployment)

הפרויקט הוא אתר סטטי טהור — כל שירות אחסון סטטי יעבוד.

### Netlify

1. חברו את הריפו ב-Netlify, או השתמשו ב-Netlify CLI.
2. **Base directory**: `mivtza-3`
3. **Build command**: `npm run build`
4. **Publish directory**: `mivtza-3/dist` (או `dist` אם ה-base כבר `mivtza-3`)

או דרך ה-CLI:

```bash
cd mivtza-3
npm run build
npx netlify-cli deploy --prod --dir=dist
```

### Vercel

1. ייבאו את הריפו ב-Vercel.
2. **Root Directory**: `mivtza-3`
3. **Build command**: `npm run build`
4. **Output directory**: `dist`

או דרך ה-CLI:

```bash
cd mivtza-3
npx vercel --prod
```

### GitHub Pages

```bash
cd mivtza-3
npm run build
```

פרסמו את תוכן `dist/` לענף `gh-pages` (למשל בעזרת `gh-pages` npm package
או GitHub Actions). `vite.config.js` כבר מוגדר עם `base: './'` כך
שהאתר עובד גם תחת נתיב משנה (`username.github.io/repo-name/`).

## בונוסים שמומשו

- **PWA**: `manifest.json` + Service Worker + אייקונים, ניתן להתקנה למסך הבית.
- **תמיכה אופליין**: קאשינג של קבצי הליבה הסטטיים.
- **אפקטי סאונד**: צלילי הצלחה/התראה דרך WebAudio (ללא קבצי אודיו
  חיצוניים) + כפתור השתקה קבוע (שמאל-תחתון), נשמר ב-localStorage.
- **קונפטי**: אנימציה קלה (Canvas, ללא ספרייה חיצונית) במסך MISSION COMPLETE בלבד.
- **איפוס מלא**: זמין בתוך מצב אבא.
