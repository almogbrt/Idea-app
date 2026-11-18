# Real run

One run of this skill's Wireflow app (`skill-ai-thumbnail-maker`, three Ideogram 4.5 nodes at 2560x1440) on 15 October 2026. The files here are downscaled to 1280x720; the originals are on the Wireflow CDN.

## Inputs

- `video_title`: I Tried Cold Plunging Every Day for 30 Days
- `headline`: DAY 30 SHOCKED ME
- `concept_1`: Close-up of a man in his 30s with a shocked face, shoulders deep in an ice bath full of ice cubes, breath steaming, cold blue light, headline in huge white letters with a black outline on the left.
- `concept_2`: Split screen: left side a tired man on day 1 under grey light, right side the same man energized on day 30 in warm sunrise light, a red arrow between them, headline in bold yellow letters across the top.
- `concept_3`: A frosted steel tub of ice water on a snowy deck at dawn, a big red circle around a thermometer reading near freezing, minimal and clean, headline in heavy white letters on a dark blue band at the top.

Execution: `4095810e-11fe-4a1f-8b42-ccd184f128ef`. Credits: 57 for the three images (account balance 4,980 before, 4,923 after). Time: about 25 seconds.

## Results

| Angle | Thumbnail | Original |
|---|---|---|
| Reaction face | ![Shocked man in an ice bath with the headline DAY 30 SHOCKED ME in white](cold-plunge-reaction.jpg) | https://cdn.wireflow.ai/1cb8daf0-c858-11f1-9610-b9bcacd1d965.png |
| Before and after | ![Split screen of a tired man and the same man smiling at sunrise under a yellow headline](cold-plunge-before-after.jpg) | https://cdn.wireflow.ai/1c1c25c0-c858-11f1-9610-b9bcacd1d965.png |
| Circle the detail | ![Frosted ice tub with a red circle around a thermometer below a dark blue headline band](cold-plunge-thermometer.jpg) | https://cdn.wireflow.ai/1c22b570-c858-11f1-9610-b9bcacd1d965.png |

Honest notes: the headline is spelled correctly in all three and no other words appear. The before and after version has a stray black brush mark above the right-hand face, and the thermometer in the third one has an unreadable scale that does not clearly show freezing. Both are the kind of miss the skill's inspection step flags before delivery.

The run used the Wireflow Apps API (`POST /api/v1/apps/skill-ai-thumbnail-maker/execute`), the same code path as the MCP `run_app` tool.
