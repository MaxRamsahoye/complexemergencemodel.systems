// Captures each model's diagram on the Models page as a high-resolution PNG
// in assets/downloads/, for the "Download diagram" links on those pages:
// the drawing alone (its list and notes hidden), nothing pointed to,
// trimmed to the drawing with an even white margin all round.
// Run from the repository root while it is served on port 8765:
//   python3 -m http.server 8765 &   node tools/make-model-images.js
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');

const MODELS = [
  ['exo-endo-structure', '.exoendo-view .md-ring'],
  ['emergence-model', '.emergence-view .em-fig'],
  ['four-quadrants', '.integral-view .quad-fig'],
  ['structures', '.structures-view .stack-scene', 'cultural-materialism'],
  ['base-superstructure', '.marx-view .stack-scene'],
  // Base-Superstructure's second view, the diagram
  ['base-superstructure', '.marx-view .marx-fig', 'base-superstructure-diagram', '.marx-view .model-modes [data-mode="diagram"]'],
];
const AROUND = 120;   // css px captured around the figure before trimming
const MARGIN = 0.08;  // the white margin left after trimming, as a share of the width

const TRIM = `
import sys
from PIL import Image
path, margin = sys.argv[1], float(sys.argv[2])
im = Image.open(path).convert('RGB')
px = im.load(); W, H = im.size
mask = Image.new('L', im.size, 0); m = mask.load()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        m[x, y] = 255 if min(r, g, b) < 244 else 0
box = mask.getbbox()
im = im.crop(box)
pad = round(im.width * margin)
out = Image.new('RGB', (im.width + 2 * pad, im.height + 2 * pad), (255, 255, 255))
out.paste(im, (pad, pad))
out.save(path, optimize=True)
`;

(async () => {
  const browser = await chromium.launch();
  for (const [hash, sel, name, before] of MODELS) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1400 }, deviceScaleFactor: 3, reducedMotion: 'reduce' });
    await page.goto('http://localhost:8765/diagram/#' + hash, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2500);
    if (before) { await page.click(before); await page.waitForTimeout(400); }
    await page.mouse.move(2, 2);
    // everything hidden but the figure itself
    await page.addStyleTag({ content: 'body * { visibility: hidden !important; } ' + sel + ', ' + sel + ' * { visibility: visible !important; } .ce-saver { display: none !important; }' });
    await page.evaluate((s) => document.querySelector(s).scrollIntoView({ block: 'center' }), sel);
    await page.waitForTimeout(600);
    const r = await page.evaluate((s) => { const b = document.querySelector(s).getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; }, sel);
    const file = 'assets/downloads/' + (name || hash) + '.png';
    await page.screenshot({ path: file, clip: { x: Math.max(0, r[0] - AROUND), y: Math.max(0, r[1] - AROUND), width: r[2] + 2 * AROUND, height: r[3] + 2 * AROUND } });
    execFileSync('python3', ['-c', TRIM, file, String(MARGIN)]);
    console.log('Wrote', file);
    await page.close();
  }
  await browser.close();
})();
