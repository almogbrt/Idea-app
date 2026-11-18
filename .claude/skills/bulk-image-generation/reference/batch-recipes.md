# Batch recipes

Ready-made templates for common bulk jobs. Fill `{placeholders}` from your CSV columns. Every template already ends with the no-text, no-border line.

## Product catalog packshots (1:1)

```
E-commerce studio packshot of {product} in {color}, {angle} view, centered on a seamless pure white background, soft even studio light, gentle contact shadow, sharp focus, no text, no logo, full bleed, no border
```

CSV:

```csv
filename,product,color,angle
mug-terracotta,matte ceramic coffee mug with a thick rounded handle,terracotta,three-quarter
tote-cream,canvas tote bag with cotton straps,natural cream with olive straps,front
```

Keep `{angle}` the same for the whole catalog unless a product really needs another view.

## Blog header images (16:9)

```
Editorial photo illustrating "{article_title}": {scene}, soft natural light, calm muted colors, empty space on the right third for a title, no text, no watermark, full bleed, no border
```

Write `{scene}` yourself from each title: one concrete object or moment, not an abstract concept.

## Social post backgrounds (3:4 or 9:16)

```
{subject} in {setting}, {season} light, {palette} color palette, lots of clean space in the top half for text added later, photo, no text, full bleed, no border
```

## Real-estate or travel destinations (3:2)

```
Wide establishing photo of {place}, {time_of_day}, {weather}, people small or absent, travel magazine style, no text, no watermark, full bleed, no border
```

## Character or mascot poses (1:1)

```
{mascot_description}, {pose}, plain light grey background, same flat illustration style and colors in every image, thick clean outlines, no text, full bleed, no border
```

Consistency across a set of illustrations is hard for any model. Describe the character the same way word for word in every row, and expect to re-run a few.

## Sizing a batch

| Rows | Credits at 19 each | Typical use |
|---|---|---|
| 3 | 57 | Pilot before a big run |
| 10 | 190 | A small collection |
| 25 | 475 | A catalog page |
| 50 | 950 | A full drop, split into two approvals |

## Manifest columns

`row, filename, aspect_ratio, prompt, status, execution_id, url, file`

`status` is `done`, `failed` or `skipped`. Keep the manifest next to the images; it is the record of what was made from which prompt, and it lets a stopped batch resume from the first row that is not `done`.
