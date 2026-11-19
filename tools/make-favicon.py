# Draws the site's favicons: the Emergence Model's four-quadrant circle as a
# crosshair in the accent colour - four quadrants in tints of the violet,
# divided by a cross whose arms run out past the circle.
# Run from the repository root: python3 tools/make-favicon.py
from PIL import Image, ImageDraw

def hexrgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def mix(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def draw(size, accent, ground, bg=None, pad=0.0):
    S = size * 8
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0) if bg is None else bg + (255,))
    d = ImageDraw.Draw(im)
    c = S / 2
    inner = S * (0.5 - pad)
    R = inner * 0.78                 # the circle
    gap = max(S * 0.045, 8)          # the cross between the quadrants
    arm = inner * 0.985              # the crosshair's reach
    line = max(S * 0.06, 8)
    # the four quadrants, as the Emergence Model has them: upper left lightest
    tints = [0.42, 0.22, 0.0, 0.12]  # ul, ur, ll, lr: toward the ground
    boxes = [(c - R, c - R, c, c), (c, c - R, c + R, c), (c - R, c, c, c + R), (c, c, c + R, c + R)]
    starts = [180, 270, 90, 0]
    for t, st in zip(tints, starts):
        d.pieslice((c - R, c - R, c + R, c + R), st, st + 90, fill=mix(accent, ground, t) + (255,))
    # the cross cut out between them, and the crosshair drawn along it,
    # through the centre and out past the circle
    cut = (0, 0, 0, 0) if bg is None else bg + (255,)
    gap = S * 0.05
    d.rectangle((c - gap, c - R - 2, c + gap, c + R + 2), fill=cut)
    d.rectangle((c - R - 2, c - gap, c + R + 2, c + gap), fill=cut)
    w = S * 0.022
    d.rectangle((c - w, c - arm, c + w, c + arm), fill=accent + (255,))
    d.rectangle((c - arm, c - w, c + arm, c + w), fill=accent + (255,))
    return im.resize((size, size), Image.LANCZOS)

for mode, accent, ground, bg in [('light', '#6a3fc4', '#ffffff', (255, 255, 255)), ('dark', '#a98be6', '#000000', (0, 0, 0))]:
    A, G = hexrgb(accent), hexrgb(ground)
    draw(32, A, G).save('favicon/favicon-32-%s.png' % mode)
    draw(192, A, G).save('favicon/favicon-192-%s.png' % mode)
    draw(180, A, G, bg, pad=0.08).convert('RGB').save('favicon/apple-touch-icon-%s.png' % mode)
    big = draw(256, A, G)
    big.save('favicon/favicon-%s.ico' % mode, sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print('ok')
