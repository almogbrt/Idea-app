---
name: ecommerce-product-video
description: "AI product video for ecommerce in Claude Code and Claude with MiniMax Hailuo 03 Max Turbo through Wireflow: one product photo to a 6 second clip. Turns the photo into a short product video for an online store or ad: picks a product-safe camera move (orbit, slow push-in, reveal, light sweep, turntable, in-context drift), keeps the product unchanged from the first frame, quotes the credits and waits for a yes, then renders the clip and saves the MP4 to ./wireflow-outputs. Use when someone asks for an ecommerce product video, a Shopify or Amazon product video, a video ad from a product photo, a spinning or 360-style product clip, or to animate a product image. Without the Wireflow connector it still writes the motion briefs and a shot plan. For general text-to-video scenes use ai-video-generation."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. The product photo must be at an https URL. Saving needs a shell; ffmpeg is optional for checking frames."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ecommerce-product-video"
---

# AI Ecommerce Product Video

Shoppers trust a product they can see move: light running over the material, the camera circling to show the side, a lid coming off. This skill turns a still product photo into that kind of clip. The photo becomes the first frame, a short motion brief says what moves, and the Wireflow app `skill-ecommerce-product-video` renders it with MiniMax Hailuo 03 Max Turbo.

## The app

| Part | Value |
|---|---|
| Slug | `skill-ecommerce-product-video` |
| `product_photo` | `https://` URL of the first frame. Always sent |
| `motion` | Camera move and what changes, up to 2,000 characters |
| Fixed in the app | Product must stay unchanged, no morphing, no extra products, no text overlays |
| Output | One MP4, about 6.5 seconds, 768P, with an audio track |
| Shape | Follows the photo: a square photo gave a 768x768 clip in our test. For a vertical 9:16 clip, start from a vertical photo |
| Price | 48 credits per clip in our test (Hailuo 03 Max Turbo, 8 credits a second, 8 Oct 2026) |

## Step A: connected?

Look for tools ending in `run_app`, `get_execution`, `get_credit_balance`, `whoami`, and for local files `create_upload_link` and `get_upload_link`. Without them, say that rendering needs the Wireflow connector and how to add it (plugin: `/mcp` → `wireflow` → Authenticate; otherwise `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`; Claude.ai: custom connector, same URL). Then give the free part: a shot plan with two or three motion briefs from `reference/product-motion.md`, written for their product, and stop.

## Step B: pick the right photo

The first frame decides everything. Prefer:

- A clean packshot with space around the product (white or simple background). Moves like an orbit need room at the edges.
- The shape you want out: vertical photo for Reels, TikTok and Stories, square for feeds and most product pages, wide for site banners.
- The real product, sharp, label readable.

If they only have a cluttered phone photo, suggest making a clean packshot first with the amazon-product-images or product-photography skill, then animating that.

Local file: `create_upload_link`, send the link, then `get_upload_link` once they have uploaded, and use the returned URL.

## Step C: choose the motion

One move per clip, slow and controlled. Product video is not the place for dramatic camera work.

| Goal | Move to brief |
|---|---|
| Show the whole shape | Slow half orbit left to right at product height |
| Premium feel | Light sweep: a soft highlight glides across the surface, camera static |
| Focus on detail | Slow push-in toward the label or texture |
| Reveal | Start close on a detail, pull back to the whole product |
| Turntable | Product rotates slowly on a plinth, camera static |
| In context | Gentle drift past the product in its setting, background slightly moving |

Write the brief as: the move, its speed, what the light does, what must stay still. Add physical actions only if the product really does them (a pump pressing, a lid opening), and say "once".

Avoid: hands appearing from nowhere, liquids pouring (often messy), fast spins, text on screen.

## Step D: quote and confirm

`whoami`, `get_credit_balance`, then: "2 clips (orbit, light sweep) x about 48 credits = about 96. Balance: 1,300." Wait for a yes to these clips.

## Step E: render

```json
{ "slug": "skill-ecommerce-product-video", "inputs": { "product_photo": "https://...", "motion": "Slow half orbit around the bottle from left to right at bottle height, soft light glides across the glass, background stays clean." } }
```

Poll `get_execution` every 5 seconds at first, then every 15; tell the person it is rendering. Hailuo 03 Max Turbo is fast: our test clip was ready in about 15 seconds, but allow a few minutes when Wireflow is busy. `COMPLETED` gives the MP4 URL; `FAILED`, `CANCELLED` or `TIMEOUT` means stop and report.

Save to `./wireflow-outputs/<YYYY-MM-DD>/product-video-<move>.mp4`.

## Step F: check the clip

If ffmpeg exists, make a strip of six frames:

```
ffmpeg -v error -i product-video-orbit.mp4 -vf "fps=1,scale=240:-2,tile=6x1" -frames:v 1 orbit-strip.jpg
```

Look at it for: label still readable, shape and color stable across frames, no second product appearing, no warping at the edges. Say plainly that frames cannot judge smoothness or sound. The clip carries an audio track the model generated; for store pages and most ads, mute it or replace it with music in an editor.

A re-render costs about 48 again. Ask first and name the change.

## Step G: hand over

Path, CDN link, credits used (balance before minus after). Then offer:

- A matching set: the same move on each product in a range, quoted as one batch.
- The board in Wireflow to change length, resolution or model: `https://www.wireflow.ai/flow/cmuz2i3fu0003jr06adbp2ohv?ref=skill-ecommerce-product-video&utm_source=github&utm_medium=skill&utm_campaign=ecommerce-product-video`

## Do not

- Render before the yes, or loop on re-renders.
- Show the product doing something it cannot do, or add claims on screen.
- Animate photos the seller does not own.
- Write keys or passwords anywhere.
- Hide errors: quote them, offer `send_feedback` if it exists.
