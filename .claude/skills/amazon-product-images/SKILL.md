---
name: amazon-product-images
description: "AI Amazon product images in Claude Code and Claude with Seedream 5 Lite through Wireflow: a listing image set built from your real product photo. It plans the listing image stack (a main image draft on white, feature infographic, lifestyle, size and scale, detail close-up, what's in the box, how to use, comparison) and renders each slot as a 2048x2048 square, with the callout text spelled exactly as you give it. Shows the credit cost and waits for a yes, then saves the set to ./wireflow-outputs. Use when someone asks for Amazon listing images, Amazon product photos, a main image on white, a product infographic, A+ style images, or Etsy, Walmart or Shopify gallery images. Check Amazon's current main-image rules before using a generated image as the main image. Without the Wireflow connector it still writes the slot plan and copy. For loose lifestyle scenes use product-photography."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. The product photo must be reachable at an https URL. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-amazon-product-images"
---

# AI Amazon Product Images

A marketplace listing is a stack of images with jobs: the first one wins the click in search, the rest answer the buyer's questions before they scroll to the reviews. This skill plans that stack from the seller's real product photo and renders each slot with the Wireflow app `skill-amazon-product-images` (Seedream 5 Lite, 2048x2048).

## App facts

| Field | Detail |
|---|---|
| Slug | `skill-amazon-product-images` |
| `product_photo` | `https://` URL of the product photo. Send it on every call |
| `slot_brief` | One slot: what the image shows, layout, and any words, quoted exactly. Up to 2,000 characters |
| Built-in rules | Keep the product unchanged; add no badges, ratings, certifications or claims beyond the brief; spell words exactly as given |
| Output | One 2048x2048 image per call |
| Price | 10 credits per image on Wireflow's price list (8 Oct 2026); our two test images measured 10 and 13 |

If `product_photo` is left out, the app falls back to its saved demo serum bottle. Always pass the buyer's own photo.

## First: connection

You need tools ending in `run_app`, `get_execution`, `get_credit_balance` and `whoami`, plus `create_upload_link` and `get_upload_link` for local photos. Missing? Explain that rendering needs the Wireflow connector (plugin users: `/mcp`, choose `wireflow`, Authenticate; others: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`; Claude.ai: custom connector with that URL). Then deliver the free part: the slot plan, every slot brief and the callout copy from `reference/listing-slots.md`, ready to hand to a designer or any image tool. Stop there.

## Gather facts before pixels

Ask in one message, and accept "skip" for anything optional:

1. The product photo (URL or file). For a local file, use `create_upload_link`, then `get_upload_link` for the uploaded URL.
2. Product name and what it is in one line.
3. Three to five real features or specs for callouts (material, size, capacity, what's included). These go into images word for word, so they must be true and supplied by the seller. Never invent them.
4. Real dimensions or weight, if a size slot is wanted.
5. Who buys it and where it is used, for the lifestyle slot.

## Plan the stack

Propose up to eight slots and let the person drop any:

| # | Slot | Purpose |
|---|---|---|
| 1 | Main image (draft) | Product alone on white, about 85% of the frame, no text or props. A generated draft: the seller checks Amazon's main-image rules before using it |
| 2 | Feature infographic | Three to four callouts with lines or icons pointing at the product |
| 3 | Lifestyle | The product in use in the buyer's real setting |
| 4 | Size and scale | Dimension lines with real measurements, or next to a familiar object |
| 5 | Detail close-up | Material, texture, mechanism, finish |
| 6 | What's in the box | Flat lay of everything included, labelled |
| 7 | How to use | Three numbered steps |
| 8 | Comparison | This product's own versions or sizes side by side; never a competitor's brand |

Write each `slot_brief` from the matching template in `reference/listing-slots.md`. Put every word that should appear in the image in quotes, and keep text short: three to five words per callout.

## Approval

Call `whoami` and `get_credit_balance`. Show the slot list, the exact on-image text for each, and the total: "6 slots x about 10 credits = about 60 credits (allow up to 13 each). Balance: 820." Wait for a yes that covers those slots and that text. Changing a word later means a re-render.

## Render

One `run_app` call per slot:

```json
{ "slug": "skill-amazon-product-images", "inputs": { "product_photo": "https://...", "slot_brief": "Feature infographic: ... callouts, exactly: 'Frosted glass bottle', '30 ml / 1 fl oz'" } }
```

Poll `get_execution` every 5 seconds until it leaves `PENDING`, `RUNNING` and `IN_PROGRESS`. Usually 15 to 30 seconds. Stop on `FAILED`, `CANCELLED` or `TIMEOUT` and report the error.

Save as `./wireflow-outputs/<YYYY-MM-DD>/amazon-<nn>-<slot>.jpg` with `curl -sSL -o` or `Invoke-WebRequest -OutFile`, numbered in listing order.

## Check every slot before handing over

- **Main image**: background truly white, no shadows creeping into a grey haze, no text, no props, product large. Our test main image came out near-white with faint shading at the edges; say so if you see it and suggest fixing the background in an editor or a re-run.
- **Text slots**: read every word in the image and compare with the approved text. One wrong letter means a re-render (ask first).
- **Product fidelity**: same shape, color, cap, label as the photo.
- **Claims**: nothing on the image the seller did not supply.

## Main image: say this every time

Every slot is generated from the seller's real product photo. Slot 1 is a draft of a main image, not a promise that Amazon will accept it. Before the seller uses a generated image as the main image, tell them plainly to check Amazon's current main-image rules in Seller Central (Product image requirements: `https://sellercentral.amazon.com/help/hub/reference/external/G1881`). The rules differ by category and they change.

What Amazon's own seller guide says (`https://sell.amazon.com/blog/product-photos`, read 8 Oct 2026): "In most cases, product shots should be taken against a white background (RGB color values: 255, 255, 255)", "Have the product fill 85% or more of the frame", and all images must be "500 to 10,000 pixels on their longest side". That guide does not say whether a generated image may be used as the main image, so never tell the seller an image is compliant.

## Report and next steps

List the files in slot order, the CDN links, and credits used (balance before minus after). Offer:

- Variants of any slot (different lifestyle setting, alternative callout order).
- The board in Wireflow to swap the model or add a background remover for a perfectly white main image: `https://www.wireflow.ai/flow/cmuz2fc46000kl506irtbvyu2?ref=skill-amazon-product-images&utm_source=github&utm_medium=skill&utm_campaign=amazon-product-images`

## Never

- Spend before the yes, or re-render without asking.
- Put invented claims, awards, star ratings, review quotes, "best seller" badges or competitor brands into an image.
- Use photos the seller has no rights to.
- Put keys or passwords in briefs or files.
- Hide a Wireflow error: quote it, and offer `send_feedback` if available.
