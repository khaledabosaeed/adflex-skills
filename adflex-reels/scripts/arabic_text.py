#!/usr/bin/env python3
"""Render Arabic (or mixed Arabic/Latin) text to a transparent PNG for overlaying.

ffmpeg's own text shaping breaks Arabic, so captions, titles and end-card lines
are drawn here with Pillow + raqm and overlaid as images.

Usage:
    python3 arabic_text.py "كلها طلعت من رسالة وحدة لـ AdFlex" -o cap.png \
        --font Cairo-ExtraBold.ttf --latin-font Cairo-Latin.ttf --size 64 \
        --box "#8738F5" --max-width 900

Arabic web-font subsets have no ASCII digits or Latin letters. Pass --latin-font
and those characters are drawn with it. Without it everything uses --font.

Needs: pip install pillow, built with raqm (install libraqm first).
"""
import argparse
import sys

LATIN_JOINERS = set(".:,%$+-/@&'")


def split_runs(text):
    """Split into (is_latin, text) runs. Punctuation between Latin characters
    (8:00, adflex.ai) stays with them; spaces and Arabic go to the Arabic font."""
    def is_latin(i):
        ch = text[i]
        if ch.isascii() and ch.isalnum():
            return True
        if ch in LATIN_JOINERS:
            before = i > 0 and text[i - 1].isascii() and text[i - 1].isalnum()
            after = i + 1 < len(text) and text[i + 1].isascii() and text[i + 1].isalnum()
            return before and after
        return False

    runs = []
    for i, ch in enumerate(text):
        latin = is_latin(i)
        if runs and runs[-1][0] == latin:
            runs[-1][1] += ch
        else:
            runs.append([latin, ch])
    return [(latin, chunk) for latin, chunk in runs]


class Renderer:
    def __init__(self, args):
        from PIL import ImageFont, features
        if not features.check("raqm"):
            sys.exit("Pillow has no raqm support, so Arabic would render broken. "
                     "Install libraqm, then: pip install --force-reinstall pillow")
        try:
            self.font = ImageFont.truetype(args.font, args.size, layout_engine=ImageFont.Layout.RAQM)
            self.latin = (ImageFont.truetype(args.latin_font, args.size,
                                             layout_engine=ImageFont.Layout.RAQM)
                          if args.latin_font else self.font)
        except OSError as e:
            sys.exit(f"Could not load a font: {e}")
        self.rtl = args.direction == "rtl"
        self.stroke = args.stroke

    def pieces(self, line):
        """(font, text, direction, width) per run, in visual left-to-right order."""
        out = []
        for latin, chunk in split_runs(line):
            font = self.latin if latin else self.font
            direction = "ltr" if latin or not self.rtl else "rtl"
            width = font.getlength(chunk, direction=direction)
            out.append((font, chunk, direction, width))
        return out[::-1] if self.rtl else out

    def width(self, line):
        return sum(p[3] for p in self.pieces(line))

    def wrap(self, text, max_width):
        lines = []
        for paragraph in text.split("\n"):
            if not max_width:
                lines.append(paragraph)
                continue
            current = ""
            for word in paragraph.split():
                trial = f"{current} {word}".strip()
                if current and self.width(trial) > max_width:
                    lines.append(current)
                    current = word
                else:
                    current = trial
            lines.append(current)
        return lines

    def render(self, args):
        from PIL import Image, ImageDraw
        lines = self.wrap(args.text.replace("\\n", "\n"), args.max_width)
        ascent, descent = self.font.getmetrics()
        line_height = int((ascent + descent) * args.line_spacing)
        widths = [self.width(line) for line in lines]
        pad = args.padding if args.box else self.stroke + 2
        text_w = int(max(widths)) + 1
        text_h = line_height * (len(lines) - 1) + ascent + descent
        img = Image.new("RGBA", (text_w + 2 * pad, text_h + 2 * pad), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        if args.box:
            draw.rounded_rectangle([0, 0, img.width - 1, img.height - 1],
                                   radius=args.radius, fill=args.box)
        for n, line in enumerate(lines):
            x = pad + {"center": (text_w - widths[n]) / 2,
                       "right": text_w - widths[n], "left": 0}[args.align]
            y = pad + n * line_height
            for font, chunk, direction, width in self.pieces(line):
                draw.text((x, y), chunk, font=font, fill=args.color, direction=direction,
                          stroke_width=self.stroke, stroke_fill=args.stroke_color)
                x += width
        img.save(args.output)
        return img.size


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("text", help='the line; use "\\n" for a manual line break')
    p.add_argument("-o", "--output", required=True, help="output PNG")
    p.add_argument("--font", required=True, help="Arabic font file (.ttf/.otf/.woff)")
    p.add_argument("--latin-font", help="font for ASCII letters and digits")
    p.add_argument("--size", type=int, default=64)
    p.add_argument("--color", default="#FFFFFF")
    p.add_argument("--direction", choices=["rtl", "ltr"], default="rtl",
                   help="base direction of the line (default rtl)")
    p.add_argument("--align", choices=["center", "right", "left"], default="center")
    p.add_argument("--max-width", type=int, default=0, help="wrap at this many pixels")
    p.add_argument("--line-spacing", type=float, default=1.0,
                   help="line height multiplier; Cairo is tall, try 0.85 for tight captions")
    p.add_argument("--box", help="background box color, e.g. #8738F5 (omit for none)")
    p.add_argument("--radius", type=int, default=28, help="box corner radius")
    p.add_argument("--padding", type=int, default=28, help="box padding")
    p.add_argument("--stroke", type=int, default=0, help="outline width in pixels")
    p.add_argument("--stroke-color", default="#000000")
    args = p.parse_args()

    try:
        import PIL  # noqa: F401
    except ImportError:
        sys.exit("Pillow is needed: pip install pillow (after installing libraqm)")
    if not args.text.strip():
        sys.exit("The text is empty.")

    width, height = Renderer(args).render(args)
    print(f"{args.output}: {width}x{height}")


if __name__ == "__main__":
    main()
