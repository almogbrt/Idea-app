---
name: ai-workflow-runner
description: "AI workflow automation in Claude Code and Claude: run your own Wireflow workflows in plain words, once or once per row of a CSV. It runs workflows you have already built in Wireflow: lists the workflows in your account, matches a request like 'make a teapot shot with my product photo flow' to the right one, reads the inputs it accepts, estimates the credits from the models inside it, waits for your yes, then runs it, polls until done, and saves the outputs to ./wireflow-outputs with a run log. Use when someone says 'run my Wireflow workflow', 'use my flow', 'run this workflow over a spreadsheet', 'automate my AI workflow from Claude', or names one of their Wireflow boards. Works with any image, video, audio or text workflow they own. Without the Wireflow connector it explains how to connect and what it would do."
license: MIT
compatibility: "Needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) with the default read and run permissions, and a Wireflow account with credits. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  mode: "user-workflows"
---

# AI Workflow Runner

People build workflows on the Wireflow canvas and then rerun them by hand: open the board, paste a new prompt, click run, download, repeat. This skill makes those boards callable from a conversation. It does not use a fixed app; it works on the workflows in the signed-in person's own account through the Wireflow tools `list_workflows`, `get_workflow`, `run_workflow` and `get_execution`.

## Tools this skill relies on

| Tool (base name) | Use | Spends credits |
|---|---|---|
| `whoami` | Confirm which Wireflow account is connected | No |
| `list_workflows` | Find candidate workflows by name | No |
| `get_workflow` | Read a workflow's nodes and the inputs it accepts | No |
| `list_models` | Look up current prices of the models inside it | No |
| `get_credit_balance` | Balance before and after | No |
| `run_workflow` | Start one run, returns an `executionId` | **Yes** |
| `get_execution` | Poll status and collect output URLs | No |

These sit inside the default read and run permissions of the connector. The prefix in front of each name depends on how the person connected.

## Not connected

If the tools are missing: explain that this skill only works with the Wireflow connector, give the setup (plugin: `/mcp`, `wireflow`, Authenticate; or `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`; Claude.ai: custom connector with that URL), and describe what it will do once connected: list their workflows, match the request, quote, run. Offer to help them sketch the workflow they would want on the canvas meanwhile. Do not invent workflow names.

## 1. Find the workflow

1. `whoami`, so both of you know which account this is.
2. `list_workflows`. Match the request against names and descriptions. If two or more fit, show the top three with their last-updated dates and ask which one. If none fit, say so; do not guess.
3. `get_workflow` on the chosen one. Note:
   - the inputs it accepts (their keys or node ids, types, and saved defaults),
   - the generative nodes (image, video, audio, LLM) and their models,
   - outputs (the last nodes, or the ones marked as outputs).

## 2. Map the request onto inputs

Translate the person's words into values for the workflow's inputs:

- Text inputs: write the value in the style the board already uses (look at its saved default prompt).
- Image, video or audio inputs: need an `https://` URL. A local file can come through `create_upload_link` and `get_upload_link` if those tools exist.
- Inputs not mentioned keep their saved defaults. Say which ones those are, because a stale saved prompt is a common surprise.

For a batch, read the CSV or list, map each column to an input, and validate every row before quoting.

## 3. Estimate cost, then ask

Wireflow does not return a price before a run, so estimate: for each generative node, look up its model with `list_models` and multiply by count, duration or images. Add the nodes up. Say it is an estimate and give a range when a model prices by length or resolution.

Then show: workflow name and link, the inputs you will send, what will come out, the estimate per run, the number of runs, the total, and the balance from `get_credit_balance`. Wait for an explicit yes. Workflows that run many nodes can cost far more than one image; read the node list before you promise a number.

## 4. Run

For each approved run, call `run_workflow` with the workflow id and the input values (keys or node ids as `get_workflow` reported). Keep each `executionId`.

- Batches: at most 3 runs in flight, and pause between starts; record each row's status as it finishes.
- Poll `get_execution` every 5 seconds for image and text workflows, every 15 for video.
- Collect every output URL (images, video, audio) and any text outputs.

## 5. Save and log

Save files to `./wireflow-outputs/<YYYY-MM-DD>/<workflow-name>/run-<n>-<node>.<ext>` with `curl -sSL -o` or `Invoke-WebRequest -OutFile`. Write `runs.csv` beside them: run, inputs (short), execution_id, status, output_url, file.

Text outputs (captions, scripts, analyses) go into `run-<n>-<node>.md`.

## 6. Report

- What ran, how many succeeded, which failed and why (exact error text).
- Where the files are.
- Credits used: balance before minus balance after, next to your estimate. If they differ a lot, say so; it improves the next estimate.
- The board link (`www.wireflow.ai/flow/<workflowId>`), so they can open what ran.

Offer to rerun failed rows (new quote, new yes), or to save the mapping you used so next time the request is one sentence.

## Guardrails

- Only the person's own workflows, or ones shared with them for editing. Never run someone else's board.
- Never call `run_workflow` without a yes to the workflow, the inputs and the total.
- Do not change the workflow itself. If the board needs edits, tell the person what to change on the canvas.
- No retries without asking. Some boards fan out into many paid nodes.
- Never put keys, tokens or passwords into inputs or logs.
- If a tool is refused or errors, quote the message. Offer `send_feedback` if it is available.

More request-to-input examples and an estimate worksheet: `reference/runner-playbook.md`. Learn more about calling workflows: `https://www.wireflow.ai/ai-workflow-api?ref=skill-ai-workflow-runner&utm_source=github&utm_medium=skill&utm_campaign=ai-workflow-runner`
