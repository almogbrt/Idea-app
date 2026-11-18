---
name: ai-thumbnail-maker
description: "AI thumbnail maker in Claude Code and Claude with Ideogram 4.5 through Wireflow: three 16:9 YouTube thumbnails with readable headline text. From a video title it writes a short headline and three different visual concepts (reaction face, before and after, circled detail and more), quotes the credits and waits for a yes, then renders all three in one call at 2560x1440 with the headline spelled exactly and saves them to ./wireflow-outputs. Use when someone asks for a YouTube thumbnail, thumbnail ideas or variants to test, a clickable cover for a video, thumbnail text, or a thumbnail generator for a channel or client. Without the Wireflow connector it still writes the headline and a concept sheet a designer can build. For a plain image with no headline use ai-image-generation."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Inputs are text only. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-thumbnail-maker"
---

# AI Thumbnail Maker

A creator or an agency has a video and needs a thumbnail people click, usually a few options to test against each other. You (Claude) turn the title into a short headline and three distinct visual concepts; the Wireflow app `skill-ai-thumbnail-maker` renders the three concepts at once with Ideogram 4.5, a model built for clean on-image lettering.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-thumbnail-maker` |
| `video_title` | The video's title, as context. It is not written on the image |
| `headline` | The exact words on the thumbnail, 2 to 5 words. The same headline goes on all three |
| `concept_1`, `concept_2`, `concept_3` | One visual concept each: subject, emotion, setting, colors, where the headline sits and its style. Up to 2,000 characters each |
| Fixed inside the app | 16:9 full bleed, the headline is the only text, spelled as given, bottom right corner kept clear for the length badge, no logos or play buttons; MagicPrompt off so nothing rewrites the words |
| Output | Three PNGs, 2560x1440 (16:9), one per concept: `thumbnail-1`, `thumbnail-2`, `thumbnail-3` |
| Price | 57 credits per run, 19 per image (Ideogram 4.5, measured 15 Oct 2026) |

Always send all five inputs. An input left out falls back to the board's saved demo text (a cold plunge video), which would end up in the person's thumbnail.

## A. Connection check

Look for tools ending in `run_app`, `get_execution`, `get_credit_balance` and `whoami`.

If they are missing, say so in one sentence and give the setup:

- With this plugin: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: custom connector, URL `https://www.wireflow.ai/api/mcp`.

Then still deliver the free part: the headline options and the concept sheet from `reference/thumbnail-concepts.md`, filled in for their video. Stop there.

## B. Collect inputs

Ask once, in one message:

1. The video title, and what actually happens in the video (the result, the twist, the best moment).
2. Who it is for, and the channel's look if they have one (colors, fonts, whether the host's face usually appears).
3. Any words they want on it. If none, you propose the headline.

A subject photo cannot go in yet: this app takes text only. If the person wants their own face on it, say so, describe the person in the concept instead, or hand over the concept sheet so a designer can composite the real photo.

Vertical Shorts covers are not rendered by this app (it is fixed at 16:9). Offer the concept sheet for those.

## C. Plan the headline and three concepts

Read `reference/thumbnail-concepts.md`. Then:

- Offer 2 or 3 headline options, 2 to 5 words each, that add to the title instead of repeating it. The person picks one. Never promise something the video does not show.
- Write three concepts, each from a different angle in the guide (reaction face, before and after, the object, circle the detail, versus, big number, scene at a moment). Each one names the subject, the emotion or action, the setting and light, two or three colors, and where the headline goes and how it looks.
- Show the plan as a short table and let the person edit any word. Text on the image cannot be changed without a new render.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`, then: "1 run x 57 credits = 57 credits for 3 thumbnails. Balance: 1,240." For a second headline, quote a second run. Short balance: stop and say so. Nothing renders until the person says yes to this plan and this cost.

## E. Generate

One `run_app` per headline:

```json
{ "slug": "skill-ai-thumbnail-maker", "inputs": { "video_title": "I Tried Cold Plunging Every Day for 30 Days", "headline": "DAY 30 SHOCKED ME", "concept_1": "...", "concept_2": "...", "concept_3": "..." } }
```

Poll `get_execution` every 5 seconds until the status is no longer `PENDING`, `RUNNING` or `IN_PROGRESS`. Our test run took about 25 seconds. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop and quote the error.

## F. Inspect, save, report

Save each image as `./wireflow-outputs/<YYYY-MM-DD>/thumbnails/<video-slug>_<angle>.png` with `curl -sSL -o` or PowerShell `Invoke-WebRequest -OutFile`.

Look at every image before calling it done:

- The headline matches the approved words letter by letter, and no other words appear.
- It still reads when you picture it at phone size: big letters, strong contrast.
- The bottom right corner is free of anything important.
- No stray marks, extra hands or warped faces. Small printed details (dials, scales, labels) are often garbled; say so when they are.

Flag every miss per file. A redo is a new run, 57 credits, after a yes.

Finish with a table (file, angle, CDN link) and the credits used (balance before minus after). YouTube wants a thumbnail under 2 MB; if a PNG is bigger, suggest exporting it as JPG. Offer:

- A second headline on the winning concept (one more run, one quote).
- YouTube Studio's Test and Compare to pit the three against each other.
- The board in Wireflow, to change the size or add a step: `https://www.wireflow.ai/flow/cmv93aouu000ojt06q6ss01bo?ref=skill-ai-thumbnail-maker&utm_source=github&utm_medium=skill&utm_campaign=ai-thumbnail-maker`

## Guardrails

- Spend only after a yes to the exact plan and cost.
- No clickbait the video does not deliver, no fake screenshots, no other channels' logos or branding.
- No real, identifiable people (celebrities, other creators) unless it is the person themselves and they asked.
- Keep keys and passwords out of prompts and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
