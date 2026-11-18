---
name: ai-background-music
description: "AI background music generator in Claude Code and Claude with Lyria 3 Pro through Wireflow: two instrumental tracks for your ad or product video. You give the mood, the genre, the length and what the footage shows; it turns that into one music brief, quotes the credits and waits for a yes, then a published Wireflow app writes an instrumental prompt and Lyria 3 Pro makes two different takes, saved to ./wireflow-outputs so you can try both under the cut. Use when someone wants a music bed for a UGC, TikTok, Reels or Shorts ad, royalty free style music for a product demo, an instrumental track under a voiceover, or a few music options to test. Without the Wireflow connector it still writes the music brief and a prompt pack to use in any music tool. It makes audio only; for the video itself use ai-video-generation, and for a voice track use ai-voiceover-for-ugc-ads."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Only text is sent; nothing to upload. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-background-music"
---

# AI Background Music

The person has the video already (a UGC clip, a product demo, a screen recording) and wants the music under it. Your part is the brief: what the track should feel like, how fast, which instruments, how long, and what it has to leave room for. The Wireflow app `skill-ai-background-music` makes the sound: Claude Haiku 4.5 turns the brief into one instrumental music prompt, and Google Lyria 3 Pro renders it twice, the second take with a different lead instrument and melody.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-background-music` |
| `mood` | How it should feel, one line: "bright and confident", "calm and premium", "tense, then a release" |
| `genre` | Style and instruments: "indie pop with acoustic guitar and claps", "lo-fi hip hop with warm keys", "cinematic strings" |
| `length` | The target length, e.g. "15 seconds", "30 seconds". Lyria treats it as a hint, not a hard stop (see below) |
| `video_context` | What the footage shows and where it runs, so the music fits the cut |
| Fixed inside the app | The prompt rules: instrumental only (no vocals, lyrics, humming or speech), a tempo in BPM, a clean ending, room left for a voiceover, no real artists or songs; take 2 line: same mood and tempo, different lead and melody |
| Output | `track-1` and `track-2`: one MP3 each |
| Price | 43 credits measured on 27 Oct 2026: 3 for the music prompt, 20 per Lyria 3 Pro track |

**Length.** Lyria 3 Pro has no duration setting. In our test, asking for 30 seconds gave one take of roughly 40 seconds and one of just over a minute. Tell the person to trim the track to the cut (or fade it out) in their editor. Never promise an exact length.

**Vocals.** Lyria has no instrumental switch either, so the app forces "instrumental only" in the prompt. You cannot hear the result: ask the person to check for stray vocals.

## A. Connection check

Look for tools whose names end in `run_app`, `get_execution`, `get_credit_balance` and `whoami`.

If they are missing, say in one line that making the audio needs the Wireflow connector, and how to add it:

- Plugin installed: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: add a custom connector with the URL `https://www.wireflow.ai/api/mcp`.

Then give the free version from `reference/music-brief.md`: the filled-in music brief and two ready prompts (take A and take B) that work in any text-to-music tool. Stop there.

## B. Collect the brief

1. What the video shows, how long the cut is, and where it runs (TikTok, Reels, Shorts, YouTube, a product page).
2. The mood. If the person only names a product, suggest one from `reference/music-brief.md` and say why.
3. The genre and instruments, or "you pick". Match energy to the footage: fast cuts want 110 to 128 BPM, slow pans 70 to 95.
4. Whether a voiceover or a talking creator sits on top. If yes, ask for a sparse bed (that is already in the app's rules; repeat it in `genre` for a busy style).

Never put a real artist, band, song or film title into the inputs ("sounds like ..."). Describe the sound instead: instruments, tempo, era, texture.

## C. Quote and confirm

Call `whoami` and `get_credit_balance`. Then quote, for example: "2 instrumental tracks: 43 credits (measured). Balance: 7,480." For several briefs, multiply.

Nothing runs until the person says yes to that brief and that cost.

## D. Generate

```json
{ "slug": "skill-ai-background-music", "inputs": { "mood": "Bright, confident and warm, like a sunny morning routine.", "genre": "Indie pop with acoustic guitar, light claps and soft synth pads.", "length": "30 seconds", "video_context": "A 30 second UGC ad for a reusable water bottle: a creator talks to camera at the gym, then on a hike." } }
```

Poll `get_execution` every 5 seconds until the status is no longer `PENDING`, `RUNNING` or `IN_PROGRESS`. Our test finished in about a minute. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop and quote the error.

## E. Save, check, report

Save each track as `./wireflow-outputs/<YYYY-MM-DD>/music/<brief-slug>-track-<n>.mp3` with `curl -sSL -o <file> <output url>` (PowerShell: `Invoke-WebRequest -Uri <output url> -OutFile <file>`).

Before you call it done:

- If ffprobe is installed, read each track's duration and compare it with the cut. Say which one is longer and where to trim.
- You cannot hear the audio. Ask the person to listen to both, check that there are no vocals, and pick one.

Report the two files, the CDN links, the brief that was sent and the credits used (balance before minus after). Offer:

- A new brief or another pair of takes (new quote, new yes).
- The board in Wireflow to change the prompt rules or add a mood reference image: `https://www.wireflow.ai/flow/cmvq3nljk0009l2071my9thr2?ref=skill-ai-background-music&utm_source=github&utm_medium=skill&utm_campaign=ai-background-music`

## Guardrails

- Spend only after a yes to the exact brief and cost; a redo is a new run and a new yes.
- No imitation of a real artist, song or score, and no claim that a track is cleared for a given platform; point to the Wireflow terms for usage rights.
- Lyria output carries a SynthID watermark. Say so if the person asks whether the music is AI-made.
- Keep keys and passwords out of inputs and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
