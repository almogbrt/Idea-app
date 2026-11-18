---
name: ai-voiceover-for-ugc-ads
description: "AI voiceover for UGC ads in Claude Code and Claude with Minimax Speech 02 HD through Wireflow: three voice takes as MP3s for your ad footage. It tidies your ad script so it sounds natural read aloud, quotes the credits and waits for a yes, then a published Wireflow app reads it in three voices (bright female, relaxed male, calm female) and saves the takes to ./wireflow-outputs so you can A/B test them under the footage you already shot. Use when someone asks for a voice over for a TikTok, Reels or Shorts ad, text to speech for an ad script, an AI voice actor, a narration track for product footage, or several voice takes to test. Without the Wireflow connector it still writes the spoken script, timing and a voice direction sheet for a human voice actor. For a whole ad with an AI creator on camera, use ugc-ad-generator instead."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Only text is sent; no files to upload. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-voiceover-for-ugc-ads"
---

# AI Voiceover for UGC Ads

The person already has footage (b-roll, a product demo, a screen recording, a silent creator clip) and needs the voice that sits on top. You shape the words so they are easy to say in the time the clip allows; the Wireflow app `skill-ai-voiceover-for-ugc-ads` makes the audio: Claude Haiku 4.5 does a final spoken pass, then Minimax Speech 02 HD reads it three times in three different voices.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-voiceover-for-ugc-ads` |
| `script` | The words to voice. Plain text, ideally 15 to 75 words (about 6 to 30 seconds spoken) |
| `tone` | How it should sound, one short line: "casual and upbeat, like a friend", "calm and confident" |
| `language` | Language and region of the voiceover, e.g. "English (US)", "Spanish (Mexico)". A script in another language is translated |
| Fixed inside the app | The spoken-rewrite rules (never longer than your script, names, numbers and offers kept); voices: take 1 `Lively_Girl` (bright female), take 2 `Casual_Guy` (relaxed male), take 3 `Calm_Woman` (calm female); speed 1, pitch 0 |
| Output | `spoken-script` (the text that was read) and `take-1`, `take-2`, `take-3`: one MP3 each |
| Price | 51 credits measured for a 19-word script, about 8.5 s a take (3 for the rewrite + 16 a take, 26 Oct 2026). Wireflow lists Minimax Speech 02 HD at 3 credits per second of speech, so a longer script can cost more |

The voices are fixed in the app: the person picks the best of three, not a named voice. Tone steers the wording; the voices carry the delivery.

## A. Connection check

Look for tools whose names end in `run_app`, `get_execution`, `get_credit_balance` and `whoami`.

If they are missing, say in one line that making audio needs the Wireflow connector, and how to add it:

- Plugin installed: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: add a custom connector with the URL `https://www.wireflow.ai/api/mcp`.

Then hand over the free version from `reference/voiceover-direction.md`: the spoken script, a word count and time estimate, and a direction sheet (pace, energy, emphasis, pauses) that a human voice actor or any TTS tool can follow. Stop there.

## B. Collect inputs

1. The script, or the facts to build one from: product, the one benefit, any real offer.
2. The footage length and where the ad runs (TikTok, Reels, Shorts, Stories), so the read fits the clip.
3. The tone and the language. Default to the language the person writes in.

## C. Fit the words to the clip

Speech runs at about 2.5 words a second. Budget the script to the footage: 6 s is about 15 words, 15 s about 35, 30 s about 75. Leave half a second of air at the end.

- Open with the hook in the first five words.
- One idea per sentence; short sentences; contractions.
- Write numbers and symbols as said ("twenty percent", "two for one"), spell out brand names the way they sound if needed.
- Keep offers, prices and claims exactly as the person gave them. Add none.

Patterns and examples by tone: `reference/voiceover-direction.md`. If the script is over the clip's budget, show a trimmed version and let the person choose before quoting.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`. Estimate the spoken length (words / 2.5). Then quote:

- Up to about 20 words: "3 voice takes: about 51 credits (measured). Balance: 1,032."
- Longer: "3 voice takes of about N seconds: 51 credits measured at 8.5 s; Wireflow lists 3 credits per second per take, so up to about 3 + 9 x N credits." For several scripts, add them up.

Nothing runs until the person says yes to that script and that cost.

## E. Generate

```json
{ "slug": "skill-ai-voiceover-for-ugc-ads", "inputs": { "script": "Okay, this tote fits my laptop, my gym clothes and my lunch. Finally, one bag. Twenty percent off this week.", "tone": "Casual and upbeat, like a friend recommending it to you.", "language": "English (US)" } }
```

Poll `get_execution` every 5 seconds until the status is no longer `PENDING`, `RUNNING` or `IN_PROGRESS`. Our test finished in well under a minute. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop and quote the error.

## F. Save, check, report

Save each take as `./wireflow-outputs/<YYYY-MM-DD>/voiceover/<script-slug>-take-<n>.mp3` with `curl -sSL -o <file> <output url>` (PowerShell: `Invoke-WebRequest -Uri <output url> -OutFile <file>`). Save `spoken-script` next to them as `<script-slug>-script.txt`.

Check before you call it done:

- Compare `spoken-script` with what was approved: names, numbers and the offer unchanged, nothing added.
- If ffprobe is installed, read each take's duration and compare it with the footage. Too long: trim words, not speed.
- You cannot hear the audio. Ask the person to listen to all three and pick one; say which voice each take is.

Report the files, the CDN links, the spoken script and the credits used (balance before minus after). Offer:

- Another script or a shorter cut (new quote, new yes).
- The board in Wireflow to change voices, speed or add a music bed: `https://www.wireflow.ai/flow/cmvoo81wd000eld088ewk6cyg?ref=skill-ai-voiceover-for-ugc-ads&utm_source=github&utm_medium=skill&utm_campaign=ai-voiceover-for-ugc-ads`

## Guardrails

- Spend only after a yes to the exact script and cost; a redo is a new run and a new yes.
- No invented claims, results, prices or reviews, and no medical or financial promises the brand cannot back.
- The voices are synthetic. Do not present them as a real customer, and follow the platform's AI or synthetic media labels.
- Never imitate a real person, a celebrity or a specific creator's voice.
- Keep keys and passwords out of inputs and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
