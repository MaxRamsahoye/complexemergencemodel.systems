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
# the pyramid (and the writing on it) drawn at K of its size, about PIV;
# the lines, their labels and the caption placed to match
K, PIV = 0.82, (600, 560)
def S(pt): return (PIV[0] + (pt[0] - PIV[0]) * K, PIV[1] + (pt[1] - PIV[1]) * K)
def pts(*ps): return ' '.join('%.1f,%.1f' % P(*q) for q in ps)
def tier(y0, y1, band, c):
    body, bandc, top, side = c
    h0, h1 = hw(y0), hw(y1)
    yb = y1 - band; hb = hw(yb)
    out = []
    # the right side, then the top, then the front (the face with the text)
    out.append('<polygon class="f-side" fill="%s" points="%s"/>' % (side, pts((h0, y0, h0), (h0, y0, -h0), (h1, y1, -h1), (h1, y1, h1))))
    out.append('<polygon class="f-top" fill="%s" points="%s"/>' % (top, pts((-h1, y1, h1), (h1, y1, h1), (h1, y1, -h1), (-h1, y1, -h1))))
    out.append('<polygon class="f-body" fill="%s" points="%s"/>' % (body, pts((-h0, y0, h0), (h0, y0, h0), (h1, y1, h1), (-h1, y1, h1))))
    return ''.join(out)
def mid(y):           # the centre of the front face, on screen, at height y
    h = hw(y); return P(0, y, h)
# the superstructure off white, the base black
V = ('#efeadf', '#e2dccd', '#f8f5ee', '#d3ccbb'); G = ('#222226', '#18181b', '#46464c', '#0b0b0d')
B0, B1 = 0, 360; S0, S1 = 392, 780; BAND = 66
svg = ['<svg class="marx-fig" viewBox="0 150 1200 900" role="img" aria-label="The base and the superstructure as two sections of a pyramid, the superstructure above: the superstructure, everything not directly to do with production, maintains (and shapes) the base; the base, the means and relations of production, shapes (and maintains) the superstructure; this moves in a spiral pattern, and the base is generally dominant">']
# the relations: plain lines with open arrowheads, mirroring each other -
# the same height, the same distance out, meeting the pyramid at the same
# two levels on either side (by the superstructure's title, and through
# the base)
def left_at(Y):       # the point on the front-left edge at screen height Y
    y = (CY + KY * A - Y) / (1 + KY * A / HP); h = hw(y); return P(-h, y, h)
def right_at(Y):      # the point on the back-right edge at screen height Y
    y = (CY - KY * A - Y) / (1 - KY * A / HP); h = hw(y); return P(h, y, -h)
YA = P(0, S1 - BAND / 2, hw(S1 - BAND / 2))[1]
YB = P(0, (B0 + B1) / 2 - 20, hw((B0 + B1) / 2 - 20))[1]
L, R = 130, 1070
svg.append('<g class="mf-around">')
a, b = S(left_at(YA)), S(left_at(YB))
YA0, YB0 = YA, YB
YA, YB = S((0, YA0))[1], S((0, YB0))[1]
svg.append('<path class="mf-line" d="M%.1f %.1f H%d V%.1f H%.1f"/>' % (a[0] - 12, YA, L, YB, b[0] - 10))
svg.append('<path class="mf-line" d="M%.1f %.1f L%.1f %.1f L%.1f %.1f"/>' % (b[0] - 22, YB - 12, b[0] - 10, YB, b[0] - 22, YB + 12))
c, d = S(right_at(YB0)), S(right_at(YA0))
svg.append('<path class="mf-line" d="M%.1f %.1f H%d V%.1f H%.1f"/>' % (c[0] + 12, YB, R, YA, d[0] + 10))
svg.append('<path class="mf-line" d="M%.1f %.1f L%.1f %.1f L%.1f %.1f"/>' % (d[0] + 22, YA - 12, d[0] + 10, YA, d[0] + 22, YA + 12))
svg.append('</g>')
svg.append('<g transform="matrix(%g 0 0 %g %.1f %.1f)">' % (K, K, PIV[0] * (1 - K), PIV[1] * (1 - K)))
svg.append('<g class="mf-tier mf-base">' + tier(B0, B1, BAND, G) + '</g>')
svg.append('<g class="mf-tier mf-super">' + tier(S0, S1, BAND, V) + '</g>')
svg.append('<g class="mf-words">')
def text(cls, y, s, fill=None, dx=0, anchor='middle', dy=0):
    x, yy = mid(y)
    f = (' fill="%s"' % fill) if fill else ''
    return '<text class="%s" x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>' % (cls, x + dx, yy + dy, anchor, f, s)
D = '#1d1b22'; W = '#fbf6ec'; INK = W
# (the writing set lower on each face, centred in it top to bottom)
DS, DB = 46, 40
# the superstructure's face
svg.append(text('mf-title mf-dark', S1 - DS - BAND / 2, 'Superstructure', dy=15))
svg.append(text('mf-head', S1 - DS - BAND - 34, 'Everything not directly to do', D))
svg.append(text('mf-head', S1 - DS - BAND - 56, 'with production', D))
for i, w in enumerate(['Art', 'Family', 'Culture', 'Religion', 'Philosophy']):
    yy = S1 - DS - BAND - 100 - i * 29
    svg.append(text('mf-item', yy, w, D, dx=-hw(yy) * 0.55))
for i, w in enumerate(['Law', 'Media', 'Politics', 'Science', 'Education']):
    yy = S1 - DS - BAND - 100 - i * 29
    svg.append(text('mf-item', yy, w, D, dx=hw(yy) * 0.55))
svg.append(text('mf-key', S1 - DS - BAND - 166, 'Ideology', D))
# the base's face
svg.append(text('mf-title', B1 - DB - BAND / 2, 'Base', dy=15))
for (yy, cls, t) in [(B1 - DB - BAND - 38, 'mf-head', 'Means of production'), (B1 - DB - BAND - 70, 'mf-item', 'Tools, machines, factories, land, raw materials'),
                     (B1 - DB - BAND - 122, 'mf-head', 'Relations of production'), (B1 - DB - BAND - 154, 'mf-item', 'Proletariat, labour aristocracy, bourgeoisie'),
                     (B1 - DB - BAND - 208, 'mf-item', 'Private property, capital, commodities, etc.')]:
    svg.append(text(cls, yy, t, INK))
# the labels by the lines
# (each label beside its line, in the gap between the two sections)
svg.append('</g></g>')
svg.append('<g class="mf-around">')
gy = S(P(0, (B1 + S0) / 2, 0))[1]
svg.append('<text class="mf-rel" x="%d" y="%.1f">Maintains</text><text class="mf-rel-sub" x="%d" y="%.1f">(and shapes)</text>' % (L + 22, gy - 70, L + 22, gy - 44))
svg.append('<text class="mf-rel" x="%d" y="%.1f" text-anchor="end">Shapes</text><text class="mf-rel-sub" x="%d" y="%.1f" text-anchor="end">(and maintains)</text>' % (R - 22, gy - 70, R - 22, gy - 44))
bot = S(P(0, 0, A))[1]
svg.append('<text class="mf-note" x="600" y="%.1f" text-anchor="middle">This moves in a spiral pattern.</text><text class="mf-note" x="600" y="%.1f" text-anchor="middle">The base is generally dominant.</text>' % (bot + 64, bot + 96))
top = P(0, S1, -hw(S1))[1]
print('top', top, 'caption', bot + 96)
svg.append('</g></svg>')
new = ('\n' + ' ' * 10).join(svg)
s, n = re.subn(r'<svg class="marx-fig".*?</svg>', lambda m: new, s, flags=re.S)
assert n == 1
open(p, 'w').write(s)
print('bottom', bot)
