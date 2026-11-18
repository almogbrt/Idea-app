# Real run

Rendered by this skill's Wireflow app (`skill-ecommerce-product-video`, MiniMax Hailuo 03 Max Turbo, 768P) on 8 October 2026. The MP4 stays on the Wireflow CDN; this folder keeps a poster frame and a frame strip.

## First frame

![Serum bottle on white](input-first-frame.jpg)

The main image made by the amazon-product-images skill test: https://cdn.wireflow.ai/e7ce0550-c2d4-11f1-9e92-2dd4e060cd9a.jpg

## Half orbit

[![Serum bottle mid-orbit, click to play](serum-orbit-poster.jpg)](https://cdn.wireflow.ai/250a9870-c2d5-11f1-9e92-2dd4e060cd9a.mp4)

![Six frames across the clip](serum-orbit-frames.jpg)

- `motion`: Slow half orbit around the serum bottle from left to right at bottle height, soft studio light glides across the frosted glass, a gentle highlight travels down the dropper, background stays clean white, calm and premium.
- Output: 768x768 MP4, 6.6 s, with an audio track, https://cdn.wireflow.ai/250a9870-c2d5-11f1-9e92-2dd4e060cd9a.mp4
- Execution: `7ed0061e-3e2e-4442-a780-ea77abb37d31`
- Credits: 48 (account balance before minus after)
- Ready in about 15 seconds.
- Honest notes: the app is set to 9:16, but with a first frame the model followed the square photo and returned a square clip; the skill now tells people to start from a photo in the shape they want. The bottle shape and cap stayed stable across the frames. Audio was not reviewed.

The run used the Wireflow Apps API (`POST /api/v1/apps/skill-ecommerce-product-video/execute`), the same code path as the MCP `run_app` tool.
