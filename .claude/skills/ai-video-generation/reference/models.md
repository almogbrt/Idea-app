# Which video model for which job

Credits per second of video from Wireflow's public price list, checked on 8 October 2026 (1 credit = US$0.01). Wireflow notes these rates are measured on a 5 second run; shorter clips can cost a little more per second. `list_models` in Wireflow returns the current prices.

This skill's app uses **MiniMax Hailuo 03 Max Turbo**: fast, cheap, text or first frame, 5 seconds at 768P cost 40 credits in our test. The board can be duplicated in Wireflow and switched to any model below.

| Job | Good pick | Credits per second | Notes |
|---|---|---|---|
| Cheap, quick text or image to video | MiniMax Hailuo 03 Max Turbo | 8 | 480P or 768P, up to 15 s, start and end frame |
| Budget clips with sound | Pixverse v6 | 9 | 360p to 1080p, optional audio |
| Fun, stylized, with audio | Grok Imagine Video | 10 | 480p or 720p |
| Higher quality from a start frame | Kling O3 | 16 | Start frame required |
| Affordable Google model with audio | Veo 3.1 Lite | 16 | Text to video with sound |
| Video from text, images or video, with audio | Gemini Omni Flash 1.1 | 16 | Also edits an existing clip |
| Strong all-rounder, start and end frames | Seedance 2.0 | 17 | 480p to 1080p, 4 to 30 s |
| Reference-driven, consistent characters | Seedance 2.5 | 26 | Up to 8 reference images or videos |
| Premium cinematic with audio | Veo 3.1 | 64 | Highest cost in this list |

## Rules of thumb

- **Generate at the real length you need.** Rendering long and trimming wastes credits.
- **Test the shot cheaply first.** Prove the idea on an 8 to 10 credit per second model, then re-render the winner on a premium one if it needs it.
- **Keep identity across shots** by starting every clip from the same still (make it with the ai-image-generation skill) or by using a reference-based model like Seedance 2.5.
- **Upscale at the end**, only for the final cut (video upscalers start at 4 credits per second).
