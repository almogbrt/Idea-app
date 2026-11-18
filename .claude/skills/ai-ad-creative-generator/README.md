# AI Ad Creative Generator for Claude Code

| 1:1 feed | 4:5 portrait feed | 9:16 stories and reels |
|---|---|---|
| ![Terracotta mug ad in 1:1 with the headline Slow mornings, made better](examples/mug-ad-1x1.jpg) | ![The same mug ad in 4:5 for portrait feed](examples/mug-ad-4x5.jpg) | ![The same mug ad in 9:16 for stories and reels](examples/mug-ad-9x16.jpg) |

*One concept, three placements, one call. Made with this skill on 8 Oct 2026: Nano Banana 2, 60 credits for all three. Brief, receipt and notes in [examples](examples/EXAMPLES.md).*

Give Claude a product image and a few lines about who you sell to. It writes several genuinely different static ad variations, each a concept with a headline and a call to action, lets you edit the words, then quotes the credits. After your yes, a Wireflow app renders every concept in 1:1, 4:5 and 9:16 at once, with your exact words on the image. Claude proofreads every headline, checks the story safe areas and names the files so they are ready to drop into an ads manager.

No Wireflow connection? You still get the concept sheet: angles, headlines, CTAs and layout briefs.

## Try it

```text
Make 3 Meta ad concepts for my terracotta stoneware mug. Product image:
https://example.com/mug.jpg. Audience: people who make coffee at home.
No discounts, we just launched.
```

Also triggered by: "ad creatives", "Instagram ads", "Facebook ad variations", "headline variants", "static ads for TikTok", "AI ad creative generator".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

The plugin brings every Wireflow skill and the connector; run `/mcp` → `wireflow` → sign in.

Only this skill: `npx skills add wireflowINC/skills --skill ai-ad-creative-generator`, or copy `skills/ai-ad-creative-generator` into `~/.claude/skills/`, then add the connector with `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (Claude.ai and Desktop: custom connector, same URL).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the image links instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Credits

| What | Credits |
|---|---|
| Concepts, headlines, layout briefs, quote | 0 |
| One concept in 3 placements | 60 (20 per image, Nano Banana 2 at 1K, measured 8 Oct 2026) |
| 3 concepts = 9 ads | 180 |
| Re-render of a concept | 60, after a yes |

Wireflow's Free plan lets you build and browse and includes a first image after setup; rendering ads needs a paid plan, from US$24 a month.

## What it will not do

- Invent prices, discounts, reviews, ratings or claims.
- Use competitor logos or real people without permission.
- Promise the ads pass a platform's review: check your ad platform's policies before launch.

## Data

- Product image URL and ad briefs go to Wireflow through the Wireflow MCP connector (`run_app`), as you.
- Images download from `cdn.wireflow.ai` into `./wireflow-outputs/`.
- No keys, scripts or other services.

## FAQ

### What sizes does it make?

Three PNGs from one brief: 1:1 (1024x1024) for feed, 4:5 (928x1152) for portrait feed and 9:16 (768x1376) for stories and reels. All three come from one call.

### Will the headline be spelled correctly?

You approve the exact words first and they go to the model in quotes. Claude then reads the headline and button text letter by letter in every image. In our test both were spelled correctly in all three sizes. A fix re-renders the whole concept, 60 credits, after your yes.

### How much does it cost?

60 Wireflow credits per concept, which is 20 per image with Nano Banana 2 at 1K (measured 8 Oct 2026). Three concepts are 180 credits for 9 ads. Writing the concepts and headlines is free.

### Does it write the ad copy too?

Yes. It writes 2 to 4 concepts from different angles, each with a headline and a call to action, and you edit the words before anything renders. That part works without a Wireflow account.

### Will the ads pass Meta or TikTok review?

The skill cannot promise that. It keeps text inside the story safe areas and will not invent prices, reviews or claims, but you check your ad platform's policies before launch.

## In this folder

- `SKILL.md`: the procedure.
- `reference/ad-angles.md`: seven angles with headline patterns, layouts that render well, safe areas and a test plan.
- `examples/`: the real concept, three placements and the brief.

Powered by the [Wireflow AI workflow builder](https://www.wireflow.ai/ai-workflow-builder?ref=skill-ai-ad-creative-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-ad-creative-generator) on [Wireflow, the node-based AI workflow platform](https://www.wireflow.ai/features/best-node-based-ai-workflow-platform?ref=skill-ai-ad-creative-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-ad-creative-generator). MIT licensed; renders use your Wireflow credits.
