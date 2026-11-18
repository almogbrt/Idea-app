---
name: ai-infographic-generator
description: "AI infographic generator in Claude Code and Claude with Ideogram 4.5 through Wireflow: two clean infographic layouts with text spelled exactly. From a brief, a set of stats or an article it picks the structure (process, comparison, list, timeline or data), writes short copy for every section, lets the person edit each word, quotes the credits and waits for a yes, then renders the same text in two portrait layouts at 1728x2304 and saves them to ./wireflow-outputs. Use when someone asks for an infographic, an explainer graphic, a process or step diagram, a comparison chart, a one-page visual summary of a blog post, or a stats graphic for a client report or social post. Without the Wireflow connector it still writes the copy deck and a layout sheet a designer can build. For product listing feature graphics from a product photo use amazon-product-images."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Inputs are text only. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-infographic-generator"
---

# AI Infographic Generator

Agencies and content teams keep needing the same thing: a long article, a client's numbers or a messy brief turned into one graphic people can read in ten seconds. You (Claude) do the thinking: pick the structure, cut the copy down and agree every word with the person. The Wireflow app `skill-ai-infographic-generator` then draws that copy twice, in two different layouts, with Ideogram 4.5, a model that keeps lettering clean.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-infographic-generator` |
| `topic` | What the graphic is about, as context. Not drawn unless it is also in `infographic_text` |
| `infographic_text` | Every word on the graphic, each piece in double quotes, in reading order: title, section labels with their short lines, figures, source, footer |
| `style` | Palette (hex codes if known), font feel and icon style. Shared by both layouts |
| `layout_1`, `layout_2` | How the sections are arranged, one arrangement each (vertical list, card grid, timeline, two columns, bar chart, cycle) |
| Fixed inside the app | Flat vector look, portrait, only the quoted words appear, spelled as given, no invented numbers, labels, logos or photos; MagicPrompt off so nothing rewrites the copy |
| Output | Two PNGs, 1728x2304 (3:4 portrait): `infographic-1`, `infographic-2` |
| Price | 38 credits per run, 19 per image (Ideogram 4.5, measured 19 Oct 2026) |

Send all five inputs every time. A missing input falls back to the board's demo text (a client onboarding process), which would then appear on the person's graphic.

## A. Connection check

Look for tools ending in `run_app`, `get_execution`, `get_credit_balance` and `whoami`.

If they are not there, say so in one sentence and give the setup:

- With this plugin: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: custom connector, URL `https://www.wireflow.ai/api/mcp`.

Then deliver the free part anyway: the copy deck and the layout sheet from `reference/infographic-planner.md`, filled in for their material. Stop there.

## B. Collect the material

Ask once, in one message:

1. The source: a brief, a pasted article or its key points, or the figures (with where each one comes from).
2. Who will see it and where (client report, LinkedIn, blog header, slide), plus the brand colors and any footer or logo text.
3. Anything that must be on it word for word.

Do not make up statistics. Every number on the graphic comes from the person or from the source they gave; if a figure has no source, ask or leave it out. A real logo file cannot go in: the app is text only, so a brand name can only appear as typed text.

## C. Plan the structure and the copy

Read `reference/infographic-planner.md`. Then:

- Pick the structure that fits the material: process (ordered steps), comparison (two options side by side), list (tips or reasons), timeline (dates), or data (3 to 6 figures with labels). Say why in one line.
- Write the copy deck: a title of 8 words or fewer, 3 to 6 sections, each with a label of 2 to 5 words and one short line of 8 words or fewer, plus an optional source line and footer. Fewer words render more reliably.
- Propose two layouts that suit that structure and differ clearly (for a process: a numbered vertical list and a card grid; for data: a bar chart and big-number tiles).
- Show the deck and the two layouts as a short table. The person can change any word now; after rendering, a text change means a new run.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`, then say, for example: "1 run x 38 credits = 38 credits for 2 layouts. Balance: 1,240." Each extra version (new copy or new layouts) is another run and another quote. If the balance is short, stop and say so. Nothing renders until the person says yes to this deck and this price.

## E. Generate

One `run_app` per approved deck:

```json
{ "slug": "skill-ai-infographic-generator", "inputs": { "topic": "How a content agency turns one blog post into a week of social content", "infographic_text": "Title: \"1 Blog Post, 7 Days of Content\". 1. \"Pull 5 key points\" - \"One idea per post\". ...", "style": "...", "layout_1": "...", "layout_2": "..." } }
```

Poll `get_execution` every 5 seconds while the status is `PENDING`, `RUNNING` or `IN_PROGRESS`. Our test took under a minute. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop and quote the error.

## F. Check, save, report

Save each file as `./wireflow-outputs/<YYYY-MM-DD>/infographics/<topic-slug>_<layout>.png`, for example `curl -sSL -o <file> <output url>` or PowerShell `Invoke-WebRequest -Uri <output url> -OutFile <file>`.

Read every image before you hand it over:

- Each word and number matches the approved deck letter by letter, nothing is missing and nothing extra appears.
- Sections are in the right order and each line sits under its own label.
- Icons fit their section; a wrong or missing icon is common, so name it.
- Arrows, connectors and chart bars match the layout asked for and do not imply numbers that are not in the text.

List every miss per file. A fix is a new run of 38 credits, after a yes.

Close with a table (file, layout, CDN link) and the credits spent (balance before minus after). Offer:

- A second version with edited copy or two other layouts (one run, one quote).
- Square or landscape crops are not rendered by this app; for those, give the layout sheet to a designer.
- The board in Wireflow, to change the size or add steps: `https://www.wireflow.ai/flow/cmveoasn70006la07q1gwpfgj?ref=skill-ai-infographic-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-infographic-generator`

## Guardrails

- Spend only after a yes to the exact deck and price.
- No invented data, no fake sources, no third-party logos or trademarks presented as endorsements.
- Keep keys and passwords out of prompts and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
