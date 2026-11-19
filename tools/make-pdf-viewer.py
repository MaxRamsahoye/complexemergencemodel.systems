# Writes pdf/index.html: the article's PDF read within the site - each page
# drawn with PDF.js (assets/pdfjs, Apache-2.0), with the site's top bar.
# Run from the repository root: python3 tools/make-pdf-viewer.py
import re
H = open('overviews/index.html').read()
head = H[:H.index('<style>')]
head = head.replace('Each section of The Complex Emergence Model in brief.', 'The Complex Emergence Model, as a PDF.')
head = head.replace('Overviews — Complex Emergence', 'PDF — Complex Emergence').replace('/overviews/', '/pdf/')
body_top = H[H.index('<body>'):H.index('<main class="page-main">')].replace('<body>', '<body class="no-band">')
tail = H[H.index('<a class="site-title"'):]
tail = re.sub(r'<script src="../assets/tools.js[^>]*></script>', lambda m: m.group(0).replace(' data-search-scope=".ov-sections" data-hide-until=".ov-top"', ''), tail)
PDF = '../The%20Complex%20Emergence%20Model.pdf'
style = '''<style>
    .site-footer,
    .top-nav { display: none !important; }

    html:not([data-theme]) body.no-band :is(.back-arrow, .theme-toggle, .top-nav, .over-band) {
      --canvas-ink: #000000;
      --muted: #8c8c8c;
      --link-blue: #1a3a9c;
    }

    .site-title,
    body.footer-in-view .site-title {
      position: absolute; z-index: 10; top: 32px; right: 40px; left: auto; bottom: auto;
      margin: 0; text-align: right; opacity: 1; pointer-events: auto;
    }

    @media (max-width: 960px) {
      .site-title, body.footer-in-view .site-title { top: 26px; right: 24px; }
    }

    @media (max-width: 600px) {
      .site-title, body.footer-in-view .site-title { top: 22px; }
    }

    /* the bar: the title, the page count, zoom, and the file itself */
    .pv-bar {
      position: sticky;
      top: 0;
      z-index: 20;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
      width: min(100% - 48px, 900px);
      margin: 84px auto 0;
      padding: 16px 0;
      background: var(--canvas-bg);
      border-bottom: 1px solid color-mix(in srgb, currentColor 16%, transparent);
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 14px;
    }

    .pv-title {
      margin: 0;
      font-family: var(--serif);
      font-size: 20px;
      font-weight: 400;
      font-style: italic;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .pv-tools {
      display: flex;
      align-items: center;
      gap: 18px;
      flex: none;
      color: var(--muted);
    }

    .pv-tools button,
    .pv-tools a {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 4px;
      border: none;
      background: none;
      font: inherit;
      color: inherit;
      text-decoration: none;
      cursor: pointer;
      transition: color 0.2s ease;
    }

    .pv-tools button:hover,
    .pv-tools a:hover {
      color: var(--canvas-ink);
    }

    .pv-tools svg {
      width: 20px;
      height: 20px;
    }

    .pv-count {
      font-variant-numeric: tabular-nums;
      min-width: 4.5em;
      text-align: center;
    }

    /* the pages, one beneath another, on a faintly tinted ground */
    .pv-pages {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 28px;
      padding: 40px 24px 120px;
    }

    .pv-page {
      position: relative;
      width: min(100%, var(--pv-w, 794px));
      aspect-ratio: 210 / 297;
      background: #fff;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 8px 28px rgba(0, 0, 0, 0.08);
    }

    .pv-page canvas {
      display: block;
      width: 100%;
      height: 100%;
    }

    .pv-note {
      margin: 80px auto;
      max-width: 560px;
      text-align: center;
      font-size: 20px;
      color: var(--muted);
    }

    .pv-note a {
      color: var(--link-blue);
    }

    @media (max-width: 600px) {
      .pv-bar { margin-top: 84px; width: calc(100% - 32px); }
      .pv-title { font-size: 17px; }
      .pv-zoom { display: none !important; }
      .pv-pages { padding: 24px 12px 80px; gap: 16px; }
    }
  </style>
</head>
'''
I = lambda d: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>'
main = '''<main class="pv-main">
    <div class="pv-bar">
      <h1 class="pv-title">The Complex Emergence Model</h1>
      <div class="pv-tools">
        <span class="pv-count" aria-live="polite">&ndash;</span>
        <button class="pv-zoom" type="button" data-zoom="-1" aria-label="Zoom out">''' + I('<circle cx="11" cy="11" r="6.5"/><path d="M8 11h6M16 16l4.5 4.5"/>') + '''</button>
        <button class="pv-zoom" type="button" data-zoom="1" aria-label="Zoom in">''' + I('<circle cx="11" cy="11" r="6.5"/><path d="M8 11h6M11 8v6M16 16l4.5 4.5"/>') + '''</button>
        <a href="''' + PDF + '''" download="The Complex Emergence Model.pdf" aria-label="Download the PDF">''' + I('<path d="M4 15v3.5A1.5 1.5 0 0 0 5.5 20h13a1.5 1.5 0 0 0 1.5-1.5V15"/><path d="M12 4v11"/><path d="M8 11l4 4 4-4"/>') + '''<span>Download</span></a>
      </div>
    </div>
    <div class="pv-pages" aria-label="The pages of the PDF"></div>
  </main>

  <script src="../assets/pdfjs/pdf.min.js"></script>
  <script>
    // each page drawn as it comes near the screen, at the screen's own
    // resolution, and drawn again when the zoom changes
    (function () {
      var URL_ = ''' + "'" + PDF + "'" + ''';
      var list = document.querySelector('.pv-pages'), count = document.querySelector('.pv-count');
      if (!window.pdfjsLib) { list.innerHTML = '<p class="pv-note">The viewer could not load. <a href="' + URL_ + '">Open the PDF directly.</a></p>'; return; }
      pdfjsLib.GlobalWorkerOptions.workerSrc = '../assets/pdfjs/pdf.worker.min.js';
      var ZOOMS = [595, 700, 794, 920, 1060, 1240], z = 2, pdf, pages = [], drawn = new Map();
      function setWidth() { document.documentElement.style.setProperty('--pv-w', ZOOMS[z] + 'px'); }
      setWidth();
      function draw(i) {
        var box = pages[i]; if (!box || box._busy) return;
        var w = box.clientWidth; if (!w || drawn.get(i) === w) return;
        box._busy = true;
        pdf.getPage(i + 1).then(function (page) {
          var v1 = page.getViewport({ scale: 1 }), dpr = Math.min(window.devicePixelRatio || 1, 3);
          var vp = page.getViewport({ scale: w / v1.width * dpr });
          var c = document.createElement('canvas');
          c.width = Math.round(vp.width); c.height = Math.round(vp.height);
          return page.render({ canvasContext: c.getContext('2d'), viewport: vp }).promise.then(function () {
            box.replaceChildren(c); drawn.set(i, w);
          });
        }).finally(function () { box._busy = false; });
      }
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) draw(+e.target.dataset.i); });
      }, { rootMargin: '1200px 0px' });
      function visible() {
        var mid = window.innerHeight / 2, best = 0;
        pages.forEach(function (p, i) { var r = p.getBoundingClientRect(); if (r.top < mid) best = i; });
        count.textContent = (best + 1) + ' / ' + pages.length;
      }
      pdfjsLib.getDocument(URL_).promise.then(function (doc) {
        pdf = doc;
        return doc.getPage(1).then(function (p1) {
          var v = p1.getViewport({ scale: 1 });
          for (var i = 0; i < doc.numPages; i++) {
            var d = document.createElement('div');
            d.className = 'pv-page'; d.dataset.i = i;
            d.style.aspectRatio = v.width + ' / ' + v.height;
            d.setAttribute('aria-label', 'Page ' + (i + 1));
            list.appendChild(d); pages.push(d); io.observe(d);
          }
          visible();
        });
      }).catch(function () {
        list.innerHTML = '<p class="pv-note">The PDF could not be shown here. <a href="' + URL_ + '">Open it directly.</a></p>';
      });
      window.addEventListener('scroll', function () { if (pages.length) visible(); }, { passive: true });
      var redraw = 0;
      function again() { clearTimeout(redraw); redraw = setTimeout(function () { pages.forEach(function (p, i) { var r = p.getBoundingClientRect(); if (r.bottom > -1200 && r.top < window.innerHeight + 1200) draw(i); }); }, 150); }
      window.addEventListener('resize', again);
      document.querySelectorAll('[data-zoom]').forEach(function (b) {
        b.addEventListener('click', function () {
          var at = pages.length ? (window.scrollY + window.innerHeight / 2) / document.documentElement.scrollHeight : 0;
          z = Math.max(0, Math.min(ZOOMS.length - 1, z + +b.dataset.zoom));
          setWidth();
          window.scrollTo(0, at * document.documentElement.scrollHeight - window.innerHeight / 2);
          again();
        });
      });
    })();
  </script>

  '''
import os
os.makedirs('pdf', exist_ok=True)
open('pdf/index.html', 'w').write(head + style + body_top + main + tail)
print('ok')
