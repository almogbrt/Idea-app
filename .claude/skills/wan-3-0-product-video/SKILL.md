---
name: wan-3-0-product-video
description: "Wan 3.0 ecommerce product video in Claude Code and Claude with Alibaba Wan 3.0 through Wireflow: a product photo becomes a 5 second clip with sound. Writes a shot and sound brief for the product (one slow camera move plus the real sound it would make: a wick crackling, a drink fizzing, steam, rain on a window), keeps the product unchanged from the start frame, shows the credit cost and waits for a yes, then runs a published Wireflow app and saves the MP4 to ./wireflow-outputs. Use when someone asks for a Wan 3.0 video, a Wan product video, a product clip with sound or ASMR-style product video, a video with audio from a product photo, or wants to try Wan 3.0 on their store images. Without the Wireflow connector it still writes shot and sound briefs. For a silent clip at a lower price use ecommerce-product-video; for a person talking about the product use heygen-video-product-video."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account on a paid plan with credits. The product photo must be at an https URL (local files go up through the connector's upload link). Saving files needs a shell; ffmpeg is optional for the picture and sound checks."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-wan-3-0-product-video"
---

# Wan 3.0 Product Video

Wan 3.0, Alibaba's video model, renders sound together with the picture: the hiss of a can, a candle wick, steam off a cup arrive in the same file, at the same price as a silent clip. This skill is built around that. You (Claude) pick a product whose sound helps sell it, write one brief that covers the camera move and what the viewer hears, and the Wireflow app `skill-wan-3-0-product-video` renders it from the seller's own photo.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-wan-3-0-product-video` |
| `product_photo` | `https://` URL of the start frame. Send it on every run |
| `shot_and_sound` | One camera move, what moves in the scene, what you hear. Up to 2,000 characters |
| Fixed inside the app | Product stays as in the photo (shape, label, logo, text), no extra products, no text on screen, no hands or people unless the brief asks; sound is the product and its setting only, no music, no voice-over |
| Model settings | Wan 3.0 (`video:wan_v3_0_t2v`), 5 seconds, 720p, ratio follows the photo, audio on, Wan's own prompt expansion on |
| Output | One MP4, 5 seconds at 30 fps with a stereo sound track; 960x960 from a square photo in our test |
| Price | 58 credits per clip: our test run's charge in Wireflow's credit history, in line with Wan 3.0's list price of 12 credits a second (16 Oct 2026) |

If `product_photo` is left out, the app falls back to its saved demo candle. Always send it.

## A. Connection check

Search your tools for names ending in `run_app`, `get_execution`, `get_credit_balance`, `whoami`, `create_upload_link` and `get_upload_link`.

Not connected? Say in one sentence that rendering needs the Wireflow connector, then:

- With this plugin: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: custom connector, URL `https://www.wireflow.ai/api/mcp`.

Then hand over the free part: two or three shot and sound briefs written for their product, using `reference/shot-and-sound.md`. They work in any start-frame video tool that makes audio. Stop there.

## B. Is sound the point?

Ask what the product is and where the clip will play. Then be straight with them:

- **Wan 3.0 earns its price** when the product or its setting makes a sound people recognise: fizz, pour, steam, a flame, a click, a zip, rain, a busy cafe. Product pages with autoplay muted still benefit on social, where sound is on.
- **It is the wrong buy** for silent products in silent settings (jewelry on velvet, a print on a wall). Point them to the ecommerce-product-video skill: a start-frame clip from a cheaper model, where the sound is an afterthought you would mute anyway.

## C. The start frame

The photo is the first frame and sets the shape:

- Square photo in, square clip out (our test). Use a vertical photo for Reels and TikTok, a wide one for site banners.
- Sharp, real product, label readable. A clean setting with one or two props that can make the sound (a glass, a cup, a shelf by a window) gives Wan something to work with.
- Local file: `create_upload_link`, send the link, then `get_upload_link` when they have uploaded, and use that URL.

If their only photo is a cluttered phone shot, suggest making a clean scene first with the product-photography skill.

## D. Write the shot and sound brief

One or two sentences, in this order: the move, what moves, the sound of that motion, the room. Examples and a table by product type: `reference/shot-and-sound.md`.

```
Slow push-in toward the lit candle on the stone shelf, the flame flickers gently and the wick crackles softly, warm afternoon light drifts across the wall, quiet room tone.
```

Rules that keep the clip clean:

- One move, slow. Wan follows the start frame closely; fast moves warp labels.
- The sound must come from something in the shot or a believable room. A crackle with no flame in view sounds wrong.
- No music, no speech, no on-screen text in the brief. Music is better added later in an editor.
- Only actions the product really does, and only once.

Write two options and let them pick.

## E. Quote and confirm

Call `whoami` and `get_credit_balance`, then: "1 Wan 3.0 clip, 5 seconds with sound: 58 credits. Balance: 2,100." For a set, multiply. A short balance or a free plan (Wan 3.0 needs a paid plan): stop and say so. Nothing runs until they say yes to that plan and that cost.

## F. Render

```json
{ "slug": "skill-wan-3-0-product-video", "inputs": { "product_photo": "https://...", "shot_and_sound": "Slow push-in toward ..." } }
```

Poll `get_execution` every 5 seconds for the first minute, then every 15. Tell them it is rendering: our test took about 2.5 minutes, and Wan's prompt expansion is part of that, so allow longer when Wireflow is busy. `COMPLETED` gives the MP4 URL. `FAILED`, `CANCELLED` or `TIMEOUT`: stop and quote the error.

Save to `./wireflow-outputs/<YYYY-MM-DD>/wan-<product>-<move>.mp4` with `curl -sSL -o` or PowerShell `Invoke-WebRequest -OutFile`.

## G. Check picture and sound

With ffmpeg:

```
ffmpeg -v error -i wan-candle-push-in.mp4 -vf "fps=1,scale=240:-2,tile=5x1" -frames:v 1 frames.jpg
ffmpeg -v info -i wan-candle-push-in.mp4 -af volumedetect -f null -
```

- Frames: label readable in every frame, shape and color stable, no second product, no warping at the edges.
- Sound: `mean_volume` well above -60 dB means there is real audio. Frames cannot tell you whether the sound matches the motion, so ask them to listen once with headphones.

A redo is another full run (58 credits). Ask first and change one thing: the move, the sound, or the photo.

## H. Hand over

Give the file path, the CDN link and the credits used (balance before minus after). Then offer:

- The same move and sound on the rest of the range, quoted as one batch.
- The board in Wireflow, to change length (Wan 3.0 goes from 2 to 30 seconds), resolution or add an end frame: `https://www.wireflow.ai/flow/cmva7a6qz000jl90697edudo9?ref=skill-wan-3-0-product-video&utm_source=github&utm_medium=skill&utm_campaign=wan-3-0-product-video`

## Guardrails

- No run before a yes to the exact plan and cost, and no silent re-runs.
- Never show the product doing something it cannot do, and add no claims, prices or ratings.
- Use only photos the person owns or has the right to use.
- Keep keys and passwords out of inputs and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
