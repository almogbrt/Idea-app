# Real run

One run of this skill's Wireflow app (`skill-ai-voiceover-for-ugc-ads`: Run any LLM with Claude Haiku 4.5 for the spoken rewrite, then Minimax Speech 02 HD in three voices) on 26 October 2026. The MP3s here are re-encoded copies (128 kbps); originals are on the Wireflow CDN. The voices are synthetic.

## Inputs

- `script`: Okay, this tote fits my laptop, my gym clothes AND my lunch!!! Finally... one bag. 20% off this week.
- `tone`: Casual and upbeat, like a friend recommending it to you.
- `language`: English (US)

## Outputs

`spoken-script` (the words that were read): "Okay, this tote fits my laptop, my gym clothes, and my lunch. Finally, one bag. Twenty percent off this week."

The rewrite dropped the shouty capitals and extra punctuation, wrote "20%" as spoken, and kept the offer as given.

| Take | Voice | File | Original |
|---|---|---|---|
| 1 | Lively_Girl (bright female) | [take-1-lively-girl.mp3](take-1-lively-girl.mp3) | https://cdn.wireflow.ai/b1964a10-d0e9-11f1-b524-212f547bd4a8.mp3 |
| 2 | Casual_Guy (relaxed male) | [take-2-casual-guy.mp3](take-2-casual-guy.mp3) | https://cdn.wireflow.ai/b1942730-d0e9-11f1-b524-212f547bd4a8.mp3 |
| 3 | Calm_Woman (calm female) | [take-3-calm-woman.mp3](take-3-calm-woman.mp3) | https://cdn.wireflow.ai/b10bbd50-d0e9-11f1-b524-212f547bd4a8.mp3 |

- Execution: `f3f8f866-5aad-44f7-82b5-a8b26b6855ef`
- Credits: 51, from `GET /credits/history`: Openrouter Router 3, then three Minimax Speech 02 HD charges of 16. The balance went from 1,032 to 981.
- Length: about 8.5 seconds a take (139 to 143 KB at 128 kbps).
- Checked: the run completed, all three takes came back as MP3s, and the spoken script keeps every name, number and the offer.
- Not checked: how the takes sound. Nobody has listened to them yet.

The run used the Wireflow Apps API (`POST /api/v1/apps/skill-ai-voiceover-for-ugc-ads/execute`), the same code path as the MCP `run_app` tool.
