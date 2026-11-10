# Draws the Cultural Materialism diagram (the three sections of a pyramid)
# into diagram/index.html, replacing the <svg class="marx-fig cm-fig"> there.
# Run from the repository root: python3 tools/make-cm-pyramid.py
# (drawn as the Base-Superstructure diagram is: tools/make-marx-pyramid.py)
import re
p = 'diagram/index.html'; s = open(p).read()
A, HP = 470, 1720            # half-width of the base, height to the apex
KX, KY = 0.2, 0.14           # how far depth recedes, across and up
CX, CY = 600, 1050           # where the centre of the base sits on screen
def hw(y): return A * (1 - y / HP)
def P(x, y, z): return (CX + x - KX * z, CY - y + KY * z)
K, PIV = 0.76, (600, 600)
def S(pt): return (PIV[0] + (pt[0] - PIV[0]) * K, PIV[1] + (pt[1] - PIV[1]) * K)
def pts(*ps): return ' '.join('%.1f,%.1f' % P(*q) for q in ps)
def tier(y0, y1, c):
    body, top, side = c
    h0, h1 = hw(y0), hw(y1)
    out = []
    out.append('<polygon class="f-side" fill="%s" points="%s"/>' % (side, pts((h0, y0, h0), (h0, y0, -h0), (h1, y1, -h1), (h1, y1, h1))))
    out.append('<polygon class="f-top" fill="%s" points="%s"/>' % (top, pts((-h1, y1, h1), (h1, y1, h1), (h1, y1, -h1), (-h1, y1, -h1))))
    out.append('<polygon class="f-body" fill="%s" points="%s"/>' % (body, pts((-h0, y0, h0), (h0, y0, h0), (h1, y1, h1), (-h1, y1, h1))))
    return ''.join(out)
def mid(y):
    h = hw(y); return P(0, y, h)
# the colours of the stack: midnight, gold, violet
BLUE = ('#1f2f8a', '#4a58a8', '#101850'); GOLD = ('#d9a520', '#e8bf4f', '#8f6d15'); VIOLET = ('#6a3fc4', '#8a66d8', '#37206f')
I0, I1 = 0, 300; T0, T1 = 330, 610; U0, U1 = 640, 900
svg = ['<svg class="marx-fig cm-fig" viewBox="0 150 1200 1000" role="img" aria-label="Cultural materialism as three sections of a pyramid: the infrastructure, the tech stack, at the base; the structure, political economy, on it; the superstructure, cultural psychology, at the top. The infrastructure shapes the structure and superstructure, and they feed back on it; the infrastructure is primary">']
def left_at(Y):
    y = (CY + KY * A - Y) / (1 + KY * A / HP); h = hw(y); return P(-h, y, h)
def right_at(Y):
    y = (CY - KY * A - Y) / (1 - KY * A / HP); h = hw(y); return P(h, y, -h)
# the two lines: up the right from the infrastructure to the superstructure,
# down the left from the superstructure to the infrastructure
YU = P(0, U1 - 70, hw(U1 - 70))[1]
YI = P(0, (I0 + I1) / 2 - 10, hw((I0 + I1) / 2 - 10))[1]
L, R = 110, 1090
svg.append('<g class="mf-around">')
a, b = S(left_at(YU)), S(left_at(YI))
c, d = S(right_at(YI)), S(right_at(YU))
YU0, YI0 = YU, YI
YU, YI = S((0, YU0))[1], S((0, YI0))[1]
svg.append('<path class="mf-line" d="M%.1f %.1f H%d V%.1f H%.1f"/>' % (a[0] - 12, YU, L, YI, b[0] - 10))
svg.append('<path class="mf-line" d="M%.1f %.1f L%.1f %.1f L%.1f %.1f"/>' % (b[0] - 22, YI - 12, b[0] - 10, YI, b[0] - 22, YI + 12))
svg.append('<path class="mf-line" d="M%.1f %.1f H%d V%.1f H%.1f"/>' % (c[0] + 12, YI, R, YU, d[0] + 10))
svg.append('<path class="mf-line" d="M%.1f %.1f L%.1f %.1f L%.1f %.1f"/>' % (d[0] + 22, YU - 12, d[0] + 10, YU, d[0] + 22, YU + 12))
svg.append('</g>')
svg.append('<g transform="matrix(%g 0 0 %g %.1f %.1f)">' % (K, K, PIV[0] * (1 - K), PIV[1] * (1 - K)))
svg.append('<g class="mf-tier mf-base">' + tier(I0, I1, BLUE) + '</g>')
svg.append('<g class="mf-tier mf-mid">' + tier(T0, T1, GOLD) + '</g>')
svg.append('<g class="mf-tier mf-super">' + tier(U0, U1, VIOLET) + '</g>')
svg.append('<g class="mf-words">')
def text(cls, y, t, dy=0):
    x, yy = mid(y)
    return '<text class="%s" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (cls, x, yy + dy, t)
# each face: its name, what it is, and what it holds
for (y1, name, aka, lines) in [
        (U1, 'Superstructure', 'Cultural Psychology', ['Values, beliefs and worldviews', 'Religion, art, science, ideology']),
        (T1, 'Structure', 'Political Economy', ['Governance and economy', 'State, market, law, property, class']),
        (I1, 'Infrastructure', 'Tech Stack', ['Modes of production and reproduction', 'Tools, energy, transport, communications'])]:
    top = y1 - 40
    svg.append(text('mf-title', top - 33, name, dy=15))
    svg.append(text('mf-head', top - 92, aka))
    for i, l in enumerate(lines):
        svg.append(text('mf-item', top - 134 - i * 32, l))
svg.append('</g></g>')
svg.append('<g class="mf-around">')
svg.append('<text class="mf-rel" x="%d" y="%.1f">Feeds back</text><text class="mf-rel-sub" x="%d" y="%.1f">(and legitimises)</text>' % (L + 22, (YU + YI) / 2 - 13, L + 22, (YU + YI) / 2 + 13))
svg.append('<text class="mf-rel" x="%d" y="%.1f" text-anchor="end">Shapes</text><text class="mf-rel-sub" x="%d" y="%.1f" text-anchor="end">(and constrains)</text>' % (R - 22, (YU + YI) / 2 - 13, R - 22, (YU + YI) / 2 + 13))
bot = S(P(0, 0, A))[1]
svg.append('<text class="mf-note" x="600" y="%.1f" text-anchor="middle">The infrastructure is primary.</text><text class="mf-note" x="600" y="%.1f" text-anchor="middle">Change begins at the base and works upwards.</text>' % (bot + 64, bot + 96))
print('top', S(P(0, U1, -hw(U1)))[1], 'caption', bot + 96)
svg.append('</g></svg>')
new = ('\n' + ' ' * 10).join(svg)
s, n = re.subn(r'<svg class="marx-fig cm-fig".*?</svg>', lambda m: new, s, flags=re.S)
assert n == 1, n
open(p, 'w').write(s)
