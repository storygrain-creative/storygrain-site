"""Focus-pull film grain for the StoryGrain mark.

Same algorithm and final settings as the approved Oct 2026 version: the mark is rendered,
blurred by a depth-of-field map (sharp at a focus point on the inner curve of the middle
blade, softer away from it), then stippled: a solid core where density is high, random dots
in the falloff. Output stays one-color vector: a core path plus a field of dots, in mark units.

Note: dot placement is random (seeded), so regenerated files match the approved look and
settings but are not dot-for-dot identical to the original Oct 2026 files.
"""
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter
import potrace
from sg_mark import polygons

S = 8.0          # raster px per mark unit
MARGIN = 70.0    # mark units of room for the soft halo

def build(focus=(0.80, 0.56), r_sharp=0.06, r_soft=0.46, max_sigma=20.0,
          cell=1.5, core_at=0.93, seed=3):
    polys = polygons()
    x0 = min(p.bounds[0] for p in polys) - MARGIN; y0 = min(p.bounds[1] for p in polys) - MARGIN
    x1 = max(p.bounds[2] for p in polys) + MARGIN; y1 = max(p.bounds[3] for p in polys) + MARGIN
    W, H = int((x1 - x0) * S), int((y1 - y0) * S)

    img = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(img)
    for p in polys:
        dr.polygon([((x - x0) * S, (y - y0) * S) for x, y in p.exterior.coords], fill=255)
    m = np.asarray(img, dtype=np.float32) / 255.0

    mx0, my0, mx1, my1 = (min(p.bounds[0] for p in polys), min(p.bounds[1] for p in polys),
                          max(p.bounds[2] for p in polys), max(p.bounds[3] for p in polys))
    fx = ((mx0 + focus[0] * (mx1 - mx0)) - x0) * S
    fy = ((my0 + focus[1] * (my1 - my0)) - y0) * S
    span = (my1 - my0) * S
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.hypot(xx - fx, (yy - fy) * 0.85) / span
    t = np.clip((dist - r_sharp) / (r_soft - r_sharp), 0, 1) ** 1.3

    levels = [0.0, 0.18, 0.36, 0.55, 0.78, 1.0]
    stack = [m if l == 0 else gaussian_filter(m, l * max_sigma * S) for l in levels]
    w = t
    D = np.zeros_like(m)
    for i in range(len(levels) - 1):
        a, b = levels[i], levels[i + 1]
        sel = (w >= a) & (w <= b)
        k = np.where(sel, (w - a) / (b - a), 0)
        D = np.where(sel, stack[i] * (1 - k) + stack[i + 1] * k, D)

    core = D >= core_at
    path = potrace.Bitmap(~core).trace(turdsize=40, alphamax=1.0, opticurve=True, opttolerance=0.3)
    U = lambda pt: (pt.x / S + x0, pt.y / S + y0)
    parts = []
    for c in path:
        sx, sy = U(c.start_point); s = f"M{sx:.2f},{sy:.2f}"
        for g in c.segments:
            if g.is_corner:
                (ax, ay), (bx, by) = U(g.c), U(g.end_point); s += f"L{ax:.2f},{ay:.2f}L{bx:.2f},{by:.2f}"
            else:
                (ax, ay), (bx, by), (ex, ey) = U(g.c1), U(g.c2), U(g.end_point)
                s += f"C{ax:.2f},{ay:.2f} {bx:.2f},{by:.2f} {ex:.2f},{ey:.2f}"
        parts.append(s + "Z")
    core_d = "".join(parts)

    rng = np.random.default_rng(seed)
    dots = []
    gx = np.arange(x0, x1, cell); gy = np.arange(y0, y1, cell)
    for yv in gy:
        jx = gx + rng.uniform(0, cell, gx.size); jy = yv + rng.uniform(0, cell, gx.size)
        px = np.clip(((jx - x0) * S).astype(int), 0, W - 1); py = np.clip(((jy - y0) * S).astype(int), 0, H - 1)
        d = D[py, px]
        keep = (d > 0.03) & (d < core_at + 0.04) & (rng.random(gx.size) < np.clip(d ** 1.15 * 1.05, 0, 1))
        for x, y, dv in zip(jx[keep], jy[keep], d[keep]):
            r = 0.42 + 0.78 * dv + rng.uniform(-0.08, 0.08)
            dots.append(f"M{x - r:.2f},{y:.2f}a{r:.2f},{r:.2f} 0 1,0 {2*r:.2f},0a{r:.2f},{r:.2f} 0 1,0 {-2*r:.2f},0Z")
    return core_d, "".join(dots), len(dots)
