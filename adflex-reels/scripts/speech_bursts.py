#!/usr/bin/env python3
"""Find when speech actually happens in a clip, for caption timing and tail trims.

Captions timed to the whole shot appear before the line is spoken. This measures
the loud bursts in the clip's own audio so each caption chunk can be timed to them.

Usage:
    python3 speech_bursts.py clip.mp4
    python3 speech_bursts.py clip.mp4 --below-peak 22 --min-gap 0.25 --json

Needs ffmpeg on PATH. No Python packages.
"""
import argparse
import array
import json
import math
import subprocess
import sys

RATE = 16000
WINDOW = 0.02  # seconds


def decode(path):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(RATE),
           "-f", "s16le", "-"]
    try:
        raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    except FileNotFoundError:
        sys.exit("ffmpeg not found. Install it first (dnf/apt/brew install ffmpeg).")
    except subprocess.CalledProcessError as e:
        sys.exit(f"ffmpeg could not read {path}: {e.stderr.decode(errors='replace').strip()}")
    samples = array.array("h")
    samples.frombytes(raw[: len(raw) // 2 * 2])
    if sys.byteorder == "big":
        samples.byteswap()
    return samples


def window_levels(samples):
    """RMS level in dBFS for each WINDOW of audio."""
    size = int(RATE * WINDOW)
    levels = []
    for start in range(0, len(samples) - size + 1, size):
        chunk = samples[start:start + size]
        rms = math.sqrt(sum(s * s for s in chunk) / size)
        levels.append(20 * math.log10(rms / 32768) if rms > 0 else -120.0)
    return levels


def find_bursts(levels, below_peak, min_gap, min_len):
    if not levels:
        return [], -120.0
    peak = max(levels)
    threshold = peak - below_peak
    bursts = []
    start = None
    for i, level in enumerate(levels + [-120.0]):
        loud = level >= threshold
        if loud and start is None:
            start = i
        elif not loud and start is not None:
            bursts.append([start * WINDOW, i * WINDOW])
            start = None
    merged = []
    for burst in bursts:
        if merged and burst[0] - merged[-1][1] < min_gap:
            merged[-1][1] = burst[1]
        else:
            merged.append(burst)
    return [b for b in merged if b[1] - b[0] >= min_len], peak


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("file", help="video or audio file")
    p.add_argument("--below-peak", type=float, default=22.0,
                   help="dB below the loudest window that still counts as speech (default 22)")
    p.add_argument("--min-gap", type=float, default=0.25,
                   help="pauses shorter than this (s) stay inside one burst (default 0.25)")
    p.add_argument("--min-len", type=float, default=0.15,
                   help="ignore bursts shorter than this (s) (default 0.15)")
    p.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = p.parse_args()

    samples = decode(args.file)
    if not samples:
        sys.exit(f"{args.file} has no audio track.")
    duration = len(samples) / RATE
    bursts, peak = find_bursts(window_levels(samples), args.below_peak, args.min_gap, args.min_len)

    if args.json:
        print(json.dumps({
            "file": args.file,
            "duration": round(duration, 2),
            "peak_dbfs": round(peak, 1),
            "bursts": [{"start": round(a, 2), "end": round(b, 2)} for a, b in bursts],
        }, ensure_ascii=False, indent=2))
        return

    print(f"{args.file}: {duration:.2f} s, loudest window {peak:.1f} dBFS, "
          f"threshold {peak - args.below_peak:.1f} dBFS")
    if not bursts:
        print("No speech bursts found. Lower --below-peak or check the audio track.")
        return
    for n, (a, b) in enumerate(bursts, 1):
        print(f"  {n}. {a:6.2f} – {b:6.2f} s  ({b - a:.2f} s)")
    print(f"Dead air: {bursts[0][0]:.2f} s before the first burst, "
          f"{duration - bursts[-1][1]:.2f} s after the last.")


if __name__ == "__main__":
    main()
