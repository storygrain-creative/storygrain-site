# StoryGrain brand

Brand name **Storygrain**. Company name **Storygrain Creative**. Category: creative marketing company, Omaha, NE. Co-founders: Eric Wendt (Co-Founder | Creative & Strategy) and Austin Asay (Co-Founder | Video & Production). One shared inbox: hello@storygrain.co. Domain: storygrain.co. Instagram: @storygrain.co (@storygrain was taken).

## Rules

### Wordmark and tagline
- The wordmark reads **"StoryGrain" only, never with a subtitle or tagline.** It's set as STORYGRAIN: STORY in Montserrat ExtraBold, GRAIN in Montserrat Regular, converted to outlines. Use the files; don't retype it.
- The tagline **"Making Consistent Creativity Possible." is for bios only.** It never goes in a logo lockup.
- No individual email addresses. Everything goes to hello@storygrain.co.

### Logo mark
- The mark is Austin's three-blade S. Each blade reads as its own S. **Refine it, don't change it.** The approved version was traced from Austin's original and differs from it by only about half a pixel, with cleaner edges and sharp tips.
- **Blades never overlap.** Keep the even gaps between them.
- Don't flatten the S-curve out of the blades. An early redraw did this and was rejected.

### Color
- The palette is **Forest, Sage, Cream, and Ink**. It was made final Oct 23, 2026.
- **No gold or bronze tones. Bronze was dropped.** Sower Media (sower.media), friends with a similar business, use metallic gold as their signature. StoryGrain should never look like it's borrowing from them: no gold, bronze, tan, or brass, and no metallic gradients or foil.
- Defaults: on light backgrounds, mark and word are both Forest. On Forest, the mark is Sage and the word is Cream.

### Grain
- "Grain" means **film grain** (a double meaning that nods to the Midwest). **No wheat, stalks, fields, or harvest imagery.**
- The grain finish works like a camera **focus pull**: sharp at one point (the inner curve of the middle blade), softening into film grain away from it. It's one color and fully vector.
- **Clean is the default.** Use the grain version large: video end cards, social posts, posters, web headers.
- **Below about 1 inch, and on anything embroidered, stitched, or vinyl-cut, use the clean mark.** Apparel always uses the clean mark, because the grain fills in or drops out at hat scale. Tell embroiderers to use the clean files only.
- Grain SVGs are heavy (about 0.5 MB). If a printer has trouble, send the PDF.

## Colors

| | HEX | RGB | CMYK (starting point) |
|---|---|---|---|
| **Forest** | `#2D3A33` | 45, 58, 51 | 81, 55, 73, 67 |
| **Sage** | `#A9B59B` | 169, 181, 155 | 38, 19, 42, 5 |
| **Cream** | `#F1EDE6` | 241, 237, 230 | 7, 7, 11, 0 |
| **Ink** | `#1C1F1D` | 28, 31, 29 | 82, 68, 61, 97 |

HEX and RGB are the approved values and match storygrain.co. **CMYK was never set with a printer.** The values above come from an ICC conversion (sRGB to FOGRA39 coated, relative colorimetric). Proof them before a large run, especially on uncoated stock, where Forest and Ink will print lighter and flatter. Machine-readable values are in `colors.json`.

The site and the one-sheet also use supporting UI tints. These are not brand colors and don't go in the logo: forest-deep `#243029`, sage-hover `#B9C4AC`, card `#F8F5EF`, tint `#E6E1D6`, line `#D9D3C7`, muted text `#5B625C`, and a form-error red `#9B3B2E`.

## Fonts

| Font | Weights | Where |
|---|---|---|
| **Montserrat** | ExtraBold (STORY), Regular (GRAIN) | Logo wordmark only, outlined. Not a text font. It was kept to the logo so headlines wouldn't feel like siblings of the wordmark. |
| **Schibsted Grotesk** | 800 headlines · 600 buttons, labels, emphasis · 500 UI · 400 body | storygrain.co, the one-sheet, social templates. For print PDFs it's embedded as static instances named "SG Print" (see `/print/packages/fonts`). |
| **IBM Plex Mono** | 400, 500 | Small uppercase labels with wide tracking (about 0.12em): eyebrows, timecode/REC details, contact lines, counters like "04 / 07". |

Font files and OFL licenses are in `fonts/`. All three are free Google Fonts.

## Logo files

Every logo comes in **SVG, PDF, and PNG** (transparent, 3000px on the long side). PDFs open as editable vectors in Illustrator.

```
logo/
  clean/   horizontal/  stacked/  mark/
  grain/   horizontal/  stacked/  mark/
  wordmark/
social-icons/            1080px SVG + PNG
storygrain-brand-board.{svg,png,pdf}
```

| File suffix | Mark / word | Use on |
|---|---|---|
| `-forest` | Forest / Forest | **Light** backgrounds (primary) |
| `-ink` | Ink / Ink | Light backgrounds |
| `-black` | Black / Black | One-color print, light backgrounds |
| `-sage-cream` | Sage / Cream | **Dark** and Forest backgrounds (primary reverse) |
| `-cream` | Cream / Cream | Dark backgrounds |
| `-white` | White / White | Dark backgrounds, photos, one-color reverse |

Mark-only files also come in `-sage` (on Forest or Ink). Social icons: `icon-forest` (Sage mark on Forest), `icon-sage` (Forest on Sage), `icon-cream` (Forest on Cream), and `icon-forest-grain`.

### How these files were made
`src/build_brand.py` builds everything from the **exact mark and wordmark vectors live on storygrain.co** (`src/_symbols.html`), so the geometry matches the site. The grain uses the same focus-pull algorithm and final settings approved in Oct 2026 (`src/grain_focus.py`). The dots are randomly placed, though, so regenerated grain files match the approved look but aren't dot-for-dot copies of the originals. Lockup spacing follows the site header: word height 0.425 × mark height, gap 0.3 × mark height. The original Oct 2026 kit (`storygrain-brand-final.zip`, downloaded from the original session) used its own spacing for the stacked lockup. If you have that zip, its files take precedence for anything already in use.

To rebuild:
```bash
pip install cairosvg svgpathtools shapely scipy pillow potracer
cd brand/src && python3 build_brand.py
```
The brand board's text renders with installed fonts. Run `print/packages/src/install_fonts.sh` first.

## Templates
See [`templates/README.md`](templates/README.md).

## Conflicts with what's live on storygrain.co (checked Nov 19, 2026)

These are flagged, not fixed. The site was left untouched.

1. **The share image puts the tagline directly under the wordmark.** `og-image.png` (used for Facebook and X link previews) shows STORYGRAIN with "Making Consistent Creativity Possible." set right below it as one unit. That reads as a logo lockup with a tagline, which breaks both the wordmark rule and the bios-only tagline rule. Its alt text even calls it the "logo with the tagline."
2. **The tagline appears on the site, not just in bios:**
   - in the homepage hero, under the buttons
   - in the footer, right beside the logo lockup
   - as `slogan` in the Google structured data
   - in the share-image alt text

   The footer placement next to the logo is the most direct conflict.
3. **The written name doesn't match.** The wordmark is STORYGRAIN (all caps, two weights), and the rule names it "StoryGrain." Site copy, page titles, and the schema use "Storygrain" and "Storygrain Creative." These are compatible (brand name Storygrain, logo StoryGrain), but decide which casing is right for running text so it stays consistent.
4. **A red outside the palette.** The release form uses `#9B3B2E` for error messages. It's functional, not brand, but it's a red near "Safelight," which was proposed and not adopted. Keep it limited to errors.
5. **Supporting tints aren't documented on the site.** The site uses seven non-palette tints (listed above). They're consistent with the palette, but anyone building new pages should use only those values.
6. **No conflicts found** with: the four palette HEX values, gold or bronze (none on the site), wheat imagery (none), blade overlap (the site mark has three separate, non-overlapping blades), or fonts (the site uses Schibsted Grotesk and IBM Plex Mono, with Montserrat only inside the outlined wordmark).

Also note: the Facebook cover in `templates/facebook-cover/` sets the tagline under the wordmark, the same pattern flagged in item 1.
