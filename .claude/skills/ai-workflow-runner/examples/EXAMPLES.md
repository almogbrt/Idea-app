# Real run

A run of one of the account owner's own image workflows, made on 8 October 2026 the way this skill does it: find the workflow, read its inputs, run it with a new value, collect the output.

## The request

"Use my GPT Image 2.5 Flare workflow to make a studio shot of a sage-green ceramic teapot."

## What the skill would find

- Workflow: a private copy of the account's "GPT Image 2.5 Flare Text to Image" board, made for this test so the original board was left untouched (`cmuz2n9ss0006os06m6nrkw77`).
- Inputs (from the workflow's input schema): one text input, key `image_prompt`, with a saved serum-bottle prompt as its default.
- Paid nodes: one GPT Image 2.5 Flare node, medium quality, 1024x1024.

## Input sent

`image_prompt`: A photorealistic studio product photo of a speckled sage-green ceramic teapot with a bamboo handle on a smooth pale stone surface, soft directional light from the left, shallow depth of field, clean minimal composition, no text or lettering, full bleed, no border

## Output

![Sage-green ceramic teapot with a bamboo handle](teapot-run-output.jpg)

- Original: https://cdn.wireflow.ai/c524c560-c2d5-11f1-a7c9-3fc28be8667b.png (1024x1024 PNG)
- Execution: `75e60f23-5508-424c-be32-707141dc1c8d`
- Credits: 5 (account balance before minus after; the execution record also reported 5)
- Time: about 24 seconds end to end

## How it was run

Through Wireflow's REST twin of the MCP tools: `GET /api/v1/workflows/{id}/run` for the input schema, `POST /api/v1/workflows/{id}/run` to start (what `run_workflow` does over MCP), and the execution poll.

## Fresh Claude session over MCP

A new headless Claude Code session with this skill installed and the Wireflow connector signed in was asked to run the same board with a cobalt-blue enamel kettle prompt, approval given up front. It found the board with `list_workflows`, read its `image_prompt` input with `get_workflow`, ran it once with `run_workflow` and saved the file plus `runs.csv`: execution `0b4eee63-886b-4dd9-b114-58a70e596dec`, output https://cdn.wireflow.ai/be885940-c2d7-11f1-b5e2-a35d962c8496.png, 5 credits (balance 4,539 to 4,534), about 16 seconds.
