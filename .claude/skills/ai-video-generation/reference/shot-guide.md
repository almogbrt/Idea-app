# Shot guide for AI video

Use it with any text-to-video or image-to-video model. The skill's Wireflow app renders 5 second 16:9 clips with MiniMax Hailuo 03 Max Turbo.

## One shot, one idea

A 5 second clip holds one beat. Write it like a line in a shot list:

> **[subject + look]** **[one action]**. **[camera move]**. **[light and place]**. **[style]**.

Example (the prompt behind this skill's README clip):

> A small paper boat drifts across a rain puddle on a city street at night. Slow dolly-in at ground level. Neon shop signs in pink and teal reflect and ripple in the water, light rain falls, shallow depth of field, cinematic, moody.

## Camera moves that models understand

| Move | What it does | Good for |
|---|---|---|
| Static / locked-off | Camera does not move | Product, talking, calm moments |
| Slow dolly-in / push-in | Camera moves toward the subject | Drama, reveal of detail |
| Dolly-out / pull-back | Camera moves away | Reveal the setting, endings |
| Pan left / right | Camera turns sideways | Landscapes, following motion |
| Tilt up / down | Camera turns vertically | Tall subjects, reveals |
| Orbit / arc | Camera circles the subject | Products, hero moments |
| Tracking / follow | Camera moves alongside a moving subject | People walking, cars, animals |
| Crane up / drone rise | Camera lifts and looks down | Openers, scale |
| Handheld | Slight natural shake | UGC feel, documentary |

Name one move. Two moves in five seconds usually look chaotic.

## Motion that fits 5 seconds

| Too much | Fits |
|---|---|
| A chef cooks a full meal | A chef flips vegetables in a pan once, flames rise |
| A woman walks through the city | A woman steps out of a doorway into the sun and squints |
| A car drives across the country | A car passes the camera on a wet road at dusk |
| A flower grows and blooms | A flower bud opens in time-lapse |

## Image to video

When you send a start image, the look is already decided. Write only:

1. what moves (subject motion, wind, water, light changes),
2. how the camera moves,
3. the pace (slow, gentle, sudden).

Do not re-describe the whole picture. Conflicting descriptions make the model drift away from your image.

## Twelve ready shots

1. Steam curls up from a cup of black coffee on a windowsill as rain streaks the glass. Static camera, close-up. Grey morning light. Calm, cinematic.
2. A golden retriever shakes water off its fur on a beach, droplets flying in slow motion. Low-angle static shot. Backlit sunset. Joyful, warm.
3. A skateboarder rolls past the camera on an empty concrete plaza. Tracking shot at board level. Hard afternoon sun, long shadows. Energetic, street style.
4. Ink drops bloom into clear water, swirling in blue and orange clouds. Macro, static. Black background, side light. Abstract.
5. A hot air balloon lifts off a misty field at dawn. Slow crane up. Soft pink light. Peaceful, epic.
6. A barista pours a heart into a latte. Overhead static shot. Warm café light. Close and satisfying.
7. Neon sign flickers on above a closed shop on a rainy night. Slow push-in. Reflections on wet pavement. Moody, noir.
8. Autumn leaves fall around a park bench. Slow pan right. Golden hour. Quiet, nostalgic.
9. A sneaker turns on a pedestal as colored light sweeps across it. Orbit around the shoe. Dark studio, rim light. Commercial.
10. Waves crash on black volcanic rocks, spray in the air. Wide static shot. Overcast. Dramatic.
11. A paper airplane glides across a classroom and lands on a desk. Tracking shot following the plane. Window light. Playful.
12. Fog rolls over a mountain ridge in time-lapse. Static wide shot. Blue hour. Majestic.

## Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| Subject melts or morphs | Too much motion or too many subjects | One subject, smaller action, slower camera |
| Nothing happens | Action too vague | Name a concrete verb ("flips", "opens", "turns") |
| Face changes mid-clip | Close-up with fast motion | Medium shot, slow camera |
| Garbled signs and logos | Models cannot spell reliably | Leave text out; add it in editing |
| Wrong framing with a start image | Prompt fights the image | Describe only motion and camera |
