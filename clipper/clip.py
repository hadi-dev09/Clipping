#!/usr/bin/env python3
"""Clipping pipeline: long video -> transcript -> chosen moments -> vertical captioned shorts.

Steps (each is a subcommand so Claude Code can run them one by one):

  fetch       URL            download the source with yt-dlp            -> work/<slug>/source.mp4
  transcribe  <slug>         word-level transcript with faster-whisper  -> transcript.json / transcript.txt
  peaks       <slug>         loudest "hype" moments (screams, laughs)   -> peaks.txt
  render      <slug>         cut + 9:16 crop + burned captions          -> out/<slug>/clip_NN.mp4

Between `transcribe` and `render`, someone (Claude Code, reading transcript.txt) writes
work/<slug>/clips.json:

  [{"start": 123.4, "end": 161.0, "title": "...", "hook": "optional on-screen text"}]

Only use sources you have the rights to clip: a campaign that hired you, your own
content, or material whose licence allows it.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
OUT = ROOT / "out"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", text).strip("-")[:60] or "video"


# ---------------------------------------------------------------- fetch
def cmd_fetch(args: argparse.Namespace) -> None:
    if not shutil.which("yt-dlp"):
        sys.exit("yt-dlp not installed: pip install yt-dlp")
    src = Path(args.url)
    if src.exists():  # local file: just copy it in
        slug = args.slug or slugify(src.stem)
        d = WORK / slug
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, d / "source.mp4")
    else:
        out = subprocess.run(
            ["yt-dlp", "--print", "id", "--skip-download", args.url],
            check=True, capture_output=True, text=True,
        ).stdout.strip().splitlines()[0]
        slug = args.slug or slugify(out)
        d = WORK / slug
        d.mkdir(parents=True, exist_ok=True)
        cmd = ["yt-dlp", "-f", "bv*[height<=1080]+ba/b[height<=1080]/b", "--merge-output-format", "mp4"]
        if args.section:  # e.g. 1:20:00-1:50:00 — grab only part of a 10-hour stream VOD
            cmd += ["--download-sections", f"*{args.section}", "--force-keyframes-at-cuts"]
        run(cmd + ["-o", str(d / "source.%(ext)s"), args.url])
    print(f"slug: {slug}")


# ---------------------------------------------------------------- transcribe
def fmt(t: float) -> str:
    m, s = divmod(t, 60)
    h, m = divmod(int(m), 60)
    return f"{h:02d}:{m:02d}:{s:05.2f}"


def cmd_transcribe(args: argparse.Namespace) -> None:
    from faster_whisper import WhisperModel  # imported lazily: heavy

    d = WORK / args.slug
    model = WhisperModel(args.model, device="auto", compute_type="int8")
    segments, info = model.transcribe(str(d / "source.mp4"), word_timestamps=True, vad_filter=True)
    segs = []
    for s in segments:
        segs.append({
            "start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
            "words": [{"start": round(w.start, 2), "end": round(w.end, 2), "word": w.word} for w in (s.words or [])],
        })
        print(f"[{fmt(s.start)}] {s.text.strip()}", flush=True)
    (d / "transcript.json").write_text(json.dumps({"language": info.language, "segments": segs}, indent=1))
    (d / "transcript.txt").write_text("\n".join(f"[{s['start']:.1f}-{s['end']:.1f}] {s['text']}" for s in segs))
    print(f"wrote {d/'transcript.txt'} ({len(segs)} segments, language={info.language})")



# ---------------------------------------------------------------- peaks
def cmd_peaks(args: argparse.Namespace) -> None:
    """Find hype moments: seconds whose loudness jumps well above the stream's normal level.

    Gaming/stream clips often peak on a reaction (scream, laugh, rage) that a transcript alone misses.
    """
    import statistics

    d = WORK / args.slug
    res = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(d / "source.mp4"), "-vn",
         "-af", "aresample=16000,asetnsamples=16000,astats=metadata=1:reset=1,"
                "ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
         "-f", "null", "-"],
        check=True, capture_output=True, text=True,
    )
    levels, t = [], None
    for line in res.stdout.splitlines():
        if "pts_time:" in line:
            t = float(line.rsplit("pts_time:", 1)[1])
        elif "RMS_level=" in line and t is not None:
            v = line.split("=", 1)[1]
            levels.append((t, -120.0 if v in ("-inf", "inf", "nan") else float(v)))
    if not levels:
        sys.exit("no audio found")
    vals = [v for _, v in levels]
    med = statistics.median(vals)
    spread = statistics.pstdev(vals) or 1.0
    # score each second against the median; keep the strongest, at least `gap` seconds apart
    scored = sorted(((v - med) / spread, t, v) for t, v in levels)[::-1]
    picked: list[tuple[float, float, float]] = []
    for z, t, v in scored:
        if z < args.min_z or len(picked) >= args.top:
            break
        if all(abs(t - pt) >= args.gap for _, pt, _ in picked):
            picked.append((z, t, v))
    picked.sort(key=lambda x: x[1])
    lines = [f"# median RMS {med:.1f} dB, stdev {spread:.1f} dB. Suggested window: peak-20s .. peak+10s"]
    lines += [f"{fmt(t)}  t={t:.0f}s  {v:.1f} dB  (+{z:.1f} sd)" for z, t, v in picked]
    (d / "peaks.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

# ---------------------------------------------------------------- render
def ass_time(t: float) -> str:
    t = max(t, 0)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,78,&H00FFFFFF,&H0000FFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,6,2,2,60,60,520,1
Style: Hook,DejaVu Sans,64,&H0000E5FF,&H0000E5FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,5,2,8,60,60,180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def words_in(transcript: dict, start: float, end: float) -> list[dict]:
    out = []
    for s in transcript["segments"]:
        ws = s.get("words") or [{"start": s["start"], "end": s["end"], "word": s["text"]}]
        for w in ws:
            if w["end"] > start and w["start"] < end:
                out.append(w)
    return out


def build_ass(words: list[dict], start: float, end: float, hook: str | None, per_line: int = 3) -> str:
    lines = [ASS_HEADER]
    if hook:
        lines.append(f"Dialogue: 1,{ass_time(0)},{ass_time(min(3.0, end - start))},Hook,,0,0,0,,{hook.upper()}")
    for i in range(0, len(words), per_line):
        chunk = words[i:i + per_line]
        a = chunk[0]["start"] - start
        b = (words[i + per_line]["start"] if i + per_line < len(words) else chunk[-1]["end"]) - start
        text = " ".join(w["word"].strip() for w in chunk).upper().replace("{", "(").replace("}", ")")
        lines.append(f"Dialogue: 0,{ass_time(a)},{ass_time(min(b, end - start))},Cap,,0,0,0,,{text}")
    return "\n".join(lines) + "\n"


def cmd_render(args: argparse.Namespace) -> None:
    d = WORK / args.slug
    clips = json.loads((d / "clips.json").read_text())
    transcript = json.loads((d / "transcript.json").read_text())
    od = OUT / args.slug
    od.mkdir(parents=True, exist_ok=True)
    # 16:9 -> 9:16: centre crop (fill) — or "blur" pads the full frame over a blurred background.
    if args.layout == "crop":
        vf_base = "crop=ih*9/16:ih,scale=1080:1920"
    elif args.layout == "stack":
        # Streamer layout: facecam box (--cam x:y:w:h in source pixels) on top, gameplay below.
        if not args.cam:
            sys.exit("--layout stack needs --cam x:y:w:h (the facecam rectangle in the source video)")
        cx, cy, cw, ch = args.cam.split(":")
        vf_base = (f"split[a][b];[a]crop={cw}:{ch}:{cx}:{cy},scale=1080:640:force_original_aspect_ratio=increase,"
                   f"crop=1080:640[cam];[b]crop=ih*27/32:ih,scale=1080:1280[game];[cam][game]vstack")
    else:
        vf_base = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20[bg];"
                   "[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
    for n, c in enumerate(clips, 1):
        start, end = float(c["start"]), float(c["end"])
        ass = d / f"clip_{n:02d}.ass"
        ass.write_text(build_ass(words_in(transcript, start, end), start, end, c.get("hook")))
        out = od / f"clip_{n:02d}_{slugify(c.get('title', ''))}.mp4"
        run([
            "ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start}", "-to", f"{end}", "-i", str(d / "source.mp4"),
            "-filter_complex", f"[0:v]{vf_base},ass={ass}[v]", "-map", "[v]", "-map", "0:a?",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
            "-movflags", "+faststart", str(out),
        ])
        print(f"rendered {out}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch"); f.add_argument("url"); f.add_argument("--slug")
    f.add_argument("--section", help="only download this time range, e.g. 1:20:00-1:50:00")
    t = sub.add_parser("transcribe"); t.add_argument("slug"); t.add_argument("--model", default="small")
    k = sub.add_parser("peaks"); k.add_argument("slug"); k.add_argument("--top", type=int, default=15)
    k.add_argument("--gap", type=float, default=30, help="min seconds between peaks")
    k.add_argument("--min-z", type=float, default=2.0, help="min loudness above normal, in std devs")
    r = sub.add_parser("render"); r.add_argument("slug")
    r.add_argument("--layout", choices=["crop", "blur", "stack"], default="blur")
    r.add_argument("--cam", help="facecam rectangle x:y:w:h for --layout stack")
    a = p.parse_args()
    {"fetch": cmd_fetch, "transcribe": cmd_transcribe, "peaks": cmd_peaks, "render": cmd_render}[a.cmd](a)


if __name__ == "__main__":
    main()
