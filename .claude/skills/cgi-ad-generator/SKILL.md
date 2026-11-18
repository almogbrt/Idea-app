---
name: cgi-ad-generator
description: "CGI ad generator in Claude Code and Claude with Seedance 2.5 through Wireflow: your product, giant, in a real street, as one vertical video. From a product photo and an idea in plain words, Claude plans a fake out-of-home (FOOH) ad with rules that keep it from looking like a sticker, writes the opening frame, the final frame and the action, shows the credit cost and waits for a yes. A Wireflow app then makes both stills with GPT Image 2.5 Sunburst Edit and a 5 second 9:16 Seedance 2.5 shot with sound between them, and Claude saves all three to ./wireflow-outputs. Use when someone asks for a CGI ad, a fake out of home ad, a FOOH ad, a giant product in a city, a viral 3D street ad, or a CGI product video for Instagram or TikTok. Without the Wireflow connector it still writes the plan sheet and all three prompts. For a plain product clip on a clean background use ecommerce-product-video."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. The product photo must be at an https URL; create_upload_link turns a local file into one. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-cgi-ad-generator"
---

# CGI Ad Generator

People who ask for a CGI ad usually have a product and a half idea ("our can, huge, in Times Square"). You (Claude) turn that into one impossible moment that works on a real street, plan it with the rules in `reference/fooh-rules.md`, and write three short prompts from that plan. The Wireflow app `skill-cgi-ad-generator` then makes the opening still from the product photo, edits it into the final still, and runs Seedance 2.5 from the first still to the second.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-cgi-ad-generator` |
| `product_photo` | `https://` URL of a clean product photo, front on, label readable |
| `opening_frame` | The first frame: the real place, where the product stands, its height in metres beside a person, the light, the camera height and what stands in front of it |
| `final_frame` | Only what has changed by the last frame. Everything else stays put |
| `what_happens` | The action from first frame to last, with times in seconds, then the sounds |
| Fixed inside the app | Phone camera at eye level or lower, product colours slightly muted, something in front of the product, shadows matched to the people, label kept letter for letter; the video opens on the opening still and ends on the final still, with real sound only and no music or voice |
| Output | `opening-still` and `final-still` (PNG, 1152x2048) and `ad-video` (MP4, 9:16, 720p, 5 s, with sound) |
| Price | About 175 credits per run: 20 for each still and 135 for 5 seconds of Seedance 2.5 (Wireflow price list, 16 Nov 2026; our test run was charged 174) |

Send all four inputs on every run, because an empty one falls back to the app's own demo, a giant noodle cup in Naples.

## A. Connection check

Search your tools for names ending in `run_app`, `get_execution`, `get_credit_balance` and `whoami`, plus `create_upload_link` and `get_upload_link` for local photos.

If they are missing, say in one sentence that rendering needs the Wireflow connector, then give the setup:

- With this plugin: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: add a custom connector with the URL `https://www.wireflow.ai/api/mcp`.

Then fill in the plan sheet from `reference/fooh-rules.md` and write the three prompts, which work in any tool that edits a photo and makes video between two frames. Stop there.

## B. Get the idea in plain words

People ask for these loosely, so take whatever they give and only ask for what is missing, in one message:

1. The product photo. A local file goes up through `create_upload_link`: the person opens the link, then `get_upload_link` returns the https URL.
2. Where it goes: a city, a kind of street, a landmark.
3. What happens: the one impossible thing.

If they only name the product, offer three ideas that follow the idea rules in the reference file (the product is the impossible thing, it reads with the sound off, the place adds something, and something happens). Let them pick one.

## C. Plan, then write the prompts

Fill in the plan sheet in `reference/fooh-rules.md` first, because the size, the light and the camera height decide whether the ad looks real. Street-scale products stand 2 to 3 times a person's height, and the light is shade or overcast unless the person asks for sun. The camera is a phone at eye level or lower, so the top of a tall product is seen from below, and a passer-by, a lamppost or a branch sits in front of its lower part.

Then write `opening_frame`, `final_frame` and `what_happens` from that one plan, in the order the reference file gives. Read them side by side before you quote. The first moment of `what_happens` should be what `opening_frame` shows, its last moment should be what `final_frame` shows, and the same people stay in the same places. In the project this skill comes from, video prompts written without looking at the stills needed facts fixed by hand.

Show the person the idea in one line and the three prompts.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`, then give the total: "1 CGI ad, 2 stills and a 5 second Seedance 2.5 shot with sound: about 175 credits. Balance: 1,240." For several ideas, list each one and add them up. If the balance is short, say so and stop. Nothing runs until the person says yes to this plan and this price.

## E. Generate

One `run_app` per approved idea:

```json
{ "slug": "skill-cgi-ad-generator", "inputs": { "product_photo": "https://...", "opening_frame": "A narrow shaded street in Naples ...", "final_frame": "A thick white cloud of steam has poured out of the cup ...", "what_happens": "At 0.0s a few faint wisps of steam ..." } }
```

Poll `get_execution` every 10 seconds while the status is `PENDING`, `RUNNING` or `IN_PROGRESS`, and keep the person posted. Our test run took just under 5 minutes from start to finish. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop and quote the error. Seedance screens prompts and images and can refuse a run after the stills are made (copyright is the usual reason), so pass that message on as it is.

## F. Check, save, report

Save to `./wireflow-outputs/<YYYY-MM-DD>/cgi-ads/<idea-slug>-opening.png`, `<idea-slug>-final.png` and `<idea-slug>.mp4` with `curl -sSL -o <file> <output url>`, or in PowerShell `Invoke-WebRequest -Uri <output url> -OutFile <file>`.

Look at both stills before the video, and check that:

- the label is spelled right, letter for letter
- the size is close to the plan next to the people
- the camera cannot see into the top of the product
- something stands in front of it, and its shadows point the same way as the people's.

If ffmpeg is installed, pull frames at 4 per second (`ffmpeg -i <file> -vf fps=4,scale=270:-1,tile=5x4 sheet.png`) and check that the product is in shot at 0.0 s, that something changes by 2 s and the main moment lands by about three quarters of the way, and that the clip plays forwards from the opening still to the final still with the label intact. You cannot hear the sound, so confirm there is an audio track and ask the person to listen.

Name every miss plainly. A retake is a full run, about 175 credits, so ask first and change one thing at a time.

End with the three files, their CDN links and the credits used (balance before minus after). Offer:

- A second shot from further back to prove the size, or a new idea, quoted the same way.
- The board in Wireflow, for longer shots, 16:9 or your own sound effects: `https://www.wireflow.ai/flow/cmwiw3pwr0014l5083yk4i97w?ref=skill-cgi-ad-generator&utm_source=github&utm_medium=skill&utm_campaign=cgi-ad-generator`

## Guardrails

- Spend only after a yes to the plan and the price.
- Use products the person owns or may advertise. Never copy another brand's ad, logo or campaign, and never use a real person's face.
- These ads show events that never happened. Suggest the platform's AI or CGI label, and never present one as news or as a real installation.
- Keep keys and passwords out of prompts and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
