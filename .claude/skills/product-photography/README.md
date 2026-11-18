# AI Product Photography for Claude Code

| Your photo | Lifestyle | Flat lay |
|---|---|---|
| ![Input: candle jar packshot](examples/input-candle-packshot.jpg) | ![Output: candle on a bedside table](examples/candle-lifestyle.jpg) | ![Output: candle in a flat lay with eucalyptus](examples/candle-flat-lay.jpg) |

*One product photo in, new scenes out. Made with this skill on 8 Oct 2026: Nano Banana Lite, 16 credits per scene. Scene text, receipts and honest notes in [examples](examples/EXAMPLES.md).*

Hand Claude a single product photo and get it back on clean white for your store, in a real room, held in a hand, laid out from above, outdoors or on a bold color backdrop. The skill picks the scenes, writes each one so the model keeps your product's shape, colors and label, quotes the credits and waits for your go. A Wireflow app (Nano Banana Lite) renders each scene, and Claude checks every result against your original before calling it done.

Without a Wireflow login you still get a photo checklist and a filled-in scene prompt pack for your product.

## Try it

```text
Here's my product photo: https://example.com/my-mug.jpg
Give me a white-background shot for Shopify, a lifestyle shot on a kitchen
counter and one held in a hand.
```

Other phrasings it answers: "AI product photography", "put my product in a scene", "packshot", "Amazon product images", "lifestyle photos of this".

## How to install

1. **Plugin for Claude Code** (brings the Wireflow connector along):

   ```text
   /plugin marketplace add wireflowINC/skills
   /plugin install wireflow-skills@wireflow
   ```

   Then `/mcp`, choose `wireflow`, sign in.

2. **skills CLI**, this skill only:

   ```bash
   npx skills add wireflowINC/skills --skill product-photography
   ```

3. **By hand**: copy `skills/product-photography` to `~/.claude/skills/`.

For options 2 and 3, add the connector: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`. In Claude.ai or Claude Desktop, add that URL as a custom connector. More in the [Wireflow MCP guide](https://www.wireflow.ai/docs/mcp?ref=skill-product-photography&utm_source=github&utm_medium=skill&utm_campaign=product-photography).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the image links instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Pricing

| Part | Credits |
|---|---|
| Photo check, scene choice, scene prompts, quote | None |
| Each finished scene | 16 (Nano Banana Lite, price checked 8 Oct 2026) |
| Six-scene set | 96 |
| Redo of a scene | 16, after you approve it |

Wireflow is free to sign up, build and browse, with a first image on the house once setup is done. After that, generating needs a paid plan from US$24 a month (1,600 credits, about 100 scenes at this price). Nothing is spent without your yes.

## Your photo and your data

- Your product photo URL and scene descriptions go to Wireflow through the Wireflow MCP connector (`run_app`), under your own account.
- For a local photo, the connector can create an upload link you open on your phone or computer (`create_upload_link`); the file goes to your Wireflow account.
- Results download from `cdn.wireflow.ai` to `./wireflow-outputs/`.
- No API keys, no install scripts, no third-party services.

## FAQ

### Will it change how my product looks?

It is built not to. The Wireflow app carries a fixed rule to keep the shape, colors, label, logo and text as photographed, and Claude compares every result with your photo. Models still drift sometimes: in our test the lid came out looking a little more like cork than in the input photo. The skill tells you when that happens, and a redo is 16 credits after your yes.

### Can I use the white background shot as my Amazon main image?

Check Amazon's current main image rules in Seller Central first. These are generated scenes built from your photo, and the skill does not check any marketplace's rules for you.

### How much does each scene cost?

16 Wireflow credits per scene with Nano Banana Lite (price checked 8 Oct 2026), so the six-scene set is 96. The photo check, scene choice and quote are free.

### Do I need a Wireflow account?

Only to generate. Scenes render on your own Wireflow account through the Wireflow MCP connector (OAuth sign-in, no API key). Without it you still get the photo checklist and a scene prompt pack for your product.

### Where do the photos end up?

In `./wireflow-outputs/<date>/`, one file per scene, named after the scene. You also get the Wireflow CDN link for each.

## Contents

- `SKILL.md`: the procedure.
- `reference/scene-pack.md`: six scene templates, props by product category, seasonal swaps.
- `reference/photo-checklist.md`: how to shoot the input photo on a phone.
- `examples/`: real before and after images with their scene text.

Built on the [Wireflow AI workflow builder](https://www.wireflow.ai/ai-workflow-builder?ref=skill-product-photography&utm_source=github&utm_medium=skill&utm_campaign=product-photography). MIT licensed; image generation runs on Wireflow and uses your credits.
