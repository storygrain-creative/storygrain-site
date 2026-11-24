#!/usr/bin/env python3
"""
Rebuilds onesheet.html (screen, letter) and onesheet-print.html (print, 8.75 x 11.25 in
with 1/8" bleed) for the Storygrain packages one-sheet.

This replays, in order, the exact edits made in the original Claude session
(Oct 2026) that produced the printed PDF. The original working files were not
recoverable, so this script was reconstructed from that session's build steps.
Change copy in the CARDS / lists below, not by hand-editing the generated HTML.

Run from this folder:  python3 build_onesheet.py
Then:                  node render.js
"""
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
sym = open(os.path.join(HERE, '_symbols.html')).read()

# ---------------------------------------------------------------- step 1: base sheet
ck = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'
def li(items): return "".join(f'<li><span class="ck">{ck}</span><span>{i}</span></li>' for i in items)

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@page{{size:Letter;margin:0}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:"Schibsted Grotesk",Arial,sans-serif;color:#1C1F1D;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:8.5in;height:11in;position:relative;background:#F1EDE6;overflow:hidden}}
.mono{{font-family:"IBM Plex Mono",monospace;letter-spacing:.12em;text-transform:uppercase}}
header{{background:#2D3A33;color:#F1EDE6;padding:.5in .55in .42in;position:relative}}
.c{{position:absolute;width:14px;height:14px;border:0 solid rgba(241,237,230,.5)}}
.brand{{display:flex;align-items:center;gap:12px}}
.brand .m{{width:15px;height:35px;color:#A9B59B}} .brand .w{{width:168px;height:18px}}
header h1{{margin:22px 0 0;font-size:31px;line-height:1.05;font-weight:800;letter-spacing:-.02em;max-width:5.6in}}
header p{{margin:9px 0 0;font-size:11.5px;line-height:1.5;color:rgba(241,237,230,.82);max-width:5.4in}}
header .tag{{position:absolute;right:.55in;top:.55in;font-size:8.5px;color:#A9B59B}}
main{{padding:.32in .55in 0}}
.label{{font-size:8.5px;color:#5B625C;margin:0 0 9px}}
.pk{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.card{{background:#F8F5EF;border:1px solid #D9D3C7;border-radius:10px;padding:16px 15px 15px;display:flex;flex-direction:column}}
.card.hl{{background:#2D3A33;color:#F1EDE6;border-color:#2D3A33}}
.card .n{{font-size:9px;color:#5B625C}} .card.hl .n{{color:#A9B59B}}
.card h2{{margin:5px 0 0;font-size:21px;font-weight:800;letter-spacing:-.02em}}
.price{{margin-top:8px;display:flex;align-items:baseline;gap:4px}}
.price b{{font-size:26px;font-weight:800;letter-spacing:-.02em}} .price span{{font-size:10.5px;color:#5B625C}} .card.hl .price span{{color:rgba(241,237,230,.7)}}
.for{{margin:7px 0 0;font-size:10px;line-height:1.4;color:#5B625C;min-height:28px}} .card.hl .for{{color:rgba(241,237,230,.78)}}
.shoot{{margin-top:10px;padding:7px 9px;border-radius:6px;background:#E6E1D6;font-size:10px;font-weight:600;color:#2D3A33}}
.card.hl .shoot{{background:rgba(169,181,155,.2);color:#F1EDE6}}
ul{{list-style:none;padding:0;margin:11px 0 0;display:grid;gap:6px}}
li{{display:flex;gap:7px;font-size:10.2px;line-height:1.35}}
.ck{{flex:none;width:13px;height:13px;margin-top:1px;border-radius:50%;background:#2D3A33;color:#F1EDE6;display:grid;place-items:center}}
.ck svg{{width:8px;height:8px}}
.card.hl .ck{{background:#A9B59B;color:#2D3A33}}
.row{{display:grid;grid-template-columns:1.25fr 1fr;gap:12px;margin-top:16px}}
.box{{border:1px solid #D9D3C7;border-radius:10px;padding:14px 15px;background:#F8F5EF}}
.box h3{{margin:0 0 8px;font-size:12.5px;font-weight:800;color:#2D3A33}}
.inc{{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin:0}}
.adds{{display:grid;gap:6px;font-size:10.2px}}
.adds div{{display:flex;justify-content:space-between;gap:10px;border-bottom:1px dashed #D9D3C7;padding-bottom:5px}}
.adds div:last-child{{border:0;padding:0}}
.adds b{{font-weight:600;color:#2D3A33;white-space:nowrap}}
.proj{{margin-top:12px;display:flex;align-items:center;gap:14px;background:#A9B59B;border-radius:10px;padding:12px 15px}}
.proj b{{font-size:12px;color:#2D3A33;white-space:nowrap}} .proj span{{font-size:10.2px;color:#2D3A33}}
footer{{position:absolute;left:0;right:0;bottom:0;background:#2D3A33;color:#F1EDE6;padding:.24in .55in;display:flex;justify-content:space-between;align-items:center;gap:20px}}
footer .cta{{font-size:13px;font-weight:800}} footer .cta small{{display:block;font-weight:400;font-size:9.5px;color:rgba(241,237,230,.75);margin-top:2px}}
footer .ct{{text-align:right;font-size:9px;color:#A9B59B;line-height:1.7}}
</style></head><body>{sym}<div class="page">
<header>
<div class="c" style="top:14px;left:14px;border-top-width:1.5px;border-left-width:1.5px"></div><div class="c" style="top:14px;right:14px;border-top-width:1.5px;border-right-width:1.5px"></div>
<div class="c" style="bottom:14px;left:14px;border-bottom-width:1.5px;border-left-width:1.5px"></div><div class="c" style="bottom:14px;right:14px;border-bottom-width:1.5px;border-right-width:1.5px"></div>
<div class="brand"><svg class="m"><use href="#sg-mark"/></svg><svg class="w"><use href="#sg-word"/></svg></div>
<span class="tag mono">Monthly Content Partnerships</span>
<h1>The marketing team for businesses that don't have one.</h1>
<p>Every month we plan, shoot and deliver finished video, photo and social content. Scripts, shot lists and captions are written before we pick up a camera, so nothing is improvised.</p>
</header>
<main>
<p class="label mono">Choose your level</p>
<div class="pk">
<div class="card"><span class="n mono">01</span><h2>Starter</h2><div class="price"><b>$2,000</b><span>/ month</span></div>
<p class="for">For businesses ready to start showing up consistently.</p><div class="shoot">2-hour monthly shoot</div>
<ul>{li(["6 short-form videos","15 edited photos","Scripts and shot list","Captions for every post"])}</ul></div>
<div class="card hl"><span class="n mono">02</span><h2>Standard</h2><div class="price"><b>$3,500</b><span>/ month</span></div>
<p class="for">For businesses that want a full month of content with a plan behind it.</p><div class="shoot">4-hour monthly shoot</div>
<ul>{li(["10 short-form videos","30 edited photos","Everything in Starter","Monthly content calendar","Monthly planning call"])}</ul></div>
<div class="card"><span class="n mono">03</span><h2>Full</h2><div class="price"><b>$6,000</b><span>/ month</span></div>
<p class="for">For businesses that want marketing handled end to end.</p><div class="shoot">6 to 8-hour monthly shoot</div>
<ul>{li(["Videos scoped to your monthly plan","Full photo library","Quarterly campaign planning","Scheduling and publishing","Meta and Instagram ad management","Ongoing communications counsel","Monthly performance review"])}</ul></div>
</div>
<div class="row">
<div class="box"><h3>Every partnership includes</h3><ul class="inc">{li(["Content planned before the shoot","Delivery by the 1st of the month","One revision round per piece","You own every file","Three-month initial commitment","Fixed deliverables, no guessing"])}</ul></div>
<div class="box"><h3>Add-ons</h3><div class="adds"><div><span>Additional short-form video</span><b>$150</b></div><div><span>Long-form video (2 to 5 min)</span><b>$750</b></div><div><span>Additional shoot day</span><b>$1,200</b></div></div></div>
</div>
<div class="proj"><b>Quoted per project</b><span>Websites, logos and brand identity, print design, event coverage and brand films.</span></div>
</main>
<footer><div class="cta">Not sure which fits?<small>Take the 3-minute Content Check at storygrain.co/check</small></div>
<div class="ct mono">hello@storygrain.co<br>storygrain.co · @storygrain.co<br>Eric Wendt &amp; Austin Asay · Omaha, NE</div></footer>
</div></body></html>'''
s = html

def rep(s, a, b, count=-1):
    assert a in s, a
    return s.replace(a, b, count)

# ---------------------------------------------------------------- step 2: exclusions + spacing
s = rep(s, '</main>', '<p class="excl"><b>Not included in packages:</b> paid ad spend, community management (replying to comments and messages), SEO and website work.</p>\n</main>')
s = rep(s, '.proj b{', '.excl{margin:14px 2px 0;font-size:9.8px;color:#5B625C;line-height:1.5}.excl b{color:#2D3A33;font-weight:600}\n.proj b{')
s = rep(s, '.row{display:grid;grid-template-columns:1.25fr 1fr;gap:12px;margin-top:16px}', '.row{display:grid;grid-template-columns:1.25fr 1fr;gap:12px;margin-top:20px}')
s = rep(s, 'main{padding:.32in .55in 0}', 'main{padding:.4in .55in 0}')

# ---------------------------------------------------------------- step 3: "Who posts" cards (draft 2)
blocks = list(re.finditer(r'<div class="card( hl)?">.*?</ul></div>', s, re.S))
assert len(blocks) == 3
CARDS = [
 ('', '01', 'Starter', '$2,000', 'For businesses ready to start showing up consistently.', 'You post', '2-hour monthly shoot',
  ["6 short-form videos", "15 edited photos", "Scripts and shot list", "Captions for every post", "Suggested post dates", "Delivered ready to post"]),
 (' hl', '02', 'Standard', '$3,500', 'For businesses that want their feed running without them.', 'We post for you', '4-hour monthly shoot',
  ["10 short-form videos", "30 edited photos", "Everything in Starter", "Monthly content calendar", "Monthly planning call", "Scheduled and published to Instagram and Facebook"]),
 ('', '03', 'Full', '$6,000', 'For businesses ready to grow with ads, campaigns and reporting.', 'We run it', '6 to 8-hour monthly shoot',
  ["Videos scoped to your monthly plan", "Full photo library", "Everything in Standard", "Quarterly campaign planning", "Meta and Instagram ad management", "Monthly performance review", "Ongoing communications counsel"]),
]
cards = [f'<div class="card{h}"><span class="n mono">{n}</span><h2>{t}</h2><div class="price"><b>{p}</b><span>/ month</span></div><p class="for">{f}</p><div class="who"><i>WHO POSTS</i>{w}</div><div class="shoot">{sh}</div><ul>{li(it)}</ul></div>' for h, n, t, p, f, w, sh, it in CARDS]
for b, h in zip(reversed(blocks), reversed(cards)):
    s = s[:b.start()] + h + s[b.end():]
s = rep(s, '.shoot{', '.who{margin-top:10px;padding-top:9px;border-top:1px solid #D9D3C7;font-size:12px;font-weight:800;color:#2D3A33;display:flex;align-items:baseline;justify-content:space-between;gap:8px}.who i{font-style:normal;font-family:"IBM Plex Mono",monospace;font-size:7.5px;letter-spacing:.12em;color:#5B625C;font-weight:400}.card.hl .who{color:#F1EDE6;border-color:rgba(241,237,230,.2)}.card.hl .who i{color:#A9B59B}\n.shoot{', 1)
s = rep(s, 'community management (replying to comments and messages)', 'community management (replying to comments and messages, which is separate from posting)')

# ---------------------------------------------------------------- step 4: static print font family
s = rep(s, 'font-family:"Schibsted Grotesk",Arial,sans-serif', 'font-family:"SG Print","Schibsted Grotesk",Arial,sans-serif')

# ---------------------------------------------------------------- step 5: add-on wording
s = rep(s, '<div><span>Additional short-form video</span><b>$150</b></div><div><span>Long-form video (2 to 5 min)</span><b>$750</b></div><div><span>Additional shoot day</span><b>$1,200</b></div>',
           '<div><span>Additional short-form video edit</span><b>$150</b></div><div><span>Long-form video edit (2 to 5 min)</span><b>$750</b></div><div><span>Additional on-location shoot</span><b>$200/hr</b></div>')

# ---------------------------------------------------------------- step 6: reorder includes + no orphans
m = re.search(r'<ul class="inc">(.*?)</ul>', s, re.S)
items = re.findall(r'<li>.*?</li>', m.group(1), re.S)
def find(t): return [i for i in items if t in i][0]
order = ['Delivery by the 1st', 'One revision round', 'You own every file', 'Fixed deliverables', 'Three-month initial', 'Content planned']
s = s[:m.start(1)] + ''.join(find(t) for t in order) + s[m.end(1):]
def glue(txt):
    txt = txt.rstrip()
    return re.sub(r'\s+(\S+)$', r'&nbsp;\1', txt) if len(txt.split()) > 2 else txt
s = re.sub(r'(<li><span class="ck">.*?</span><span>)(.*?)(</span></li>)', lambda m: m.group(1)+glue(m.group(2))+m.group(3), s, flags=re.S)
s = re.sub(r'(<p class="for">)(.*?)(</p>)', lambda m: m.group(1)+glue(m.group(2))+m.group(3), s)
s = re.sub(r'(<p class="excl"><b>.*?</b>)(.*?)(</p>)', lambda m: m.group(1)+glue(m.group(2))+m.group(3), s)
s = re.sub(r'(<div class="proj"><b>.*?</b><span>)(.*?)(</span>)', lambda m: m.group(1)+glue(m.group(2))+m.group(3), s)
s = re.sub(r'(<header>.*?<p>)(.*?)(</p>)', lambda m: m.group(1)+glue(m.group(2))+m.group(3), s, flags=re.S)
s = re.sub(r'(<h1[^>]*>)(.*?)(</h1>)', lambda m: m.group(1)+glue(m.group(2))+m.group(3), s)
s = rep(s, 'body{margin:0;', 'body{margin:0;text-wrap:pretty;', 1)

# ---------------------------------------------------------------- step 7: forced line break
s = rep(s, 'Content planned before the&nbsp;shoot', 'Content planned before<br>the&nbsp;shoot')

open(os.path.join(HERE, 'onesheet.html'), 'w').write(s)

# ---------------------------------------------------------------- print version (bleed + safe zone)
p = s
for a, b in [
    ('@page{size:Letter;margin:0}', '@page{size:8.75in 11.25in;margin:0}'),
    ('.page{width:8.5in;height:11in;', '.page{width:8.75in;height:11.25in;'),
    ('header{background:#2D3A33;color:#F1EDE6;padding:.5in .55in .42in;', 'header{background:#2D3A33;color:#F1EDE6;padding:.625in .675in .42in;'),
    ('header .tag{position:absolute;right:.55in;top:.55in;', 'header .tag{position:absolute;right:.675in;top:.675in;'),
    ('main{padding:.4in .55in 0}', 'main{padding:.4in .675in 0}'),
    ('footer{position:absolute;left:0;right:0;bottom:0;background:#2D3A33;color:#F1EDE6;padding:.24in .55in;', 'footer{position:absolute;left:0;right:0;bottom:0;background:#2D3A33;color:#F1EDE6;padding:.24in .675in .365in;'),
]:
    p = rep(p, a, b)
p = p.replace('top:14px;left:14px', 'top:.425in;left:.425in').replace('top:14px;right:14px', 'top:.425in;right:.425in') \
     .replace('bottom:14px;left:14px', 'bottom:.3in;left:.425in').replace('bottom:14px;right:14px', 'bottom:.3in;right:.425in')
open(os.path.join(HERE, 'onesheet-print.html'), 'w').write(p)
print('wrote onesheet.html and onesheet-print.html')
