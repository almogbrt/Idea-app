# Real runs

Two listing slots rendered by this skill's Wireflow app (`skill-amazon-product-images`, Seedream 5 Lite, 2048x2048) on 8 October 2026. Files here are downscaled; originals are on the Wireflow CDN.

## Input photo

![Frosted serum bottle on a stone ledge](input-serum-photo.jpg)

An unbranded serum bottle photographed in a lifestyle setting (itself generated in Wireflow earlier): https://cdn.wireflow.ai/9d3be4a0-c2a0-11f1-a0d0-9fb19b0b815f.png

## Slot 1: main image

![Serum bottle on white](slot1-main-image.jpg)

- `slot_brief`: Main image: the frosted glass serum bottle with its white dropper cap alone, upright, centered on a pure white background (RGB 255,255,255), filling about 85% of the frame, soft even studio light, a gentle contact shadow, no text, no props, no plants, no stone.
- Output: https://cdn.wireflow.ai/e7ce0550-c2d4-11f1-9e92-2dd4e060cd9a.jpg
- Execution: `65d11170-0899-4a47-9468-2b00b5c93862`
- Credits: 10
- Honest note: the background is near-white with faint shading at the top left, not a flat RGB 255 white, and the bottle fills less than 85% of the frame. Fine for a draft; for upload, whiten the background or re-run with a stronger brief.

## Slot 2: feature infographic

![Infographic with three callouts](slot2-feature-infographic.jpg)

- `slot_brief`: Feature infographic: the serum bottle on the right half against a soft warm off-white background, with three short callouts on the left, each with a thin line pointing to the bottle and a simple outline icon. Callout text, exactly: 'Frosted glass bottle', '30 ml / 1 fl oz', 'Precise dropper'. Clean sans-serif type in dark grey, generous spacing, no other words.
- Output: https://cdn.wireflow.ai/09752210-c2d5-11f1-8393-3d6c9b57c1f8.jpg
- Execution: `0664a94d-1a49-49f5-8c3e-82d0dd8a29fe`
- Credits: 13 (account balance before minus after; the list price is 10, so 3 credits may be other account activity)
- Honest note: all three callouts are spelled exactly right. The right half kept the original stone-and-plant scene instead of the off-white background asked for.

Both runs above used the Wireflow Apps API (`POST /api/v1/apps/skill-amazon-product-images/execute`), the same code path as the MCP `run_app` tool.

## Fresh Claude session over MCP

A new headless Claude Code session with this skill installed and the Wireflow connector signed in rendered slot 1 again through `run_app`, with the approval given up front: execution `8fa65304-59b2-4321-bc0e-ad6bb2915847`, output https://cdn.wireflow.ai/7219d9d0-c2d7-11f1-9e92-2dd4e060cd9a.jpg, 10 credits (balance 4,549 to 4,539). The session flagged the same near-white background (edge pixels 242 to 255) and recommended fixing it before upload.
