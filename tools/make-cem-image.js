// Captures the Complex Emergence Model diagram (page 2 of model/) as a
// high-resolution PNG, assets/downloads/complex-emergence-model.png, for the
// article: the drawing alone, nothing selected, trimmed with an even margin.
// Run from the repository root while it is served on port 8765:
//   python3 -m http.server 8765 &   node tools/make-cem-image.js
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
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
im = im.crop(mask.getbbox())
pad = round(im.width * margin)
out = Image.new('RGB', (im.width + 2 * pad, im.height + 2 * pad), (255, 255, 255))
out.paste(im, (pad, pad))
out.save(path, optimize=True)
`;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 3, reducedMotion: 'reduce' });
  await page.goto('http://localhost:8765/model/', { waitUntil: 'networkidle' });
  await page.evaluate(() => window.scrollTo(0, document.querySelector('.md-scene').getBoundingClientRect().top + scrollY));
  // the opening run up the stack, then nothing selected
  await page.waitForTimeout(17000);
  await page.mouse.move(2, 2);
  await page.addStyleTag({ content: 'body * { visibility: hidden !important; } .md-svg, .md-svg * { visibility: visible !important; } .md-svg .hit { fill: transparent !important; }' });
  await page.evaluate(() => document.querySelectorAll('.md-svg .on').forEach((el) => el.classList.remove('on')));
  await page.waitForTimeout(800);
  const file = 'assets/downloads/complex-emergence-model.png';
  await page.locator('.md-svg').screenshot({ path: file });
  execFileSync('python3', ['-c', TRIM, file, '0.06']);
  console.log('Wrote', file);
  await browser.close();
})();
