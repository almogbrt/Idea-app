# Runner playbook

## Matching requests to workflows

| The person says | Look for workflows named or described with | Inputs to fill |
|---|---|---|
| "Make a product shot with my GPT Image flow" | gpt image, product, packshot | the prompt text input |
| "Run my ad flow on these 10 products" | ad, ads, creative | product image + headline per CSV row |
| "Voice this script with my voiceover board" | voice, voiceover, tts, elevenlabs | script text; voice stays as saved |
| "Animate this picture with my video flow" | video, animate, i2v | start image URL + motion prompt |
| "Do the weekly thumbnails" | thumbnail, youtube | title text per row |

When two workflows fit, prefer the one updated most recently, and ask.

## Reading a workflow before running it

From `get_workflow`, write down:

1. **Inputs**: key or node id, type (text, image, video, audio, number), saved default.
2. **Paid nodes**: every image, video, audio and LLM node, with its model.
3. **Fan-out**: iterators, lists or several model nodes on one prompt multiply the cost.
4. **Outputs**: which nodes produce the files the person wants.

## Estimate worksheet

| Node | Model | Unit | Units per run | Credits per unit | Subtotal |
|---|---|---|---|---|---|
| Image | GPT Image 2.5 Flare | image | 1 | from `list_models` | |
| Video | e.g. Hailuo 03 Max Turbo | second | 6 | from `list_models` | |
| **Per run** | | | | | **sum** |
| **Batch** | | | | runs x per run | **total** |

Notes:
- Quality and size settings change image prices (our 1024x1024 GPT Image 2.5 Flare run at medium quality cost 5 credits).
- Video prices scale with length; very short clips can cost more per second.
- Text and utility nodes are cheap or free, but LLM nodes add a few credits each.
- Say "estimate" and give a range when unsure. Compare with the balance change afterwards.

## Batch CSV shape

```csv
row,prompt,image_url
1,"speckled sage-green ceramic teapot, bamboo handle, pale stone, soft light",
2,"matte black travel kettle on a camp table at dawn",
```

Map each column to an input key from `get_workflow`. Empty cells keep the saved default, so check that this is intended.

## Run log

`runs.csv`: `run, inputs, execution_id, status, output_url, file, credits_note`

Keep it next to the outputs. It is the record of which inputs made which file and lets a stopped batch resume.

## Common surprises

- **Saved defaults**: an input left empty runs with whatever the board last had.
- **Private vs shared**: only workflows the account owns or can edit can be run.
- **Long boards**: a workflow that renders a full video edit can take many minutes; poll calmly and keep the person informed.
- **Outputs on the board**: every run also lands on the board in Wireflow, so the person can open, compare and tweak there.
