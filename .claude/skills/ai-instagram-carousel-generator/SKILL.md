---
name: ai-instagram-carousel-generator
description: "AI Instagram carousel generator in Claude Code and Claude with Seedream 5 Lite through Wireflow: six matching slides with your words on them. From a topic, notes or a blog post it writes a hook slide, four content slides and a call to action, sets one brand style, quotes the credits and waits for a yes, then renders all six portrait slides in one call (the cover first, the other five made from it so colours, fonts and layout match) and saves them to ./wireflow-outputs. Use when someone asks for an Instagram carousel, a LinkedIn carousel or document post, swipe slides, a carousel from a blog post or newsletter, or a multi-slide social post in their brand colours. Without the Wireflow connector it still writes the slide copy and a design sheet anyone can build. For a single image use ai-image-generation; for paid ad statics use ai-ad-creative-generator."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Inputs are text only. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-instagram-carousel-generator"
---

# AI Instagram Carousel Generator

A brand, a creator or an agency wants a carousel that teaches one thing in six swipes and looks like one designed set. You (Claude) turn their topic into slide copy and a brand style; the Wireflow app `skill-ai-instagram-carousel-generator` draws the cover with Seedream 5 Lite, then builds slides 2 to 6 as edits of that cover, so all six keep the same background, type, margins and footer.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-instagram-carousel-generator` |
| `brand_style` | One paragraph for the whole set: background, text and accent colours (hex codes if they have them), the feel of the headline font, the icon style, and the footer handle in quotes |
| `slide_1` | The cover: the hook headline and a small line, both in quotes, the visual, and the slide number in quotes (`"1/6"`) |
| `slide_2` to `slide_5` | One point each: headline and body line in quotes, a simple wordless visual, the slide number in quotes |
| `slide_6` | The call to action: headline and small line in quotes, a visual, `"6/6"` |
| Fixed inside the app | Only words inside quotation marks are written on a slide; everything else is direction. Words and the main visual stay inside the centred 4:5 area. Slides 2 to 6 are edits of slide 1 that keep its canvas, colours, fonts, margins and footer |
| Output | Six portrait 3:4 JPGs, `slide-image-1` to `slide-image-6`. In our test slide 1 came back at 2304x3072 and slides 2 to 6 at 1920x2560 |
| Price | 60 credits per run, 10 per slide (Seedream 5 Lite, measured 16 Oct 2026) |

Send all seven inputs every time. Any input left out falls back to the board's saved demo text (a carousel about carousel design for a made-up studio), and those words would end up on the person's slides.

## A. Connection check

Look for the Wireflow tools `run_app`, `get_execution`, `get_credit_balance` and `whoami`.

When they are not there, say so in one sentence and show how to connect:

- Installed as a plugin: `/mcp`, pick `wireflow`, then Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp` to sign in.
- Claude.ai or Claude Desktop: add a custom connector with the URL `https://www.wireflow.ai/api/mcp`.

Then hand over the free part anyway: the slide sheet from `reference/carousel-planner.md` filled in for their topic, the brand style block and a caption. Stop there.

## B. Collect inputs

Ask once, in a single message:

1. The topic, or the blog post, newsletter or notes to turn into slides. If they share a link and you have a web tool, read the page; otherwise ask them to paste the main points.
2. Who the post is for, and the one thing readers should do at the end (save, follow, comment a word, tap the link in bio).
3. Their look: colours, font feel, icon style and the handle for the footer. No brand yet? Propose one with strong contrast and let them pick.

The app takes text only, so no logo or photo goes in. A logo described in words gets redrawn, never copied: leave it off and add the real file in a design tool afterwards.

## C. Plan the six slides

Read `reference/carousel-planner.md`, then:

- Choose the shape: a hook, four points (or a short story) and one call to action.
- Headlines of 3 to 7 words, body lines of 12 words or fewer, in plain common words. Small body text is where misspellings creep in: our test run got every headline right but two body words wrong.
- Put every word that should be on a slide inside quotation marks, including the handle and the slide number.
- Describe each visual as a simple shape and say it has no text: "a list icon with three bullet lines, no letters or numbers". In our test, "a numbered list icon" came back with made-up words beside it.
- Write the brand style block once; it is sent with every slide.

Show the plan as a table (slide, headline, line, visual) with the brand style under it, and let the person change any word. Text on a slide cannot be edited after the render without a new run.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`, then say: "1 run x 60 credits = 60 credits for 6 slides. Balance: 1,240." The app always renders all six, so any redo is another 60. If the balance is short, stop and say so. Nothing runs until the person says yes to this plan and this cost.

## E. Generate

One `run_app` per carousel:

```json
{ "slug": "skill-ai-instagram-carousel-generator", "inputs": { "brand_style": "Deep forest green background (#1F3D2B), cream text (#F4EBDD), mustard yellow accent (#E3B23C) ...", "slide_1": "Cover slide, the hook. Big headline: \"Turn 1 blog post into 4 posts\". Small line under it: \"Swipe for the plan\". Visual: ... Slide number in the footer: \"1/6\".", "slide_2": "...", "slide_3": "...", "slide_4": "...", "slide_5": "...", "slide_6": "..." } }
```

Poll `get_execution` every 5 seconds until the status is no longer `PENDING`, `RUNNING` or `IN_PROGRESS`. The cover renders first and the other five follow together; our test took about 90 seconds. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop and quote the error word for word.

## F. Check, save, report

Save the slides in order as `./wireflow-outputs/<YYYY-MM-DD>/carousel/<topic-slug>_<n>.jpg` with `curl -sSL -o <file> <output url>` or PowerShell `Invoke-WebRequest -Uri <output url> -OutFile <file>`.

Open every slide before you call it finished:

- Read each word against the approved plan, letter by letter: headline, body line, handle and slide number.
- No extra words, letters or numbers anywhere, icons included.
- Slides 2 to 6 match the cover: background, colours, fonts, underline and footer.
- Nothing important sits in the top or bottom strip that a 4:5 crop would trim.

Name every miss per slide. Two ways to fix one: a single wrong word on a plain background takes a minute to patch in a design tool, or the whole set runs again (60 credits, after a yes) with that word swapped for a simpler one.

End with a table (slide, headline, file, CDN link), the credits used (balance before minus balance after) and a caption draft from the planner. Then offer:

- Another colour way or a different hook, as one more quoted run.
- For LinkedIn: put the six images into one PDF in order and post it as a document.
- The board in Wireflow, to change the size or add steps: `https://www.wireflow.ai/flow/cmvadu8bg0003lb08en8c4hls?ref=skill-ai-instagram-carousel-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-instagram-carousel-generator`

## Guardrails

- Spend credits only after a yes to the exact plan and price.
- Only true claims: no invented statistics, results, testimonials, or quotes put in a real person's mouth.
- No other brands' logos and no real, identifiable people.
- Keep keys and passwords out of prompts and files.
- When Wireflow refuses or a tool fails, quote the exact message and offer `send_feedback` if that tool exists.
