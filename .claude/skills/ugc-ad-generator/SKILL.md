---
name: ugc-ad-generator
description: "UGC ad generator for Claude Code and Claude: makes a UGC-style video ad from a product photo with Seedream 5 Lite and Veo 3.1 Lite through Wireflow. From the photo and an angle it writes the hook and a short spoken line, casts an AI creator, makes a selfie-style still of them holding the product, then turns it into a 6 second vertical talking clip with sound. Quotes the credits, waits for a yes, saves the still and the MP4 to ./wireflow-outputs, and flags that the creator is AI so the ad can be labelled honestly. Use when someone asks for a UGC ad, a UGC video, a talking-head product ad, a TikTok or Reels creator-style ad, testimonial-style video, or a UGC ad generator. Without the Wireflow connector it still writes hooks, scripts and a creator brief. Not for real customer testimonials or cloning a real person."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. The product photo must be at an https URL. Saving needs a shell; ffmpeg is optional for checks."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ugc-ad-generator"
---

# UGC Ad Generator

UGC ads work because they feel like a friend talking into their phone, not like an ad. This skill produces that format end to end: the hook, the line, the creator, the selfie frame with the product in hand, and the talking clip. Rendering happens in the Wireflow app `skill-ugc-ad-generator`: Seedream 5 Lite makes the still, Veo 3.1 Lite animates it with voice.

## How the app is wired

| Input | What to send |
|---|---|
| `product_photo` | `https://` URL of a clean product photo. Required every time |
| `creator` | Who talks and where: age range, look, clothes, room, mood. Up to 2,000 characters |
| `line` | The spoken words, in double quotes, about 12 to 18 words for 6 seconds |

| Stage | Model | Output |
|---|---|---|
| Selfie still | Seedream 5 Lite, 9:16 | JPEG, 1920x3416 in our test |
| Talking clip | Veo 3.1 Lite, 9:16, 6 s, 720p, audio on | MP4, 720x1280 |

**Price: about 106 credits by Wireflow's price list** (Seedream 5 Lite 10 per image, Veo 3.1 Lite 16 per second x 6 s, 8 Oct 2026). Our only test run showed a 224-credit balance drop, but other jobs were spending on the same account at the same time, so that figure is not clean. Quote about 106 and say it can be higher, up to about 225, until a clean run confirms it. The still is generated fresh each run.

## 1) Connection

Look for tools ending in `run_app`, `get_execution`, `get_credit_balance`, `whoami`; `create_upload_link` and `get_upload_link` handle local photos. If they are missing, say rendering needs the Wireflow connector (plugin: `/mcp`, `wireflow`, Authenticate; or `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`; Claude.ai: custom connector, same URL). Then write the free script pack: three hooks, three lines and a creator brief per hook from `reference/ugc-scripts.md`, usable with a real creator or any video tool. Stop there.

## 2) Angle and audience

Ask briefly: what the product is, who buys it, the one benefit that is true and visible, and where the ad runs (TikTok, Reels, Stories). Offers or prices go in only if real.

## 3) Script

Six seconds is one hook plus one proof:

- **Hook (first 2 seconds)**: a reaction, a confession or a "you know when..." moment. Spoken, not shouted.
- **Proof (next 4 seconds)**: one concrete, true detail the viewer can picture.
- About 12 to 18 words in total. Contractions, everyday words, no slogans.

Examples and patterns: `reference/ugc-scripts.md`. Write two or three options and let the person pick. Lines must be honest: no medical, financial or results claims the brand cannot prove, and no "I've used this for years" from an AI creator.

## 4) Cast the creator

Describe a plausible everyday person who matches the buyer: age range, style, setting, light, mood. Avoid real or famous people, children, and anything that implies a real customer. Keep the description concrete ("curly dark hair, denim jacket, sofa, plants, afternoon light").

## 5) Quote and confirm

`whoami`, `get_credit_balance`, then: "1 UGC clip (still + 6 s talking video): about 106 credits by list price, possibly up to about 225. Balance: 2,400." For several hooks, multiply. Wait for an explicit yes.

## 6) Render

```json
{ "slug": "skill-ugc-ad-generator", "inputs": { "product_photo": "https://...", "creator": "A friendly woman in her late 20s ...", "line": "\"Okay, this tote fits my laptop, my gym clothes and my lunch. Finally, one bag.\"" } }
```

Poll `get_execution` every 10 seconds and keep the person posted: the still comes first, the clip about a minute later (our test took about 90 seconds). Outputs: `creator-still` (image) and `ugc-video` (MP4).

Save to `./wireflow-outputs/<YYYY-MM-DD>/ugc/<hook-slug>-still.jpg` and `<hook-slug>.mp4`.

## 7) Review

- Look at the still: product unchanged, held naturally, label visible, hands believable.
- If ffmpeg is installed, pull a frame strip (`fps=1,tile=6x1`) and check the face and product stay stable.
- Audio: confirm there is sound (`ffmpeg -af volumedetect`). You cannot judge the words or lip sync from stills; ask the person to watch it and check the line was spoken as written. Veo sometimes paraphrases.

A new take is another full run (about 106 credits, possibly more); ask first and change one thing (line, creator or setting).

## 8) Hand over, honestly

Give paths, CDN links, credits used (balance before minus after). Then say clearly:

- The creator is AI-generated. Many platforms require AI or synthetic media labels on ads, and presenting an AI person as a real customer can break advertising rules. Label it and do not call it a testimonial.
- Add captions and music in an editor; keep the spoken line as the hook.

Offer the board in Wireflow to swap the voice model, length or add captions: `https://www.wireflow.ai/flow/cmuz2il6j000kjr06ti05j8c6?ref=skill-ugc-ad-generator&utm_source=github&utm_medium=skill&utm_campaign=ugc-ad-generator`

## Never

- Spend before the yes or re-run without asking.
- Imitate a real person, a celebrity or a specific influencer, or use someone's face without consent.
- Write fake reviews, fake results or claims the product cannot back.
- Put keys or passwords in inputs or files.
- Hide a Wireflow error. Quote it, and offer `send_feedback` if available.
