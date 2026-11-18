# Wan 3.0 Ecommerce Product Video for Claude Code

| Start frame (your product photo) | Wan 3.0 clip with sound (click to play) |
|---|---|
| ![Start frame: a lit amber candle with a Tavrin label on a stone shelf](examples/start-frame-candle.jpg) | [![Wan 3.0 output: the candle clip mid push-in, click to play with sound](examples/candle-push-in-poster.jpg)](https://cdn.wireflow.ai/de09ddc0-c8f4-11f1-bb62-0520a10573d1.mp4) |

![Five frames across the Wan 3.0 candle clip](examples/candle-push-in-frames.jpg)

*Made with this skill on 16 Oct 2026: Wan 3.0, 5 seconds, 960x960 with sound, 58 credits. Brief, receipt and honest notes in [examples](examples/EXAMPLES.md).*

Make a Wan 3.0 ecommerce product video from a photo you already have, with the sound built in. Tell Claude what the product is; it writes one brief with a slow camera move and the sound that move would make (a wick crackling, a drink fizzing, steam rising), quotes the credits and waits for your yes. A Wireflow app runs Alibaba's Wan 3.0 with your photo as the first frame, and the MP4 lands in `./wireflow-outputs/`.

Without a Wireflow login you still get shot and sound briefs for your product.

## Try it

```text
Make a short product video with sound from this photo of my candle:
https://example.com/candle-on-shelf.jpg. Slow and cosy.
```

Other phrasings it answers: "Wan 3.0 video", "product video with sound", "ASMR product clip", "animate my product photo with audio".

## How to install

1. **Plugin for Claude Code** (brings the Wireflow connector along):

   ```text
   /plugin marketplace add wireflowINC/skills
   /plugin install wireflow-skills@wireflow
   ```

   Then `/mcp`, choose `wireflow`, sign in.

2. **skills CLI**, this skill only:

   ```bash
   npx skills add wireflowINC/skills --skill wan-3-0-product-video
   ```

3. **By hand**: copy `skills/wan-3-0-product-video` to `~/.claude/skills/`.

For options 2 and 3, add the connector: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`. In Claude.ai or Claude Desktop, add that URL as a custom connector. More in the [Wireflow MCP guide](https://www.wireflow.ai/docs/mcp?ref=skill-wan-3-0-product-video&utm_source=github&utm_medium=skill&utm_campaign=wan-3-0-product-video).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the video link instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Pricing

| Part | Credits |
|---|---|
| Shot and sound briefs, quote | None |
| Each clip (5 seconds, 720p, with sound) | 58 (Wan 3.0, our test run's charge, 16 Oct 2026) |
| A redo | The same again, after you approve it |

Wireflow is free to sign up, build and browse. Wan 3.0 needs a paid plan, from US$24 a month (1,600 credits). Nothing is spent without your yes.

## Good to know

- The clip takes your photo's shape: square in, square out. Use a vertical photo for Reels and TikTok.
- The sound is made with the picture, so it follows what moves: a flame, bubbles, steam. Quiet products in quiet rooms gain little from it.
- One slow move per clip keeps the label readable.

## Your data

- Your photo URL and the brief go to Wireflow through the Wireflow MCP connector (`run_app`), under your own account; local photos go up through the connector's upload link.
- The MP4 downloads from `cdn.wireflow.ai` to `./wireflow-outputs/`. If ffmpeg is installed, frames and a volume reading are taken locally.
- No API keys, no install scripts, no third-party services.

## FAQ

### What is Wan 3.0 and what is different about it?

Wan 3.0 is Alibaba's video model. It makes the picture and a matching sound track in one pass, starts from your photo as the first frame, and on Wireflow costs the same with or without sound. This skill uses it for 5 second product clips at 720p.

### How much does a clip cost?

58 Wireflow credits for one 5 second clip, the charge for our test run on 16 Oct 2026 (Wan 3.0 lists at 12 credits a second). The briefs and the quote are free, and nothing runs until you say yes.

### Do I need a Wireflow account?

Only to render. It runs on your own Wireflow account through the Wireflow MCP connector (OAuth sign-in, no API key), and Wan 3.0 needs a paid plan. Without it you still get shot and sound briefs to use in any tool.

### Will my product stay the same?

Your photo is the first frame, and the app carries fixed rules against changing the shape, label or logo and against extra products. Claude checks a strip of frames before handing the clip over. In our test the candle's label, logo, jar and lid stayed the same across all five seconds while the camera pushed in.

### Where are the files saved?

In `./wireflow-outputs/<date>/` inside the folder where Claude Code is running.

## Contents

- `SKILL.md`: the procedure.
- `reference/shot-and-sound.md`: how to write a shot and sound brief, ten briefs by product type and a three-clip plan for a product page.
- `examples/`: the real start frame, clip poster and frames from the test run, with the exact inputs.

Built on the [Wireflow AI video workflow](https://www.wireflow.ai/features/ai-video-workflow?ref=skill-wan-3-0-product-video&utm_source=github&utm_medium=skill&utm_campaign=wan-3-0-product-video). MIT licensed; rendering runs on Wireflow and uses your credits.
