---
name: bulk-image-generation
description: "Bulk AI image generation in Claude Code and Claude with Flux Pro Ultra through Wireflow. Turns a CSV, spreadsheet or list of prompts (or one prompt template plus a column of products) into a folder of images and a manifest.csv, with one cost quote and one yes for the whole batch. Checks every row before spending, runs the Wireflow app once per row, keeps going past a failed row, and can resume only the rows that failed. Use when someone asks for bulk or batch image generation, images for every product in a catalog, a spreadsheet of prompts, 50 blog headers, many variations at once, or 'generate images from this CSV'. Without the Wireflow connector it still cleans the CSV and returns a ready-to-run prompt sheet. For a single image use ai-image-generation."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Reading the CSV and writing files needs file access; downloads need curl or PowerShell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-bulk-image-generation"
---

# Bulk AI Image Generation

Many images, one decision. The person brings a spreadsheet or a list; you turn every row into a clean prompt, quote the whole batch once, and after one yes you work through the rows with the Wireflow app `skill-bulk-image-generation` (Flux Pro Ultra), filing each result with a manifest so nothing gets lost.

## The app

| | |
|---|---|
| Slug | `skill-bulk-image-generation` |
| `prompt` | Text for one image, 2,000 characters max |
| `aspect_ratio` | `21:9`, `16:9`, `4:3`, `3:2`, `1:1`, `2:3`, `3:4`, `9:16` or `9:21` |
| Result | One JPEG per call, about 4 megapixels |
| Price | 19 credits per row (Wireflow price list, 8 Oct 2026) |

A batch of N rows costs N x 19. Twenty rows = 380 credits.

## 0. Is Wireflow connected?

The tools you need end in `run_app`, `get_execution`, `get_credit_balance` and `whoami`. If any is missing, the batch cannot render. Tell the person, give the setup (plugin: `/mcp` then `wireflow` then Authenticate; otherwise `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` and `/mcp`; Claude.ai: custom connector with that URL), then still do steps 1 and 2 and hand back `prompts.csv`, ready for any batch tool. Do not pretend to run.

## 1. Read the batch

Accept any of these:

- A CSV or spreadsheet export with a `prompt` column, plus optional `aspect_ratio` and `filename` columns.
- A template and a table: "Studio packshot of {product} in {color} on white" plus rows of `product,color`. Fill the template per row.
- A plain list in chat, one subject per line. Write a full prompt for each.

Then check every row:

- Prompt present, under 2,000 characters after filling.
- Ratio is one of the nine allowed values; blank means the batch default (ask once, or pick from the destination).
- Filenames are unique and safe (letters, numbers, hyphens). Make them from the subject if missing.
- Exact duplicates removed, after asking.
- Every prompt ends with "no text, no watermark, full bleed, no border" unless the row needs something else.

Show the cleaned rows as a short table (first 10, then a count). Fix problems before money is involved.

## 2. Keep the batch consistent

Bulk sets look professional when they share a style line. Suggest one and append it to every prompt, for example: "e-commerce packshot, seamless pure white background, soft even studio light, gentle contact shadow, three-quarter view". Same light, angle and background across a catalog matters more than any single image. Prompt tips: `reference/batch-recipes.md`.

## 3. One quote, one yes

Call `whoami` and `get_credit_balance`. Present:

```
Batch: 24 rows, 1:1, style line "white seamless packshot"
Cost: 24 x 19 = 456 credits. Balance: 1,610. After: about 1,154.
```

Short balance: offer to run only the first rows the balance covers. Large batch (over 50 rows): suggest a 3-row pilot first. Wait for an explicit yes to this batch and this total.

## 4. Run the rows

Create `./wireflow-outputs/<YYYY-MM-DD>/<batch-name>/` and a `manifest.csv` with columns `row,filename,aspect_ratio,prompt,status,execution_id,url,file`.

For each row, call `run_app`:

```json
{ "slug": "skill-bulk-image-generation", "inputs": { "prompt": "<row prompt>", "aspect_ratio": "1:1" } }
```

- Keep at most 3 rows in flight; start the next when one finishes. Stay under 15 starts a minute.
- Poll each `executionId` with `get_execution` every 5 seconds. `COMPLETED` gives the image URL (`url`, or the items of `urls`).
- Download each image as `<filename>.jpg` (`curl -sSL -o`, or `Invoke-WebRequest -OutFile` on Windows) and write its manifest line right away, so an interrupted batch can resume.
- A row that ends `FAILED`, `CANCELLED` or `TIMEOUT` gets `status=failed` and the error text. Do not retry it now; keep going.
- Every 10 rows, post one progress line ("14 of 24 done, 1 failed").

## 5. Close out

1. Open a handful of results (first, middle, last, any outliers) and check them against the style line.
2. Report: rows done, rows failed with reasons, the folder path, `manifest.csv`, credits used (balance before minus after).
3. Offer to re-run only the failed or weak rows: list them, quote rows x 19, and wait for a new yes.
4. Offer the board in Wireflow for model swaps or adding an upscaler: `https://www.wireflow.ai/flow/cmuz2dg9d0008l506evjmtrjw?ref=skill-bulk-image-generation&utm_source=github&utm_medium=skill&utm_campaign=bulk-image-generation`

## Batch rules

- The yes covers the rows and total you showed. Added rows need a new quote.
- Never loop on failures; each re-run needs consent.
- No images of real private people, no trademarks the person does not own, nothing deceptive.
- Never write keys or tokens into prompts, the CSV or the manifest.
- If Wireflow rejects a row or a tool breaks, record the exact error in the manifest; offer `send_feedback` when that tool exists.
