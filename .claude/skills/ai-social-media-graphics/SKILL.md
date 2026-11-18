---
name: ai-social-media-graphics
description: "AI social media graphics in Claude Code and Claude with Ideogram 4.5 through Wireflow: one branded text post in square, portrait and story sizes. Give it a quote, a stat or an announcement and the brand colors. It trims the words, lets the person approve every piece of text, quotes the credits and waits for a yes, then renders one post at 2048x2048, 1728x2304 and 1440x2560 and saves all three to ./wireflow-outputs, ready to schedule. Use when someone asks for a quote card, a stat post, an announcement graphic, a branded text post, an event or launch post, or the same post sized for feed and stories for a client. Without the Wireflow connector it still writes the post sheet and a design spec a designer can build. For a multi-slide story use ai-instagram-carousel-generator; for paid product ads use ai-ad-creative-generator."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Inputs are text only. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-social-media-graphics"
---

# AI Social Media Graphics

Social teams at agencies spend hours on small jobs: one client quote, one number, one "we're open" post, each resized for feed and stories. You (Claude) settle the words and the arrangement with the person. The Wireflow app `skill-ai-social-media-graphics` then draws that single post in three sizes with Ideogram 4.5.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-social-media-graphics` |
| `post_text` | Every word on the graphic, each piece in double quotes. Anything outside quotes is a label and stays off the image |
| `post_type` | Quote, stat or announcement, plus how the pieces are arranged and any single accent shape |
| `brand_colors` | Background, text and accent colors (hex if known) and the font feel |
| Fixed inside the app | Flat graphic design, no photos of people, no logos, no added words, MagicPrompt off so nothing rewrites the copy. Each size has its own margin note |
| Output | Three PNGs: `square` 2048x2048 (1:1), `portrait` 1728x2304 (3:4), `story` 1440x2560 (9:16) |
| Price | 57 credits per run, 19 per image (Ideogram 4.5, measured 2 Nov 2026) |

Send all three inputs every run. A missing one falls back to the board's demo text (a Northline Studio quote), and that would land on the person's post.

Ideogram 4.5 has no 4:5 size, so `portrait` is 3:4, which Instagram and LinkedIn both accept. The app keeps the words out of the top and bottom 10 percent, so a designer or scheduler can crop it to 4:5 without losing text.

## A. Connection check

Search your tools for names ending in `run_app`, `get_execution`, `get_credit_balance` and `whoami`.

Not connected? Say so in one line and give the setup:

- With this plugin: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: custom connector, URL `https://www.wireflow.ai/api/mcp`.

Then hand over the free part: a filled-in post sheet and design spec from `reference/post-sheet.md`. Stop there.

## B. Get the post

One message, three questions:

1. What is the post: a quote (and who said it), a stat (and where it comes from), or an announcement (what, when, where)?
2. Which brand: colors, font feel, and the name or handle to show as plain text?
3. Is this one post, or a batch for a content calendar?

A logo file cannot go in, because the app takes text only. A quote needs a real speaker who agreed to it, and a figure needs a real source. If either is missing, ask or leave it out.

## C. Settle the words

Use `reference/post-sheet.md`. Then:

- Cut hard. The hero line is 10 words or fewer, the whole post 25 or fewer. Short posts render cleanest and read on a phone.
- Keep the piece count to three at most: hero, one supporting line, one name or handle. In our test the smallest piece was the one that went missing, so make that last piece large enough to matter, or drop it.
- If the post has a date, check that the weekday and the date agree before you quote. The app draws whatever it receives, wrong or right.
- Write `post_type` as one sentence: which piece is the hero, where the others sit, the accent.
- Show the exact `post_text` and let the person change any of it. Afterwards, a word change means a new run.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`, then say, for example: "1 post x 57 credits = 57 credits for 3 sizes. Balance: 1,240." For a batch, multiply and list the posts. The app always draws all three sizes, so a single size costs the same as the set. If the balance is short, stop and say so. Nothing renders until the person says yes to these words and this price.

## E. Generate

One `run_app` per approved post:

```json
{ "slug": "skill-ai-social-media-graphics", "inputs": { "post_text": "Headline: \"We just opened our Austin studio\". Detail: \"Open house, Saturday 14 November, 5 to 8 pm\". Footer: \"Brightline Content\"", "post_type": "Announcement: the headline as the hero in very big type, the detail line smaller underneath it, the footer small at the bottom of the text block, one coral underline under the headline as the only accent.", "brand_colors": "Warm off-white background (#FAF7F2), charcoal text (#222222), coral accent (#FF6B4A), bold rounded sans serif." } }
```

Poll `get_execution` every 5 seconds while the status is `PENDING`, `RUNNING` or `IN_PROGRESS`. Our test took about a minute. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop and quote the error.

## F. Read, save, report

Save the files as `./wireflow-outputs/<YYYY-MM-DD>/social-graphics/<post-slug>_<size>.png` with `curl -sSL -o <file> <output url>` or PowerShell `Invoke-WebRequest -Uri <output url> -OutFile <file>`.

Open all three images and compare each against the approved `post_text`. The sizes are drawn separately, so one can be wrong while the others are right:

- Every quoted piece is there. A dropped small line is the most likely miss: our test lost the footer on the square.
- Each word, number, capital and punctuation mark matches, letter by letter, and nothing was added.
- The type weight stays even within a line, and letters from one line do not touch the line below.
- The brand colors are right, and the layout may differ between sizes (centered in one, left aligned in another). Name it if it does.
- On the story, the words stay clear of the top and bottom app buttons.

List each miss per file. A fix means a new run of all three sizes for 57 credits, after a yes. Never call a post ready to schedule while a miss is open.

Close with a table (size, file, CDN link) and the credits spent (balance before minus after). Offer:

- The next post in the calendar (one quote for the batch).
- The board in Wireflow, to add sizes or a fixed brand look: `https://www.wireflow.ai/flow/cmvyoaify000tjp08r0ij691c?ref=skill-ai-social-media-graphics&utm_source=github&utm_medium=skill&utm_campaign=ai-social-media-graphics`

## Guardrails

- Spend only after a yes to the exact words and price.
- No invented quotes, statistics, sources or testimonials, and no words put in a real person's mouth without their consent.
- No third-party logos or trademarks shown as endorsements.
- Keep keys and passwords out of prompts and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
