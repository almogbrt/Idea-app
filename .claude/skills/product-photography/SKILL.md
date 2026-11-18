---
name: product-photography
description: "AI product photography in Claude Code and Claude with Nano Banana Lite through Wireflow: turn one product photo into studio and lifestyle shots. Picks scenes (clean white background, lifestyle, in hand, flat lay, outdoor, colored studio backdrop, seasonal), keeps the product itself unchanged, shows the credit cost and waits for a yes, then runs a published Wireflow app and saves the photos to ./wireflow-outputs. Use when someone asks for AI product photography, product photos, packshots, e-commerce, Shopify or Amazon product images, lifestyle shots, or to put a product in a new scene or background. Without the Wireflow connector it still writes a scene prompt pack and a photo checklist. Needs a photo of a real product; for images from text alone use ai-image-generation."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. The product photo must be reachable at an https URL (the connector's upload link can provide one). Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-product-photography"
---

# AI Product Photography

The person has one photo of a product. They want it shot in scenes they never set up: on white for a listing, on a kitchen counter, in a hand, from above on linen. The Wireflow app `skill-product-photography` does the rendering with Nano Banana Lite. You choose the scenes, protect the product's look, keep spending under control and file the results.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-product-photography` |
| `product_photo` | `https://` URL of the product photo (required on every run) |
| `scene` | Where and how to show the product, up to 2,000 characters |
| Fixed inside the app | A rule block telling the model to keep shape, colors, label, logo and text exactly as photographed |
| Output | One image per run. The ratio is set to auto, so it follows the input photo (a square input gave 1024x1024 in our test) |
| Price | 16 credits per image (Wireflow price list, 8 Oct 2026) |

Always send `product_photo`. If it is left out, the app falls back to its own saved demo product, and the person pays for a photo of someone else's candle.

## A. Connection check

Search your tools for names ending in `run_app`, `get_execution`, `get_credit_balance`, `whoami`, `create_upload_link` and `get_upload_link`.

Not connected? Explain in one sentence, then:

- With this plugin: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: custom connector, URL `https://www.wireflow.ai/api/mcp`.

Then give the free deliverable: the photo checklist from `reference/photo-checklist.md` and a scene prompt for each of the six standard scenes in `reference/scene-pack.md`, filled in for their product. Stop.

## B. Get the photo in

1. Ask for the product photo if you do not have it. One product, whole and in focus, plain background preferred. Check it against `reference/photo-checklist.md` and say what would improve it, but do not block on small issues.
2. Turn it into an `https://` URL:
   - Already online: use the direct image link.
   - Local file: call `create_upload_link`, give the person the link (it works on a phone, no login), and when they confirm, call `get_upload_link` and take the uploaded file's URL.
   - No upload tools: ask for a public link (cloud drive direct link, store CDN image).
3. Write down what the product is in a few words (for example "amber glass candle jar, oak lid, cream band label"). You will reuse it in every scene so the model does not reinterpret it.

## C. Choose scenes

Default set of six; offer it and let the person cut it down:

1. **White background**: pure white seamless, soft shadow. Marketplace main image.
2. **Lifestyle**: in its natural room or setting, in use if that makes sense.
3. **In hand**: held by a hand that suits the buyer, cropped at the wrist.
4. **Flat lay**: top-down on a textured surface with a few props that fit the brand.
5. **Outdoor or context**: where the product is used outside (beach, trail, desk, gym).
6. **Colored backdrop**: bold single-color studio set with a hard shadow, for ads.

Write each `scene` input as: the setting, the surface the product stands on, the light, two or three props at most, the camera angle. Say "the product" rather than renaming it, and add the short description from B.3. Physical logic matters: a candle shown burning needs its lid off; a bottle being poured needs its cap off. Ask if unsure.

Templates and props per category (beauty, food and drink, apparel, electronics, home): `reference/scene-pack.md`.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`, then show the scene list with the total: "4 scenes x 16 credits = 64 credits. Balance: 900." Short balance: stop and say so. Nothing runs until the person says yes to that list and that cost.

## E. Generate

Call `run_app` for each approved scene:

```json
{ "slug": "skill-product-photography", "inputs": { "product_photo": "https://...", "scene": "<scene text>" } }
```

Poll `get_execution` every 5 seconds until the status leaves `PENDING`, `RUNNING` and `IN_PROGRESS`. A scene usually takes under 15 seconds. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop that scene and report the error.

## F. Inspect, save, report

Save each result as `./wireflow-outputs/<YYYY-MM-DD>/product-<scene-name>.<ext>` using `curl -sSL -o` or PowerShell `Invoke-WebRequest -OutFile`. Keep the extension from the URL.

Compare every result with the original photo before you call it done:

- Same silhouette and proportions?
- Same colors and materials?
- Label, logo and printed text intact, not rewritten?
- Believable scale against the props and hands?

Flag any drift plainly ("the lid came out cork instead of oak"). A redo is another 16 credits and needs a yes.

Close with the saved files, the CDN links and the credits used (balance before minus after). Offer:

- The same scenes for another product (one quote for the batch).
- The board in Wireflow, to add an upscaler or a background remover: `https://www.wireflow.ai/flow/cmuyrxf720005nz069nu7y39w?ref=skill-product-photography&utm_source=github&utm_medium=skill&utm_campaign=product-photography`

## Guardrails

- Spend only after a yes to the exact scenes and cost.
- Do not invent product claims, certifications, prices or reviews in any scene.
- Use only photos the person has the right to use. No real people's faces from other sources.
- Keep keys and passwords out of prompts and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
