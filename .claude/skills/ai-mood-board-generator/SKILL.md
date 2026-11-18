---
name: ai-mood-board-generator
description: "AI mood board generator in Claude Code and Claude with Seedream 5 Lite through Wireflow: four matching images plus a palette and tone note. From a campaign brief, a few mood words and written reference notes, it drafts the inputs, shows the credit cost and waits for a yes, then one app run writes a direction note with hex colours and draws a hero picture, a texture close-up, a place and a detail in one look, saved to ./wireflow-outputs. Use when an agency, freelancer or brand team asks for a visual direction, a look and feel, a style exploration, a moodboard for a client pitch, or two or three routes to compare before a campaign. Without the Wireflow connector it still writes the direction note and four image prompts by hand. For a shot-by-shot sequence use ai-storyboard-generator; to apply a brand that already exists use brand-consistent-images."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Inputs are text only. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-mood-board-generator"
---

# AI Mood Board Generator

An agency or freelancer has a pitch coming up and needs to show a client where a campaign could go visually, before anyone writes scenes or books a shoot. You (Claude) turn their notes into a tight brief; the Wireflow app `skill-ai-mood-board-generator` has Claude Haiku 4.5 set the direction and Seedream 5 Lite draw it. One run is one route. Two routes means two runs, side by side.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-mood-board-generator` |
| `campaign_brief` | Who the client is, what the campaign is for, who it speaks to. Up to 2,000 characters |
| `mood_words` | Three to six words for the feeling |
| `reference_notes` | Eras, places, materials and things to avoid, in words. The app cannot see pictures |
| Inside the app | Claude Haiku 4.5 returns a direction note and four prompts. Image 1 is drawn from its prompt; images 2 to 4 use image 1 as the reference for medium, palette and light, each with its own subject |
| Output | `direction-note` (text: the idea, Palette with hex codes, Tone, Avoid), then four landscape 4:3 JPGs with no text: `board-1` hero (3072x2304 in the test), `board-2` texture, `board-3` place, `board-4` detail (2560x1920 each) |
| Price | 43 credits per run: 10 per Seedream 5 Lite image plus 3 for the direction step (measured 2 Nov 2026) |

Send all three inputs every time. A missing one falls back to the board's saved demo (an oat milk launch), which would leak into the result. With no references to give, send "No references, choose freely".

## A. Connection check

Find the tools ending in `run_app`, `get_execution`, `get_credit_balance` and `whoami`.

When they are missing, say so in one sentence and give the setup:

- Plugin installed: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: custom connector, URL `https://www.wireflow.ai/api/mcp`.

Then give the free version from `reference/direction-guide.md`: a direction note and four image prompts written by you, ready for a designer or any image tool. Stop there.

## B. Collect the brief

Ask once, in one message:

1. The client and the campaign: what it sells, to whom, and why now.
2. How it should feel, in a few words, and what it must not feel like.
3. Anything to lean on: eras, places, materials, photographers' habits described in plain words.
4. One route or several. Each route is one run.

A pasted client brief is fine: pull the answers out of it yourself and show what you took.

## C. Shape the routes

Read `reference/direction-guide.md`, then fill in the three inputs for each route.

- Make routes truly different: change the world or the era, not only the colours.
- Turn named brands, artists and films into descriptions before they go in ("1960s travel posters", not a designer's name).
- Leave out double quotes; the app passes these words through a JSON step.

Show a table (route, brief, mood words, reference notes) and let the person edit it.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`, then: "2 routes x 43 credits = 86 credits for 8 images and 2 notes. Balance: 1,240." If the balance is short, stop and say so. Nothing runs before a yes to this table and this cost.

## E. Run it

One `run_app` per route:

```json
{ "slug": "skill-ai-mood-board-generator", "inputs": { "campaign_brief": "...", "mood_words": "Salty, warm, handmade", "reference_notes": "..." } }
```

Poll `get_execution` every 5 seconds while the status is `PENDING`, `RUNNING` or `IN_PROGRESS`. The test took about a minute: image 1 comes first and the other three wait for it. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop that route and quote the error. A `json_extract_field` error means the direction step wrote broken JSON, so offer one retry after a new yes.

## F. Check, save, report

The note arrives as `text` on the `direction-note` output. Any image link on that output is a copy of board 1; ignore it.

Save to `./wireflow-outputs/<YYYY-MM-DD>/mood-boards/<route-slug>/`: write `direction-note.md`, then each image with `curl -sSL -o <file> <output url>` or PowerShell `Invoke-WebRequest -Uri <url> -OutFile <file>`, named `1-hero.jpg`, `2-texture.jpg`, `3-place.jpg`, `4-detail.jpg`.

Look at all four before calling it done:

- They read as one look: same medium, same light, the palette from the note.
- No stray writing: small marks on dials, labels, signs and packaging are where it slips in.
- Nothing from the Avoid line, and nothing a client could mistake for a real brand.
- Object details can drift between images (a ceramic cup in one, an enamel mug in the next). Fine for direction; name it.

Name every miss per file. A redo is a new run at 43 credits after a yes.

Report a table (route, file, CDN link), the direction note, the credits used (balance before minus after) and one line on how the routes differ. These are direction references, not final art. Offer:

- Another route on the same brief (one quote per route).
- The next step: `ai-storyboard-generator` for scenes, once a route is picked.
- The board in Wireflow, to change the image size or add a fifth image: `https://www.wireflow.ai/flow/cmvyohqn0001vi207otm0ic3x?ref=skill-ai-mood-board-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-mood-board-generator`

## Guardrails

- Spend only after a yes to the exact table and cost.
- No real people, celebrities, other brands' logos or the named style of a living artist.
- Keep unreleased client details the person would not want on a third-party service out of the brief; ask when unsure.
- Keep keys and passwords out of prompts and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
