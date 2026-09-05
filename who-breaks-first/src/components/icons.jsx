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

export function RoomCardIcon({ size = 24, color = 'currentColor', ...props }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...props}>
      <rect x="3" y="6" width="18" height="12" rx="2.4" stroke={color} {...base} />
      <circle cx="8" cy="12" r="1.9" stroke={color} {...base} />
      <path d="M13 9.5h5M13 12h5M13 14.5h3.5" stroke={color} {...base} />
    </svg>
  );
}
