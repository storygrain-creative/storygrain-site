# Storygrain packages one-sheet (print archive)

This is an archive of the one-page packages sheet as it went to print. Don't change the wording here. Make any new version in a new folder.

## Files

| File | What it is |
|---|---|
| `Storygrain-OneSheet-PRINT-8.75x11.25-bleed.pdf` | **The print file.** 8.75 × 11.25 in: 8.5 × 11 trim plus 1/8" bleed on every side. |
| `Storygrain-Packages-OneSheet.pdf` | Screen version, US Letter, no bleed. Same content. This is the file served at storygrain.co/packages/storygrain-packages.pdf. |
| `src/build_onesheet.py` | Source. Generates both HTML files below. Edit copy here. |
| `src/onesheet.html` / `src/onesheet-print.html` | Generated HTML for screen and print. |
| `src/render.js` | Renders both PDFs with headless Chromium (Playwright). |
| `src/install_fonts.sh` | Installs the fonts the HTML expects. |
| `src/_symbols.html` | StoryGrain mark and wordmark as SVG symbols, from storygrain.co. |
| `fonts/` | `SGPrint-*.ttf` (static Schibsted Grotesk 400/500/600/800), `IBMPlexMono-*.ttf`, the variable source font, `make_sgprint.py`, and OFL licenses. |
| `preview/` | PNG previews of both PDFs. |

There are no raster images. Everything on the sheet is vector: text, logo, icons, and shapes.

## How these files were recovered

The original working files lived in a Claude session that couldn't be reached from the handoff session. `build_onesheet.py` replays, step by step, the exact edits made in that session (Oct 2026). It was checked against the PDF on storygrain.co:

- **Text:** identical (`pdftotext` diff is empty).
- **Embedded fonts:** the same set (SGPrint ExtraBold, SemiBold, Regular, and IBM Plex Mono Regular).
- **Rendering:** pixel-identical at 150 dpi (0 differing pixels).

The print PDF comes from the same source, with only the page-size, bleed, and safe-zone changes made in the original session. The original print file was downloaded from that session's chat. If you have that download, it should match this one. If the two ever differ, the downloaded original wins.

## Print details

| | |
|---|---|
| Built | October 30, 2026. The screen PDF on the site was created 2026-10-30 11:00 CDT. |
| Print date | **Not recorded.** Fill this in. |
| Printer | **Not confirmed.** The file was built for UPrinting's 8.5 × 11 template with bleed. |
| Trim size | 8.5 × 11 in (US Letter), single-sided |
| File size | 8.75 × 11.25 in (1/8" bleed each side) |
| Safe zone | All text and corner brackets at least 3/8" inside trim |
| Color | RGB file. The printer converts to CMYK, so Forest may print slightly darker and Sage slightly duller. A single proof copy was recommended first. |
| Paper | Recommended, not confirmed: uncoated or matte cover stock, about 100 lb. |
| Quantity | Recommended, not confirmed: 25 to 50 copies, since pricing was expected to change after early meetings. |
| Fonts | Embedded as standard TrueType. Static instances were made on purpose because some printers' preflight rejects variable fonts. |

## How to regenerate the PDFs

Requires Python 3 and Node with Playwright (`npm i -g playwright && npx playwright install chromium`).

```bash
cd print/packages/src
bash install_fonts.sh          # installs SG Print + IBM Plex Mono as user fonts
python3 build_onesheet.py      # writes onesheet.html and onesheet-print.html
NODE_PATH=$(npm root -g) node render.js   # writes both PDFs into print/packages/
```

The HTML loads fonts by family name ("SG Print", "IBM Plex Mono") with no `@font-face`, so the fonts must be installed first. To rebuild the SG Print fonts from the variable font, run `pip install fonttools`, then `python3 make_sgprint.py` in `fonts/`.

To make a new version: copy this folder, edit the copy in `build_onesheet.py`, and rebuild. Orphan control (the last two words joined with a non-breaking space) is applied automatically.

## Exact wording as printed

Line breaks inside the boxes are layout only. The one forced break is marked `⏎`.

**Header**
- Logo: StoryGrain mark + STORYGRAIN wordmark
- MONTHLY CONTENT PARTNERSHIPS
- The marketing team for businesses that don't have one.
- Every month we plan, shoot and deliver finished video, photo and social content. Scripts, shot lists and captions are written before we pick up a camera, so nothing is improvised.

**CHOOSE YOUR LEVEL**

**01 Starter**: $2,000 / month
- For businesses ready to start showing up consistently.
- WHO POSTS: You post
- 2-hour monthly shoot
- 6 short-form videos
- 15 edited photos
- Scripts and shot list
- Captions for every post
- Suggested post dates
- Delivered ready to post

**02 Standard**: $3,500 / month (highlighted card, Forest background)
- For businesses that want their feed running without them.
- WHO POSTS: We post for you
- 4-hour monthly shoot
- 10 short-form videos
- 30 edited photos
- Everything in Starter
- Monthly content calendar
- Monthly planning call
- Scheduled and published to Instagram and Facebook

**03 Full**: $6,000 / month
- For businesses ready to grow with ads, campaigns and reporting.
- WHO POSTS: We run it
- 6 to 8-hour monthly shoot
- Videos scoped to your monthly plan
- Full photo library
- Everything in Standard
- Quarterly campaign planning
- Meta and Instagram ad management
- Monthly performance review
- Ongoing communications counsel

**Every partnership includes** (two columns, read left to right)
- Delivery by the 1st of the month
- One revision round per piece
- You own every file
- Fixed deliverables, no guessing
- Three-month initial commitment
- Content planned before ⏎ the shoot

**Add-ons**
- Additional short-form video edit: $150
- Long-form video edit (2 to 5 min): $750
- Additional on-location shoot: $200/hr

**Quoted per project**: Websites, logos and brand identity, print design, event coverage and brand films.

**Not included in packages:** paid ad spend, community management (replying to comments and messages, which is separate from posting), SEO and website work.

**Footer**
- Not sure which fits?
- Take the 3-minute Content Check at storygrain.co/check
- HELLO@STORYGRAIN.CO
- STORYGRAIN.CO · @STORYGRAIN.CO
- ERIC WENDT & AUSTIN ASAY · OMAHA, NE

## Differences from storygrain.co/packages/

Checked November 19, 2026. All package names, prices, deliverables, terms, add-ons, and exclusions are word-for-word the same. The differences are below.

| # | Printed PDF | storygrain.co/packages/ |
|---|---|---|
| 1 | "Content planned before" ⏎ "the shoot" (forced line break) | "Content planned before the shoot" (no forced break) |
| 2 | Footer: "Take the 3-minute Content Check at storygrain.co/check" | "Take the 3-minute Content Check." ("Content Check" is a link to /check/) |
| 3 | No buttons | "Book a call" button (links to /#contact) and "Download PDF" button |
| 4 | Every partnership includes: two-column grid, read left to right | Same order, but it reflows on the page by screen width (one column on phones) |
| 5 | Package cards side by side | Cards stack into one column on phones |
| 6 | No page title or meta | Page title "Packages \| Storygrain Creative", marked noindex, nofollow, noarchive, and left out of the site nav and sitemap |

Casing is the same in both. "Monthly content partnerships", "Choose your level", and "Who posts" are written in sentence case in the page markup but display in uppercase through CSS, as they do in print.
