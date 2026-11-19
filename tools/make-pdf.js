#!/usr/bin/env node
// Render the article as The Complex Emergence Model.pdf (named after the
// article, so that it saves under its title however the browser fetches it),
// the file the PDF icon on the Article page downloads.
//
// Usage (from the repository root): node tools/make-pdf.js
// Needs Playwright (NODE_PATH=$(npm root -g) where it is installed globally)
// and a Chromium (PLAYWRIGHT_BROWSERS_PATH, or CHROMIUM=/path/to/chromium).
//
// The article's header and sections are lifted out of index.html into a
// plain document set for print: one column, the site's typefaces, no bands,
// buttons or menus, the site's name and page numbers in the margins. Run it again whenever the
// article changes (after each sync from the Live doc).
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'The Complex Emergence Model.pdf');

const CSS = `
  @font-face { font-family: 'ET Bembo'; src: url('fonts/ETBembo-RomanOSF.woff2') format('woff2'); font-weight: 400; font-style: normal; }
  @font-face { font-family: 'ET Bembo'; src: url('fonts/ETBembo-SemiBoldOSF.woff2') format('woff2'); font-weight: 600; font-style: normal; }
  @font-face { font-family: 'ET Bembo'; src: url('fonts/et-book-bold-line-figures.woff') format('woff'); font-weight: 700; font-style: normal; }
  @font-face { font-family: 'ET Bembo'; src: url('fonts/ETBembo-DisplayItalic.woff2') format('woff2'); font-weight: 400; font-style: italic; }
  /* the site's name and page numbers in the page margins, in IBM Plex as
     on the site; on the first page its name in the top right corner too */
  @page {
    size: A4;
    margin: 24mm 24mm 22mm;
    @bottom-left { content: 'complexemergencemodel.systems'; font-family: 'IBM Plex Sans', sans-serif; font-size: 8pt; color: #6a3fc4; vertical-align: middle; }
    @bottom-right { content: counter(page); font-family: 'IBM Plex Sans', sans-serif; font-size: 8pt; color: #777; vertical-align: middle; }
  }
  @page :first {
    @top-right { content: 'Complex\\A Emergence'; white-space: pre; font-family: 'IBM Plex Sans', sans-serif; font-weight: 500; font-size: 10pt; line-height: 1.15; letter-spacing: 0.06em; text-transform: uppercase; text-align: right; vertical-align: bottom; padding-bottom: 2mm; color: #000; }
  }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  /* the models' diagrams, centred, a caption beneath in IBM Plex */
  .article-figure { margin: 8mm auto 9mm; max-width: 115mm; text-align: center; break-inside: avoid; }
  .article-figure img { display: block; width: 100%; height: auto; }
  .article-figure figcaption { margin-top: 3mm; font-family: 'IBM Plex Sans', sans-serif; font-size: 7pt; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #777; }
  /* quotations set apart, the source beneath; the generative dynamics' own
     unruled, above their headings */
  .article-quote { margin: 5mm 0 6mm; padding-left: 5mm; border-left: 0.5pt solid #bbb; break-inside: avoid; }
  .article-quote p { margin: 0; font-style: italic; }
  .article-quote .quote-source { margin-top: 2mm; font-family: 'IBM Plex Sans', sans-serif; font-style: normal; font-size: 8pt; color: #777; }
  .article-quote.article-epigraph { border-left: none; padding-left: 0; margin-top: 9mm; }
  h4 { font-family: 'IBM Plex Sans', sans-serif; font-size: 10pt; font-weight: 600; margin: 5mm 0 1mm; break-after: avoid; }
  h4 span { margin-left: 2mm; font-weight: 400; color: #777; }
  h4 + p { margin-top: 0; }
  body { margin: 0; font-family: 'ET Bembo', Georgia, serif; font-size: 13.5pt; line-height: 1.42; color: #000; }
  a { color: #6a3fc4; text-decoration: none; }
  .amp { font-style: normal; }
  /* the title on a page of its own, a little below the middle */
  .title-page { padding-top: 92mm; break-after: page; }
  /* set as on the site, in proportion: the author in grey IBM Plex, the
     title in Inter Bold (its second line the width of the text), the
     subtitle in semibold ET Bembo */
  .author { margin: 0 0 18pt; font-family: 'IBM Plex Sans', sans-serif; font-size: 10pt; color: #8c8c8c; }
  .author a { color: inherit; }
  h1 { margin: 0 0 14pt; font-family: 'Inter', sans-serif; font-weight: 700; letter-spacing: -0.02em; font-size: 29pt; line-height: 1.08; }
  h1 .title-line { display: block; white-space: nowrap; }
  .subtitle { margin: 0; font-weight: 600; font-size: 14.5pt; line-height: 1.3; }
  section { margin: 0 0 8pt; }
  h2 { margin: 28pt 0 9pt; font-size: 20pt; font-weight: 600; line-height: 1.2; break-after: avoid; }
  h3 { margin: 20pt 0 7pt; font-size: 15.5pt; font-weight: 600; font-style: italic; break-after: avoid; }
  h4, h5 { margin: 16pt 0 5pt; font-size: 13.5pt; font-weight: 600; break-after: avoid; }
  /* (a heading never left at the foot of a page: room for some lines after
     it is kept, invisibly, or it moves over to the next page) */
  :is(h2, h3, h4):not(.band-page *):not(.article-band *)::after { content: ''; display: block; height: 32mm; margin-bottom: -32mm; }
  h2, h3 { break-inside: avoid; }
  /* (the last section's spacers, and anything else, kept from spilling onto
     a page of their own after the end) */
  body > section:last-of-type > :last-child { margin-bottom: 0; }
  .pdf-end { height: 0; overflow: hidden; }
  body { overflow: hidden; }
  p { margin: 0 0 9pt; orphans: 3; widows: 3; }
  /* the article's bands within it (Paradigmatic Cases, the generative
     dynamics' quotations, Critical Realism), in the same midnight purple,
     edge to edge across the page, carried on where one breaks across pages */
  .article-band {
    /* (each a page of its own, as the Overview's are, edge to edge in the
       midnight purple, its text centred on the page) */
    page: band; break-before: page; break-after: page;
    box-sizing: border-box; min-height: 296.5mm; padding: 24mm;
    display: flex; flex-direction: column; justify-content: center;
    background: #1d1135; color: #fbf6ec;
    font-size: 12pt; line-height: 1.38;
    -webkit-box-decoration-break: clone; box-decoration-break: clone;
  }
  .article-band > :first-child { margin-top: 0; }
  .article-band > :last-child { margin-bottom: 0; }
  .article-band a { color: inherit; }
  .article-band :is(.quote-source, h4 span) { color: rgba(251, 246, 236, 0.65); }
  .article-band .article-quote { border-left-color: rgba(251, 246, 236, 0.35); }
  .article-band-quote { break-inside: avoid; }
  /* (Critical Conclusions, the longest, kept to its page) */
  #critical-conclusions .article-band { font-size: 11pt; line-height: 1.34; justify-content: center; }
  #critical-conclusions .article-band h2 { margin: 0 0 8pt; }
  #critical-conclusions .article-band h3 { margin: 12pt 0 4pt; font-size: 13pt; }
  #critical-conclusions .article-band p { margin: 0 0 6pt; }
  #critical-conclusions .article-band ul { margin: 4pt 0 6pt; }
  #critical-conclusions .article-band li { margin-bottom: 2pt; }
  .article-band-quote .article-quote.article-epigraph { margin: 0; font-size: 15pt; line-height: 1.4; }
  .article-band-quote + h3 { margin-top: 0; font-style: normal; font-size: 18pt; }
  /* (the three generative dynamics' headings upright and larger, as in the article) */
  /* the sections in the site's band (the Overview, then Basis and Contents
     together) on pages of their own in its midnight purple, edge to edge,
     their text centred on the page */
  @page band { margin: 0; background: #1d1135; @bottom-left { content: none; } @bottom-right { content: none; } }
  .band-page {
    page: band; break-before: page; break-inside: avoid;
    box-sizing: border-box; min-height: 296.5mm; padding: 24mm;
    display: flex; flex-direction: column; justify-content: center;
    background: #1d1135; color: #fbf6ec;
  }
  .band-page a { color: inherit; text-decoration: underline; text-underline-offset: 2pt; }
  /* a little smaller than the article's text, so that the Overview keeps to its page */
  .band-page { font-size: 12pt; line-height: 1.38; }
  .band-page h2 { font-size: 18pt; }
  .band-page section + section { margin-top: 26pt; }
  .band-page h2 { margin-top: 0; }
  .band-page section > :last-child { margin-bottom: 0; }
  /* the darker band of the site (Basis): edge to edge across its page, in
     the darker shade of the midnight purple */
  .band-page section.band-alt { margin: 0 -24mm; padding: 16mm 24mm; background: #170e2a; }
  /* first on its page, it runs up to the top edge: the top of the page, not
     a band across it, and what follows sits below it rather than centred */
  .band-page:has(> section.band-alt:first-child) { justify-content: flex-start; }
  .band-page > section.band-alt:first-child { margin-top: -24mm; padding-top: 30mm; padding-bottom: 20mm; }
  .band-page section.band-alt + section { margin-top: 38pt; }
  /* the article proper starts on a page of its own */
  .article-start { break-before: page; }
  .article-start > h2:first-child { margin-top: 0; }
  .overview-keywords { margin-top: 26pt; font-family: 'IBM Plex Sans', sans-serif; font-size: 9pt; letter-spacing: 0.02em; }
  ul { margin: 6pt 0 10pt; padding: 0; list-style: none; }
  li { margin: 0 0 4pt; padding-left: 1.3em; text-indent: -1.3em; }
  .live-list > li::before { content: '\\2014\\00a0\\00a0'; }
  .live-sub { margin: 4pt 0 0; }
  .live-sub li::before { content: '\\25CB\\00a0\\00a0'; font-size: 0.75em; vertical-align: 0.1em; }
  #contents .live-list:not(.live-sub) { font-family: 'IBM Plex Sans', sans-serif; font-size: 10.5pt; }
  #contents .live-sub { font-size: 9pt; }
  hr { border: 0; border-top: 0.75pt solid #999; margin: 16pt 0; }
`;

(async () => {
  const exe = process.env.CHROMIUM || (process.env.PLAYWRIGHT_BROWSERS_PATH ? path.join(process.env.PLAYWRIGHT_BROWSERS_PATH, 'chromium') : undefined);
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const page = await browser.newPage();
  // read the article out of the page as it is written, before any script runs
  await page.goto('file://' + path.join(ROOT, 'index.html'), { waitUntil: 'domcontentloaded' });
  const parts = await page.evaluate(() => {
    const q = (s) => document.querySelector(s);
    const body = q('.article-body').cloneNode(true);
    body.querySelectorAll('button, .sidenote, .sidenote-label').forEach((n) => n.remove());
    // the live diagram (a frame onto the model's page) printed as its image,
    // assets/downloads/complex-emergence-model.png: run
    // tools/make-cem-image.js first, so that the image is the page as it is
    // (the Models' frames likewise, each as its own download image)
    body.querySelectorAll('.article-embed-figure').forEach((n) => {
      const f = document.createElement('figure');
      f.className = 'article-figure';
      f.innerHTML = '<img src="' + n.querySelector('.article-embed').dataset.print + '" alt=""><figcaption>' + n.querySelector('figcaption').innerHTML + '</figcaption>';
      n.replaceWith(f);
    });
    body.querySelectorAll('.article-embed').forEach((n) => {
      const f = document.createElement('figure');
      f.className = 'article-figure';
      f.innerHTML = '<img src="' + n.dataset.print + '" alt="The Complex Emergence Model"><figcaption>The Complex Emergence Model</figcaption>';
      n.replaceWith(f);
    });
    // headings lose their self-links, keeping their text
    body.querySelectorAll('.heading-link').forEach((a) => a.replaceWith(...a.childNodes));
    const sections = Array.from(body.children);
    // the sections in the Overview's band, kept together as the lead-in
    let n = 0;
    while (n < sections.length && (sections[n].id === 'overview' || sections[n].classList.contains('in-band'))) n++;
    const html = (els) => els.map((e) => e.outerHTML).join('\n');
    const title = q('.article-title').cloneNode(true);
    title.querySelectorAll('.heading-link').forEach((a) => a.replaceWith(...a.childNodes));
    return {
      author: q('.article-author').innerHTML,
      title: title.innerHTML,
      titleText: q('.article-title').textContent.replace(/\s+/g, ' ').trim(),
      subtitle: q('.article-subtitle').innerHTML,
      // the Overview on one page, the sections after it in the band on another
      bandPages: n ? [html(sections.slice(0, 1))].concat(n > 1 ? [html(sections.slice(1, n))] : []) : [],
      rest: html(sections.slice(n)),
    };
  });
  const doc = '<!doctype html><html><head><meta charset="utf-8"><base href="file://' + ROOT + '/">' +
    '<title>' + parts.titleText + '</title>' +
    '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Inter:wght@700&display=swap" rel="stylesheet">' +
    '<style>' + CSS + '</style></head><body>' +
    '<div class="title-page"><p class="author">' + parts.author + '</p><h1>' + parts.title + '</h1><p class="subtitle">' + parts.subtitle + '</p></div>' +
    parts.bandPages.map((h) => '<div class="band-page">' + h + '</div>').join('') +
    parts.rest.replace('<section', '<section class="article-start"') + '<div class="pdf-end"></div></body></html>';
  await page.setContent(doc, { waitUntil: 'load', timeout: 20000 }).catch(() => page.setContent(doc, { waitUntil: 'domcontentloaded' }));
  // the margins' type is not in the page itself, so load it by name
  await page.evaluate(() => Promise.all(['400 8pt "IBM Plex Sans"', '500 10pt "IBM Plex Sans"', '700 29pt "Inter"'].map((f) => document.fonts.load(f))).then(() => document.fonts.ready));
  await page.pdf({
    path: OUT,
    format: 'A4',
    preferCSSPageSize: true,
    printBackground: true,
  });
  await browser.close();
  console.log('Wrote ' + path.relative(ROOT, OUT));
})().catch((e) => { console.error(e); process.exit(1); });
