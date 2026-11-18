# Real run

One run of this skill's Wireflow app (`skill-ai-background-music`: Run any LLM with Claude Haiku 4.5 writes the instrumental music prompt, then Lyria 3 Pro makes two tracks) on 27 October 2026. The MP3s here are re-encoded preview copies (128 kbps, cut at 60 seconds at most); the full originals are on the Wireflow CDN.

## Inputs

- `mood`: Bright, confident and warm, like a sunny morning routine.
- `genre`: Indie pop with acoustic guitar, light claps and soft synth pads.
- `length`: 30 seconds
- `video_context`: A 30 second UGC ad for a reusable water bottle: a creator talks to camera at the gym, then on a hike.

## Outputs

| Track | File | Original |
|---|---|---|
| 1 | [Listen to track 1](water-bottle-ad-track-1.mp3) | https://cdn.wireflow.ai/dd72d3f0-d1b2-11f1-8659-5b834f32614a.mp3 |
| 2 (different lead and melody) | [Listen to track 2](water-bottle-ad-track-2.mp3) | https://cdn.wireflow.ai/ea692820-d1b2-11f1-8659-5b834f32614a.mp3 |

- Execution: `606cc4ce-160e-47f4-b94d-ade20dea655b`
- Credits: 43, from `GET /credits/history`: Openrouter Router 3, then two Lyria3 Pro charges of 20. The balance went from 7,480 to 7,437.
- Length: the brief asked for 30 seconds. Judging by file size, track 2 is roughly 40 seconds and track 1 just over a minute (the copy here stops at 60 seconds). Trim to your cut.
- Checked: the run completed and both tracks came back as MP3s on the Wireflow CDN.
- Not checked: how they sound, or that they are free of vocals. Nobody has listened to them yet.

The run used the Wireflow Apps API (`POST /api/v1/apps/skill-ai-background-music/execute`), the same code path as the MCP `run_app` tool.
