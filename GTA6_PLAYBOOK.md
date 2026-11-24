# GTA 6 Clipping Playbook (written November 24, 2026)

> Not financial or legal advice. Rates and campaign details below come from third-party campaign
> trackers and blogs, not official listings, and they change by the hour. Check the live campaign
> page before you clip anything.

## 1. The opportunity (verified)
- **GTA VI launched November 19, 2026** on **PS5 / PS5 Pro / Xbox Series X|S only** (no PC at launch; Rockstar hasn't confirmed a PC date).
- Streams Charts measured a **peak of ~7.91M concurrent viewers** across streaming platforms, its biggest game launch ever,
  and ~125.5M hours watched in the first 24 h (via CNBC).
- Sales: Take-Two estimates ~$3.79B on day one; Sensor Tower's independent estimate is lower (~$1.84–2.36B). Both are preliminary.
- Streamers and brands are paying clippers to spread GTA 6 content. Trackers counted **~13–29 live GTA 6 campaigns** in the week of launch.

## 2. Real campaign numbers (third-party snapshots)
| Data point | Figure | Date / source |
|---|---|---|
| CPM range across open GTA 6 campaigns | **$0.18 – $2.00 per 1k views** (22 campaigns) | Nov 22 (gtasixclipping.com) |
| CPM on launch-week campaigns | $0.70 – $1.50 | Nov 17 (wayin.ai) |
| Max pay per clip | $35 – $400 depending on campaign | Nov 19 (openclip.app) |
| Campaign budgets | from ~$1,000 to $5,000+ | gtaclipper.com |
| Budget burn | one $2 CPM campaign had only **$818 left** | Nov 22 |
| Lacy GTA VI marathon (Reach) | **$12,500 pool**; you need **≥750,000 approved views** to get a share; caption must mention LACY + `#LACY`; footage only from his marathon starting Nov 18; TikTok / Reels / Shorts / X | reachclipping.com/LACYGTA |
| Content Rewards fee | 10% of CPM payouts | contentrewards.com |
| Earning window | a CPM clip earns for **7 days**, then payout is held ~3 days | gtaclipper.com |

**What that means in money:** at $1 CPM minus 10%, **100,000 views ≈ $90**. A clip that hits 1M views ≈ $900,
but per-clip caps ($35–$400) often stop you sooner. Thousands of clippers are cutting the same streams,
so most clips will get far fewer views. Pool campaigns like Lacy's pay nothing below their view threshold.

## 3. Pick your route

### Route A: clip streamers' GTA 6 streams (recommended, no console needed)
The footage is the streamer's **official VOD** (Twitch/Kick/YouTube). The campaign pays you to spread it.
- No PS5 needed and no game purchase. The copyright position is clean because the streamer hired you.
- Rejected if you use a re-upload, another streamer's footage, or miss the required name/hashtag.

### Route B: your own gameplay
Needs a PS5 or Xbox Series and the game. Only works for campaigns that **accept your own gameplay**
(most are streamer campaigns, so check the brief).
- Rockstar's video policy welcomes gameplay videos but says "non-commercial". Whether paid clips are OK is
  **unresolved**: it runs on Rockstar's tolerance, not a licence. Never post leaks or standalone cutscenes.
- In-game **radio music can trigger Content ID claims**. Turn the radio off while recording.

Start with **Route A**. It needs nothing you don't already have.

## 4. Setup, step by step (do this today)

**Step 1: Accounts (about 1 hour)**
1. Create **fresh, dedicated GTA clip accounts** on TikTok, YouTube (Shorts) and Instagram. Some campaigns
   require an account made only for that streamer. Use a GTA-themed name and avatar, and post 2–3 clips before submitting anything.
2. Sign up on **Content Rewards** (contentrewards.com) and **Reach** (reachclipping.com). Optionally add Vyro or ClipFarm.
3. Finish **ID verification and payout setup now**. Payouts are blocked without it.
4. In **Publora** (already connected, Starter plan: 15 posts/month, 2 free account slots), connect TikTok and YouTube.

**Step 2: Choose 1–3 campaigns**
Filter for: GTA 6, **budget still remaining**, CPM ≥ $1, per-clip cap ≥ $100, platforms you have. Copy each **brief** into
`work/<slug>/brief.md`. Claude follows it when picking and captioning clips.

**Step 3: Make clips with Claude Code (on your own PC)**
```bash
# grab only a 30-minute chunk of the streamer's official 10-hour VOD
python3 clipper/clip.py fetch "https://www.twitch.tv/videos/<VOD_ID>" --slug lacy-day1 --section 2:10:00-2:40:00
python3 clipper/clip.py transcribe lacy-day1          # what was said
python3 clipper/clip.py peaks lacy-day1               # where the streamer screamed/laughed (hype moments)
# → ask Claude: "Read brief.md, transcript.txt and peaks.txt, write clips.json with the 5 best moments"
python3 clipper/clip.py render lacy-day1 --layout stack --cam 1500:60:380:280   # facecam on top, gameplay below
```
To find `--cam`, pause the VOD and note the facecam box (x, y, width, height in a 1920×1080 frame),
or ask Claude to grab a frame with ffmpeg and read the box off it.

**Step 4: Post and submit**
- Caption must include what the brief requires (e.g. `LACY` + `#LACY`) plus `#gta6 #gtavi`.
- Post via Publora or the app, then **submit each post URL** on the campaign page within its window.
- Log the URL, campaign and views (a sheet, or Supabase).

## 5. What gets GTA clips views (and approved)
- **Hook in the first 1–2 s:** start on the reaction or the chaos, not the setup. The text hook is burned in for the first 3 s.
- **Best moment types:** first-time reactions to the map or graphics, police chases going wrong, glitches, rage or laughter,
  streamer vs chat moments, "wait for it" endings. `peaks.txt` finds the loud ones automatically.
- **Length:** 20–45 s for Shorts and TikTok. Burned captions (most people watch muted).
- **Volume:** 3–10 clips a day across accounts. Launch hype fades fast, so **this week and next matter most**.
- **Story spoilers:** avoid them when the brief says so. Spoiler clips also annoy viewers who haven't played yet.

## 6. Instant-ban list
- View bots, view exchanges, engagement pods. These lead to a ban and withheld pay.
- Re-uploading someone else's clip, or using footage the brief didn't name.
- Leaked or pre-release footage, standalone cutscenes.
- Unedited re-uploads on YouTube: Shorts reused-content rules can demonetise **the whole channel**.

## 7. Running this inside Claude Code in the cloud
This cloud session's network **blocks** Twitch, YouTube and huggingface.co (Whisper models), so fetch and transcribe
can't run here unless those hosts are allowed in the environment's network settings. Running Claude Code on your
own PC (see `SETUP_GUIDE.md` §5A) avoids that entirely.

## Sources
- Launch and viewership: [Streams Charts](https://streamscharts.com/news/gta-vi-breaks-streaming-launch-records-within-minutes-its-release), [CNBC](https://www.cnbc.com/2026/11/20/gta-vi-launch-streaming-content-economy.html), [Forbes](https://www.forbes.com/sites/antoniopequenoiv/2026/11/20/gta-6-raked-in-38-billion-sales-on-first-day-the-largest-entertainment-launch-ever/), [Streams Charts GTA6 stats](https://streamscharts.com/specials/gta6)
- Platforms: [NME](https://www.nme.com/guides/gaming-guides/gta-6-release-date-xbox-ps5-pc-3553782), [Beebom](https://beebom.com/gta-6-platforms-list/), [Sportskeeda](https://sportskeeda.com/gta/news-gta-6-platforms-list-platforms-confirmed-game)
- Campaigns and rates: [gtasixclipping.com](https://gtasixclipping.com/), [wayin.ai](https://wayin.ai/blog/gta-6-clipping-campaigns/), [openclip.app](https://openclip.app/clipping/gta-6-clipping), [gtaclipper.com](https://gtaclipper.com/guides/gta-6-clipping), [gtaclipper campaigns](https://gtaclipper.com/campaigns), [contentrewards.com](https://contentrewards.com/articles/gta-6-clipping), [clipcpm.com](https://clipcpm.com/gta-6), [Reach: Lacy campaign](https://reachclipping.com/LACYGTA), [oakgen.ai](https://oakgen.ai/blog/gta-6-clipping-campaigns), [picxstudio.com](https://picxstudio.com/blog/gta-6-clipping-campaigns)
- Rockstar and YouTube rules: [prepublish.ai](https://prepublish.ai/blog/gta-6-youtube-copyright-monetization), [openworlddaily.com](https://openworlddaily.com/guides/gta-6-footage-streaming-policy/), [oakgen.ai streaming rules](https://oakgen.ai/blog/gta-6-streaming-rules), [copyrightshark.com](https://copyrightshark.com/gta-6-copyright-rules/), [YouTube Shorts monetization policies](https://support.google.com/youtube/answer/12504220?hl=en)
