---
name: ai-ad-creative-generator
description: "AI ad creative generator in Claude Code and Claude with Nano Banana 2 through Wireflow: static ad variations in 1:1, 4:5 and 9:16. From a product photo and a short brief it writes distinct ad concepts and headline variants, then renders each concept in all three placements at once (1:1 feed, 4:5 portrait feed, 9:16 stories and reels) with the headline and call to action spelled exactly. Quotes the credits and waits for a yes, saves the set with test-ready file names to ./wireflow-outputs. Use when someone asks for ad creatives, Facebook, Instagram, Meta or TikTok static ads, ad variations to A/B test, headline variants on images, or an AI ad creative generator. Without the Wireflow connector it still writes the concepts, headlines and layout briefs. For plain product scenes with no text use product-photography."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. The product image must be at an https URL. Saving needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ad-creative-variations"
---

# AI Ad Creative Generator

Paid social rewards volume and variety: several angles, each with a few headlines, each in every placement. Making that by hand is a day of design work. Here Claude does the strategy and copy, and the Wireflow app `skill-ad-creative-variations` renders one concept in three placements per call with Nano Banana 2, which handles on-image text well.

## What one call produces

| | |
|---|---|
| App slug | `skill-ad-creative-variations` |
| `product_photo` | `https://` URL of the product, packshot or logo on a plain background. Always send it |
| `ad_brief` | One concept: headline and CTA in quotes, the visual, the palette and type style. Max 2,000 characters |
| Rules inside the app | Product unchanged, words spelled exactly as quoted and kept inside the safe area, no extra text, no fake logos or ratings |
| Output | Three PNGs from the same brief: 1:1 (1024x1024), 4:5 (928x1152), 9:16 (768x1376) |
| Price | 60 credits per call, 20 per image (Nano Banana 2 at 1K, measured 8 Oct 2026) |

So 2 concepts = 6 ads = 120 credits.

## 1. Tools check

Need: tools ending in `run_app`, `get_execution`, `get_credit_balance`, `whoami` (and `create_upload_link` / `get_upload_link` for a local image). If they are absent, explain the Wireflow connector setup in two lines (plugin: `/mcp`, `wireflow`, Authenticate; else `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`; Claude.ai: custom connector) and still deliver the concept sheet from step 3, so a designer can build it. Stop.

## 2. The brief behind the ads

Collect, in one message:

- What is sold, to whom, and the one thing that should make them stop scrolling.
- The offer, if any, exactly as it really is (price, discount, free shipping). Never invent one.
- Words the brand uses or avoids; brand colors if they have them.
- The product image (URL, or upload via `create_upload_link` then `get_upload_link`).

## 3. Concepts and headlines

Write 2 to 4 concepts, each a different angle, not the same idea reworded. Use the angle list in `reference/ad-angles.md` (problem/solution, outcome, social moment, product hero, offer, comparison with the old way, ritual). For each concept give:

- **Headline**: 2 to 6 words. Fits on two lines in a 9:16 story.
- **CTA**: 2 to 3 words for the button ("Shop the mug").
- **Visual**: the scene, where the product sits, where the headline goes.
- **Style**: palette and type ("bold modern serif, cream and terracotta").

Rules for copy: plain words, no claims the product cannot back up, no fake urgency, no ALL CAPS paragraphs, no emojis in the image. Present the concepts as a table and let the person edit words before anything renders. Words in the image cannot be changed later without a new render.

## 4. Quote

`whoami`, `get_credit_balance`, then: "3 concepts x 60 credits = 180 credits for 9 ads. Balance: 1,020." Wait for an explicit yes.

## 5. Render

One `run_app` per concept:

```json
{ "slug": "skill-ad-creative-variations", "inputs": { "product_photo": "https://...", "ad_brief": "Headline, exactly: \"Slow mornings, made better\". Call to action button, exactly: \"Shop the mug\". Visual: ..." } }
```

Poll `get_execution` every 5 seconds; a concept takes about 20 to 30 seconds. The finished run lists three outputs (`ad-1x1`, `ad-4x5`, `ad-9x16`).

Save with names an ads manager can sort: `./wireflow-outputs/<YYYY-MM-DD>/ads/<concept-slug>_<headline-slug>_<ratio>.png`, e.g. `ritual_slow-mornings_4x5.png`.

## 6. Proofread like a media buyer

For every image:

- Read the headline and CTA letter by letter against the approved copy.
- Text inside the safe area: in 9:16, nothing in the top 14% or bottom 20% (app UI covers it).
- Product looks like the real product.
- No stray words, watermarks or invented badges.

Report problems per file. A fix re-renders the whole concept (60 credits) after a yes.

## 7. Deliver

Give a table: file, concept, headline, ratio, CDN link. Add the credits used (balance before minus after). Suggest a simple test: run all concepts at equal budget for a few days, keep the winner, then make headline variants of the winning concept only.

Offer the board in Wireflow to swap models, change sizes or add a logo layer: `https://www.wireflow.ai/flow/cmuz2ijfk000djr06ftosg7f5?ref=skill-ai-ad-creative-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-ad-creative-generator`

## Limits

- No render without the yes; no unasked re-renders.
- No false claims, fake reviews or prices, competitor logos, or real people who did not agree to appear.
- Ad platforms have their own policies; the person is responsible for checking them before launch.
- Never place keys or passwords in briefs or files.
- Quote any Wireflow error exactly and offer `send_feedback` if the tool is present.
