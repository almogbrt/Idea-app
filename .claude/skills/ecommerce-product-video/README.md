# AI Ecommerce Product Video for Claude Code

| First frame (product photo) | Result (click to play) |
|---|---|
| ![Input: serum bottle on white, used as the first frame](examples/input-first-frame.jpg) | [![Output: the serum bottle mid-orbit, click to play the clip](examples/serum-orbit-poster.jpg)](https://cdn.wireflow.ai/250a9870-c2d5-11f1-9e92-2dd4e060cd9a.mp4) |

![Six frames across the clip](examples/serum-orbit-frames.jpg)

*Made with this skill on 8 Oct 2026: MiniMax Hailuo 03 Max Turbo, half orbit, 6.6 seconds, 48 credits. Brief and receipt in [examples](examples/EXAMPLES.md).*

Make an AI product video for ecommerce from a photo you already have. Your product photo becomes the first frame of a short, calm product clip: a slow orbit, a light sweep over the material, a push-in on the label, a turntable spin. Claude picks a move that suits the product, writes a brief that keeps the product unchanged, quotes the credits and waits for your yes. A Wireflow app renders the clip and Claude checks a strip of frames for warping or label changes before handing it over.

Without Wireflow connected you still get motion briefs and a shot plan you can use in any image-to-video tool.

## Try it

```text
Make a product video for my Shopify page from this photo:
https://example.com/bottle-on-white.jpg. Something premium, a slow orbit.
```

Also triggered by: "product video", "animate my product photo", "360 spin video", "video ad from a product image", "Amazon product video".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

Installs all Wireflow skills and the connector; then `/mcp` → `wireflow` → sign in.

Single skill: `npx skills add wireflowINC/skills --skill ecommerce-product-video`, or copy `skills/ecommerce-product-video` into `~/.claude/skills/`, then `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (Claude.ai and Desktop: custom connector with that URL).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the video link instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Cost

| Item | Credits |
|---|---|
| Motion plan, briefs, quote | 0 |
| One clip (about 6.5 s, 768P) | 48 in our test (8 per second, Wireflow list price, 8 Oct 2026) |
| A three-clip set (hero, detail, in use) | About 144 |

Wireflow's Free plan is for building and browsing, with a first image after setup; video needs a paid plan, from US$24 a month.

## Good to know

- The clip takes the shape of your photo. Square in, square out; use a vertical photo for Reels and TikTok.
- One slow move per clip looks most premium and keeps the product stable.
- The model adds an audio track. Mute it or add music in your editor.

## What it sends and fetches

- Your photo URL and motion brief go to Wireflow over the Wireflow MCP connector (`run_app`), signed in as you; local photos go up through the connector's upload link.
- The MP4 downloads from `cdn.wireflow.ai` to `./wireflow-outputs/`. If ffmpeg is installed, frames are pulled locally for the check.
- No keys, no scripts, no other services.

## FAQ

### How long is the video, and what shape?

About 6.5 seconds at 768P. The shape follows your photo: a square photo gave a 768x768 clip in our test. For a vertical clip for Reels or TikTok, start from a vertical photo.

### Does the clip have sound?

Yes, the model adds an audio track. For store pages and most ads, mute it or replace it with music in your editor.

### Can I use it on Shopify or Amazon?

You get a standard MP4 file. Check your store's or marketplace's current video requirements (length, shape, file size) before you upload; the skill does not check them for you.

### What does a product video cost?

48 Wireflow credits per clip in our test (MiniMax Hailuo 03 Max Turbo, 8 credits a second, 8 Oct 2026). The motion plan and the quote are free.

### Will my product stay the same in the video?

That is what the skill is built around. Your photo is the first frame, the app carries a fixed rule against morphing or extra products, and Claude checks a strip of frames for label or shape changes. In our test the bottle shape and cap stayed stable.

## Contents

- `SKILL.md`: the procedure.
- `reference/product-motion.md`: six motion briefs, a category table and a product-page shot plan.
- `examples/`: the real first frame, clip poster and frames.

Powered by the [Wireflow AI video workflow](https://www.wireflow.ai/features/ai-video-workflow?ref=skill-ecommerce-product-video&utm_source=github&utm_medium=skill&utm_campaign=ecommerce-product-video). More on [node-based video generation](https://www.wireflow.ai/node-based-video-generation?ref=skill-ecommerce-product-video&utm_source=github&utm_medium=skill&utm_campaign=ecommerce-product-video). MIT licensed; clips use your Wireflow credits.
