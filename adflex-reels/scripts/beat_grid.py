#!/usr/bin/env python3
"""Get the real beat grid of a music track, for cuts that land on the beat.

Prints the tempo, the beat times, cut points every N beats, and where the track
really goes silent (generated music often ends earlier or later than asked).

Usage:
    python3 beat_grid.py track.mp3
    python3 beat_grid.py track.mp3 --every 2 --json

Needs: pip install librosa numpy
"""
import argparse
import json
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("file", help="music file")
    p.add_argument("--every", type=int, default=2, help="cut every N beats (default 2)")
    p.add_argument("--silence-db", type=float, default=40.0,
                   help="dB below the peak that counts as silence (default 40)")
    p.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = p.parse_args()
    if args.every < 1:
        sys.exit("--every must be 1 or more.")

    try:
        import librosa
        import numpy as np
    except ImportError:
        sys.exit("librosa and numpy are needed: pip install librosa numpy")

    try:
        y, sr = librosa.load(args.file, sr=None, mono=True)
    except Exception as e:  # librosa raises many backend-specific errors
        sys.exit(f"Could not read {args.file}: {e}")
    if y.size == 0:
        sys.exit(f"{args.file} has no audio.")

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(np.atleast_1d(tempo)[0])
    beats = [float(t) for t in librosa.frames_to_time(beat_frames, sr=sr)]
    cuts = beats[::args.every]

    # Last moment the track is still audible.
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(rms, sr=sr)
    level = librosa.amplitude_to_db(rms, ref=np.max)
    audible = np.where(level > -args.silence_db)[0]
    last_sound = float(times[audible[-1]]) if audible.size else 0.0
    duration = float(len(y) / sr)

    if args.json:
        print(json.dumps({
            "file": args.file,
            "duration": round(duration, 2),
            "bpm": round(tempo, 1),
            "beat_seconds": round(60 / tempo, 3) if tempo else None,
            "beats": [round(b, 3) for b in beats],
            "cuts": [round(c, 3) for c in cuts],
            "last_sound": round(last_sound, 2),
        }, indent=2))
        return

    print(f"{args.file}: {duration:.2f} s, about {tempo:.0f} BPM "
          f"(one beat = {60 / tempo:.3f} s)" if tempo else f"{args.file}: no clear tempo")
    print(f"Sound ends at {last_sound:.2f} s ({duration - last_sound:.2f} s of silence at the end).")
    print(f"Cut points, every {args.every} beat(s):")
    print("  " + "  ".join(f"{c:.2f}" for c in cuts))


if __name__ == "__main__":
    main()
