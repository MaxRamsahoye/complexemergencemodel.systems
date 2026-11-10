# Draws the Base-Superstructure diagram (the two sections of a pyramid) into
# diagram/index.html, replacing the <svg class="marx-fig"> there. Run from
# the repository root: python3 tools/make-marx-pyramid.py
import re
p='diagram/index.html';s=open(p).read()
# a pyramid in oblique projection: x across, y up, z towards the viewer;
# the back of the pyramid recedes up and to the right
A, HP = 430, 1350            # half-width of the base, height to the apex
KX, KY = 0.2, 0.14          # how far depth recedes, across and up
CX, CY = 600, 930           # where the centre of the base sits on screen
def hw(y): return A * (1 - y / HP)
def P(x, y, z): return (CX + x - KX * z, CY - y + KY * z)
def pts(*ps): return ' '.join('%.1f,%.1f' % P(*q) for q in ps)
def tier(y0, y1, band, c):
    body, bandc, top, side = c
    h0, h1 = hw(y0), hw(y1)
    yb = y1 - band; hb = hw(yb)
    out = []
    # the right side, then the top, then the front (the face with the text)
    out.append('<polygon fill="%s" points="%s"/>' % (side, pts((h0, y0, h0), (h0, y0, -h0), (h1, y1, -h1), (h1, y1, h1))))
    out.append('<polygon fill="%s" points="%s"/>' % (top, pts((-h1, y1, h1), (h1, y1, h1), (h1, y1, -h1), (-h1, y1, -h1))))
    out.append('<polygon fill="%s" points="%s"/>' % (body, pts((-h0, y0, h0), (h0, y0, h0), (h1, y1, h1), (-h1, y1, h1))))
    out.append('<polygon fill="%s" points="%s"/>' % (bandc, pts((-hb, yb, hb), (hb, yb, hb), (h1, y1, h1), (-h1, y1, h1))))
    return ''.join(out)
def mid(y):           # the centre of the front face, on screen, at height y
    h = hw(y); return P(0, y, h)
V = ('#6a3fc4', '#4f2d9c', '#8a66d8', '#37206f'); G = ('#d9a520', '#a87d12', '#e8bf4f', '#8f6d15')
B0, B1 = 0, 360; S0, S1 = 392, 780; BAND = 66
svg = ['<svg class="marx-fig" viewBox="0 0 1200 1160" role="img" aria-label="The base and the superstructure as two sections of a pyramid, the superstructure above: the superstructure, everything not directly to do with production, maintains (and shapes) the base; the base, the means and relations of production, shapes (and maintains) the superstructure; this moves in a spiral pattern, and the base is generally dominant">']
# the relations: plain lines with open arrowheads
ys = S1 - BAND / 2; xs = P(-hw(ys), ys, hw(ys))       # the superstructure's left edge, by its title
yb = (B0 + B1) / 2 - 40; xb = P(-hw(yb), yb, hw(yb))   # the base's left edge
L = 50
svg.append('<path class="mf-line" d="M%.1f %.1f H%d V%.1f H%.1f"/>' % (xs[0] - 12, xs[1], L, xb[1], xb[0] - 10))
svg.append('<path class="mf-line" d="M%.1f %.1f L%.1f %.1f L%.1f %.1f"/>' % (xb[0] - 22, xb[1] - 12, xb[0] - 10, xb[1], xb[0] - 22, xb[1] + 12))
yr = B1 - 120; hr = hw(yr); xr = P(hr, yr, -hr)          # the base's right side, its far edge
ys2 = S0 + 160; h2 = hw(ys2); xs2 = P(h2, ys2, -h2)       # the superstructure's right side
R = 1150
svg.append('<path class="mf-line" d="M%.1f %.1f H%d V%.1f H%.1f"/>' % (xr[0] + 12, xr[1], R, xs2[1], xs2[0] + 10))
svg.append('<path class="mf-line" d="M%.1f %.1f L%.1f %.1f L%.1f %.1f"/>' % (xs2[0] + 22, xs2[1] - 12, xs2[0] + 10, xs2[1], xs2[0] + 22, xs2[1] + 12))
svg.append(tier(B0, B1, BAND, G))
svg.append(tier(S0, S1, BAND, V))
def text(cls, y, s, fill=None, dx=0, anchor='middle', dy=0):
    x, yy = mid(y)
    f = (' fill="%s"' % fill) if fill else ''
    return '<text class="%s" x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>' % (cls, x + dx, yy + dy, anchor, f, s)
W = '#fbf6ec'; INK = W
# the superstructure's face
svg.append(text('mf-title', S1 - BAND / 2, 'Superstructure', dy=15))
svg.append(text('mf-head', S1 - BAND - 34, 'Everything not directly to do', W))
svg.append(text('mf-head', S1 - BAND - 56, 'with production', W))
for i, w in enumerate(['Art', 'Family', 'Culture', 'Religion', 'Philosophy']):
    yy = S1 - BAND - 100 - i * 29
    svg.append(text('mf-item', yy, w, W, dx=-hw(yy) * 0.55))
for i, w in enumerate(['Law', 'Media', 'Politics', 'Science', 'Education']):
    yy = S1 - BAND - 100 - i * 29
    svg.append(text('mf-item', yy, w, W, dx=hw(yy) * 0.55))
svg.append(text('mf-key', S1 - BAND - 166, 'Ideology', W))
# the base's face
svg.append(text('mf-title', B1 - BAND / 2, 'Base', dy=15))
for (yy, cls, t) in [(B1 - BAND - 38, 'mf-head', 'Means of production'), (B1 - BAND - 70, 'mf-item', 'Tools, machines, factories, land, raw materials'),
                     (B1 - BAND - 122, 'mf-head', 'Relations of production'), (B1 - BAND - 154, 'mf-item', 'Lumpenproletariat, proletariat, labour aristocracy,'),
                     (B1 - BAND - 182, 'mf-item', 'petty bourgeoisie, bourgeoisie'), (B1 - BAND - 232, 'mf-item mf-em', 'Private property, capital, commodities, etc.')]:
    svg.append(text(cls, yy, t, INK))
# the labels by the lines
# (each label beside its line, in the gap between the two sections)
gy = P(0, (B1 + S0) / 2, 0)[1]
svg.append('<text class="mf-rel" x="%d" y="%.1f">Maintains</text><text class="mf-rel-sub" x="%d" y="%.1f">(and shapes)</text>' % (L + 22, gy - 70, L + 22, gy - 44))
svg.append('<text class="mf-rel" x="%d" y="%.1f" text-anchor="end">Shapes</text><text class="mf-rel-sub" x="%d" y="%.1f" text-anchor="end">(and maintains)</text>' % (R - 22, gy - 70, R - 22, gy - 44))
bot = P(0, 0, A)[1]
svg.append('<text class="mf-note" x="600" y="%.1f" text-anchor="middle">This moves in a spiral pattern.</text><text class="mf-note" x="600" y="%.1f" text-anchor="middle">The base is generally dominant.</text>' % (bot + 64, bot + 96))
top = P(0, S1, -hw(S1))[1]
print('top', top, 'caption', bot + 96)
svg.append('</svg>')
new = ('\n' + ' ' * 10).join(svg)
s, n = re.subn(r'<svg class="marx-fig".*?</svg>', lambda m: new, s, flags=re.S)
assert n == 1
open(p, 'w').write(s)
print('bottom', bot)
