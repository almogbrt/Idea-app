# Real run

Made by this skill's Wireflow app (`skill-wan-3-0-product-video`, Wan 3.0, 720p setting, 5 seconds, sound on) on 16 October 2026. The MP4 stays on the Wireflow CDN; this folder keeps the start frame, a poster frame and a frame strip, all 1280px or less.

## Start frame

![Start frame: a lit Tavrin candle on a stone shelf](start-frame-candle.jpg)

A 1024x1024 photo of a candle from a fictional brand, made earlier by the brand-consistent-images skill test: https://cdn.wireflow.ai/gemini-f010eda6-fd25-4a94-98ae-59581dc1f234.jpg

## Candle push-in with sound

[![Wan 3.0 candle clip at the end of the push-in, click to play](candle-push-in-poster.jpg)](https://cdn.wireflow.ai/de09ddc0-c8f4-11f1-bb62-0520a10573d1.mp4)

![Five frames across the Wan 3.0 candle clip, one per second](candle-push-in-frames.jpg)

- `product_photo`: https://cdn.wireflow.ai/gemini-f010eda6-fd25-4a94-98ae-59581dc1f234.jpg
- `shot_and_sound`: Slow push-in toward the lit Tavrin candle on the stone shelf, the flame flickers gently and the wick crackles softly, warm afternoon light drifts slowly across the wall, quiet room tone.
- Output: 960x960 MP4, 5.0 s, 30 fps, stereo AAC sound track, https://cdn.wireflow.ai/de09ddc0-c8f4-11f1-bb62-0520a10573d1.mp4
- Execution: `fd5e1ede-e2a9-43b9-80c1-9e739d9daf4a`
- Render time: about 2.5 minutes (the Wan node ran 152 seconds).
- Credits: 58, the charge Wireflow's credit history shows for this run (`Wan V3.0 I2v`, 2026-10-15T23:59:54Z UTC), equal to Wireflow's own estimate for the node. The account balance fell 170 across the run because another job's seven Nano Banana Lite images were charged in the same minutes; the history shows each charge separately.
- Honest notes: the camera pushed in smoothly and the jar, lid, label, logo and "TAVRIN CANDLE CO." text stayed the same in every frame; the flame moved, nothing warped and no second product appeared. The square photo gave a square clip. The sound track is real (mean volume -35.6 dB, peaks -4.1 dB), but we only measured it and did not judge by ear whether it is a wick crackle or room tone.

## How this was run

The Wireflow Apps API (`POST /api/v1/apps/skill-wan-3-0-product-video/execute`), the same code path as the MCP `run_app` tool. The execution id above matches `testReceipt.executionId` in the queue item.
