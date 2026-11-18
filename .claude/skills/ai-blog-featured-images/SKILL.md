---
name: ai-blog-featured-images
description: "AI blog featured images in Claude Code and Claude with Seedream 5 Lite through Wireflow: a 16:9 hero and a share card for each post. From a post title and summary (or the draft itself) plus the blog's style note, it writes the inputs, shows the credit cost and waits for a yes, then one app run picks a wordless visual concept, draws the hero image and turns it into a social share card with the title, and saves both to ./wireflow-outputs. Use when someone asks for a featured image, blog header or hero image, an Open Graph or og:image, a link preview or social share image for a post, or matching cover images across a blog. Without the Wireflow connector it still writes a style note and a concept brief per post a designer can build. For a CSV of prompts use bulk-image-generation; for YouTube covers use ai-thumbnail-maker."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Inputs are text only. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-blog-featured-images"
---

# AI Blog Featured Images

A blogger, content marketer or agency publishes posts that each need a header image and a link preview, and wants every post to look like it belongs to the same blog. You (Claude) boil the post down to a title, a short summary and a reusable style note; the Wireflow app `skill-ai-blog-featured-images` has Claude Haiku 4.5 choose the visual idea and Seedream 5 Lite draw both images in one run.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-blog-featured-images` |
| `post_title` | The title exactly as published. It is the only text written on the share card |
| `post_summary` | Two to four sentences: what the post argues or teaches and what the reader gets. Up to 2,000 characters |
| `style_note` | The blog's shared look: medium (flat illustration, 3D clay, photo, collage), palette, mood, how busy. Same note for every post |
| Inside the app | Claude Haiku 4.5 writes one visual concept with no words in it; the hero carries no text, logos or UI; the share card is an edit of the hero with the title added, kept clear of the top and bottom 8% and 5% at the sides |
| Output | Two JPGs, both 16:9: `hero` (about 3072x1728, no text) and `share-card` (about 3416x1920, title on it, safe to crop to 1.91:1 / 1200x630) |
| Price | 23 credits per run: 10 per Seedream 5 Lite image plus 3 for the concept step (measured 28 Oct 2026) |

Send all three inputs every time. A missing one falls back to the board's saved demo text (an onboarding email post), which would leak into the images.

## A. Connection check

Look for tools ending in `run_app`, `get_execution`, `get_credit_balance` and `whoami`.

If they are missing, say it in one sentence and give the setup:

- With this plugin: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: custom connector, URL `https://www.wireflow.ai/api/mcp`.

Then hand over the free part from `reference/featured-image-guide.md`: a style note for their blog and a one-line concept brief per post. Stop there.

## B. Collect inputs

Ask once, in one message:

1. Which posts: a title and summary, a link to a draft, or the file itself. Several posts are fine; each is one run.
2. The blog's look: a few existing featured images described in words, brand colours, or "pick one for me".
3. Where the images go (WordPress, Ghost, Webflow, a static site), only so you can name the right fields when you hand them over.

If they give a whole draft, write the summary yourself and show it. Keep the style note in the conversation and reuse it word for word for every post, that is what keeps the set consistent.

## C. Prepare each post

Read `reference/featured-image-guide.md`, then for each post:

- Copy the title exactly. Over about 70 characters the card gets crowded; offer a shorter display title, but only change it with the person's okay.
- Write the summary around the reader's payoff, not the post's structure. Leave out numbers and names you do not want drawn.
- Draft or reuse the style note: medium, three colours, mood, and "plenty of empty space".

Show a small table (post, title, summary, style note) and let the person edit it.

## D. Quote and confirm

Call `whoami` and `get_credit_balance`, then: "3 posts x 23 credits = 69 credits for 6 images. Balance: 1,240." If the balance is short, stop and say so. Nothing renders before a yes to this table and this cost.

## E. Generate

One `run_app` per post:

```json
{ "slug": "skill-ai-blog-featured-images", "inputs": { "post_title": "The 15-Minute Friday Review That Keeps Our Remote Team in Sync", "post_summary": "...", "style_note": "..." } }
```

Poll `get_execution` every 5 seconds while the status is `PENDING`, `RUNNING` or `IN_PROGRESS`. The test run took under a minute (the share card waits for the hero). On `FAILED`, `CANCELLED` or `TIMEOUT`, stop that post and quote the error.

## F. Inspect, save, report

Save to `./wireflow-outputs/<YYYY-MM-DD>/blog-images/<post-slug>-hero.jpg` and `<post-slug>-share.jpg` with `curl -sSL -o <file> <output url>` or PowerShell `Invoke-WebRequest -Uri <url> -OutFile <file>`.

Check both before you call them done:

- Hero: no stray letters, fake logos or screens with writing; the idea fits the post; it still reads as a small card in a blog list.
- Share card: the title matches letter by letter, nothing else is written, and no word sits near the top or bottom edge (a 1200x630 crop trims about 3.5% off each).
- The set: same medium and palette as the earlier posts.

Name every miss per file. A redo is a new run at 23 credits after a yes.

Report a table (post, file, CDN link), the credits used (balance before minus after), and where each file goes: the hero as the featured image, the share card as the Open Graph / social image (Yoast, Rank Math, Ghost "Facebook card" and "X card", or an `og:image` tag). Offer:

- The next batch of posts with the same style note (one quote for the batch).
- The board in Wireflow, to change sizes or add a square card: `https://www.wireflow.ai/flow/cmvrj2yak0007l408zq5bfgfv?ref=skill-ai-blog-featured-images&utm_source=github&utm_medium=skill&utm_campaign=ai-blog-featured-images`

## Guardrails

- Spend only after a yes to the exact table and cost.
- No real people, celebrities, other brands' logos or fake screenshots; no charts with invented numbers.
- The share card shows the real title only, never a claim the post does not make.
- Keep keys and passwords out of prompts and files.
- When Wireflow refuses or a tool errors, quote the exact message and offer `send_feedback` if it exists.
