---
name: ai-sound-effects-for-video-ads
description: "AI sound effects generator in Claude Code and Claude with ElevenLabs Sound Effects through Wireflow: a pack of four spot effects for a video ad. Describe the scene and the moments that need sound; Claude fills in a whoosh, a pop, a click and a room ambience, quotes the credits and waits for a yes, then a published Wireflow app gives all four one shared sound world and returns four MP3 files saved to ./wireflow-outputs. Use when someone wants a swipe or transition whoosh, a pop for a price badge or caption, a button or lid click, background room tone for a UGC, TikTok, Reels or Shorts ad or a product clip, or SFX to sync in CapCut or Premiere. Without the Wireflow connector it still writes the cue sheet and four prompts for any SFX tool. Effects only: for a music bed use ai-background-music, for speech use ai-voiceover-for-ugc-ads."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Only text is sent; nothing to upload. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-sound-effects-for-video-ads"
---

# AI Sound Effects for Video Ads

Someone has an edit that feels flat: the cut snaps without a swish, the sale badge appears in silence, the room has no air. You plan the cues. The Wireflow app `skill-ai-sound-effects-for-video-ads` makes them: Claude Haiku 4.5 reads the scene and writes a single "sound world" line (the space, the materials, the style), and ElevenLabs Sound Effects v2 renders four effects that each carry that line, so they sound like they belong to the same clip.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-sound-effects-for-video-ads` |
| `scene` | What the clip shows, where it takes place and its style, in one or two sentences |
| `whoosh_moment` | The cut, swipe or camera move the whoosh covers |
| `pop_moment` | The text, sticker, badge or product that appears with a pop |
| `click_moment` | The button, lid, switch, tap or latch that clicks |
| `ambience_moment` | The background under the whole clip: the place and what is going on quietly in it |
| Fixed inside the app | One lead per effect (single whoosh, single pop, single click, steady ambience, never music or voice), the sound world rules, lengths: whoosh 1.5 s, pop 1 s, click 1 s, ambience 6 s set to loop |
| Output | `whoosh`, `pop`, `click`, `ambience`: one MP3 each |
| Price | 19 credits measured on 30 Oct 2026: 3 for the sound world line, 4 per effect |

The lengths are set in the app, not by the inputs. A moment that says "3 seconds" will not stretch the click. For a longer bed, the ambience loops cleanly: repeat it on the timeline.

## A. Connection check

Check that tools ending in `run_app`, `get_execution`, `get_credit_balance` and `whoami` are available.

When they are not, explain in one line that the audio is made by the Wireflow connector, then how to connect:

- With the plugin: `/mcp` → `wireflow` → Authenticate.
- Claude Code without the plugin: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: a custom connector with the URL `https://www.wireflow.ai/api/mcp`.

Then hand over the free version from `reference/sfx-cue-sheet.md`: the cue sheet with timecodes filled in and four prompts that paste into any text-to-sound-effects tool. End there.

## B. Plan the cues

1. Ask what the clip shows, how long it is and where it will run. One or two sentences become `scene`.
2. Walk the timeline with the person and find the four moments: the biggest cut or swipe (whoosh), the thing that appears on screen (pop), the physical or UI action (click), and the place (ambience). Write the timecode for each into your notes; it is not an input, but it goes into the report so the person knows where to drop each file.
3. If a moment is missing, suggest one from the cue table in `reference/sfx-cue-sheet.md` rather than leaving it blank. Every input needs text.
4. Describe sounds by what makes them ("a plastic flip-top snapping shut", "rain on a window"), not by brand or by a film or game they come from.

## C. Quote and confirm

Call `whoami` and `get_credit_balance`, then quote, for example: "4 sound effects (whoosh, pop, click, ambience): 19 credits (measured). Balance: 4,492." For several clips, multiply by the number of runs.

Nothing runs until the person says yes to these cues and this price.

## D. Generate

```json
{ "slug": "skill-ai-sound-effects-for-video-ads", "inputs": { "scene": "A 15 second product ad for a hand-poured soy candle: a hand lights the wick in a cosy wooden living room at night, the camera pushes in on the flame, then the label and a 15% off sticker appear.", "whoosh_moment": "Quick push-in from the wide shot of the room to the close-up of the candle flame.", "pop_moment": "The 15% off sticker pops onto the corner of the screen.", "click_moment": "The lighter clicks once to strike the flame.", "ambience_moment": "A quiet cosy living room at night: soft rain on the window and a faint crackle of the wick." } }
```

Check `get_execution` every 5 seconds while the status reads `PENDING`, `RUNNING` or `IN_PROGRESS`. The test run took well under a minute. If it ends `FAILED`, `CANCELLED` or `TIMEOUT`, stop and show the error as returned.

## E. Save, check, report

Save the four files as `./wireflow-outputs/<YYYY-MM-DD>/sfx/<clip-slug>-<effect>.mp3`, one call per effect: `curl -sSL -o <file> <output url>` (PowerShell: `Invoke-WebRequest -Uri <output url> -OutFile <file>`).

Before you call it done:

- With ffprobe available, read each length: about 1.5, 1, 1 and 6 seconds. A file far off that is worth mentioning.
- You cannot listen. Ask the person to play each one and say which to redo.

Report a small table: effect, file, CDN link, the timecode it goes on, plus the credits spent (balance before minus after). Mix tips: whoosh starts a few frames before the cut, pop and click sit on the exact frame, ambience runs under everything about 15 to 20 dB below the voice.

Offer next:

- A redo of one effect with a sharper moment (it reruns the whole pack: new quote, new yes).
- The board in Wireflow, to change lengths, add a fifth effect or switch the loop: `https://www.wireflow.ai/flow/cmvudzbzn0010l007v2j1qalq?ref=skill-ai-sound-effects-for-video-ads&utm_source=github&utm_medium=skill&utm_campaign=ai-sound-effects-for-video-ads`

## Guardrails

- No spend without a yes to the exact cues and price; every rerun gets its own quote and yes.
- Do not copy a trademarked sound (a famous startup chime, a console boot, a film or game effect). Describe the sound instead.
- Make no promise about licensing for a given platform; point to the Wireflow terms.
- Keep keys and passwords out of inputs and files.
- When Wireflow refuses or a tool errors, show the exact message and offer `send_feedback` if it exists.
