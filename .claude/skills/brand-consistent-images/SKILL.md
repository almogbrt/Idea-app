---
name: brand-consistent-images
description: "Brand consistent AI images in Claude Code and Claude with Nano Banana Lite through Wireflow: your logo, product and palette in, on-brand images out. Builds a short brand brief, writes each image request so the logo and product stay as given, shows the credit cost and waits for a yes, then runs a published Wireflow app with up to 3 brand reference images and saves square images to ./wireflow-outputs. Use when someone asks for on-brand images, images that match their brand kit, style guide or logo, a consistent visual set for social posts, ads or a campaign, or their logo on a product shot. Without the Wireflow connector it still writes a brand brief and an on-brand request pack. For plain product scenes with no brand kit use product-photography; for images from text alone use ai-image-generation."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Brand images must be reachable at https URLs (the connector's upload link can provide them). Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-brand-consistent-images"
---

# Brand Consistent Images

Someone owns or works for a brand and wants new images that look like they came from that brand: the real logo, the real product, the house colors, the same light every time. You build the brand brief, write each image request, guard the spend and check the results. The Wireflow app `skill-brand-consistent-images` renders each image with Nano Banana Lite, reading up to three brand images as references.

## What the app takes

| Input key | What to send |
|---|---|
| `brand_image_1` | `https://` URL of the logo (or the single most important brand image). Send it on every run |
| `brand_image_2` | Optional `https://` URL: a product photo, packaging, or a second logo version |
| `brand_image_3` | Optional `https://` URL: a palette card, brand guideline page, or a past image whose style should carry over |
| `brand_brief` | Palette, light, surfaces, people rule, mood and what to avoid, up to 2,000 characters. Send the same text on every run of a set |
| `image_request` | This image only: use, scene, where the logo appears, any exact words in quotes, up to 2,000 characters |

Facts from the test run on 15 Oct 2026 and the Wireflow price list:

- One image per run, square, 1024x1024. The ratio is fixed at 1:1 because Nano Banana Lite's ratio is a setting the app cannot expose.
- 16 credits per image.
- About 15 seconds per image.
- A fixed rule block inside the app tells the model to copy the logo exactly, keep any product as photographed and add no words beyond the ones the request quotes.

Leaving an input out has side effects. Without `brand_image_1` or `image_request` the app uses its own saved demo (an invented candle brand called Tavrin), and the person pays for someone else's picture. Without `brand_brief` it falls back to "match the references". Leave slots 2 and 3 out when there is nothing to put there. They are saved empty, and the test showed an empty slot runs cleanly. Never send a placeholder URL.

## 1. Is Wireflow connected?

Look for tools ending in `run_app`, `get_execution`, `get_credit_balance`, `whoami`, `create_upload_link` and `get_upload_link`.

If they are missing, say so in one line and show how to connect:

- This plugin installed: run `/mcp`, pick `wireflow`, sign in.
- Claude Code without the plugin: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Claude Desktop: add a custom connector with the URL `https://www.wireflow.ai/api/mcp`.

Then hand over the free version and stop: fill in `reference/brand-brief.md` for their brand from what they tell you or from their website, and write three to six image requests from `reference/request-pack.md` that they can paste into any image tool that accepts reference images.

## 2. Gather the brand kit

Ask only for what is missing.

1. **Logo.** A clean file on a plain background, as large as they have. PNG or JPG. This always goes in `brand_image_1`.
2. **Product or packaging** (optional). One product, whole and in focus, on a plain background in even light. A blank label is fine: the request can put the logo on it.
3. **Style reference** (optional). A palette card, a page from their brand guidelines, or one past image they love. Pick the single most useful one; three images is the app's limit.
4. **Rights.** Confirm it is their brand or a client's. Do not take logos, products or photos of companies they have no right to use.

Turn every file into an `https://` URL:

- Already online: the direct image link (it should open as an image, not a web page).
- On their computer or phone: call `create_upload_link`, share the link (no login needed), wait for their word, then `get_upload_link` returns the file URL.
- No upload tools: ask for a public direct link.

## 3. Write the brand brief once

Fill the template in `reference/brand-brief.md`: palette as names plus hex codes, light, surfaces and materials, the people rule, mood words, and an avoid list. Read their website or the guideline image if they gave one, and show the brief back for a quick yes or edit. Keep it under about 600 characters. The same brief goes into every run of a set; that is what keeps image five looking like image one.

## 4. Plan the images

Write one `image_request` per image. Each one names:

- What it is for (Instagram post, ad, email header, website tile, product page).
- The scene: setting, surface, two or three props at most, light, camera angle.
- Where the logo shows: on the product label, on a sign, on a bag, on a card in the scene. The model paints it into the scene, so say where it sits physically. It is not a watermark.
- Exact words, if any, in double quotes. Short lines work best (two to four words).
- "The product from the product photo" rather than a new name for it.

Check the physics before you run: a lit candle needs its lid off; a poured drink needs an open bottle. Ask when unsure.

Every image comes back square. For 9:16 stories or 16:9 banners, say so up front: they can crop the square, or open the board in Wireflow and change the ratio there.

Ready-made requests for common uses (social post, flat lay, ad backdrop, seasonal, packaging close-up, lifestyle in use): `reference/request-pack.md`.

## 5. Quote, then wait

Call `whoami` and `get_credit_balance`. Show the list of images and the total in one line, for example: "4 images x 16 credits = 64 credits. Your balance: 1,240." If the balance is short, stop there. Nothing runs until the person says yes to that list at that price.

## 6. Run each approved image

```json
{
  "slug": "skill-brand-consistent-images",
  "inputs": {
    "brand_image_1": "https://.../logo.png",
    "brand_image_2": "https://.../product.jpg",
    "brand_brief": "<the approved brief>",
    "image_request": "<this image's request>"
  }
}
```

Call `run_app` with that shape, then poll `get_execution` every 5 seconds while the status is `PENDING`, `RUNNING` or `IN_PROGRESS`. On `FAILED`, `CANCELLED` or `TIMEOUT`, report the exact error for that image and carry on with the others only if the person agrees.

## 7. Check, save, report

Look at each result next to the brand images before calling it done:

- Logo: same mark, same letters in the same order, same colors? Small taglines under a wordmark can come out soft; say so.
- Product: same shape, proportions, material and label area?
- Palette and light: does it sit with the brief, or did a stray color creep in?
- Quoted words: spelled exactly, nothing extra added?

Name any drift plainly ("the tagline under the logo is blurry", "the jar is a little slimmer than yours"). A redo costs 16 credits and needs its own yes.

Save each file as `./wireflow-outputs/<YYYY-MM-DD>/brand-<short-name>.<ext>` with `curl -sSL -o` (or PowerShell `Invoke-WebRequest -OutFile`), keeping the extension from the CDN URL. Finish with the file paths, the CDN links and the credits used (balance before minus balance after).

Then offer:

- More images with the same brief and kit (one quote for the batch).
- The board in Wireflow, to change the ratio, add an upscaler or swap the model: `https://www.wireflow.ai/flow/cmv8xyt520006jr06o7pcfwqu?ref=skill-brand-consistent-images&utm_source=github&utm_medium=skill&utm_campaign=brand-consistent-images`

## Guardrails

- No spend without a yes to the exact images and the exact cost.
- Only brands the person owns or works for. No other companies' logos, products or trademarks in the kit or the requests.
- No invented claims, awards, prices, reviews or certifications in any image.
- No real people's faces taken from elsewhere.
- Keys and passwords never go into briefs, requests or files.
- If Wireflow refuses a run or a tool errors, quote the message and offer `send_feedback` if the tool exists.
