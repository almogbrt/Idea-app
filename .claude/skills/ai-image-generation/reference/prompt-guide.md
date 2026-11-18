# Image prompt guide

Works with any text-to-image model. Written for Flux Pro Ultra, the model behind this skill's Wireflow app.

## The six-part prompt

Write full sentences in this order. Models weight the start of the prompt most.

| Part | Ask yourself | Weak | Strong |
|---|---|---|---|
| Subject | What exactly is in frame? | a dog | a scruffy grey terrier puppy with one ear flopped over |
| Setting | Where, and what is around it? | outside | on a wet cobblestone lane outside a bakery |
| Light | Where does light come from, and what is it like? | nice lighting | low morning sun from behind, warm rim light, soft fill |
| Camera | How far, what angle, what lens feel? | photo | eye-level close-up, 85mm, shallow depth of field |
| Style | Photo, film, illustration, render? Mood? | realistic | editorial photo, Kodak Portra film look, gentle and warm |
| Exclusions | What must not appear? | (nothing) | no text, no logos, no watermark, full bleed, no border, no frame |

## Choosing the frame

| Use | Ratio | Composition tip |
|---|---|---|
| Feed post | 1:1 or 3:4 | Center the subject, keep the edges calm |
| Story, Reel cover, wallpaper | 9:16 | Subject in the middle third; top and bottom get covered by app UI |
| Website hero, blog header | 16:9 | Put the subject on one side and leave the other side open for a headline |
| YouTube thumbnail background | 16:9 | Big simple shapes, strong contrast, room for a face and text added later |
| Banner | 21:9 | Horizontal subject, lots of breathing room |
| Print, catalog | 3:2 or 4:3 | Classic photo framing |

## Words that change the picture

- **Shot size**: extreme close-up, close-up, medium shot, full body, wide shot, aerial view, overhead flat lay.
- **Angle**: eye level, low angle (heroic), high angle (small, vulnerable), Dutch angle (tense).
- **Lens feel**: 24mm wide (space, distortion), 50mm (natural), 85mm (portrait compression), macro (tiny detail).
- **Light**: golden hour, blue hour, overcast soft light, hard noon sun, window light, neon, candlelight, studio softbox, rim light, backlit haze.
- **Finish**: film grain, matte, high contrast, pastel, muted earth tones, glossy commercial.
- **Styles beyond photo**: watercolor, gouache, ink line art, flat vector illustration, isometric 3D, claymation, paper cut-out, risograph print.

## Worked examples

These are ready to paste. The first one is the real prompt behind this skill's README image. Add the exclusions line ("no text, no logos, no watermark, full bleed, no border, no frame") to any of them before running.

1. **Travel editorial, 16:9**: A red vintage bicycle leaning against a pastel blue tiled wall in a narrow Lisbon street, pink bougainvillea spilling over the top, late afternoon sun casting long diagonal shadows, warm golden light, shot on 35mm film, editorial travel photography.
2. **Product packshot, 1:1**: E-commerce studio packshot of an amber glass candle jar with a light oak wooden lid and a plain cream paper band label with no text, centered on a seamless pure white background, soft even studio lighting, gentle contact shadow, sharp focus, high detail product photography.
3. **Blog header, 16:9**: A tidy home office desk seen from the side, laptop closed, a ceramic mug and a notebook, morning window light from the left, plants softly out of focus, calm muted colors, empty wall space on the right, editorial photo, no text.
4. **Story background, 9:16**: Looking straight up through tall pine trees to a pale sky, light fog between the trunks, cool green and grey tones, quiet and spacious, fine art photograph.
5. **Food, 3:4**: Overhead shot of a bowl of ramen on a dark slate table, soft-boiled egg, scallions and chili oil, steam rising, a pair of wooden chopsticks resting on the rim, moody side light, food magazine style.
6. **Illustration, 1:1**: A flat vector illustration of a fox reading a book under a mushroom during light rain, limited palette of orange, teal and cream, thick clean outlines, children's book style, no text.
7. **Portrait, 2:3**: Environmental portrait of an elderly potter at her wheel, clay on her hands, looking at the camera with a slight smile, workshop shelves behind her, window light, 85mm, documentary photo.
8. **Banner, 21:9**: A long empty beach at blue hour, a single lifeguard tower on the left, gentle waves, pink and violet sky, minimalist, lots of negative space, cinematic still.

## Fixing common problems

| Problem | Fix |
|---|---|
| Looks generic | Add two specific details to the subject and one to the setting |
| Wrong mood | Change the light first, then the color words |
| Cluttered | Say what is NOT there ("empty background", "only one person") |
| Garbled text | Remove text from the prompt; add it later in a design tool |
| Hands or faces off | Use a medium shot instead of a close-up of hands; keep poses simple |
| Too dark or flat | Name a light source and its direction |
| Thin border, frame or dark strip at an edge | End the prompt with "full bleed, no border, no frame" and avoid words like "poster", "print" or "framed" |
