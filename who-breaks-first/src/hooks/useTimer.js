import { useCallback, useEffect, useRef, useState } from 'react';
import { vibrate } from '../utils/vibrate';
import { playChime } from '../utils/sound';

export function useTimer(durationSeconds) {
  const [secondsLeft, setSecondsLeft] = useState(durationSeconds);
  const [status, setStatus] = useState('idle'); // idle | running | done
  const intervalRef = useRef(null);

  useEffect(() => {
    setSecondsLeft(durationSeconds);
    setStatus('idle');
  }, [durationSeconds]);

  useEffect(() => {
    return () => clearInterval(intervalRef.current);
  }, []);

  const start = useCallback(() => {
    if (status === 'running') return;
    setStatus('running');
    clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev <= 1) {
          clearInterval(intervalRef.current);
          setStatus('done');
          vibrate([80, 60, 80]);
          playChime();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  }, [status]);

  const reset = useCallback(() => {
    clearInterval(intervalRef.current);
    setSecondsLeft(durationSeconds);
    setStatus('idle');
  }, [durationSeconds]);

  return { secondsLeft, status, start, reset };
}
