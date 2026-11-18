# AI Poster Generator for Claude Code

| Layout 1 | Layout 2 |
|---|---|
| ![Plum jazz night poster with a gold serif headline, a saxophone over a skyline and centered event details](examples/jazz-night-layout-1.jpg) | ![Plum jazz night poster with a stacked capital headline on the left, details in a right column and a gold booking band](examples/jazz-night-layout-2.jpg) |

*Same words, two layouts, one run. Made with this skill on 3 Nov 2026 with Ideogram 4.5, 38 credits for both. Layout 1 is clean. Layout 2 has a ghosted "OO" and a stray line across the details. The unedited run and full proof notes are in [examples](examples/EXAMPLES.md).*

This AI poster generator is for agencies and in-house teams that keep getting the same request: a poster or flyer for a gig, a sale, a workshop or an opening. Tell Claude the headline, the date, the venue and what people should do next. Claude agrees every word with you, checks that the weekday matches the date and quotes the credits. Once you say yes, a Wireflow app sets the poster twice in your brand colors, as two portrait layouts you can put in front of the client. Claude then proofs both against the approved copy, letter by letter, and tells you which one is ready.

No Wireflow connection? You still get a filled-in poster copy sheet and two layout briefs for a designer.

## Try it

```text
Poster for our client Copper Kettle Bakery: "Sourdough Workshop",
Sunday 6 December, 10am to 1pm, at 48 Elm Road. Book at
copperkettle.co/class, small print "Flour and apron included, £45".
Cream and rust colors, warm hand-drawn feel. Two options please.
```

Also triggered by: "event poster", "flyer", "gig poster", "sale poster", "promo poster", "two poster layouts for the client".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

The plugin includes the Wireflow skills and the connector. Run `/mcp` → `wireflow` and sign in.

To add just this skill: `npx skills add wireflowINC/skills --skill ai-poster-generator`, or copy `skills/ai-poster-generator` into `~/.claude/skills/`. Then connect Wireflow with `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (in Claude.ai and Desktop, add a custom connector with the same URL).

## Works with

- **Claude Code**: the main target. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: connect Wireflow as a custom connector. Without a shell nothing is saved to disk, so you get the image links.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI can install it there. Rendering needs the agent connected to the Wireflow MCP server. We have not tested these agents ourselves.

## Credits

| Step | Credits |
|---|---|
| Copy, layouts, quote | 0 |
| Two poster options | 38 (19 per poster, Ideogram 4.5, measured 3 Nov 2026) |
| A re-run or another event | 38 more, after a yes |

You can build and browse on Wireflow's Free plan, and it includes a first image after setup. Rendering these posters needs a paid plan, from US$24 a month.

## What it will not do

- Make up dates, prices, line-ups or offers. Every word comes from you or your client.
- Place a logo or a photo. The app takes text only, so a brand name appears as typed words.
- Produce print files with bleed. Each output is a 1728x2304 PNG in 3:4 portrait, with text kept inside a trim margin. For press, a designer sets it up at A3, A2 or tabloid size.
- Promise both layouts come out clean. Each one is drawn separately, so Claude proofs both and names any miss.
- Make social post sizes (use `ai-social-media-graphics`) or a sectioned explainer (use `ai-infographic-generator`).

## Data

- The poster text, colors, style and layout briefs go to Wireflow as you, through the Wireflow MCP connector (`run_app`).
- The posters download from `cdn.wireflow.ai` into `./wireflow-outputs/`.
- No keys, no scripts, no other services.

## FAQ

### How much does an AI poster cost?

One run gives two poster options for 38 Wireflow credits, 19 each with Ideogram 4.5 (measured 3 Nov 2026). Writing and approving the copy is free. Claude quotes the price and waits for your yes before it renders anything.

### Do I need a Wireflow account?

To render, yes: a Wireflow account with credits, connected through the Wireflow MCP connector. Without one you still get the copy sheet and the layout briefs.

### Which model makes the poster, and will the date be spelled right?

Ideogram 4.5, chosen for its lettering, with prompt rewriting switched off. In our test every word and number was spelled correctly in both layouts. One layout still had a ghosted letter and a line through the text, which is why Claude proofs both posters before you send them.

### Where are the files saved?

As PNGs in `./wireflow-outputs/<date>/posters/`, named after the event and layout, with the CDN links in Claude's report.

## In this folder

- `SKILL.md`: the procedure Claude follows.
- `reference/poster-sheet.md`: the copy sheet, style lines, layout patterns and a brief for a designer.
- `examples/`: the real run with both posters and the inputs.

Built on the [Wireflow AI workflow builder](https://www.wireflow.ai/ai-workflow-builder?ref=skill-ai-poster-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-poster-generator) and its [node based image generation](https://www.wireflow.ai/node-based-image-generation?ref=skill-ai-poster-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-poster-generator). MIT licensed. Renders use your Wireflow credits.
