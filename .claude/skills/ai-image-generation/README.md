# AI Image Generation for Claude Code

![A red vintage bicycle against a blue tiled Lisbon wall, made with this skill](examples/lisbon-bicycle-16x9.jpg)

*Made with this skill on 8 Oct 2026: Flux Pro Ultra, 16:9, 19 credits. Prompt and receipt in [examples](examples/EXAMPLES.md).*

Ask Claude for an image in plain words. The skill writes a proper prompt (subject, setting, light, camera, style), picks the right aspect ratio for where the image will be used, tells you the credit cost and waits for your yes. Then it runs a Wireflow app with Flux Pro Ultra, saves the files to `./wireflow-outputs/` and tells you what it spent.

No Wireflow account yet? It still gives you a ready-to-paste prompt pack you can use in any image tool.

## Try it

```text
Make me a 16:9 hero image for a small bakery's website: fresh sourdough on a
wooden counter, morning light, space on the right for a headline.
```

Other things that trigger it: "generate an image of...", "text to image", "make a wallpaper", "I need a blog header", "four options for an Instagram post".

## How to install

**Claude Code plugin (recommended).** Installs all Wireflow skills and the Wireflow connector together:

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

Then run `/mcp`, pick `wireflow` and sign in.

**skills CLI** (Claude Code, Cursor, Codex and other agents):

```bash
npx skills add wireflowINC/skills --skill ai-image-generation
```

**Manual.** Copy the `skills/ai-image-generation` folder into `~/.claude/skills/` (or your project's `.claude/skills/`).

With the CLI or manual install, connect Wireflow once:

```bash
claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp
```

In Claude.ai or Claude Desktop, add a custom connector with the same URL. Setup details: [Wireflow MCP connector docs](https://www.wireflow.ai/docs/mcp?ref=skill-ai-image-generation&utm_source=github&utm_medium=skill&utm_campaign=ai-image-generation).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the image links instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## What is free and what costs credits

| Step | Cost |
|---|---|
| Prompt writing, ratio choice, prompt pack, cost quote | Free, runs in Claude |
| Each image rendered by the Wireflow app | 19 Wireflow credits (Flux Pro Ultra, price checked 8 Oct 2026) |
| A re-run or extra variation | Another 19 credits, only after you say yes |

Wireflow's Free plan is for building and browsing and includes a first image on the house when you finish setup. Generating more needs a paid plan, from US$24 a month for 1,600 credits. The skill always shows the cost and your balance before it spends anything.

## What the skill sends and fetches

- Sends your prompt and chosen aspect ratio to Wireflow through the Wireflow MCP connector (`run_app`), using your own Wireflow login.
- Reads your credit balance (`get_credit_balance`) and the run status (`get_execution`).
- Downloads the finished images from `cdn.wireflow.ai` into `./wireflow-outputs/`.
- No API keys, no install scripts, nothing sent anywhere else.

## FAQ

### Can Claude generate images?

Not on its own: Claude writes text and code. With this skill Claude writes the prompt and picks the ratio, a Wireflow app renders the image with Flux Pro Ultra, and Claude saves the file and checks it.

### How much does AI image generation in Claude Code cost with this skill?

19 Wireflow credits per image (price checked 8 Oct 2026). The prompt, the ratio choice and the quote are free, and nothing renders until you say yes.

### Do I need a Wireflow account?

Only to render. Generation runs on your own Wireflow account through the Wireflow MCP connector, which signs in with OAuth, so there is no API key to copy. Without an account you still get the prompt pack.

### Which model does it use?

Flux Pro Ultra v1.1, one JPEG of about 4 megapixels per run, in nine aspect ratios from 21:9 to 9:21. For another model, duplicate the app's board in Wireflow; `reference/models.md` lists the options.

### Where are the images saved?

In `./wireflow-outputs/<date>/` inside the folder where Claude Code is running. In Claude.ai, where there is no shell, you get the links instead.

## Files

- `SKILL.md`: the steps Claude follows.
- `reference/prompt-guide.md`: the prompt method, ratio picker and eight worked prompts. Useful on its own.
- `reference/models.md`: which Wireflow image model suits which job, with prices.
- `examples/`: real outputs from this skill with their exact prompts.

Powered by [Wireflow node-based image generation](https://www.wireflow.ai/node-based-image-generation?ref=skill-ai-image-generation&utm_source=github&utm_medium=skill&utm_campaign=ai-image-generation). The skill text is MIT licensed; image generation runs on Wireflow and uses your Wireflow credits.
