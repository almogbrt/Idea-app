# Real run

One run of this skill's Wireflow app (`skill-ai-sound-effects-for-video-ads`: Run any LLM with Claude Haiku 4.5 writes the shared sound world line, then ElevenLabs Sound Effects v2 makes four effects) on 30 October 2026. The MP3s here are re-encoded preview copies at 128 kbps; the originals are on the Wireflow CDN.

## Inputs

- `scene`: A 15 second product ad for a hand-poured soy candle: a hand lights the wick in a cosy wooden living room at night, the camera pushes in on the flame, then the label and a 15% off sticker appear.
- `whoosh_moment`: Quick push-in from the wide shot of the room to the close-up of the candle flame.
- `pop_moment`: The 15% off sticker pops onto the corner of the screen.
- `click_moment`: The lighter clicks once to strike the flame.
- `ambience_moment`: A quiet cosy living room at night: soft rain on the window and a faint crackle of the wick.

## Outputs

| Effect | File | Original |
|---|---|---|
| Whoosh (1.5 s) | [Listen to the whoosh](candle-ad-whoosh.mp3) | https://cdn.wireflow.ai/59510a70-d40e-11f1-a7cd-adbf9b234f3a.mp3 |
| Pop (1 s) | [Listen to the pop](candle-ad-pop.mp3) | https://cdn.wireflow.ai/59e88f80-d40e-11f1-a7cd-adbf9b234f3a.mp3 |
| Click (1 s) | [Listen to the click](candle-ad-click.mp3) | https://cdn.wireflow.ai/59e50d10-d40e-11f1-a7cd-adbf9b234f3a.mp3 |
| Ambience (6 s, loops) | [Listen to the ambience](candle-ad-ambience.mp3) | https://cdn.wireflow.ai/5a896360-d40e-11f1-a7cd-adbf9b234f3a.mp3 |

- Execution: `f223b32c-26e7-4b98-9ff7-26f86cdf267f`
- Credits: 19, from `GET /credits/history`: Openrouter Router 3, then four Elevenlabs Sound Effects charges of 4 each. The balance went from 4,492 to 4,473.
- Lengths: by file size at 128 kbps, about 1.5, 1, 1 and 6 seconds, matching the app settings.
- Checked: the run completed and all four effects came back as MP3s on the Wireflow CDN.
- Not checked: how they sound. Nobody has listened to them yet.

The run used the Wireflow Apps API (`POST /api/v1/apps/skill-ai-sound-effects-for-video-ads/execute`), the same code path as the MCP `run_app` tool.
