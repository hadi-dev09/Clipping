# Clipping workspace

Turns long videos into vertical (1080x1920) captioned short clips for clipping campaigns.

## Workflow (run in order)
1. `python3 clipper/clip.py fetch <URL or local file> [--slug NAME]` → `work/<slug>/source.mp4`
   - Prefer the raw-footage link (Google Drive / Dropbox) the campaign gives you. Local files work too.
2. `python3 clipper/clip.py transcribe <slug> [--model small]` → `work/<slug>/transcript.txt`
3. **Claude picks moments**: read `work/<slug>/transcript.txt` and the campaign brief, then write
   `work/<slug>/clips.json` — 3–8 clips, each 20–60 s, starting on a strong hook (question, bold claim,
   conflict, punchline), ending on a complete thought. Format:
   `[{"start": 123.4, "end": 161.0, "title": "short-name", "hook": "≤6-word on-screen text"}]`
4. `python3 clipper/clip.py render <slug> [--layout blur|crop]` → `out/<slug>/clip_NN_*.mp4`
5. Post: via the Publora MCP connector (TikTok / Instagram / YouTube) or manually; then submit each
   post URL to the campaign on its platform (Content Rewards / Vyro / etc.).

## Rules
- Follow each campaign brief exactly (required tags, links, disclosure, banned edits). Rejections are mostly brief violations.
- Never use view bots, view exchanges or engagement pods — campaigns ban accounts and withhold pay for it.
- Only clip content you have rights to clip (campaign footage, own content, permissive licence).
