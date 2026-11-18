# AI Sound Effects Generator for Claude Code

| Effect | Listen | Original |
|---|---|---|
| Whoosh, push-in to the flame | [Listen to the whoosh](examples/candle-ad-whoosh.mp3) | https://cdn.wireflow.ai/59510a70-d40e-11f1-a7cd-adbf9b234f3a.mp3 |
| Pop, 15% off sticker | [Listen to the pop](examples/candle-ad-pop.mp3) | https://cdn.wireflow.ai/59e88f80-d40e-11f1-a7cd-adbf9b234f3a.mp3 |
| Click, lighter strike | [Listen to the click](examples/candle-ad-click.mp3) | https://cdn.wireflow.ai/59e50d10-d40e-11f1-a7cd-adbf9b234f3a.mp3 |
| Ambience, rainy living room (loops) | [Listen to the ambience](examples/candle-ad-ambience.mp3) | https://cdn.wireflow.ai/5a896360-d40e-11f1-a7cd-adbf9b234f3a.mp3 |

*Made with this skill on 30 Oct 2026 for a 15 second soy candle ad (a wick lit in a wooden living room at night, push-in on the flame, a sale sticker). 19 credits for all four. GitHub does not play audio in the page, so the links open the MP3s. Receipt in [examples](examples/EXAMPLES.md).*

A silent cut feels cheap; a few small sounds make an ad feel finished. Describe your clip and point at the moments: the swipe, the badge, the tap, the room. Claude writes the cues and quotes the credits. After your yes, a Wireflow app sets one sound world for the scene and ElevenLabs Sound Effects makes a whoosh, a pop, a click and a looping ambience that all fit it, ready to drop on your timeline.

No Wireflow connection? You still get the cue sheet and four prompts for any sound effects tool.

## Try it

```text
Sound effects for my 20 second TikTok ad: unboxing wireless earbuds on a desk,
a swipe to the close-up, the case lid snaps shut, a "new" badge appears.
```

Also triggered by: "whoosh for my transitions", "pop sound for the price badge", "SFX pack for a UGC ad", "room tone under my product video".

## How to install

```text
/plugin marketplace add wireflowINC/skills
/plugin install wireflow-skills@wireflow
```

Then `/mcp` → `wireflow` → sign in. That adds the Wireflow skills and the connector together.

Just this skill: `npx skills add wireflowINC/skills --skill ai-sound-effects-for-video-ads`, or copy `skills/ai-sound-effects-for-video-ads` into `~/.claude/skills/`, then `claude mcp add --transport http wireflow https://www.wireflow.ai/api/mcp` (Claude.ai and Desktop: a custom connector with that URL).

## Works with

- **Claude Code**: where this skill is built and tested. Use the plugin or the skills CLI.
- **Claude.ai and Claude Desktop**: connect Wireflow as a custom connector. There is no shell to save files, so you get the four MP3 links.
- **Cursor, Codex and other agents that read `SKILL.md`**: the skills CLI installs it there. The effects need the agent connected to the Wireflow MCP server; we have not tested those agents ourselves.

## Cost

| Step | Credits |
|---|---|
| Cue sheet and quote | 0 |
| Four sound effects | 19, measured on 30 Oct 2026 (3 for the sound world line, 4 per effect) |
| A rerun | Quoted again, only with your yes |

## Honest by design

- The lengths are fixed in the app: whoosh 1.5 s, pop 1 s, click 1 s, ambience 6 s. Loop the ambience for longer clips.
- One run makes the whole pack of four. Redoing just the click still reruns all four (and costs the same).
- Claude cannot hear the files. Listen before you publish.
- No copies of trademarked sounds (famous chimes, game or film effects).

## Sent and fetched

- The scene and the four moments go to Wireflow through the Wireflow MCP connector (`run_app`), as you.
- The four MP3s download from `cdn.wireflow.ai` to `./wireflow-outputs/`.
- No keys, no scripts, no other services.

## FAQ

### How much does a pack of sound effects cost?

19 Wireflow credits for four effects in our 30 Oct 2026 test: 3 to write the shared sound world and 4 for each effect. Claude quotes first and waits for your yes.

### Which model makes the sounds?

ElevenLabs Sound Effects v2, run inside Wireflow. Claude Haiku 4.5 first writes one sound world line from your scene so the four effects match.

### Do I need a Wireflow account?

Only for the audio files. Without one you still get the cue sheet and four prompts to paste into any text-to-sound-effects tool.

### Where do the files go?

Into `./wireflow-outputs/<date>/sfx/` in your project, one MP3 per effect. The CDN links are in the report as well.

### Can it make music or a voiceover?

No, only short spot effects and room tone. For a music bed use ai-background-music; for speech use ai-voiceover-for-ugc-ads.

## Folder contents

- `SKILL.md`: the procedure.
- `reference/sfx-cue-sheet.md`: the cue sheet, which moment gets which effect, sound worlds by footage, mixing tips and the free prompt pack.
- `examples/`: the four real effects from the test run and the receipt.

Powered by the [Wireflow AI video workflow](https://www.wireflow.ai/features/ai-video-workflow?ref=skill-ai-sound-effects-for-video-ads&utm_source=github&utm_medium=skill&utm_campaign=ai-sound-effects-for-video-ads). Connector guide: [Wireflow MCP docs](https://www.wireflow.ai/docs/mcp?ref=skill-ai-sound-effects-for-video-ads&utm_source=github&utm_medium=skill&utm_campaign=ai-sound-effects-for-video-ads). MIT licensed; audio uses your Wireflow credits.
