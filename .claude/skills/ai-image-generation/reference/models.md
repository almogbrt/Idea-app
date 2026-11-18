# Which image model for which job

Prices are Wireflow credits per image from Wireflow's public price list, checked on 8 October 2026 (1 credit = US$0.01). Prices and the model list change; inside Wireflow, `list_models` returns the current numbers.

This skill's app uses **Flux Pro Ultra** because its aspect ratio can be set per run. Every other model below is one node swap away on the app's board in Wireflow.

| Job | Good pick | Credits | Why |
|---|---|---|---|
| Photoreal scenes in any ratio | Flux Pro Ultra v1.1 | 19 | Up to 4 megapixels, strong photo realism, ratio from 21:9 to 9:21 |
| Newest Flux, many ratios | FLUX 3 Image | 15 | Black Forest Labs' current model, 14 aspect ratios |
| Readable text, posters, logos | Ideogram 4.5 | 19 | Accurate typography and layout |
| Text plus precise detail | GPT Image 2.5 Sunburst | 17 | Holds faces, fine geometry and small text |
| Fast drafts with good prompt following | GPT Image 2.5 Flare | 17 | Quick tier of GPT Image 2.5 |
| Editing a photo you already have | Nano Banana Lite | 16 | Cheap, fast image editing with a reference photo |
| Higher-end edits and text in image | Nano Banana Pro / Nano Banana 2.1 | 20 | Better detail and lettering than Lite |
| Design-style graphics, vector look | Recraft V4 | 13 | Clean design output and text |
| Cheap volume | Seedream 5 Lite, Imagen 4, Qwen Image | 10 | Good quality per credit |
| Rough ideas, lots of them | Flux Schnell | 1 per megapixel | Very cheap, lower quality |

## Rules of thumb

- **Draft cheap, finish good.** Explore ideas on a 10-credit model, then render the keeper on the model you trust.
- **Text in the image?** Pick Ideogram 4.5, GPT Image 2.5 or Nano Banana Pro. Flux Pro Ultra is weak at letters.
- **Need it bigger?** Upscale the keeper (Crystal Upscaler, 5 credits per megapixel) instead of generating at a huge size.
- **Need a transparent background?** Run the image through a background remover node (BiRefNet or Bria, 6 to 7 credits).
