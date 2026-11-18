# AI Workflow Runner for Claude Code

![Teapot image produced by running an existing Wireflow workflow from a plain request](examples/teapot-run-output.jpg)

*Made on 8 Oct 2026 by running one of the account's own Wireflow workflows (GPT Image 2.5 Flare, medium, 1024x1024) with a new prompt: 5 credits. The steps and receipt are in [examples](examples/EXAMPLES.md).*

AI workflow automation in plain words: you already built the workflow on the Wireflow canvas, now run it from Claude. Say "use my product shot flow for a sage-green teapot", or "run my ad flow over these 20 rows". The skill lists your workflows, picks the one that matches (or asks), reads which inputs it accepts and which saved defaults will be used, estimates the credits from the models inside it, and waits for your yes. Then it runs once or once per CSV row, polls until done, saves every output with a run log, and tells you what it really cost.

There is no fixed app behind this skill: it works on your own boards through the Wireflow connector's `list_workflows`, `get_workflow` and `run_workflow` tools.

## Try it

```text
Run my "GPT Image 2.5 Flare Text to Image" workflow with this prompt:
a speckled sage-green ceramic teapot on pale stone, soft light.
```

```text
Use my thumbnail workflow for every title in titles.csv.
```

Also triggered by: "run my Wireflow workflow", "use my flow", "run this board over a spreadsheet", "automate my AI workflow from Claude".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

Then `/mcp` → `wireflow` → sign in. The plugin includes every Wireflow skill and the connector.

Or only this skill: `npx skills add wireflowINC/skills --skill ai-workflow-runner`, or copy `skills/ai-workflow-runner` into `~/.claude/skills/`, then connect with `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (Claude.ai and Desktop: custom connector, same URL). The default read and run permissions are enough.

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the output links instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Running a workflow needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Cost

The skill itself spends nothing. Each run costs whatever your workflow's models cost; the skill estimates it from current model prices before asking, and reports the real number (balance before minus after) afterwards. Our one-image test run cost 5 credits. Wireflow's Free plan covers building and browsing plus a first image after setup; running workflows needs a paid plan, from US$24 a month.

## Safety

- Runs only workflows in your account (or shared with you to edit), never someone else's.
- Never changes your workflow; it only fills inputs and runs it.
- Asks before every run or batch, and before any retry.

## What leaves your machine

- Requests go to Wireflow through the Wireflow MCP connector, signed in as you: listing and reading your workflows, starting runs, reading results.
- Outputs download from `cdn.wireflow.ai` to `./wireflow-outputs/` with a `runs.csv` log.
- No API keys, no scripts, no other services.

## FAQ

### Does it build workflows for me?

No. It runs workflows you have already built on the Wireflow canvas and never changes them. To build workflows from Claude with an API key, see the separate [Wireflow builder skill](https://github.com/wireflowINC/wireflow-skill).

### What kinds of workflow can it run?

Any image, video, audio or text workflow in your own Wireflow account, or one shared with you to edit.

### Can it run a workflow over a spreadsheet?

Yes. It maps each CSV column to a workflow input, checks every row, quotes the whole batch, and after your yes runs once per row with at most 3 runs at a time.

### What does it cost?

The skill itself spends nothing. Each run costs whatever the models inside your workflow cost. It estimates that from current model prices before asking, then reports the real number afterwards. Our one-image test run cost 5 credits.

### Does it need an API key?

No. It uses the Wireflow MCP connector, which signs in with OAuth, and the default read and run permissions are enough.

## Contents

- `SKILL.md`: the procedure.
- `reference/runner-playbook.md`: request-to-workflow matching, an estimate worksheet, the batch CSV shape and common surprises.
- `examples/`: a real run with its input and output.

Built on the [Wireflow AI workflow API](https://www.wireflow.ai/ai-workflow-api?ref=skill-ai-workflow-runner&utm_source=github&utm_medium=skill&utm_campaign=ai-workflow-runner) and the [Wireflow node editor](https://www.wireflow.ai/ai-node-editor-with-api?ref=skill-ai-workflow-runner&utm_source=github&utm_medium=skill&utm_campaign=ai-workflow-runner). MIT licensed.
