---
name: ai-image-generation
description: "AI image generation in Claude Code and Claude with Flux Pro Ultra through Wireflow. Turns a plain request into a strong image prompt, picks the aspect ratio (1:1, 16:9, 9:16, 4:3 and more), shows the credit cost and waits for a yes, then runs a published Wireflow app and saves the images to ./wireflow-outputs. Use when someone asks to generate, create or make an image, picture, photo, illustration, blog or hero image, social post image, wallpaper or thumbnail background, or says 'AI image generation', 'text to image' or 'make me an image of'. Without the Wireflow connector it still writes a ready-to-paste prompt pack. For a photo of an existing product use product-photography; for motion use ai-video-generation."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Without it the skill still returns prompts. Saving files needs a shell (curl or PowerShell)."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-image-generation"
---

# AI Image Generation

You turn a request like "a hero image for my bakery's website" into finished image files. The pixels are made by the Wireflow app `skill-ai-image-generation` (Flux Pro Ultra). Your job is the part people are bad at: the prompt, the frame shape, the cost check and the file handling.

## The app this skill drives

| Item | Value |
|---|---|
| App slug for `run_app` | `skill-ai-image-generation` |
| Input `prompt` | The full image prompt, up to 2,000 characters |
| Input `aspect_ratio` | One of `21:9`, `16:9`, `4:3`, `3:2`, `1:1`, `2:3`, `3:4`, `9:16`, `9:21` |
| Output | One JPEG per run (about 4 megapixels) |
| Price | 19 credits per image (Wireflow price list, 8 Oct 2026) |

One run makes one image. For four options, run the app four times with four different prompts. Variety between prompts beats four copies of one prompt.

## Step 1: find the Wireflow tools

Look for the Wireflow MCP tools by their base names: `run_app`, `get_execution`, `get_credit_balance`, `whoami`. The prefix depends on how the person connected (for example `mcp__wireflow__run_app`), so match on the ending.

If they are missing, say so in one line and give the connect steps:

- Claude Code with this plugin installed: run `/mcp`, pick `wireflow`, choose Authenticate and sign in.
- Claude Code without the plugin: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp` to sign in.
- Claude.ai or Claude Desktop: add a custom connector with the URL `https://www.wireflow.ai/api/mcp`.

Then still deliver value: write the prompt pack from Step 2 (prompts plus the ratio for each) so they can paste it into any image tool. Stop there. Never fake a run.

## Step 2: write the prompt

Ask at most one question, and only if the subject is unclear. Otherwise decide yourself and say what you chose.

Build each prompt in this order, as plain descriptive sentences, not a tag list:

1. Subject: what is in frame, with concrete details (material, color, age, count).
2. Setting: where it is and what surrounds it.
3. Light: time of day or light source, and its direction and quality.
4. Camera: shot size and lens feel (close-up, wide, 35mm, overhead).
5. Style: photo, film stock, illustration style, 3D render, and the mood.
6. Exclusions, written as plain words, always ending with the frame rule: "no text, no logos, no watermark, full bleed, no border, no frame". Flux can add a thin dark strip or a frame along an edge; asking for full bleed prevents most of it.

Pick the ratio from where the image will live:

| Destination | Ratio |
|---|---|
| Instagram or LinkedIn feed post | `1:1`, or `3:4` for a taller post (4:5 is not offered) |
| Story, Reel, TikTok cover, phone wallpaper | `9:16` |
| Blog header, website hero, YouTube thumbnail background, slide | `16:9` |
| Wide banner or cinematic still | `21:9` |
| Print, product listing, catalog | `3:2` or `4:3` |

Flux Pro Ultra renders short words poorly. If the image needs readable text, leave space for it and say the text should be added in a design tool, or suggest a text-capable model from `reference/models.md` inside Wireflow.

More patterns and worked examples: `reference/prompt-guide.md`.

## Step 3: quote it and wait

1. Call `whoami` and `get_credit_balance`.
2. Show a short plan: each prompt (shortened is fine), its ratio, the number of images, and the cost at 19 credits each. Example: "3 images x 19 = 57 credits. Your balance: 1,240."
3. If the balance is lower than the cost, stop and say so. Wireflow plans start at US$24 a month.
4. Ask for a yes. Do not call `run_app` until the person clearly agrees to this plan and this cost.

## Step 4: run

For each approved prompt, call `run_app` with:

```json
{ "slug": "skill-ai-image-generation", "inputs": { "prompt": "<prompt>", "aspect_ratio": "16:9" } }
```

Put every value inside `inputs`. A key outside `inputs` is refused.

Keep the returned `executionId`. Poll `get_execution` every 5 seconds. Keep polling while the status is `PENDING`, `RUNNING` or `IN_PROGRESS`. Stop at `COMPLETED`, `FAILED`, `CANCELLED` or `TIMEOUT`. Images usually finish in 10 to 20 seconds.

The finished run lists outputs. Take every `url` (or each entry of `urls`). If the app belongs to someone else, outputs arrive as entries with `nodeId`, `label`, `status` and `url`.

## Step 5: save and check

Save each image to `./wireflow-outputs/<YYYY-MM-DD>/ai-image-<n>.jpg`:

- macOS or Linux: `curl -sSL -o "<path>" "<url>"`
- Windows PowerShell: `Invoke-WebRequest -Uri "<url>" -OutFile "<path>"`
- No shell (Claude.ai): list the links instead.

Open each saved file and look at it. Check the subject, the ratio and obvious faults (extra fingers, broken text, cropped heads, a border or dark strip along any edge). Describe any fault honestly. A new attempt costs another 19 credits, so ask before re-running, with the reason and the cost.

## Step 6: report

End with:

- the saved paths and the Wireflow CDN links,
- credits used: balance before minus balance after (from `get_credit_balance`),
- one line on what you would change next time, if anything.

Then offer two next steps:

- Edit or remix it in Wireflow: the app's board is `https://www.wireflow.ai/flow/cmuyrvkpx0004nh0606sz0d3k?ref=skill-ai-image-generation&utm_source=github&utm_medium=skill&utm_campaign=ai-image-generation`. Duplicate it to swap the model or add an upscaler. If a `clone_template` tool is available, offer to copy it into their account instead.
- Run a batch: give a list of prompts and get one quote for the whole set.

## Rules

- No `run_app` call without a yes to the exact plan and cost. One yes covers that plan only.
- Never retry a failed or weak image without asking first.
- Never put API keys, tokens or passwords in prompts or files.
- Do not make images of real private people, or images meant to deceive. Wireflow's terms apply.
- If Wireflow refuses a prompt or a tool fails, report the exact error. If `send_feedback` exists and the person agrees, file it there.
