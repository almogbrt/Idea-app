// צלילים קצרים דרך WebAudio — אין צורך בקבצי אודיו חיצוניים.
import { getState, setState } from './state.js';

let ctx = null;

function getCtx() {
  if (!ctx) {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return null;
    ctx = new AudioCtx();
  }
  if (ctx.state === 'suspended') ctx.resume();
  return ctx;
}

function tone(freq, duration, delay = 0, type = 'sine', gainPeak = 0.18) {
  if (getState().muted) return;
  const audioCtx = getCtx();
  if (!audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = type;
  osc.frequency.value = freq;
  const startAt = audioCtx.currentTime + delay;
  gain.gain.setValueAtTime(0, startAt);
  gain.gain.linearRampToValueAtTime(gainPeak, startAt + 0.02);
  gain.gain.exponentialRampToValueAtTime(0.001, startAt + duration);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start(startAt);
  osc.stop(startAt + duration + 0.05);
}

export function playSuccess() {
  tone(523.25, 0.16, 0);
  tone(659.25, 0.16, 0.12);
  tone(783.99, 0.22, 0.24);
}

export function playAlert() {
  tone(880, 0.18, 0, 'square', 0.14);
  tone(880, 0.18, 0.28, 'square', 0.14);
}

export function playTick() {
  tone(440, 0.05, 0, 'square', 0.08);
}

export function isMuted() {
  return getState().muted;
}

export function toggleMute() {
  setState({ muted: !getState().muted });
  return getState().muted;
}
