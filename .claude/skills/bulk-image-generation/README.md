# Bulk AI Image Generation for Claude Code

![Three catalog packshots generated in one batch](examples/batch-contact-sheet.jpg)

*A 3-row pilot batch from a CSV, made with this skill on 8 Oct 2026: Flux Pro Ultra, 1:1, 19 credits per row, 57 total. CSV, manifest and receipts in [examples](examples/EXAMPLES.md).*

Hand Claude a spreadsheet, a CSV or just a list, and get a folder of images back with a manifest that records which prompt made which file. The skill cleans every row first (missing prompts, bad ratios, duplicate filenames), adds one shared style line so the set looks consistent, and quotes the whole batch at once. After a single yes it runs a Wireflow app once per row, a few at a time, saves each image as it lands, logs failures without stopping, and can re-run just the failed rows later.

Not connected to Wireflow yet? You still get a cleaned, ready-to-run prompt sheet.

## Try it

```text
Here's products.csv with name and color columns. Make a white-background
packshot for every row, 1:1, same angle and light for all of them.
```

Also triggered by: "batch image generation", "images for my whole catalog", "generate 30 blog headers", "one image per row".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

That adds every Wireflow skill and the Wireflow connector; finish with `/mcp` → `wireflow` → sign in.

Just this one: `npx skills add wireflowINC/skills --skill bulk-image-generation`, or copy `skills/bulk-image-generation` into `~/.claude/skills/`. Then connect Wireflow: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (in Claude.ai or Desktop, add the URL as a custom connector). Help: [Wireflow MCP docs](https://www.wireflow.ai/docs/mcp?ref=skill-bulk-image-generation&utm_source=github&utm_medium=skill&utm_campaign=bulk-image-generation).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Reading a CSV file and writing the manifest need file access, so there you paste the rows into chat and get image links back.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Cost

| Batch size | Credits (19 per row, Flux Pro Ultra, list price 8 Oct 2026) |
|---|---|
| 3-row pilot | 57 |
| 10 rows | 190 |
| 25 rows | 475 |
| Re-run of failed rows | 19 each, only after a new yes |

Checking the CSV, writing prompts and the quote cost nothing. Wireflow's Free plan includes a first image after setup; batches need a paid plan, from US$24 a month (1,600 credits, about 84 rows at this price).

## What you get

- `./wireflow-outputs/<date>/<batch-name>/` with one JPEG per row, named from your `filename` column or the subject.
- `manifest.csv`: row, filename, ratio, prompt, status, execution id, CDN link, local file.
- A summary: done, failed with reasons, credits used.

## Data flow

- Each row's prompt and ratio go to Wireflow over the Wireflow MCP connector (`run_app`), as you.
- Images download from `cdn.wireflow.ai`. The CSV and manifest stay on your machine.
- No API keys, no install scripts, no other services.

## FAQ

### How many images can it make in one batch?

The skill sets no fixed cap. It runs at most 3 rows at a time and stays under 15 starts a minute. Over 50 rows it suggests a 3-row pilot first, and if your balance is short it offers to run only the rows the balance covers.

### What happens if a row fails?

The row is marked failed in `manifest.csv` with the error text and the batch carries on. At the end you can re-run only the failed rows, with a new quote and a new yes.

### What does my CSV need?

A `prompt` column. `aspect_ratio` and `filename` columns are optional. You can also give one prompt template plus a table of values, or a plain list in chat.

### How much does bulk AI image generation cost here?

19 Wireflow credits per row with Flux Pro Ultra (list price, 8 Oct 2026), so 25 rows are 475 credits. Checking the CSV, writing prompts and the quote are free.

### Where do the files go?

Into `./wireflow-outputs/<date>/<batch-name>/`: one JPEG per row plus `manifest.csv`, which records the prompt, status, execution id and CDN link for every row.

## Files

- `SKILL.md`: the batch procedure.
- `reference/batch-recipes.md`: templates for catalogs, blog headers, social backgrounds and more, plus batch sizing.
- `examples/`: the real pilot batch.

Built on the [Wireflow AI workflow API](https://www.wireflow.ai/ai-workflow-api?ref=skill-bulk-image-generation&utm_source=github&utm_medium=skill&utm_campaign=bulk-image-generation). MIT licensed; each image uses your Wireflow credits.
