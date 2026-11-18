---
name: ai-video-generation
description: "AI video generation in Claude Code and Claude with MiniMax Hailuo 03 Max Turbo through Wireflow. Plans the shot first (subject, action, camera move, light), turns a text prompt or a start image into a 5 second 16:9 clip, shows the credit cost and waits for a yes, then runs a published Wireflow app and saves the MP4 to ./wireflow-outputs. Use when someone asks to generate, create or make a video, clip, b-roll, short animation, text to video or image to video, says 'AI video generation', or asks to animate a picture. Without the Wireflow connector it still writes a shot list and prompt pack. Not for cutting, captioning or editing footage that already exists."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Without it the skill still returns a shot list. Saving files needs a shell; ffmpeg is optional for frame checks."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-video-generation"
---

# AI Video Generation

A good AI clip is decided before anything renders: one subject, one action, one camera move, in one short beat. This skill writes that shot, prices it, gets a yes, and has the Wireflow app `skill-ai-video-generation` render it with MiniMax Hailuo 03 Max Turbo.

## What the app takes and returns

| Item | Value |
|---|---|
| App slug | `skill-ai-video-generation` |
| `prompt` (required) | The shot description, up to 2,000 characters |
| `start_image` (optional) | An `https://` image URL. The clip opens on this frame (image to video). Leave it out for text to video |
| Output | One MP4, 5 seconds, 16:9, about 1344x768, with an audio track |
| Price | About 40 credits per clip (8 credits a second, Wireflow price list, 8 Oct 2026) |

The format is fixed: 16:9 and 5 seconds. If the person needs vertical 9:16 or a longer clip, say so before you plan, and offer the board link in the report step, where they can change those settings.

## 1. Check the connection

The Wireflow tools end in `run_app`, `get_execution`, `get_credit_balance` and `whoami` (the prefix varies with the client). When they are not there:

1. Tell the person generation needs the Wireflow connector.
2. Plugin users: `/mcp`, select `wireflow`, Authenticate. Others: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`. Claude.ai or Desktop: add a custom connector with `https://www.wireflow.ai/api/mcp`.
3. Hand over the shot list from section 2 anyway, written so it works in any video model, and stop.

## 2. Plan the shot

Write each shot as four to six sentences covering:

- **Subject and look**: who or what, with the details that must stay stable.
- **Action**: one clear thing that happens in 5 seconds. Two actions usually blur into mush.
- **Camera**: one move, named plainly: static, slow dolly-in, dolly-out, pan left, tilt up, orbit, handheld follow, crane up.
- **Light and place**: time of day, light source, weather, environment.
- **Style**: live-action cinematic, documentary handheld, stop-motion, 3D animation, anime.

Rules of thumb that save credits:

- Ask for motion that fits 5 seconds. "Walks across the whole city" will not fit; "steps off the curb" will.
- Faces and hands stay cleaner when the camera is slow and the subject is mid-distance.
- With a start image, describe only what moves and how the camera moves. The image already fixes the look.
- Text and logos inside the video come out garbled. Plan them as an overlay added later.

Shot vocabulary and twelve ready shots: `reference/shot-guide.md`. Model choices beyond this app: `reference/models.md`.

## 3. Getting a start image (optional)

The app needs a public `https://` URL, not a local path.

- An image the person already has online: use its direct URL.
- A local file: if `create_upload_link` exists, call it, send the person the link, and after they upload call `get_upload_link` to get the file's URL. If those tools are missing, ask for a public link.
- An image made a moment ago with Wireflow: its `cdn.wireflow.ai` URL works directly.

## 4. Price it, then wait

Call `whoami` and `get_credit_balance`. Present:

```
Shot 1: <one-line summary> (text to video)
Shot 2: <one-line summary> (from start image)
2 clips x ~40 credits = ~80 credits. Balance: <n> credits.
```

If the balance is short, stop and say how many credits are missing. Wait for an explicit yes before any `run_app` call. A yes covers only the shots and cost you showed.

## 5. Render

Call `run_app` once per shot:

```json
{ "slug": "skill-ai-video-generation", "inputs": { "prompt": "<shot>", "start_image": "https://..." } }
```

Drop `start_image` entirely for text to video; do not send an empty string. All inputs go inside `inputs`.

Poll `get_execution` with the `executionId` every 10 seconds. `PENDING`, `RUNNING` and `IN_PROGRESS` mean wait. `COMPLETED` means done; `FAILED`, `CANCELLED` and `TIMEOUT` mean stop and report the error text. A clip usually takes under a minute, sometimes longer. While waiting, tell the person it is rendering instead of going silent.

Collect the video URL from the outputs (`url`, or each item of `urls`).

## 6. Save and review

Download to `./wireflow-outputs/<YYYY-MM-DD>/video-<n>.mp4` with `curl -sSL -o` (macOS, Linux) or `Invoke-WebRequest -OutFile` (Windows). In Claude.ai, give the link.

If ffmpeg is installed, pull three stills to check the clip without watching it blind:

```
ffmpeg -v error -i video-1.mp4 -vf "fps=0.6,scale=480:-2,tile=3x1" -frames:v 1 video-1-frames.jpg
```

Look at the strip: does the subject stay the same, does the action happen, is anything melting or warping? Report what you see. Say clearly that stills cannot judge motion smoothness or sound.

A second take costs another ~40 credits. Ask first, and say what you would change in the prompt.

## 7. Wrap up

Report the file path, the CDN link, and the credits used (balance before minus after). Then offer:

- Open the board in Wireflow to change ratio, length or model: `https://www.wireflow.ai/flow/cmuyryl0w000gnz06lizb92us?ref=skill-ai-video-generation&utm_source=github&utm_medium=skill&utm_campaign=ai-video-generation`
- Chain shots: render a still with the ai-image-generation skill, then use it as the start image so every clip shares one look.

## Hard limits

- Never call `run_app` before a yes to the shown plan and cost.
- No automatic retries. Every extra render needs its own yes.
- No videos of real private people, no deceptive or harmful content.
- Never write keys or passwords into prompts or files.
- If Wireflow refuses or a tool breaks, quote the exact error. Offer to report it with `send_feedback` if that tool is present.
