---
name: ai-poster-generator
description: "AI poster generator in Claude Code and Claude with Ideogram 4.5 through Wireflow: a print-style event or promo poster in two portrait layouts. Give it the event or offer, the date, the venue, the call to action and the brand colors. Claude locks the exact wording with the person, checks weekday against date, quotes the credits and waits for a yes, then renders two 1728x2304 poster options with the same words in different layouts and saves both to ./wireflow-outputs. Use when someone asks for an event poster, a flyer, a gig or club night poster, a store promo or sale poster, a workshop or conference poster, or two poster layouts to show a client. Without the Wireflow connector it still writes the poster copy sheet and a layout brief a designer can build. For a short post in social sizes use ai-social-media-graphics; for an explainer with sections use ai-infographic-generator."
license: MIT
compatibility: "Generation needs the Wireflow MCP connector (https://www.wireflow.ai/api/mcp) and a Wireflow account with credits. Inputs are text only. Saving files needs a shell."
metadata:
  author: "Wireflow"
  version: "0.1.0"
  app-slug: "skill-ai-poster-generator"
---

# AI Poster Generator

A poster carries more facts than a social post: a headline, a day and time, an address, a way to book, sometimes a line of small print. One wrong digit and the print run is wasted. You (Claude) pin down every word with the person first. The Wireflow app `skill-ai-poster-generator` then sets those words twice with Ideogram 4.5, in two different portrait layouts, so the agency can send the client a choice.

## App contract

| Item | Value |
|---|---|
| App slug | `skill-ai-poster-generator` |
| `poster_text` | Every word on the poster, each piece labelled and in double quotes: Headline, Date, Venue, Call to action, optional Small print. Only quoted words get drawn |
| `brand_colors` | Background, headline and body text colors, hex codes when known |
| `style` | The look shared by both options: illustration or graphic style, type feel, texture |
| `layout_1` | Where the headline, artwork and details sit in option 1 |
| `layout_2` | A clearly different arrangement of the same words for option 2 |
| Fixed inside the app | Poster hierarchy (headline, then date, venue, call to action, small print), a 5 percent trim margin, no logos, no QR codes, no added words, MagicPrompt off |
| Output | Two PNGs, `poster-1` and `poster-2`, each 1728x2304 (3:4 portrait) |
| Price | 38 credits per run, 19 per poster (Ideogram 4.5, measured 3 Nov 2026) |

Fill in all five inputs on every run. An empty one falls back to the board's demo (a "Night Market" poster) and those words would end up on the client's poster.

3:4 is the only tall size Ideogram 4.5 offers next to 9:16. It sits between A-series paper (about 1:1.41) and US letter (1:1.29), so a printer trims a little top and bottom. The trim margin rule keeps text away from that edge.

## A. Connection check

Look for tools whose names end in `run_app`, `get_execution`, `get_credit_balance` and `whoami`.

If they are missing, say so in a sentence and give the setup:

- Plugin users: `/mcp` → `wireflow` → Authenticate.
- Plain Claude Code: `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp`, then `/mcp`.
- Claude.ai or Desktop: add a custom connector with the URL `https://www.wireflow.ai/api/mcp`.

Then give the free deliverable: the poster copy sheet and two layout briefs from `reference/poster-sheet.md`, filled in. Stop there.

## B. Collect the details

Ask in one message:

1. What is it: event, sale, launch, class? The headline as the client wants it.
2. When and where: weekday, date, start (and end) time, venue name and address.
3. What should people do: book, RSVP, visit, call? The exact URL or number.
4. Brand colors and the feel (elegant, loud, playful, retro), plus anything to avoid.

The app takes text only, so a logo file or a photo cannot go in; the brand name can appear as typed words. A price, discount or claim needs to come from the client.

## C. Lock the copy

Work from `reference/poster-sheet.md`:

- Headline at most 6 words. Whole poster at most 35 words. Fewer words, cleaner lettering.
- Check the weekday against the date and year before you quote. The app draws what it gets, mistakes included.
- Write URLs short and without `https://`. Spell addresses the way the client prints them.
- Five labelled pieces at most. Put each in double quotes inside `poster_text`.
- Write `style` once and two layout briefs that really differ (for example headline on top with centered art, versus a stacked headline on one side with details in a column).
- Show the final `poster_text` back to the person, word for word, and get it approved. Any later word change is a new run.

## D. Quote and wait

Call `whoami` and `get_credit_balance`, then say something like: "2 poster options x 19 credits = 38 credits. Balance: 1,240." For several events, multiply and list them. The app always makes both layouts, so one option costs the same as two. If the balance is too low, say so and stop. Nothing is rendered until the person says yes to these words and this price.

## E. Render

One `run_app` per approved poster:

```json
{ "slug": "skill-ai-poster-generator", "inputs": { "poster_text": "Headline: \"Rooftop Jazz Night\". Date: \"Saturday 21 November, 7pm\". Venue: \"The Linden Hotel Rooftop, 12 Mill Street\". Call to action: \"Book tickets at lindenhotel.co/jazz\". Small print: \"Live quartet, cocktails, 18+\".", "brand_colors": "Deep plum background (#3B1F3A), gold headline (#E8B04B), cream text (#F6EFE3).", "style": "Art deco music poster, elegant tall serif headline, thin gold line art of a saxophone and a city skyline, subtle paper grain.", "layout_1": "Headline large across the top third, saxophone line art centered in the middle, date, venue and call to action stacked and centered in the bottom third.", "layout_2": "Skyline line art along the bottom edge, headline set vertically stacked on the left half, date and venue in a right-hand column, call to action in a gold band near the foot." } }
```

Check `get_execution` every 5 seconds while the status is `PENDING`, `RUNNING` or `IN_PROGRESS`. The test run finished in about a minute. On `FAILED`, `CANCELLED` or `TIMEOUT`, stop and report the error as given.

## F. Proof, save, report

Save to `./wireflow-outputs/<YYYY-MM-DD>/posters/<event-slug>_layout-1.png` and `_layout-2.png` with `curl -sSL -o <file> <output url>`, or in PowerShell `Invoke-WebRequest -Uri <output url> -OutFile <file>`.

Open both posters and proof them like a print proof, against the approved `poster_text`:

- Every quoted piece is present, in the right order of size.
- Every letter, digit, time, address and URL matches exactly. Nothing extra is written.
- Letterforms are clean: no doubled, ghosted or overlapping letters. In the test, option 2 drew the "OO" of "ROOFTOP" with a faint shadow copy.
- Artwork does not cross the text. In the test, a loose line from the saxophone ran through the date and venue on option 2.
- Text stays clear of the outer 5 percent, for the trim.

List each miss per file. A fix is a new run of both layouts for 38 credits, after a yes. Do not call a poster print-ready while a miss is open; say which option is clean enough to send for approval.

End with a table (option, file, CDN link) and the credits spent (balance before minus after). Offer:

- The next event or a revised wording.
- The board in Wireflow, to change sizes or add a layout: `https://www.wireflow.ai/flow/cmw03q40r001ljh0782wdcjrh?ref=skill-ai-poster-generator&utm_source=github&utm_medium=skill&utm_campaign=ai-poster-generator`

## Guardrails

- Spend only after a yes to the exact words and the price.
- Never invent dates, prices, discounts, line-ups, sponsors or addresses.
- No third-party logos, artist likenesses or trademarks presented as endorsements.
- Never ask for or store keys or passwords.
- If Wireflow refuses or a tool errors, quote the message and offer `send_feedback` when it exists.
