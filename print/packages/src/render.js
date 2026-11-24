// Renders both PDFs with headless Chromium (Playwright).
// Fonts must be installed as system fonts first (see install_fonts.sh): the HTML
// references "SG Print" and "IBM Plex Mono" by family name, with no @font-face.
// Usage: node render.js   (from this folder)
const { chromium } = require('playwright');
const path = require('path');
const out = path.resolve(__dirname, '..');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();

  // Screen / web version: US Letter, no bleed (also served at storygrain.co/packages/storygrain-packages.pdf)
  await p.goto('file://' + path.join(__dirname, 'onesheet.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(out, 'Storygrain-Packages-OneSheet.pdf'), format: 'Letter', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });

  // Print version: 8.75 x 11.25 in = 8.5 x 11 trim + 1/8" bleed each side
  await p.goto('file://' + path.join(__dirname, 'onesheet-print.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(out, 'Storygrain-OneSheet-PRINT-8.75x11.25-bleed.pdf'), width: '8.75in', height: '11.25in', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });

  await b.close();
  console.log('PDFs written to', out);
})();
