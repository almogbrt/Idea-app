# AI Video Generation for Claude Code

[![A paper boat drifting on a neon-lit puddle at night, made with this skill](examples/paper-boat-poster.jpg)](https://cdn.wireflow.ai/e95405b0-c2ab-11f1-81b3-8fc0dc6bd2a6.mp4)

*Click to play. Made with this skill on 8 Oct 2026: MiniMax Hailuo 03 Max Turbo, text to video, 5 seconds, 40 credits. Prompt and receipt in [examples](examples/EXAMPLES.md).*

Describe a clip and Claude plans it like a director: one subject, one action, one camera move, the light and the style, sized to fit five seconds. You see the shot list and the credit cost first. After your yes, a Wireflow app renders each shot with Hailuo 03 Max Turbo and the MP4s land in `./wireflow-outputs/`. Give it a start image and it animates that picture instead.

**Format today:** one 5 second, 16:9 MP4 per shot, about 1344x768, with an audio track the model adds. Vertical or longer clips need the board edited in Wireflow (see [Limits today](#limits-today)).

Not connected to Wireflow? You still get a shot list and prompts that work in any video model.

## Try it

```text
Make a 5 second b-roll clip for a coffee shop reel: steam rising from a cup
on a rainy windowsill, slow push-in, cozy and moody.
```

Also triggered by: "text to video", "animate this image", "make a short clip of...", "AI video generation", "I need b-roll for...".

## How to install

Claude Code plugin, which adds every Wireflow skill plus the Wireflow connector:

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

Finish with `/mcp` → `wireflow` → Authenticate.

Just this skill, with the skills CLI:

```bash
npx skills add wireflowINC/skills --skill ai-video-generation
```

Or copy `skills/ai-video-generation` into `~/.claude/skills/`.

Without the plugin, connect Wireflow yourself, once:

```bash
claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp
```

Claude.ai and Claude Desktop take the same URL as a custom connector.

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the video link instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Cost

| What | Credits |
|---|---|
| Shot planning, prompts, the quote | 0, it all happens in Claude |
| One rendered clip (5 s, 16:9, 768P) | About 40 (8 per second, price checked 8 Oct 2026) |
| A second take | About 40 more, only with your yes |

On Wireflow's Free plan you can build and browse, and your first image is free when you finish setup. Rendering video needs a paid plan, from US$24 a month (1,600 credits, roughly 40 clips at this price).

## Limits today

- Clips are 16:9 and 5 seconds. Vertical or longer clips need the board duplicated and edited in Wireflow (the skill gives you the link).
- Image to video needs the start image at a public `https://` URL. For a local file, the Wireflow connector can send you an upload link.
- Text and logos inside generated video come out garbled; add them in your editor.

## Data flow

- Your shot prompt, and the start image URL if you give one, go to Wireflow over the Wireflow MCP connector (`run_app`), signed in as you.
- The skill reads your credit balance and run status from Wireflow.
- Finished clips download from `cdn.wireflow.ai` to `./wireflow-outputs/`. If ffmpeg is installed, the skill pulls a few stills locally to check the clip.
- No keys, no scripts to install, no other services.

## FAQ

### Can Claude generate video?

Not by itself. With this skill Claude plans the shot and writes the prompt, a Wireflow app renders it with MiniMax Hailuo 03 Max Turbo, and Claude saves the MP4.

### How long are the clips, and do they have sound?

Each clip is 5 seconds, 16:9, about 1344x768, with an audio track the model generates. Vertical or longer clips need the board duplicated and edited in Wireflow.

### What does a clip cost?

About 40 Wireflow credits (8 per second, price checked 8 Oct 2026). Shot planning and the quote are free, and a second take only runs after your yes.

### Do I need a Wireflow account?

To render, yes: a Wireflow account with credits, connected through the Wireflow MCP connector (OAuth sign-in, no API key). Without it you still get the shot list and prompts.

### Can it animate my own image?

Yes. Give it a start image at a public `https://` URL and the clip opens on that frame. For a local file, the Wireflow connector can send you an upload link.

## Inside the folder

- `SKILL.md`, the procedure Claude runs.
- `reference/shot-guide.md`, camera moves, what fits in five seconds, and twelve ready shots.
- `reference/models.md`, Wireflow's video models side by side with credits per second.
- `examples/`, a real clip from this skill with its exact prompt.

Powered by the [Wireflow AI video workflow](https://www.wireflow.ai/features/ai-video-workflow?ref=skill-ai-video-generation&utm_source=github&utm_medium=skill&utm_campaign=ai-video-generation). Connector setup: [Wireflow MCP docs](https://www.wireflow.ai/docs/mcp?ref=skill-ai-video-generation&utm_source=github&utm_medium=skill&utm_campaign=ai-video-generation). MIT licensed skill; rendering runs on Wireflow with your credits.
