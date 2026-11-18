# AI Infographic Generator for Claude Code

| Numbered list | Card grid |
|---|---|
| ![Process infographic titled 1 Blog Post, 7 Days of Content with five coral numbered steps in a vertical list](examples/repurpose-list-layout.jpg) | ![The same five steps as white rounded cards in a two column grid under a coral blog post icon](examples/repurpose-card-grid-layout.jpg) |

*One copy deck, two layouts, one call. Made with this skill on 19 Oct 2026: Ideogram 4.5, 38 credits for both. Inputs, receipt and honest notes in [examples](examples/EXAMPLES.md).*

Hand Claude a brief, an article or a set of figures. This AI infographic generator picks the right structure (process, comparison, list, timeline or data), cuts the copy down to a title and a few short sections, and lets you change any word. After your yes to the quoted credits, a Wireflow app draws the same text in two portrait layouts at 1728x2304, spelled exactly as approved. Claude then reads both images for spelling, order and icon mistakes and saves them for your client report, post or slide.

No Wireflow connection? You still get the copy deck and a layout sheet a designer can build.

## Try it

```text
Turn this blog post into an infographic for our client's LinkedIn:
one post becomes a week of content (carousel Monday, three short
videos Tuesday to Thursday, quote card Friday, newsletter at the
weekend). Off-white, charcoal and coral, footer "Made by Brightline Content".
```

Also triggered by: "make an infographic", "explainer graphic", "process diagram", "comparison chart", "visual summary of this article", "stats graphic for a client report".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

The plugin brings the Wireflow skills and the connector; run `/mcp` → `wireflow` → sign in.

Only this skill: `npx skills add wireflowINC/skills --skill ai-infographic-generator`, or copy `skills/ai-infographic-generator` into `~/.claude/skills/`, then add the connector with `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (Claude.ai and Desktop: custom connector, same URL).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the image links instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Credits

| What | Credits |
|---|---|
| Structure, copy deck, layouts, quote | 0 |
| One run: 2 layouts, same text | 38 (19 per image, Ideogram 4.5, measured 19 Oct 2026) |
| Another version (new copy or layouts) | 38 more, after a yes |

Wireflow's Free plan lets you build and browse and includes a first image after setup; rendering infographics needs a paid plan, from US$24 a month.

## What it will not do

- Invent statistics or sources. Every figure comes from you or the source you give.
- Place a real logo file: the app takes text only, so a brand name appears as typed text.
- Render square or landscape versions: both layouts are 3:4 portrait.
- Fit a whole article on one graphic. Past about 60 words it suggests splitting it.

## Data

- The topic, copy, style and layouts go to Wireflow through the Wireflow MCP connector (`run_app`), as you.
- Images download from `cdn.wireflow.ai` into `./wireflow-outputs/`.
- No keys, scripts or other services.

## FAQ

### How much does an infographic cost?

One run makes two layouts of the same infographic for 38 Wireflow credits, 19 per image with Ideogram 4.5 (measured 19 Oct 2026). Planning the structure and copy is free. Claude quotes the cost and waits for your yes before anything renders.

### Do I need a Wireflow account?

Yes, to render: a Wireflow account with credits, connected through the Wireflow MCP connector. Without it you still get the copy deck and the layout sheet.

### Which model draws it, and is the text spelled right?

Ideogram 4.5, picked for clean lettering. You approve every word first and the app sends it with prompt rewriting off. In our test all 12 text pieces were spelled correctly on both layouts; Claude still reads every image and flags wrong icons or connectors.

### What size are the files, and where do they go?

1728x2304 PNG (3:4 portrait), which fits LinkedIn and Instagram portrait posts, portrait slides and PDF reports. They are saved to `./wireflow-outputs/<date>/infographics/`, with the CDN links in the report.

## In this folder

- `SKILL.md`: the procedure.
- `reference/infographic-planner.md`: picking a structure, copy rules, two layouts per structure, the copy deck and layout sheet.
- `examples/`: the real run, two infographics and the inputs.

Powered by [node based image generation](https://www.wireflow.ai/node-based-image-generation?ref=skill-ai-infographic-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-infographic-generator) on [Wireflow, the node-based AI workflow platform](https://www.wireflow.ai/features/best-node-based-ai-workflow-platform?ref=skill-ai-infographic-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-infographic-generator). MIT licensed; renders use your Wireflow credits.
