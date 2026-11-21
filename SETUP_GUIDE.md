# Clipping with Claude Code: Setup Guide (researched November 21, 2026)

> **Note on the word:** I read "creeping" as **clipping** (your repo is named `Clipping`).
> Clipping means cutting short vertical clips out of long videos (podcasts, streams, interviews)
> and getting paid **per 1,000 views** by the creator or brand who runs a *clipping campaign*.

> **Disclaimer:** This is not financial or legal advice. Earnings are not guaranteed, and most rates
> below come from third-party blogs, not official price lists. Check each campaign's live rate and
> terms before you put time into it.

---

## 1. How the money works

1. A creator or brand (a podcaster, streamer, app, or musician) puts a **budget** into a campaign on
   a clipping marketplace and sets a **rate per 1,000 views (CPM)**. Each campaign has a brief:
   which footage to use, required tags and links, allowed platforms, and the maximum pay per clip.
2. You cut clips from their footage and post them on **your own** TikTok, Instagram Reels,
   YouTube Shorts or X accounts.
3. You submit each post link. The platform checks the **public view count via the social platforms' APIs**,
   usually for 7–30 days per clip.
4. You are paid *(approved views ÷ 1000) × CPM*, minus the platform fee, until the per-clip cap
   is reached or the campaign budget runs out.

### Real numbers (from research, not invented)

| Item | Figure | Source quality |
|---|---|---|
| CPM range on Content Rewards (100 campaigns sampled Oct 12, 2026) | **$0.20 – $5.00, median $1.30** | Third-party sample (openclip.app) |
| Typical CPM, bulk of Whop campaigns | ~$0.50 – $2 | Several third-party guides |
| Music campaigns | can be as low as $0.30 / 1k | Cited by guides from Whop |
| Vyro | ~$3 CPM flat, cap reported at $1,000 per clip | Third-party / competitor blogs |
| Content Rewards fee | 10% of CPM earnings | Third-party guides |
| Whop minimum withdrawal | $10 ("if applicable") | **Whop docs** |
| Whop payouts | bank / mobile wallet / crypto, 200+ countries, KYC with government ID | **Whop docs** |
| Pakistan payouts | Reported as supported (PKR to a local bank after KYC) | TechJuice news report. Check in the dashboard |

**Worked example:** at the $1.30 median CPM with a 10% fee you net about **$1.17 per 1,000 views**.

| Views on approved clips (per month) | Gross | Net (after 10%) |
|---|---|---|
| 10,000 | $13 | $11.70 |
| 100,000 | $130 | $117 |
| 1,000,000 | $1,300 | $1,170 |

**Honest reality check:** views are very uneven. A new account's clips often get a few hundred
views, and one clip that takes off can make most of a month's earnings. I found **no reliable
public data** on what a typical clipper earns. Ignore income claims from "clipping course" sellers.
Other things that cut earnings:
- Budgets can be **reserved within minutes** of a campaign launching, so speed matters.
- Clips are **rejected** for breaking the brief (missing tag or link, wrong footage, a low-effort re-upload).
- Some clippers report **earnings holds of up to 90 days**, and support handoffs between Whop and Content Rewards.

---

## 2. Where to find campaigns (the "where do we provide it" part)

| Platform | What it is | Notes |
|---|---|---|
| **Content Rewards** (contentrewards.com, formerly inside Whop) | Largest marketplace | Became a separate company (Content Rewards Inc.). Whop still handles payments. Its own app launched Aug 2026 |
| **Vyro** | CPM campaigns | Higher flat CPM, smaller roster |
| **ClipFarm** | Whop-powered community (Airrack) | Entertainment and launch campaigns |
| **ClipAffiliates** | CPM + UGC | $1–$5 CPM set per brand |
| **Clipping.net** | Network | Reported 100k-view eligibility threshold |
| Direct deals | DM a podcaster or streamer | Monthly retainer for a set number of clips. Often steadier than CPM |

Most working clippers use 2–3 of these at once. The comparison articles are written by competing
platforms, so treat any "best platform" claim as marketing.

**Where the source footage comes from:** the campaign brief. It usually links a Google Drive or Dropbox
folder of raw episodes, or names the creator's YouTube or Twitch channel. You don't scrape random
videos. Clip only footage you are permitted to use.

---

## 3. Apps you need: free options first

| Job | Free option | Paid option (if you scale) |
|---|---|---|
| Download source | **yt-dlp** (open source) | n/a |
| Transcribe with word timings | **faster-whisper** (open source, runs on CPU) | n/a |
| Pick the best moments | **Claude Code**, reading the transcript (this repo) | OpusClip / similar |
| Cut, 9:16 reframe, burned captions | **FFmpeg** (this repo's `clip.py`) | n/a |
| Manual polish | **CapCut** free plan, **DaVinci Resolve** (free) | CapCut Pro ($19.99/mo per a third-party check) |
| AI clipper (no-code) | **OpusClip free**: 60 credits/mo (60 min of video), **watermark**, clips expire after 3 days | OpusClip Starter ($15/mo) removes the watermark |
| Open-source alternatives | AutoClip, OpenClip, ClippedAI, clipsai, OpenShorts (GitHub) | n/a |
| Posting | Native apps (free) | **Publora** (you already have it connected) |
| Tracking | A spreadsheet, or **Supabase** (connected, free tier) | n/a |

CapCut's free-plan watermark and resolution limits conflict between sources. Check before relying on them.

---

## 4. Connectors in your Claude Code session (checked live on Nov 21, 2026)

| Connector | Status in this session | Use for clipping |
|---|---|---|
| **Publora** | ✅ Connected. **Starter plan: 15 posts/month, 3 scheduled at a time, 7-day schedule horizon, 3 account slots (1 used by LinkedIn)**. Allowed platforms include TikTok, Instagram, YouTube | Publish clips from Claude Code. Connect your TikTok, IG and YouTube clipping accounts in Publora first |
| **Google Drive** | ✅ Available | Pull campaign raw footage, store finished clips |
| **Supabase** | ✅ Available | Optional table of clips, posted URLs, views and earnings |
| **Apify** | ⚠️ Connected, but **free $5/month usage is used up** until the cycle resets | Scrape public view counts and trending clips |
| Zapier / Make | Available | Automations (e.g. new Drive file → notify) |
| n8n, Canva | Need sign-in in claude.ai connector settings | Optional |
| GHL | Failed to connect | Not needed |

Limits you will hit if you post through official APIs instead:
- **YouTube Data API:** 10,000 units a day by default, and an upload costs 1,600 units, so about **6 uploads a day**. More requires an audit.
- **TikTok Content Posting API:** unaudited apps can **only post privately** (max 5 users a day). Public posting needs TikTok's audit.
  That's why a posting service like Publora, which has already passed those audits, is the practical route.

---

## 5. Setup, step by step

### A. Run Claude Code on your own PC (recommended)
This cloud session's network **blocks youtube.com, huggingface.co (Whisper models) and archive.org**,
so downloading and transcription can't run here. On your own machine:

```bash
# 1. Prerequisites: Python 3.10+, FFmpeg, Node 18+
#    Windows: winget install Gyan.FFmpeg  |  macOS: brew install ffmpeg  |  Ubuntu: sudo apt install ffmpeg
# 2. Claude Code
npm install -g @anthropic-ai/claude-code
# 3. This repo
git clone https://github.com/hadi-dev09/Clipping && cd Clipping
pip install -r requirements.txt
claude
```
Claude Code reads `CLAUDE.md` and knows the workflow. Then tell it something like:
> "Fetch <campaign footage link>, transcribe it, pick 5 clips that fit this brief: <paste brief>, and render them."

To run it in **this cloud environment** instead, allow `huggingface.co` plus your footage hosts
(`drive.google.com`, `www.youtube.com`, `*.googlevideo.com`) in the environment's network settings.
YouTube often blocks downloads from data-centre IPs even when the host is allowed.

### B. The pipeline in this repo (`clipper/clip.py`)
```
fetch URL ─► work/<slug>/source.mp4
transcribe ─► transcript.txt (timestamped) + transcript.json (word timings)
Claude reads the transcript + brief ─► clips.json  (start, end, title, hook)
render ─► out/<slug>/clip_NN.mp4   1080×1920, H.264, burned 3-word captions, hook text for the first 3 s
```
`--layout blur` (default) keeps the whole frame over a blurred background. `--layout crop` centre-crops
to fill the screen. The render step was tested in this session and produced a 1080×1920 clip with
audio and captions.

### C. Accounts
1. Make dedicated clipping accounts (one niche per account) on TikTok, Instagram and YouTube.
2. Sign up on Content Rewards and/or Vyro. Finish **KYC and payout setup first**, since payouts need it.
3. In Publora, connect the 2 remaining slots (e.g. TikTok + YouTube). More accounts need a higher plan.

### D. Daily loop
1. Check new campaigns early (budgets fill fast) and read the brief.
2. Run fetch → transcribe → choose clips → render with Claude Code.
3. Review every clip yourself (hook in the first 1–2 s, captions correct, brief followed).
4. Post (Publora or the app) with the required tags and links, then submit the post URLs on the campaign platform.
5. Log URLs and views (sheet or Supabase). Double down on the hooks and accounts that perform.

---

## 6. Rules that get clippers banned or demonetised
- **Fake views:** Content Rewards' Creator Terms (§12.1–12.2) ban buying views, bots, view farms,
  click farms and engagement pods. The result is rejection, a ban, and lost pay.
- **YouTube reused content:** unedited re-uploads and compilations with nothing added are **not eligible**
  for Shorts monetization, and the policy applies to the **whole channel**. Permission from the creator
  does *not* exempt you. YouTube also ranks re-uploaded Shorts lower. Campaign CPM pay is separate
  from YouTube's own ad revenue, but low reach still means low campaign pay. Add real editing:
  hooks, captions, framing, context.
- **Downloading:** YouTube's Terms restrict downloading without permission. Use the footage links the
  campaign provides whenever possible.

---

## 7. Benefits (realistically)
- Startup cost near **$0**: free tools, your own accounts, Claude Code doing the transcript analysis.
- Builds real skills (short-form editing, hooks, audience growth) and accounts that keep their value.
  Those can lead to steadier **retainer clipping deals** directly with creators.
- Downsides: income is uneven and front-loaded on luck, campaigns compete for budget, platforms
  change algorithm and policy often, and payouts can be held.

---

## Sources
- Whop clipping / Content Rewards rates: [openclip.app](https://openclip.app/guides/whop-clipping-guide), [reap.video](https://reap.video/blog/whop-clipping), [clyper.io](https://www.clyper.io/guides/whop-clipping), [elev8or.io](https://www.elev8or.io/blog/whop-clipping), [shopiator.com](https://shopiator.com/blog/whop-content-reward-campaigns)
- Platform comparisons: [ssemble.com](https://www.ssemble.com/blog/best-clipping-platforms-2026), [clipaffiliates.com](https://www.clipaffiliates.com/blog/best-clipping-platforms-compared), [tryearnable.com](https://www.tryearnable.com/post/best-clipping-platforms-compared-2026), [nextclip.pro](https://www.nextclip.pro/blog/best-clipping-platforms-2026), [ascynd.io](https://ascynd.io/en/blog/clipping-platforms-like-whop)
- Fake-view rules and verification: [contentrewards.com/articles/clipping-view-fraud](https://contentrewards.com/articles/clipping-view-fraud), [Whop docs: Content Rewards](https://docs.whop.com/manage-your-business/growth-marketing/content-rewards), [findclout.com](https://findclout.com/blog/content-rewards-bot-views)
- Whop payouts: [Whop docs: set up payouts](https://docs.whop.com/manage-your-business/manage-payouts/set-up-payouts), [payout methods](https://docs.whop.com/manage-your-business/manage-payouts/payout-methods), [TechJuice (Pakistan)](https://www.techjuice.pk/did-pakistan-finally-get-a-stripe-alternative/)
- YouTube policy: [Shorts monetization policies](https://support.google.com/youtube/answer/12504220?hl=en), [YPP policies](https://support.google.com/youtube/answer/1311392), [Search Engine Journal](https://searchenginejournal.com/youtube-original-shorts-reposted-clips-reach/591774/)
- APIs: [YouTube quota costs](https://developers.google.com/youtube/v3/determine_quota_cost), [TikTok content sharing guidelines](https://developers.tiktok.com/doc/content-sharing-guidelines)
- Tools: [OpusClip pricing (castmagic)](https://www.castmagic.io/blog/opus-clip-pricing), [CapCut help](https://www.capcut.com/help/different-free-usage-limits-features), [dupple.com CapCut](https://dupple.com/learn/is-capcut-free), [AutoClip](https://github.com/artbyjazi/autoclip), [OpenClip](https://github.com/aionixos/openclip), [ClippedAI](https://github.com/Shaarav4795/ClippedAI), [clipsai](https://github.com/ClipsAI/clipsai), [OpenShorts](https://github.com/mutonby/openshorts)
