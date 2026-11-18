# AI Background Music Generator for Claude Code

| Track | Listen | Original |
|---|---|---|
| 1 | [Listen to the first take](examples/water-bottle-ad-track-1.mp3) | https://cdn.wireflow.ai/dd72d3f0-d1b2-11f1-8659-5b834f32614a.mp3 |
| 2 (different lead and melody) | [Listen to the second take](examples/water-bottle-ad-track-2.mp3) | https://cdn.wireflow.ai/ea692820-d1b2-11f1-8659-5b834f32614a.mp3 |

*Made with this skill on 27 Oct 2026 for a 30 second UGC water bottle ad (gym, then a hike): bright, confident indie pop with acoustic guitar, claps and soft pads. 43 credits for both tracks. GitHub cannot play audio in the page, so the links open the MP3s. Receipt in [examples](examples/EXAMPLES.md).*

Your footage is cut; it needs a music bed. Tell Claude the mood, the style, how long the video is and what it shows. Claude turns that into a music brief and quotes the credits. After your yes, a Wireflow app writes an instrumental prompt and Google Lyria 3 Pro makes two different takes, so you can drop each under the video and keep the one that fits.

Not connected to Wireflow? You still get the brief and two ready prompts for any music tool.

## Try it

```text
Background music for my 20 second Reels ad: a candle being lit in a dark room,
calm and premium, soft piano and pads, a voiceover on top.
```

Also triggered by: "music bed for my TikTok ad", "instrumental track for a product demo", "royalty free style music for a UGC video", "two music options to test under this clip".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

Then `/mcp` → `wireflow` → sign in. That installs the Wireflow skills and the connector.

Only this skill: `npx skills add wireflowINC/skills --skill ai-background-music`, or copy `skills/ai-background-music` into `~/.claude/skills/`, then `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (Claude.ai and Desktop: a custom connector with that URL).

## Works with

- **Claude Code**: the home of this skill. Install the plugin or use the skills CLI.
- **Claude.ai and Claude Desktop**: add Wireflow as a custom connector. With no shell to save files, you get the MP3 links instead.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI can install it. Making audio needs the agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Cost

| Step | Credits |
|---|---|
| Brief and quote | 0 |
| Two instrumental tracks | 43, measured on 27 Oct 2026 (3 for the music prompt, 20 per Lyria 3 Pro track) |
| Another run | Quoted again, only with your yes |

## Honest by design

- Lyria 3 Pro has no length setting. The brief asks for your length, but takes can run longer; in our test a 30 second brief gave about 40 seconds and just over a minute. Trim in your editor.
- The app asks for instrumental music only, but nobody can promise a model never adds a voice. Listen before you publish.
- No "in the style of" a real artist or song. Lyria output carries a SynthID watermark.

## Sent and fetched

- The mood, genre, length and video description go to Wireflow through the Wireflow MCP connector (`run_app`), as you.
- The two MP3s download from `cdn.wireflow.ai` to `./wireflow-outputs/`.
- No keys, no scripts, no other services.

## FAQ

### What does a background music track cost with this skill?

43 Wireflow credits for two tracks in our 27 Oct 2026 test: 3 for writing the music prompt and 20 for each Lyria 3 Pro track. The skill quotes before anything runs.

### Which model makes the music?

Claude Haiku 4.5 turns your brief into one instrumental prompt, then Google Lyria 3 Pro renders it twice, the second time with a different lead instrument and melody.

### Do I need a Wireflow account?

Only to make the audio. Without one you still get the music brief and two prompts for any text-to-music tool.

### Where do the files go?

Into `./wireflow-outputs/<date>/music/` in your project, one MP3 per track. The CDN links are in the report too.

### Can it make the video or a voiceover too?

No, it makes only the music bed for footage you already have. For the video use ai-video-generation; for a voice track use ai-voiceover-for-ugc-ads.

## Folder contents

- `SKILL.md`: the procedure.
- `reference/music-brief.md`: the brief, mood and tempo by footage, voice-friendly beds and the free prompt pack.
- `examples/`: the two real tracks from the test run and the receipt.

Powered by the [Wireflow AI video workflow](https://www.wireflow.ai/features/ai-video-workflow?ref=skill-ai-background-music&utm_source=github&utm_medium=skill&utm_campaign=ai-background-music). Connector guide: [Wireflow MCP docs](https://www.wireflow.ai/docs/mcp?ref=skill-ai-background-music&utm_source=github&utm_medium=skill&utm_campaign=ai-background-music). MIT licensed; audio uses your Wireflow credits.
