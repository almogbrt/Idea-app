# Post sheet

This turns a rough idea into the exact words and arrangement for one post. Filled in, it is also the free deliverable when Wireflow is not connected: a designer can build the post from it in any design tool.

## Pick the post type

| Type | Hero piece | Supporting piece | Must be true first |
|---|---|---|---|
| Quote | The quote, 15 words at most | Name and role | The person said it and agreed to the post |
| Stat | The figure, with its unit ("42%", "3x") | What it measures, plus the source | The source is real and can be named |
| Announcement | What is happening, 10 words at most | Date, time, place or offer | The details are confirmed, weekday and date agree |

## Word rules

- Whole post: 25 words or fewer.
- At most three pieces. A fourth small piece is likely to go missing or crowd the layout.
- Put every piece in double quotes. `Headline:` or `Footer:` outside the quotes tells the app the role and is not drawn.
- Write capitals and punctuation exactly as they should appear.
- Leave hashtags and links for the caption. They render poorly and cannot be tapped on an image.

## Writing post_type

One sentence: which piece is the hero, where the others sit, the single accent shape.

- Quote: "Quote card: the quote as the hero in big type, the attribution small underneath."
- Stat: "Stat post: the figure huge in the accent color, the label under it, the source small at the bottom of the text block."
- Announcement: "Announcement: the headline as the hero, the detail line smaller underneath, one underline as the only accent."

## Writing brand_colors

Background, text color, one accent (hex codes if the brand has them) and a font feel: bold geometric sans, rounded sans, editorial serif. Pick text and background with strong contrast. Keep the line the same for every post in a client's calendar so the feed stays consistent. The look still varies a little between runs, because each image is drawn fresh.

## Post sheet (free deliverable)

| Field | Value |
|---|---|
| Client and channel | ... |
| Post type | ... |
| Hero | "..." |
| Supporting line | "..." |
| Name or handle | "..." |
| Source or consent checked | ... |

## Design spec (free deliverable)

| | Square | Portrait | Story |
|---|---|---|---|
| Size in pixels | 2048x2048 | 1728x2304 | 1440x2560 |
| Ratio | 1:1 | 3:4 | 9:16 |
| Where the words sit | Centered, even margins | Middle 80% of the height | Middle 60% of the height |
| Keep empty | Outer margin | Top and bottom 10% | Top and bottom 20% |
| Colors and fonts | ... | same | same |

## Cropping portrait to 4:5

The app renders 3:4 because Ideogram 4.5 has no 4:5 size. Trimming 72 pixels off the top and 72 off the bottom gives 1728x2160, which is 4:5. The words sit inside the kept area, so nothing is lost. Check it on each post, since the margin is a request to the model and not a guarantee.
