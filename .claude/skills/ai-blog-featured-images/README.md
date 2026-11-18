# AI Blog Featured Images for Claude Code

![Social share card with a peach clay clipboard and a teal check mark beside the post title in dark bold type](examples/friday-review-share-card.jpg)

| Hero image (no text) | Share card (title added) |
|---|---|
| ![Peach clay clipboard with a glowing teal check mark floating on a pale sage background](examples/friday-review-hero.jpg) | ![The same clipboard moved left with the title The 15-Minute Friday Review on the right](examples/friday-review-share-card.jpg) |

*One post, one run, both images. Made with this skill on 28 Oct 2026: Seedream 5 Lite, 23 credits for the pair. Inputs, receipt and honest notes in [examples](examples/EXAMPLES.md).*

Give Claude a blog post (title and summary, or the draft) and a note on how your blog looks. Claude prepares the inputs and quotes the credits; after your yes, one Wireflow app run picks a visual idea for the post, draws a clean 16:9 featured image with no text, then turns that same picture into a social share card with your title on it. Claude checks the spelling and the crop-safe margins and saves both files, ready for your CMS and your Open Graph tags. Reuse the style note and every post in the blog gets a matching pair.

No Wireflow connection? You still get a style note for your blog and a concept brief per post that a designer can build.

## Try it

```text
Make the featured image and share card for my post "The 15-Minute
Friday Review That Keeps Our Remote Team in Sync". Soft 3D clay look,
sage green and peach, calm and friendly.
```

Also triggered by: "blog header image", "featured image for this post", "og:image", "link preview image", "social share image", "cover images for my blog".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

The plugin brings the Wireflow skills and the connector; run `/mcp` → `wireflow` → sign in.

Only this skill: `npx skills add wireflowINC/skills --skill ai-blog-featured-images`, or copy `skills/ai-blog-featured-images` into `~/.claude/skills/`, then add the connector with `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (Claude.ai and Desktop: custom connector, same URL).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Without a shell you get the image links instead of saved files.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Credits

| What | Credits |
|---|---|
| Summary, style note, quote | 0 |
| One post: hero + share card | 23 (10 per Seedream 5 Lite image + 3 for the concept step, measured 28 Oct 2026) |
| Ten posts | 230, quoted once before the batch |

Wireflow's Free plan lets you build and browse and includes a first image after setup; regular rendering needs a paid plan, from US$24 a month.

## What it will not do

- Put words, logos or fake screenshots on the hero image: it stays text-free so it works in any theme.
- Render a true 1.91:1 file: both images are 16:9, and the share card keeps the title inside the 1200x630 crop area.
- Draw real people or other brands.
- Use your own photos as input yet: the app takes text only.

## Data

- The title, summary and style note go to Wireflow through the Wireflow MCP connector (`run_app`), as you.
- Images download from `cdn.wireflow.ai` into `./wireflow-outputs/`.
- No keys, scripts or other services.

## FAQ

### How much does it cost per blog post?

23 Wireflow credits per post for both images: 10 for each Seedream 5 Lite image and 3 for the step that picks the visual concept (measured 28 Oct 2026). Preparing the inputs is free, and Claude quotes the total and waits for your yes.

### Do I need a Wireflow account?

Yes, to render: a Wireflow account with credits, connected through the Wireflow MCP connector (sign-in, no keys). Without it you still get the style note and concept briefs.

### Which model makes the images?

Claude Haiku 4.5 inside the app turns your title and summary into one wordless visual concept, and Seedream 5 Lite draws the hero and then edits it into the share card, so both match.

### What sizes are the files, and where do they go?

Both are 16:9 JPGs (about 3072x1728 and 3416x1920). Use the hero as the featured image; use the share card as the Open Graph or social image, where a 1200x630 crop keeps the whole title. Files are saved to `./wireflow-outputs/<date>/blog-images/` with the CDN links in the report.

## In this folder

- `SKILL.md`: the procedure.
- `reference/featured-image-guide.md`: style notes that hold a set together, how to write the summary, concept patterns, sizes per platform and the free concept brief.
- `examples/`: the real run, both images and the inputs.

Powered by [node based image generation](https://www.wireflow.ai/node-based-image-generation?ref=skill-ai-blog-featured-images&utm_source=github&utm_medium=skill&utm_campaign=ai-blog-featured-images) on [Wireflow, the node-based AI workflow platform](https://www.wireflow.ai/features/best-node-based-ai-workflow-platform?ref=skill-ai-blog-featured-images&utm_source=github&utm_medium=skill&utm_campaign=ai-blog-featured-images). MIT licensed; renders use your Wireflow credits.
