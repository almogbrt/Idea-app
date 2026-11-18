# Real run

One UGC clip made by this skill's Wireflow app (`skill-ugc-ad-generator`: Seedream 5 Lite still, then Veo 3.1 Lite image-to-video with audio) on 8 October 2026. Files here are downscaled; originals are on the Wireflow CDN. The person is AI-generated.

## Product photo

![Canvas tote packshot](input-tote-packshot.jpg)

A packshot made in the bulk-image-generation skill test: https://cdn.wireflow.ai/b1f03200-c2d4-11f1-9e92-2dd4e060cd9a.jpg

## Inputs

- `creator`: A friendly woman in her late 20s with curly dark hair and a denim jacket, sitting on a sofa in a bright apartment with plants, relaxed and smiling, holding the tote bag up beside her face.
- `line`: "Okay, this tote fits my laptop, my gym clothes and my lunch. Finally, one bag."

## Outputs

| Stage | Preview | Original |
|---|---|---|
| Selfie still (1920x3416) | ![AI creator holding the canvas tote, selfie-style still](creator-still.jpg) | https://cdn.wireflow.ai/66e71980-c2d5-11f1-9e92-2dd4e060cd9a.jpg |
| Talking clip (720x1280, 6 s, audio) | [![Frame from the talking clip, click to play](ugc-video-poster.jpg)](https://cdn.wireflow.ai/84d63750-c2d5-11f1-9e92-2dd4e060cd9a.mp4) | https://cdn.wireflow.ai/84d63750-c2d5-11f1-9e92-2dd4e060cd9a.mp4 |

![Six frames across the clip](ugc-video-frames.jpg)

- Execution: `ad783c09-288a-4201-bb1a-c6ae2f5f20c9` (about 90 seconds end to end)
- Credits: about 106 by Wireflow's list price (Seedream 5 Lite 10 + Veo 3.1 Lite 16 per second x 6). The account balance dropped 224 during the run, but other jobs were spending on the same account at the time (it dropped about 200 more in the next 15 minutes with no skill runs), so 224 is an upper bound, not a clean measurement. The execution log shows one Seedream call and one Veo 3.1 Lite image-to-video call, no retries.
- Checks done: the tote matches the input (cream canvas, olive straps); the face and bag stay stable across the frame strip; the audio track is continuous speech-level sound (mean -19.9 dB).
- Not checked: the exact spoken words and lip sync. Nobody has listened to it yet.

The run used the Wireflow Apps API (`POST /api/v1/apps/skill-ugc-ad-generator/execute`), the same code path as the MCP `run_app` tool.
