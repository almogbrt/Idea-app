---
name: ai-fashion-model-photos-for-ecommerce
description: "AI fashion model photos for ecommerce in Claude Code and Claude with Nano Banana Lite through Wireflow: put a garment photo on an AI model. From one flat-lay or ghost-mannequin photo it writes a model brief (age, look, hair, expression, shoes) and a lifestyle setting, quotes the credits and waits for a yes, then renders a store-ready on-model set in one call: a front shot and a 3/4 shot on a grey studio backdrop plus one lifestyle shot, with the garment kept as photographed, and saves them to ./wireflow-outputs. Use when someone asks for on-model photos, virtual models for clothing, a model shot from a flat lay, apparel catalog images, store clothing photos without a photoshoot, or the same garment on different models. Without the Wireflow connector it still writes a model brief pack and a garment photo checklist. For a product shown alone in a scene use product-photography."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. The garment photo must be reachable at an https URL (the connector's upload link can provide one). Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-fashion-model-photos-for-ecommerce"
---

# AI Fashion Model Photos for Ecommerce

A clothing seller has the garment photographed flat on a table or on a ghost mannequin, and no budget or time for a model shoot. You (Claude) plan who wears it and where; the Wireflow app `skill-ai-fashion-model-photos-for-ecommerce` dresses a generated model in that exact garment and returns three catalog shots in one call with Nano Banana Lite. Your job is to keep the garment honest, keep spending under the person's control and file the results.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-fashion-model-photos-for-ecommerce` |
| `garment_photo` | `https://` URL of one garment, flat lay or ghost mannequin (required on every run) |
| `model` | Who wears it: age range, look, hair, expression, plus plain shoes or bottoms if the outfit needs them. Up to 2,000 characters |
| `lifestyle_setting` | Place, light and mood for the third shot. Up to 2,000 characters |
| Fixed inside the app | A rule block that keeps cut, length, color, fabric, collar, buttons, pockets, seams, trims and prints as photographed; shot 1 full-length front and shot 2 full-length 3/4, both on a plain light grey seamless backdrop; shot 3 a candid lifestyle pose in the setting |
| Output | Three 3:4 JPEGs (896x1200 in our test): `front`, `three-quarter`, `lifestyle` |
| Price | 48 credits per run, 16 per image (Nano Banana Lite, measured 15 Oct 2026) |

Always send all three inputs. A missing one falls back to the board's saved demo (a sage green shirt dress, a curly-haired model, a cobblestone street), and the person pays for photos of someone else's dress.

## A. Connection check

Look for tools ending in `run_app`, `get_execution`, `get_credit_balance`, `whoami`, `create_upload_link` and `get_upload_link`.

If they are missing, say so in one sentence and give the setup:

- With this plugin: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: custom connector, URL `https://www.wireflow.ai/api/mcp`.

Then still deliver the free part from `reference/model-brief-pack.md`: the garment photo checklist, a filled-in model brief and three shot prompts for their garment that work in any image editor that takes a reference photo. Stop there.

## B. Get the garment in

1. Ask for the garment photo if you do not have it. One garment, whole, flat or on a ghost mannequin, front side up, even light, true color. Check it against the checklist in `reference/model-brief-pack.md` and say what would help, but do not block on small issues.
2. Make it an `https://` URL:
   - Already online: the direct image link.
   - Local file: call `create_upload_link`, give the person the link (works on a phone, no login), and once they confirm, call `get_upload_link` and use the file's URL.
   - No upload tools: ask for a public direct link (store CDN, cloud drive direct link).
3. Note the garment's details in one line (for example "sage shirt dress, point collar, seven white buttons, chest pocket, tie belt, tab cuffs"). You will check every result against this line.

## C. Plan the model and the setting

Ask once, in one message: who the buyer is, the look of the store (studio, street, beach, office), and any model the brand already uses in its photos (described in words, never a real person's name or photo).

Then write:

- **Model**: age range, build, skin tone, hair, expression, and the plain items that complete the outfit (white sneakers, straight dark jeans). Keep extras neutral so the garment stays the focus. Templates in `reference/model-brief-pack.md`.
- **Lifestyle setting**: place, time of day, light, one or two background details, kept simple enough that the whole garment stays visible.

Show both as a short table and let the person edit any word. For the same garment on several models (size inclusive range, different looks), plan one run per model.

The app takes one garment per run. Tops worn with bottoms the person also sells need two runs or a description of the bottoms in the model brief; say that the described piece is generated, not their product.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`, then: "1 run x 48 credits = 48 credits for 3 on-model photos. Balance: 1,240." For several models or garments, multiply and show the total. Short balance: stop and say so. Nothing runs until the person says yes to this plan and this cost.

## E. Generate

One `run_app` per garment and model:

```json
{ "slug": "skill-ai-fashion-model-photos-for-ecommerce", "inputs": { "garment_photo": "https://...", "model": "<model brief>", "lifestyle_setting": "<setting>" } }
```

Poll `get_execution` every 5 seconds until the status is no longer `PENDING`, `RUNNING` or `IN_PROGRESS`. Our test run took about 20 seconds. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop and quote the error.

## F. Inspect, save, report

Save each image as `./wireflow-outputs/<YYYY-MM-DD>/fashion/<garment-slug>_<model-slug>_<shot>.jpg` with `curl -sSL -o` or PowerShell `Invoke-WebRequest -OutFile`. Keep the extension from the URL.

Compare every shot with the garment photo and the detail line from B.3 before calling it done:

- Same color, fabric look and print?
- Same collar, buttons (count them when they show), pockets, cuffs, belt and trims?
- Same length and fit? Models often wear a dress shorter or a shirt looser than the flat lay suggests.
- Nothing added: no extra logos, bags, jackets or jewelry the brief did not ask for.
- Hands, feet and faces look natural.

Flag every miss per file ("the lifestyle shot added a brown shoulder bag"). A redo is a new run, 48 credits, after a yes.

Finish with a table (file, shot, CDN link) and the credits used (balance before minus after). Offer:

- The same garment on another model, or the same model in the next garment (one quote for the batch).
- The board in Wireflow, to change the backdrop, the ratio or add a background remover: `https://www.wireflow.ai/flow/cmv93h2qp0003la06264bhke2?ref=skill-ai-fashion-model-photos-for-ecommerce&utm_source=github&utm_medium=skill&utm_campaign=ai-fashion-model-photos-for-ecommerce`

## Guardrails

- Spend only after a yes to the exact plan and cost.
- Generated models only. Never make a real, identifiable person (celebrity, influencer, employee) wear the garment unless it is the person themselves and they asked.
- Use only garment photos the person has the right to use.
- Do not invent fabric claims, sizes, certifications or prices in any image or caption.
- Some marketplaces and countries have rules on AI-generated people in listings and ads. Tell the person to check theirs; do not promise compliance.
- Keep keys and passwords out of prompts and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
