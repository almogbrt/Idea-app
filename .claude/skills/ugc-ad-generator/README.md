# UGC Ad Generator for Claude Code

| Product photo | Generated creator still | Talking clip (click to play) |
|---|---|---|
| ![Input: canvas tote packshot on white](examples/input-tote-packshot.jpg) | ![Output: AI creator holding the tote in a selfie-style still](examples/creator-still.jpg) | [![Frame from the talking UGC clip, click to play](examples/ugc-video-poster.jpg)](https://cdn.wireflow.ai/84d63750-c2d5-11f1-9e92-2dd4e060cd9a.mp4) |

*Made with this skill on 8 Oct 2026: Seedream 5 Lite still, Veo 3.1 Lite 6 second 9:16 clip with sound, about 106 credits by list price. The creator is AI-generated. Script, receipt and notes in [examples](examples/EXAMPLES.md).*

Give Claude a product photo and who you sell to. It writes a few hooks and short spoken lines, describes a believable everyday creator, and quotes the credits. After your yes, a Wireflow app makes a selfie-style still of that creator holding your product and turns it into a 6 second vertical clip where they say the line, with sound. You get the still and the MP4, plus a reminder to label the creator as AI.

Not connected to Wireflow? You still get hooks, lines and creator briefs you can hand to a real creator.

## Try it

```text
Make a UGC ad for my canvas tote: https://example.com/tote.jpg
Audience: students and commuters. TikTok, casual, no discount.
```

Also triggered by: "UGC video ad", "talking head ad", "creator-style ad", "TikTok UGC", "UGC ad generator".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

Then `/mcp` → `wireflow` → sign in. This installs every Wireflow skill and the connector.

This skill only: `npx skills add wireflowINC/skills --skill ugc-ad-generator`, or copy `skills/ugc-ad-generator` into `~/.claude/skills/`, then `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (Claude.ai and Desktop: custom connector with that URL).

## Works with

- **Claude Code**: where this skill is built to run. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. Saving files needs a shell, so there you get the video link instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. Rendering needs that agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Cost

| Step | Credits |
|---|---|
| Hooks, lines, creator brief, quote | 0 |
| One clip (still + 6 s talking video) | About 106 by Wireflow list price (8 Oct 2026); quoted as up to about 225 until re-measured |
| Another take | The same again, only with your yes |

Our test run's balance drop was 224 credits, but other jobs were spending on the same account during the run, so the skill quotes the list price and warns that it may be higher. Wireflow's Free plan covers building and browsing plus a first image after setup; video needs a paid plan, from US$24 a month.

## Honest by design

- The creator is AI. Label the ad as AI-generated where your platform asks, and never present it as a real customer testimonial.
- No real people, celebrities or influencer look-alikes; no invented results or reviews.
- Lines are short and true to the product.

## Sent and fetched

- Product photo URL, creator description and spoken line go to Wireflow through the Wireflow MCP connector (`run_app`), as you.
- The still and MP4 download from `cdn.wireflow.ai` to `./wireflow-outputs/`.
- No keys, no scripts, no other services.

## FAQ

### Is the creator a real person?

No. The creator is AI-generated from a written description. Label the ad as AI-generated where your platform asks for it, and never present it as a real customer testimonial.

### How long is the video?

One 6 second vertical clip (9:16, 720x1280) with spoken sound, plus the selfie-style still it was made from.

### What does a UGC ad cost with this skill?

About 106 Wireflow credits per clip by list price on 8 Oct 2026: 10 for the still and 16 per second for 6 seconds of video. Our one test run showed a 224 credit drop while other jobs were spending on the same account, so the skill quotes about 106 and warns it can reach about 225 until a clean run confirms it.

### Can it copy a real person or use my face?

No. It will not imitate a real person, a celebrity or a specific influencer, and it is not for cloning a real person.

### Do I need a Wireflow account?

Only to render. Without one you still get hooks, spoken lines and creator briefs you can hand to a real creator.

## Folder contents

- `SKILL.md`: the procedure.
- `reference/ugc-scripts.md`: hook patterns, writing rules, creator briefs by audience, disclosure.
- `examples/`: the real input, still, clip frames and inputs.

Powered by the [Wireflow AI video workflow](https://www.wireflow.ai/features/ai-video-workflow?ref=skill-ugc-ad-generator&utm_source=github&utm_medium=skill&utm_campaign=ugc-ad-generator). Connector guide: [Wireflow MCP docs](https://www.wireflow.ai/docs/mcp?ref=skill-ugc-ad-generator&utm_source=github&utm_medium=skill&utm_campaign=ugc-ad-generator). MIT licensed; renders use your Wireflow credits.
