// אייקונים עדינים בקו אחיד — ללא מילוי בוטה, ברוח יוקרתית ומינימליסטית.

const base = {
  fill: 'none',
  strokeWidth: 1.4,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
};

export function EnvelopeIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <rect x="2.5" y="5.5" width="19" height="13" rx="2" stroke={color} {...base} />
      <path d="M3.5 6.5L12 13L20.5 6.5" stroke={color} {...base} />
    </svg>
  );
}

export function SealIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <circle cx="12" cy="12" r="6.5" stroke={color} {...base} />
      <path d="M12 8.2v3.6l2.4 1.4" stroke={color} {...base} />
    </svg>
  );
}

export function KeyIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <circle cx="8" cy="12" r="3.6" stroke={color} {...base} />
      <path d="M11 12h9.5M17 12v3M20 12v2.5" stroke={color} {...base} />
    </svg>
  );
}

export function CardIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <rect x="4.5" y="3" width="15" height="18" rx="2.4" stroke={color} {...base} />
      <path d="M9 8h6M9 12h6M9 16h3.5" stroke={color} {...base} />
    </svg>
  );
}

export function LockIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <rect x="5" y="10.5" width="14" height="10" rx="2" stroke={color} {...base} />
      <path d="M8 10.5V7.5a4 4 0 0 1 8 0v3" stroke={color} {...base} />
    </svg>
  );
}

export function MaskIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <path
        d="M2.5 9.2c2.2-1.9 6.1-2.3 9.5-.9 3.4-1.4 7.3-1 9.5.9 0 3.1-2 5.8-4.8 5.8-2.1 0-3-1.6-4.7-1.6s-2.6 1.6-4.7 1.6C4.5 15 2.5 12.3 2.5 9.2z"
        stroke={color}
        {...base}
      />
      <path d="M4.9 10.7q2-1.7 4.1 0q-2 1.3-4.1 0zM15 10.7q2-1.7 4.1 0q-2 1.3-4.1 0z" stroke={color} {...base} />
      <path d="M2.5 9.2 1 12.5M21.5 9.2 23 12.5" stroke={color} {...base} />
    </svg>
  );
}

export function HandcuffsIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <circle cx="6.5" cy="15.5" r="4" stroke={color} {...base} />
      <circle cx="17.5" cy="15.5" r="4" stroke={color} {...base} />
      <path d="M5.3 11.7V9.6h2.4v2.1M16.3 11.7V9.6h2.4v2.1" stroke={color} {...base} />
      <path d="M7.7 9.6 10 7.8M16.3 9.6 14 7.8" stroke={color} {...base} />
      <ellipse cx="12" cy="7.4" rx="2" ry="1.1" stroke={color} {...base} />
    </svg>
  );
}

export function LaceIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <path d="M3 7.5h18l-2.6 4.6c-2.1 1-3.6 3.1-4.6 5.9h-3.6c-1-2.8-2.5-4.9-4.6-5.9L3 7.5z" stroke={color} {...base} />
      <path d="M3 7.5q1.5 1.6 3 0t3 0 3 0 3 0 3 0 3 0" stroke={color} {...base} />
      <path d="M10.8 9.6 12 10.6l1.2-1M12 10.6v1.1" stroke={color} {...base} />
    </svg>
  );
}

export function BriefsIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <path d="M3.5 6.5h17v3.2L19.4 18h-5.1L12 12.4 9.7 18H4.6L3.5 9.7V6.5z" stroke={color} {...base} />
      <path d="M3.5 9h17" stroke={color} {...base} />
    </svg>
  );
}

export function WineIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <path
        d="M10.3 2h3.4v3.6c0 1.4 2.2 2.4 2.2 5.1V21a1 1 0 0 1-1 1H9.1a1 1 0 0 1-1-1V10.7c0-2.7 2.2-3.7 2.2-5.1V2z"
        stroke={color}
        {...base}
      />
      <path d="M8.1 13.2h7.8v4.2H8.1zM10.3 3.8h3.4" stroke={color} {...base} />
    </svg>
  );
}

export function RoomCardIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <rect x="3" y="6" width="18" height="12" rx="2.4" stroke={color} {...base} />
      <circle cx="8" cy="12" r="1.9" stroke={color} {...base} />
      <path d="M13 9.5h5M13 12h5M13 14.5h3.5" stroke={color} {...base} />
    </svg>
  );
}
