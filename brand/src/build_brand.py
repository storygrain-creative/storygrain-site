#!/usr/bin/env python3
"""
Builds the StoryGrain logo kit from the exact vectors live on storygrain.co.

Outputs (relative to /brand):
  logo/clean/{horizontal,stacked,mark}/   SVG + PDF + PNG
  logo/grain/{horizontal,stacked,mark}/   SVG + PDF + PNG (focus-pull film grain)
  logo/wordmark/                          SVG + PDF + PNG
  social-icons/                           1080px SVG + PNG
  storygrain-brand-board.{svg,png,pdf}

Requires: pip install cairosvg svgpathtools shapely scipy pillow potracer
Run from /brand/src:  python3 build_brand.py
"""
import os, json
import cairosvg
import sg_mark, grain_focus

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
COLORS = json.load(open(os.path.join(ROOT, 'colors.json')))['brand']
F, SG, CR, INK = (COLORS[k]['hex'] for k in ('forest', 'sage', 'cream', 'ink'))
BLACK, WHITE = '#000000', '#FFFFFF'

MX0, MY0, MX1, MY1 = sg_mark.bounds()
MW, MH = MX1 - MX0, MY1 - MY0
HALO = 40.0  # mark units of extra room for the grain falloff (same as the Oct 2026 kit)

print('building grain mark (about 30 seconds)...')
_core, _dots, _n = grain_focus.build()
MARK = {'clean': [(sg_mark.path_d(), 'nonzero')], 'grain': [(_core, 'nonzero'), (_dots, 'nonzero')]}

# wordmark geometry: viewBox "28 28 686 74", path has its own transform
WX, WY, WW, WH = sg_mark.word_box()

def mark_paths(fin, fill, x, y, h):
    """Mark with its clean-bounds top-left at (x, y) and clean height h."""
    sc = h / MH
    t = f'translate({x - MX0 * sc:.3f},{y - MY0 * sc:.3f}) scale({sc:.5f})'
    return ''.join(f'<path fill="{fill}" fill-rule="{r}" transform="{t}" d="{d}"/>' for d, r in MARK[fin]), MW * sc

def word_paths(fill, x, y, h):
    sc = h / WH
    t = f'translate({x - WX * sc:.3f},{y - WY * sc:.3f}) scale({sc:.5f}) {sg_mark.WORD_TRANSFORM}'
    return f'<path fill="{fill}" fill-rule="nonzero" transform="{t}" d="{sg_mark.WORD_D}"/>', WW * sc

def svg(body, w, h, bg=None):
    r = f'<rect width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
            f'width="{w:.2f}" height="{h:.2f}">{r}{body}</svg>')

# --- lockups (proportions from the site header: word height = 0.425 x mark height, gap = 0.3 x mark height)
MARK_H = 400.0
def horizontal(fin, mc, wc):
    pad = 30 + (HALO * MARK_H / MH if fin == 'grain' else 0)
    wh = MARK_H * 0.425; gap = MARK_H * 0.30
    m, mw = mark_paths(fin, mc, pad, pad, MARK_H)
    ww = WW * wh / WH
    w, _ = word_paths(wc, pad + mw + gap, pad + (MARK_H - wh) / 2, wh)
    return svg(m + w, pad * 2 + mw + gap + ww, pad * 2 + MARK_H)

def stacked(fin, mc, wc):
    pad = 30 + (HALO * MARK_H / MH if fin == 'grain' else 0)
    mw = MW * MARK_H / MH
    ww = mw * 2.6; wh = WH * ww / WW; gap = MARK_H * 0.14
    W = pad * 2 + max(ww, mw)
    m, _ = mark_paths(fin, mc, (W - mw) / 2, pad, MARK_H)
    w, _ = word_paths(wc, (W - ww) / 2, pad + MARK_H + gap, wh)
    return svg(m + w, W, pad * 2 + MARK_H + gap + wh)

def mark_only(fin, fill, bg=None):
    pad = 30 + (HALO * MARK_H / MH if fin == 'grain' else 0)
    m, mw = mark_paths(fin, fill, pad, pad, MARK_H)
    return svg(m, pad * 2 + mw, pad * 2 + MARK_H, bg)

def wordmark(fill):
    h = 120.0; pad = 30
    w, ww = word_paths(fill, pad, pad, h)
    return svg(w, pad * 2 + ww, pad * 2 + h)

def write(folder, name, s, png_w=None, png_h=None):
    d = os.path.join(ROOT, folder); os.makedirs(d, exist_ok=True)
    base = os.path.join(d, name)
    open(base + '.svg', 'w').write(s)
    cairosvg.svg2pdf(bytestring=s.encode(), write_to=base + '.pdf')
    kw = {'output_width': png_w} if png_w else {'output_height': png_h or 3000}
    cairosvg.svg2png(bytestring=s.encode(), write_to=base + '.png', **kw)

# name, mark color, word color   (background guide lives in BRAND.md)
LOCKUPS = [('forest', F, F), ('ink', INK, INK), ('black', BLACK, BLACK),
           ('sage-cream', SG, CR), ('cream', CR, CR), ('white', WHITE, WHITE)]
MARKS = [('forest', F), ('sage', SG), ('ink', INK), ('black', BLACK), ('cream', CR), ('white', WHITE)]
WORDS = [('forest', F), ('ink', INK), ('black', BLACK), ('cream', CR), ('white', WHITE)]

for fin in ('clean', 'grain'):
    for sch, mc, wc in LOCKUPS:
        write(f'logo/{fin}/horizontal', f'storygrain-horizontal-{fin}-{sch}', horizontal(fin, mc, wc), png_w=3000)
        write(f'logo/{fin}/stacked', f'storygrain-stacked-{fin}-{sch}', stacked(fin, mc, wc), png_h=3000)
    for sch, c in MARKS:
        write(f'logo/{fin}/mark', f'storygrain-mark-{fin}-{sch}', mark_only(fin, c), png_h=3000)
for sch, c in WORDS:
    write('logo/wordmark', f'storygrain-wordmark-{sch}', wordmark(c), png_w=3000)

# --- social / app icons
os.makedirs(os.path.join(ROOT, 'social-icons'), exist_ok=True)
def icon(fin, mark_fill, bg, size=1080):
    mh = size * 0.62
    sc = mh / MH; mw = MW * sc
    m, _ = mark_paths(fin, mark_fill, (size - mw) / 2, (size - mh) / 2, mh)
    return svg(m, size, size, bg)
for name, (fin, mf, bg) in {
    'icon-forest': ('clean', SG, F),
    'icon-sage': ('clean', F, SG),
    'icon-cream': ('clean', F, CR),
    'icon-forest-grain': ('grain', SG, F),
}.items():
    s = icon(fin, mf, bg)
    p = os.path.join(ROOT, 'social-icons', f'storygrain-{name}')
    open(p + '.svg', 'w').write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to=p + '.png', output_width=1080)

# --- brand board (text uses installed fonts: Schibsted Grotesk as "SG Print", IBM Plex Mono)
def lockup_img(s, x, y, w):
    import base64, re
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    h = w * float(vb.group(2)) / float(vb.group(1))
    return f'<image x="{x}" y="{y}" width="{w}" height="{h:.1f}" href="data:image/svg+xml;base64,{base64.b64encode(s.encode()).decode()}"/>', h

BW, BH = 1600, 1200
o = [f'<rect width="{BW}" height="{BH}" fill="{CR}"/>']
img, h = lockup_img(horizontal('clean', F, F), 80, 90, 760); o.append(img)
o.append(f'<rect x="900" y="60" width="620" height="300" rx="16" fill="{F}"/>')
img, h = lockup_img(horizontal('clean', SG, CR), 960, 160, 500); o.append(img)
o.append(f'<text x="80" y="440" font-family="IBM Plex Mono" font-size="15" letter-spacing="2" fill="#5B625C">COLOR</text>')
for i, key in enumerate(['forest', 'sage', 'cream', 'ink']):
    c = COLORS[key]; x = 80 + i * 370
    o.append(f'<rect x="{x}" y="465" width="340" height="250" rx="14" fill="{c["hex"]}" stroke="#D9D3C7"/>')
    tc = INK if key in ('cream', 'sage') else CR
    o.append(f'<text x="{x+24}" y="510" font-family="SG Print" font-weight="800" font-size="30" fill="{tc}">{c["name"]}</text>')
    for j, line in enumerate([c['hex'], 'RGB ' + ' '.join(map(str, c['rgb'])), 'CMYK ' + ' '.join(map(str, c['cmyk']))]):
        o.append(f'<text x="{x+24}" y="{640+j*26}" font-family="IBM Plex Mono" font-size="16" fill="{tc}">{line}</text>')
o.append(f'<text x="80" y="790" font-family="IBM Plex Mono" font-size="15" letter-spacing="2" fill="#5B625C">TYPE</text>')
o.append(f'<text x="80" y="860" font-family="SG Print" font-weight="800" font-size="56" fill="{INK}">Schibsted Grotesk</text>')
o.append(f'<text x="80" y="900" font-family="SG Print" font-size="22" fill="#5B625C">Headlines 800 · Body 400 · UI 500 and 600</text>')
o.append(f'<text x="80" y="980" font-family="IBM Plex Mono" font-size="40" fill="{INK}">IBM PLEX MONO</text>')
o.append(f'<text x="80" y="1018" font-family="SG Print" font-size="22" fill="#5B625C">Labels, timecode, small caps details · 400 and 500</text>')
o.append(f'<text x="80" y="1098" font-family="SG Print" font-size="22" fill="#5B625C">Logo wordmark: Montserrat (STORY ExtraBold, GRAIN Regular), outlined. Not used as a text font.</text>')
for k, (fin, mc, bg) in enumerate([('clean', F, CR), ('clean', SG, F), ('grain', F, CR), ('clean', F, SG)]):
    x = 900 + k * 160
    o.append(f'<rect x="{x}" y="790" width="140" height="240" rx="12" fill="{bg}" stroke="#D9D3C7"/>')
    img, _ = lockup_img(mark_only(fin, mc), x + 25, 815, 90); o.append(img)
board = svg(''.join(o), BW, BH)
bp = os.path.join(ROOT, 'storygrain-brand-board')
open(bp + '.svg', 'w').write(board)
cairosvg.svg2png(bytestring=board.encode(), write_to=bp + '.png', output_width=BW)
cairosvg.svg2pdf(bytestring=board.encode(), write_to=bp + '.pdf')
print('done')
