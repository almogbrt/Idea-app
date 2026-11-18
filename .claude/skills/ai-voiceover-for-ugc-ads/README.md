# AI Voiceover for UGC Ads for Claude Code

| Take | Voice | Listen | Original |
|---|---|---|---|
| 1 | Lively_Girl (bright female) | [Listen to take 1](examples/take-1-lively-girl.mp3) | https://cdn.wireflow.ai/b1964a10-d0e9-11f1-b524-212f547bd4a8.mp3 |
| 2 | Casual_Guy (relaxed male) | [Listen to take 2](examples/take-2-casual-guy.mp3) | https://cdn.wireflow.ai/b1942730-d0e9-11f1-b524-212f547bd4a8.mp3 |
| 3 | Calm_Woman (calm female) | [Listen to take 3](examples/take-3-calm-woman.mp3) | https://cdn.wireflow.ai/b10bbd50-d0e9-11f1-b524-212f547bd4a8.mp3 |

*Made with this skill on 26 Oct 2026 from the script "Okay, this tote fits my laptop, my gym clothes AND my lunch!!! Finally... one bag. 20% off this week." The app read it as "Okay, this tote fits my laptop, my gym clothes, and my lunch. Finally, one bag. Twenty percent off this week." About 8.5 seconds a take, 51 credits for all three. GitHub cannot play audio in the page, so the links open the MP3s. Receipt in [examples](examples/EXAMPLES.md).*

You have the footage; you need the voice. Paste your ad script and say how long the clip is. Claude trims it to fit, rewrites anything that is awkward to say out loud, and quotes the credits. After your yes, a Wireflow app reads it in three different voices and you get three MP3 takes to drop under the video and A/B test.

Not connected to Wireflow? You still get the spoken script, a timing check and a direction sheet for a human voice actor.

## Try it

```text
Voiceover for my 10 second TikTok ad, casual and upbeat:
"Our tote has a padded 15" laptop sleeve & water-resistant canvas. 20% off this week!"
```

Also triggered by: "voice over for my Reels ad", "text to speech for an ad script", "AI voice actor", "narration for product footage", "three voice takes to test".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

Then `/mcp` → `wireflow` → sign in. That installs the Wireflow skills and the connector.

Only this skill: `npx skills add wireflowINC/skills --skill ai-voiceover-for-ugc-ads`, or copy `skills/ai-voiceover-for-ugc-ads` into `~/.claude/skills/`, then `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (Claude.ai and Desktop: a custom connector with that URL).

## Works with

- **Claude Code**: the home of this skill. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. There is no shell to save files, so you get the MP3 links instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI can install it. Making audio needs the agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Cost

| Step | Credits |
|---|---|
| Script fit, timing, quote | 0 |
| Three takes of a short script (about 20 words, 8.5 s) | 51, measured on 26 Oct 2026 (3 for the rewrite, 16 a take) |
| Longer scripts | Wireflow lists Minimax Speech 02 HD at 3 credits per second of speech, so the skill quotes up to about 3 + 9 per second |
| Another run | Quoted again, only with your yes |

## Honest by design

- Your names, numbers and offer stay as written; the rewrite adds no claims.
- The voices are synthetic. Label the ad where your platform asks, and do not present the voice as a real customer.
- No copies of real people's or celebrities' voices.

## Sent and fetched

- The script, tone and language go to Wireflow through the Wireflow MCP connector (`run_app`), as you.
- The three MP3s download from `cdn.wireflow.ai` to `./wireflow-outputs/`.
- No keys, no scripts, no other services.

## FAQ

### What does an AI voiceover cost with this skill?

51 Wireflow credits for three takes of a short script in our 26 Oct 2026 test: 3 for the spoken rewrite and 16 for each take of about 8.5 seconds. Wireflow lists Minimax Speech 02 HD at 3 credits per second, so longer scripts are quoted higher before anything runs.

### Which model and voices does it use?

Claude Haiku 4.5 for the spoken rewrite, then Minimax Speech 02 HD in three fixed voices: Lively_Girl (bright female), Casual_Guy (relaxed male) and Calm_Woman (calm female). To change voices, open the board in Wireflow.

### Do I need a Wireflow account?

Only to make the audio. Without one you still get the spoken script, the timing and a direction sheet for a voice actor or another tool.

### Where do the files go?

Into `./wireflow-outputs/<date>/voiceover/` in your project: one MP3 per take plus the spoken script as a text file. The CDN links are in the report too.

### Can it make the video as well?

No, it makes only the voice track for footage you already have. For a full ad with an AI creator talking on camera, use the ugc-ad-generator skill.

## Folder contents

- `SKILL.md`: the procedure.
- `reference/voiceover-direction.md`: word budgets, sayable-script rules, tone lines and the direction sheet.
- `examples/`: the three real takes from the test run and the receipt.

Powered by the [Wireflow AI video workflow](https://www.wireflow.ai/features/ai-video-workflow?ref=skill-ai-voiceover-for-ugc-ads&utm_source=github&utm_medium=skill&utm_campaign=ai-voiceover-for-ugc-ads). Connector guide: [Wireflow MCP docs](https://www.wireflow.ai/docs/mcp?ref=skill-ai-voiceover-for-ugc-ads&utm_source=github&utm_medium=skill&utm_campaign=ai-voiceover-for-ugc-ads). MIT licensed; audio uses your Wireflow credits.
