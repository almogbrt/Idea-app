# Brand Consistent AI Images for Claude Code

| Shelf post | Flat lay | The logo it was given |
|---|---|---|
| ![Tavrin candle lit on a stone bathroom shelf](examples/tavrin-bathroom-shelf.jpg) | ![Tavrin candle flat lay with a Slow evenings card](examples/tavrin-flat-lay-card.jpg) | ![Input: Tavrin arch and flame logo](examples/input-tavrin-logo.jpg) |

*A logo, a blank product photo and a palette card in, on-brand images out. Made with this skill on 15 Oct 2026: Nano Banana Lite, 16 credits per image. Inputs, receipts and honest notes in [examples](examples/EXAMPLES.md).*

Brand consistent AI images from Claude: give it your logo, a product photo and your colors, and every image comes back with the same mark, the same product and the same look. Claude writes a short brand brief once, plans each image (the scene, where the logo sits, any exact words), quotes the credits and waits for your go. A Wireflow app renders each one with Nano Banana Lite, reading up to three of your brand images as references, and Claude checks the logo and product against your originals before saving the files.

Without a Wireflow login you still get a filled-in brand brief and a set of on-brand image requests for any tool that takes reference images.

## Try it

```text
Here's our logo: https://example.com/logo.png and our best seller:
https://example.com/jar.jpg. Our colors are deep red, amber and cream.
Make three Instagram posts for the autumn launch that look like us.
```

Other phrasings it answers: "make on-brand images", "images that match our brand kit", "keep our logo on every image", "a consistent set for our ads", "put our logo on the product shot".

## How to install

1. **Plugin for Claude Code** (brings the Wireflow connector along):

   ```text
   /plugin marketplace add wireflowINC/skills
   /plugin install wireflow-skills@wireflow
   ```

   Then `/mcp`, choose `wireflow`, sign in.

2. **skills CLI**, this skill only:

   ```bash
   npx skills add wireflowINC/skills --skill brand-consistent-images
   ```

3. **By hand**: copy `skills/brand-consistent-images` to `~/.claude/skills/`.

For options 2 and 3, add the connector: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`. In Claude.ai or Claude Desktop, add that URL as a custom connector. More in the [Wireflow MCP guide](https://www.wireflow.ai/docs/mcp?ref=skill-brand-consistent-images&utm_source=github&utm_medium=skill&utm_campaign=brand-consistent-images).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the image links instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Pricing

| Part | Credits |
|---|---|
| Brand brief, image plans, quote | None |
| Each finished image | 16 (Nano Banana Lite, price checked 15 Oct 2026) |
| A set of six | 96 |
| A redo of one image | 16, after you approve it |

Wireflow is free to sign up, build and browse, with a first image on the house once setup is done. After that, generating needs a paid plan from US$24 a month (1,600 credits, about 100 images at this price). Nothing is spent without your yes.

## Your brand files and your data

- Your logo, product photo and style reference (as `https://` links), the brand brief and each image request go to Wireflow through the Wireflow MCP connector (`run_app`), under your own account.
- For files on your computer, the connector can make an upload link you open on any device (`create_upload_link`); the files go to your Wireflow account.
- Results download from `cdn.wireflow.ai` to `./wireflow-outputs/`.
- No API keys, no install scripts, no third-party services.

## FAQ

### Will it copy my logo exactly?

It is built to. The app sends your logo as a reference image with a fixed rule to copy it exactly, and Claude compares every result with your file. In our test the mark and the wordmark came through cleanly, but the small tagline under the wordmark came out soft. Claude flags that kind of drift, and a redo is 16 credits after your yes.

### How much does each image cost?

16 Wireflow credits per image with Nano Banana Lite (price checked 15 Oct 2026). Writing the brand brief, planning the images and the quote are free.

### Do I need a Wireflow account?

Only to generate. Images render on your own Wireflow account through the Wireflow MCP connector (OAuth sign-in, no API key). Without it you still get the brand brief and the image requests.

### Which model does it use, and what size are the images?

Nano Banana Lite, with up to three of your images as references (logo, product, palette or style). Every image is square, 1024x1024. For stories or banners, crop the square or open the board in Wireflow and change the ratio there.

### Where are the images saved?

In `./wireflow-outputs/<date>/` inside the folder where Claude Code is running, one file per image, plus the Wireflow CDN link for each.

## Contents

- `SKILL.md`: the procedure.
- `reference/brand-brief.md`: the brand brief template with a worked example, useful in any image tool.
- `reference/request-pack.md`: six on-brand image request shapes (social post, flat lay, ad backdrop, seasonal, close-up, lifestyle).
- `examples/`: real runs with the exact brand images, brief, requests and receipts.

Built on [Wireflow's AI workflow canvas](https://www.wireflow.ai/features/best-node-based-ai-workflow-platform?ref=skill-brand-consistent-images&utm_source=github&utm_medium=skill&utm_campaign=brand-consistent-images). MIT licensed; image generation runs on Wireflow and uses your credits.
