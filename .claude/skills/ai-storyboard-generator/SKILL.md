---
name: ai-storyboard-generator
description: "AI storyboard generator in Claude Code and Claude with Seedream 5 Lite through Wireflow: six 16:9 frames, one character and one look. From a script, an ad brief or a pitch idea it breaks the story into six shots (framing, angle, action, setting), writes one character note and one visual style, quotes the credits and waits for a yes, then renders all six frames in one call (panel 1 first, panels 2 to 6 drawn from it so the hero and the style hold) and saves them to ./wireflow-outputs with a shot list. Use when someone asks to storyboard a video ad, a commercial, a client pitch, a TikTok or Reels concept, a shot list with pictures, frames to plan a shoot, or panels to brief an AI video model. Without the Wireflow connector it still writes the shot list and frame prompts. For finished static ads use ai-ad-creative-generator; for one image use ai-image-generation."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Inputs are text only. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-storyboard-generator"
---

# AI Storyboard Generator

An agency, a brand team or a solo creator has a script or a rough idea for a short video and needs to show it before anything is shot or generated. You (Claude) turn that idea into six shots, one hero and one look; the Wireflow app `skill-ai-storyboard-generator` paints panel 1 with Seedream 5 Lite and then paints panels 2 to 6 with panel 1 as the reference, so the main character and the style carry through while the camera moves.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-storyboard-generator` |
| `style` | One paragraph for all six frames: medium (pencil sketch, ink and marker, digital painting, 3D, photoreal), palette, line and light, grain |
| `character` | The hero as they look in every frame: age, face, hair, skin, build, glasses, the full outfit with colours |
| `panel_1` | The opening shot. It sets the look for the rest, so make it a clear wide or medium shot with the hero's face visible |
| `panel_2` to `panel_6` | One shot each: camera distance, angle, action, setting, light. Any second person is described in full every time they appear |
| Fixed inside the app | Frames carry no text: no captions, numbers, arrows, speech bubbles, logos or borders. Panels 2 to 6 copy the hero and the style of panel 1 but get a new composition |
| Output | Six landscape 16:9 JPGs, `frame-1` to `frame-6`. In our test panel 1 came back at 3072x1728 and panels 2 to 6 at 3416x1920 |
| Price | 60 credits per run, 10 per frame (Seedream 5 Lite, measured 21 Oct 2026) |

Send all eight inputs every time. An input left out falls back to the board's saved demo (a woman in a yellow robe making coffee), and that scene would land in the person's storyboard.

## A. Connection check

Look for the Wireflow tools `run_app`, `get_execution`, `get_credit_balance` and `whoami`.

If they are missing, say so in one sentence and show how to connect:

- Installed as a plugin: `/mcp`, pick `wireflow`, then Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp` to sign in.
- Claude.ai or Claude Desktop: add a custom connector with the URL `https://www.wireflow.ai/api/mcp`.

Then deliver the free part: the shot list from `reference/storyboard-planner.md` filled in for their idea, with the style and character blocks, ready to sketch by hand or paste into any image tool. Stop there.

## B. Collect inputs

Ask once, in one message:

1. The script, voiceover, brief or idea, and the length of the finished video (15, 30 or 60 seconds).
2. The hero: who they are and what they wear. No idea yet? Offer two options that fit the audience.
3. The look: sketch for an internal pitch, painted or photoreal for a client deck or an AI video brief. Mention the format the video will run in; the frames are 16:9 either way (see the planner for vertical ads).

Text only goes in. A real person's photo, a product shot or a logo cannot be used: describe the product in plain words and leave brand marks for the edit.

## C. Plan the six shots

Read `reference/storyboard-planner.md`, then:

- Fit the story into six beats: open, problem, turn, help or product, payoff, end shot.
- Vary the camera: at least one wide, one close-up and one medium; never two identical framings in a row.
- Write each panel as one or two sentences that name camera distance and angle first, then action, place and light.
- Keep the hero in panel 1 clearly, face visible, so the later panels have something to match.
- Describe every other person in full (age, hair, clothes) in every panel they appear in. The app only locks the hero from panel 1; in our test a mechanic described once came back as a different person two panels later.
- Leave out words, signs, screens with text and brand names: frames are wordless by design.

Show the plan as a table (panel, shot, action, timing, voiceover line) with the style and character notes under it, and let the person change anything. A frame cannot be changed after the run without running all six again.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`, then say: "1 run x 60 credits = 60 credits for 6 frames. Balance: 1,240." The app always renders all six, so a redo is another 60. If the balance is short, stop and say so. Nothing runs until the person says yes to this plan and this cost.

## E. Generate

One `run_app` per storyboard:

```json
{ "slug": "skill-ai-storyboard-generator", "inputs": { "style": "Cinematic colour storyboard frames, soft digital painting ...", "character": "A man in his late 40s with a short salt-and-pepper beard ...", "panel_1": "Wide establishing shot, high angle: ...", "panel_2": "...", "panel_3": "...", "panel_4": "...", "panel_5": "...", "panel_6": "..." } }
```

Poll `get_execution` every 5 seconds until the status is no longer `PENDING`, `RUNNING` or `IN_PROGRESS`. Panel 1 renders first and the other five follow together; our test finished in a few minutes. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop and quote the error word for word.

## F. Check, save, report

Save the frames in order as `./wireflow-outputs/<YYYY-MM-DD>/storyboard/<project-slug>_<n>.jpg` with `curl -sSL -o <file> <output url>` or PowerShell `Invoke-WebRequest -Uri <output url> -OutFile <file>`.

Look at every frame before calling it done:

- The hero matches panel 1: face, beard or hair, skin, outfit colours.
- Each frame shows the planned shot: distance, angle, action.
- Side characters match their description in every panel.
- No stray text, numbers, logos or split panels.

Name each miss per panel. Small ones (a prop in the wrong place) are fine for a planning board; a wrong person or a missing action needs another run of 60 credits, after a yes, with that panel rewritten.

Write `storyboard.md` next to the images: a table with panel number, the image, shot, action and voiceover line, so it pastes into a deck or a doc. End with the files, the CDN links and the credits used (balance before minus balance after). Then offer:

- A second look (sketch versus painted) or a vertical version for Reels and TikTok, as one more quoted run.
- Using the frames as start images for an AI video model, one shot at a time.
- The board in Wireflow, to change the size or add steps: `https://www.wireflow.ai/flow/cmvhizh16003vl207z7xw3ln0?ref=skill-ai-storyboard-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-storyboard-generator`

## Guardrails

- Spend credits only after a yes to the exact plan and price.
- No real, identifiable people, celebrities or other brands' logos in the frames.
- Mark the frames as concept art when they go to a client; they are a plan, not the final ad.
- Keep keys and passwords out of prompts and files.
- When Wireflow refuses or a tool fails, quote the exact message and offer `send_feedback` if that tool exists.
