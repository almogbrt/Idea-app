---
name: heygen-video-product-video
description: "HeyGen video ecommerce product video in Claude Code and Claude with HeyGen Video through Wireflow: a presenter holds your product and talks about it. From one product photo it writes a short script (about 15 to 20 words), casts an AI presenter and a setting, shows the credit cost and waits for a yes, then runs a published Wireflow app that makes an 8 second vertical clip with the presenter's voice and saves the MP4 to ./wireflow-outputs. Use when someone asks for a HeyGen product video, a presenter or spokesperson video for a product, a talking product demo, an AI presenter holding a product, or a short explainer ad for a store listing or social. Without the Wireflow connector it still writes presenter scripts and a casting brief. For a clip with no person use wan-3-0-product-video or ecommerce-product-video; for a selfie-style creator ad use ugc-ad-generator."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account on a paid plan with credits. The product photo must be at an https URL (local files go up through the connector's upload link). Saving files needs a shell; ffmpeg is optional for checks."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-heygen-video-product-video"
---

# HeyGen Video Product Video

A presenter video is the quickest way to explain a product: one person, looking at the camera, holding it up and saying what it is. HeyGen Video, HeyGen's own video model, makes the whole shot in one pass, voice and room sound included, and it takes the product photo as a reference, so the bottle or box in their hand gets its shape and colour from the seller's own picture. You (Claude) write the script and the presenter brief; the Wireflow app `skill-heygen-video-product-video` renders it.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-heygen-video-product-video` |
| `product_photo` | `https://` URL of a clear product photo. HeyGen reads it as Picture 1. Send it on every run |
| `presenter` | Who talks, how they look, where they stand. Up to 2,000 characters |
| `script` | The exact words, about 15 to 20 for 8 seconds, plain text without quote marks |
| Fixed inside the app | One presenter at chest height facing the camera, product held near the face and kept as in the photo, no added labels or text on the product, steady camera, voice and light room tone only, no music, no captions, no on-screen text |
| Model settings | HeyGen Video (`video:heygen_video_1`), 8 seconds, 9:16, 768p, HeyGen's prompt rewrite off so the script stays as written |
| Output | One vertical MP4, 768x1344, 8 seconds at 24 fps, with a stereo voice track (our test) |
| Price | 72 credits per clip, charged on both test runs (16 Oct 2026). Wireflow's price list says 5 credits a second, about 40 for 8 seconds; the real charge was 72, so quote 72 |

If `product_photo` is left out, the app falls back to its saved demo serum bottle. Always send it.

## A. Connection check

Search your tools for names ending in `run_app`, `get_execution`, `get_credit_balance`, `whoami`, `create_upload_link` and `get_upload_link`.

Not connected? Say in one sentence that rendering needs the Wireflow connector, then:

- With this plugin: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: custom connector, URL `https://www.wireflow.ai/api/mcp`.

Then write the free part from `reference/presenter-scripts.md`: three script options and a presenter brief for their product. A real person can film those on a phone. Stop there.

## B. What to ask

- What the product is and who buys it.
- One detail that is true and easy to picture: how it is used, what is in the box, what it fits.
- Where the clip runs. The app makes 9:16, which suits Reels, TikTok, Shorts and Stories, and works as a vertical video on most product pages.
- The product photo. Sharp, the real product with its real label facing the camera, on a plain background if possible: HeyGen copies the product from it, and a busy photo can pull the background in too. Local file: `create_upload_link`, then `get_upload_link`.

Tell them one known limit before quoting: HeyGen Video tends to put a label on a product that has none. In both of our test runs it printed a made-up label with unreadable text on a plain serum bottle, even with a rule against it in the app. Shape, cap and colour came out right. A plain or unbranded product may come back with a fake label; a product photographed with its real label gives HeyGen the real thing to copy, but check it in every take.

## C. Script

Eight seconds holds one sentence that names the product and one true detail. Patterns and examples: `reference/presenter-scripts.md`.

- 15 to 20 words. Read it out loud: over 8 seconds at a calm pace means cut it.
- Everyday words and contractions. No slogans, no prices or offers unless the seller gave them, no results the brand cannot prove, nothing medical.
- An AI presenter never claims years of personal use or speaks as a named customer.

Offer two or three options and let them pick.

## D. Presenter

One or two sentences: age range, look, clothes that suit the product, where they stand, mood. Match the buyer, not a model shoot. No real, famous or named people, no children, no likeness of a specific influencer.

## E. Quote and confirm

Call `whoami` and `get_credit_balance`, then: "1 presenter clip, 8 seconds with voice: 72 credits. Balance: 2,100." For several scripts, multiply. A short balance or a free plan (HeyGen Video needs a paid plan): stop and say so. Nothing runs until they say yes to the plan and the cost.

## F. Render

```json
{ "slug": "skill-heygen-video-product-video", "inputs": { "product_photo": "https://...", "presenter": "A friendly woman in her early 30s ...", "script": "This is the serum I use every night. Three drops, pat it in, and that is my whole routine." } }
```

Poll `get_execution` every 5 seconds and keep them posted; both test clips were ready in about 20 seconds, but allow a few minutes when Wireflow or HeyGen is busy. `COMPLETED` gives the MP4 URL. `FAILED`, `CANCELLED` or `TIMEOUT`: stop and quote the error.

Save to `./wireflow-outputs/<YYYY-MM-DD>/presenter-<product>-<script-name>.mp4` with `curl -sSL -o` or PowerShell `Invoke-WebRequest -OutFile`.

## G. Review

- If ffmpeg is installed, pull a strip of frames (`fps=1,scale=240:-2,tile=8x1`): the product in hand should match the photo (shape, cap, color, label), the face should stay the same person, hands should look natural.
- Look hard at the label. Any text or logo that is not on the real product (see section B) means the take should not go on a store page or in an ad as it is; say so plainly.
- Confirm there is sound: `ffmpeg -i clip.mp4 -af volumedetect -f null -`.
- Frames cannot show lip sync or whether every word was said. Ask them to watch it once and check the script was spoken as written.

A new take is another full run (72 credits). Ask first and change one thing: the script, the presenter or the photo.

## H. Hand over, honestly

Give the file path, the CDN link and the credits used (balance before minus after). Then say plainly:

- The presenter is AI-made. Label it where ad platforms ask for AI or synthetic media, and never present it as a customer testimonial.
- Captions help on social, where many people watch muted. Add them in an editor.

Offer the board in Wireflow to change the length (5 to 15 seconds), the shape or the resolution: `https://www.wireflow.ai/flow/cmva7ak9l001ol906x7c42oco?ref=skill-heygen-video-product-video&utm_source=github&utm_medium=skill&utm_campaign=heygen-video-product-video`

## Guardrails

- No run before a yes to the exact plan and cost, and no re-runs without asking.
- Never imitate a real person or use someone's face or voice without consent.
- No fake reviews, results or claims the product cannot back.
- Use only product photos the person has the right to use.
- Keep keys and passwords out of inputs and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
