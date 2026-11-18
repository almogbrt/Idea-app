# On-brand image requests

Six request shapes for the `image_request` input. Replace the angle brackets, keep the brief separate (it goes in `brand_brief`), and say "the product from the product photo" so the model reuses the real one. Every image comes back square.

## 1. Social post, product in its place

> Instagram post: the product from the product photo on `<surface>` in `<room or setting>`, beside `<one or two props in brand colors>`, the logo printed on `<the label / the box / the bag>`, `<light from the brief>`, calm negative space around it.

## 2. Flat lay with a short line of text

> Flat lay seen from directly above on `<textured surface>`: the product from the product photo, `<two or three props>`, and a small card that reads "`<two to four words>`" in a simple `<serif / sans-serif>`. `<light>`, neat balanced layout, no other text.

## 3. Ad backdrop with room for copy

> Square ad image: the product from the product photo on the right third, a wide empty area of `<brand color>` on the left for a headline added later, the logo small on the product label only, clean studio light, no words in the image.

## 4. Seasonal or launch moment

> `<Season or event>` post: the product from the product photo with `<two seasonal props in brand colors>`, the logo on the product, `<light>`, festive but uncluttered, no other logos or words.

## 5. Packaging close-up

> Close-up of the logo on the product's `<label / lid / tag>`, shallow depth of field, `<surface>` behind it, `<light>`, the logo sharp and exactly as in the logo reference.

## 6. Lifestyle in use

> `<Who>` using the product from the product photo in `<setting>`, seen from `<angle>`, hands and product in focus, face out of frame, the logo visible on the product, `<light>`, natural and unposed.

## Tips that held up in testing

- Put the logo on a physical thing in the scene (label, card, sign). The model then sizes and lights it to fit.
- Quote exact words and keep them short. "Slow evenings" came out spelled right in our test; long sentences are riskier.
- Small taglines under a wordmark can come out soft. If the tagline matters, ask for a closer shot.
- State the physics: lid off for a lit candle, cap off for a pour.
