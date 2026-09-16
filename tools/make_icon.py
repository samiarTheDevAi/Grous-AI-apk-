#!/usr/bin/env python3
"""Render the Grous AI launcher icon (gradient star) to PNG.

No third-party dependencies — pure Python (zlib + struct).

The artwork is faithful to the real app icon shipped inside the APK:
  * adaptive icon canvas: 108 x 108 dp
  * foreground star path (res/drawable/ic_launcher_fg.xml):
        M54,34 L60,48 L76,48 L63,57 L68,72 L54,63 L40,72 L45,57 L32,48 L48,48 Z
  * brand colors from the app UI: #635bff (accent) -> #00c2a8 (accent-2)

Usage:
    python3 make_icon.py [output.png] [size]
Defaults: grous-ai-icon.png, 512 px.
"""
import math
import struct
import sys
import zlib

STAR = [(54, 34), (60, 48), (76, 48), (63, 57), (68, 72),
        (54, 63), (40, 72), (45, 57), (32, 48), (48, 48)]
CANVAS = 108.0            # adaptive-icon canvas size (dp)
RADIUS_RATIO = 115 / 512  # squircle corner radius relative to output size
C1 = (0x63, 0x5B, 0xFF)   # #635bff
C2 = (0x00, 0xC2, 0xA8)   # #00c2a8


def point_in_polygon(x, y, poly):
    """Ray-casting point-in-polygon test."""
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def render(size, supersample=3):
    scale = size / CANVAS
    star = [(x * scale, y * scale) for x, y in STAR]
    r = RADIUS_RATIO * size
    cx = cy = size / 2
    half = size / 2
    inner = half - r

    buf = bytearray(size * size * 4)
    step = 1.0 / supersample
    for py in range(size):
        for px in range(size):
            r_acc = g_acc = b_acc = a_acc = 0.0
            samples = supersample * supersample
            for sy in range(supersample):
                y = (py + (sy + 0.5) * step)
                for sx in range(supersample):
                    x = (px + (sx + 0.5) * step)
                    # rounded-rect SDF for the corner alpha
                    dx = abs(x - cx) - inner
                    dy = abs(y - cy) - inner
                    dist = math.hypot(max(dx, 0.0), max(dy, 0.0)) - r
                    aa = 0.5 - dist  # 1px anti-alias band
                    corner_alpha = 1.0 if aa >= 1.0 else (0.0 if aa <= 0.0 else aa)
                    if corner_alpha <= 0.0:
                        continue
                    t = (x + y) / (2.0 * (size - 1.0))
                    tr, tg, tb = C1
                    rr = tr + (C2[0] - tr) * t
                    rg = tg + (C2[1] - tg) * t
                    rb = tb + (C2[2] - tb) * t
                    if point_in_polygon(x, y, star):
                        rr = rg = rb = 255.0
                    r_acc += rr * corner_alpha
                    g_acc += rg * corner_alpha
                    b_acc += rb * corner_alpha
                    a_acc += corner_alpha
            n = samples
            a = a_acc / n
            if a > 0.0:
                buf[(py * size + px) * 4 + 0] = min(255, round(r_acc / n))
                buf[(py * size + px) * 4 + 1] = min(255, round(g_acc / n))
                buf[(py * size + px) * 4 + 2] = min(255, round(b_acc / n))
                buf[(py * size + px) * 4 + 3] = min(255, round(a))
    return bytes(buf)


def write_png(path, size, rgba):
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        c += struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)
        return c

    raw = b''.join(b'\x00' + rgba[y * size * 4:(y + 1) * size * 4]
                   for y in range(size))
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(raw, 9))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'grous-ai-icon.png'
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 512
    rgba = render(size)
    write_png(out, size, rgba)
    print(f'wrote {out} ({size}x{size})')


if __name__ == '__main__':
    main()
