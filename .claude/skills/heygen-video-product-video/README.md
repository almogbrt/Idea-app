# HeyGen Video Ecommerce Product Video for Claude Code

| Product photo (Picture 1) | HeyGen Video presenter clip (click to play) |
|---|---|
| ![Product photo: a frosted serum bottle with a white dropper on white](examples/product-serum.jpg) | [![HeyGen Video output: a presenter holding the serum bottle, click to play with sound](examples/presenter-serum-poster.jpg)](https://cdn.wireflow.ai/e4aa6130-c8f5-11f1-bb62-0520a10573d1.mp4) |

![Eight frames across the HeyGen Video presenter clip](examples/presenter-serum-frames.jpg)

*Made with this skill on 16 Oct 2026: HeyGen Video, 8 seconds, 9:16, 72 credits. Note the label: our bottle was plain and HeyGen printed a made-up one. Script, receipt and honest notes in [examples](examples/EXAMPLES.md).*

Make a HeyGen video ecommerce product video with a presenter who holds your product and talks about it. Send Claude a product photo; it writes a short script with one true detail, describes an AI presenter and a setting, quotes the credits and waits for your yes. A Wireflow app runs HeyGen Video with your photo as the product reference and saves an 8 second vertical MP4, voice included, to `./wireflow-outputs/`.

Without a Wireflow login you still get presenter scripts and a casting brief you can film yourself.

## Try it

```text
Make a short presenter video for my serum from this photo:
https://example.com/serum-on-white.jpg. A friendly woman in a bright bathroom, one line about how it's used.
```

Other phrasings it answers: "HeyGen product video", "AI spokesperson video for my product", "talking product demo", "presenter holding my product".

## How to install

1. **Plugin for Claude Code** (brings the Wireflow connector along):

   ```text
   /plugin marketplace add wireflowINC/skills
   /plugin install wireflow-skills@wireflow
   ```

   Then `/mcp`, choose `wireflow`, sign in.

2. **skills CLI**, this skill only:

   ```bash
   npx skills add wireflowINC/skills --skill heygen-video-product-video
   ```

3. **By hand**: copy `skills/heygen-video-product-video` to `~/.claude/skills/`.

For options 2 and 3, add the connector: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`. In Claude.ai or Claude Desktop, add that URL as a custom connector. More in the [Wireflow MCP guide](https://www.wireflow.ai/docs/mcp?ref=skill-heygen-video-product-video&utm_source=github&utm_medium=skill&utm_campaign=heygen-video-product-video).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the video link instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Pricing

| Part | Credits |
|---|---|
| Scripts, presenter brief, quote | None |
| Each clip (8 seconds, 9:16, 768p, with voice) | 72 (HeyGen Video, charged on both test runs, 16 Oct 2026) |
| A new take | The same again, after you approve it |

Wireflow is free to sign up, build and browse. HeyGen Video needs a paid plan, from US$24 a month (1,600 credits). Nothing is spent without your yes.

## Good to know

- You do not need a HeyGen account or a HeyGen avatar: the presenter is described in words and made fresh each run.
- The presenter is AI-made. Label it where ad platforms ask, and never present it as a customer review.
- Eight seconds fits about 15 to 20 spoken words. Longer scripts get rushed.
- HeyGen Video may add a label to a product that has none. Use a photo that shows your real label, and check every take.

## Your data

- Your photo URL, the presenter brief and the script go to Wireflow through the Wireflow MCP connector (`run_app`), under your own account; local photos go up through the connector's upload link.
- The MP4 downloads from `cdn.wireflow.ai` to `./wireflow-outputs/`. If ffmpeg is installed, frames are pulled locally for the check.
- No API keys, no install scripts, no third-party services.

## FAQ

### Can Claude make a HeyGen video of someone presenting my product?

Yes, with the Wireflow connector. Claude writes the script and the presenter brief, and a Wireflow app runs HeyGen Video, HeyGen's own video model, with your product photo as the reference. You get an 8 second vertical clip with the presenter's voice. In our tests the presenter, the bottle's shape, cap and colour held steady, but HeyGen printed a made-up label on our plain bottle, so check the label before you use a take.

### How much does it cost?

72 Wireflow credits per 8 second clip, charged on both test runs on 16 Oct 2026. That is more than Wireflow's price list suggests (5 credits a second), so the skill quotes the real charge. Scripts and the quote are free, and nothing runs until you say yes.

### Do I need a HeyGen or Wireflow account?

No HeyGen account: HeyGen Video runs inside Wireflow. You need a Wireflow account on a paid plan, connected through the Wireflow MCP connector (OAuth sign-in, no API key). Without it you still get scripts and a casting brief.

### Can I use my own face or a real spokesperson?

Not with this skill. It makes a new AI presenter from a written description and does not clone anyone's face or voice.

### Where are the files saved?

In `./wireflow-outputs/<date>/` inside the folder where Claude Code is running.

## Contents

- `SKILL.md`: the procedure.
- `reference/presenter-scripts.md`: script length and structure, seven script patterns, casting notes and product-to-presenter pairings.
- `examples/`: the real product photo, clip poster and frames from the test run, with the exact inputs.

Built on the [Wireflow AI video workflow](https://www.wireflow.ai/features/ai-video-workflow?ref=skill-heygen-video-product-video&utm_source=github&utm_medium=skill&utm_campaign=heygen-video-product-video). MIT licensed; rendering runs on Wireflow and uses your credits.
