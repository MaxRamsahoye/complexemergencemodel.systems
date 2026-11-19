# Writes matrices/index.html: the Matrices page - three tables drawn from
# the article (its sections 3-4, 5 and 6-7), with a preview card for each.
# Run from the repository root: python3 tools/make-matrices.py
import re
HEAD = open('overviews/index.html').read()
head = HEAD[:HEAD.index('<style>')]
head = head.replace('Each section of The Complex Emergence Model in brief.', 'Three matrices drawn from The Complex Emergence Model: its genealogy of models, its structural reductionisms and its generative dynamics.')
head = head.replace('Overviews — Complex Emergence', 'Matrices — Complex Emergence').replace('/overviews/', '/matrices/')

M = []
M.append(dict(
  id='model-genealogy', kicker='Matrix 1 · Sections 3–4', title='Model Genealogy',
  desc='The models of civilisation as interacting structures, from Marx to the Complex Emergence Model: their structures, where each places causal primacy, and their limits.',
  read='../#precursors',
  cols=['Model', 'Theorist', 'Structures', 'Causal primacy', 'Organising principle', 'Limits'],
  rows=[
    ['Classical Marxism: Base-Superstructure', 'Karl Marx; elaborated by Gramsci and Althusser',
     '<b>2</b> &ndash; Base (economy: the modes, forces and relations of production); Superstructure (law, politics, ideology, culture, art)',
     'The base: <em>economic determinism</em>', 'Two layers, the superstructure rising on the base',
     'Classical Marxism attended mainly to the base; post-Marxists (&lsquo;cultural hegemony&rsquo;, &lsquo;ideological apparatuses&rsquo;) had to elaborate the superstructure'],
    ['Cultural Materialism: Infrastructure-Structure-Superstructure', 'Marvin Harris',
     '<b>3</b> &ndash; Infrastructure (technology); Structure (political economy); Superstructure (cultural psychology)',
     'The infrastructure: <em>infrastructural determinism</em>', 'Three layers: infrastructure added beneath structure (previously base)',
     'Primacy still attributed to a single structure'],
    ['Integral Model: Four Quadrants', 'Ken Wilber',
     '<b>4</b> quadrants &ndash; Interior-Individual, Exterior-Individual, Interior-Collective, Exterior-Collective',
     'None: the quadrants arise together', 'Two axes: interior vs. exterior, individual vs. collective',
     'A metatheory of all dimensions of reality, not a model of civilisational structures'],
    ['The Emergence Model', 'Daniel Schmachtenberger (2017)',
     '<b>4</b> &ndash; Superstructure; Physiologic structure; Social structure; Infrastructure',
     'None: each &lsquo;equally fundamental, irreducible to the others&rsquo;', 'Cultural materialism set in the four quadrants, adding the physiologic structure (bodies and brains)',
     'Culture and biology assigned to the interior, though both exist at population level; the quadrants do not neatly map onto the structures'],
    ['The Complex Emergence Model', 'This article',
     '<b>11</b> &ndash; Micro-, meso-, macro-, meta-, infra-, inter-, super-, sub-, bio-, eco- and cosmostructure',
     'None: problems co-produced across every structure and scale of human agency', 'A stack of structures, with system dynamics (metastructure) and developmental process (macrostructure) running through all',
     '&mdash;'],
  ]))
M.append(dict(
  id='structural-reductionisms', kicker='Matrix 2 · Section 5', title='Structural Reductionisms',
  desc='The recurring tendency to reduce civilisation to a single structure: for each reductionism, the structure it privileges, its determinism, its problematisation and its solutionism.',
  read='../#structural-primacy',
  cols=['Reductionism', 'Structure', 'Determinism', 'Problematisation', 'Solutionism', 'Exemplars'],
  rows=[
    ['Culturalism', 'Superstructure', 'History is the unfolding of &lsquo;mind&rsquo;; institutions crystallise what a society believes and values', 'Mistaken models of self and world, giving rise to disenchantment and nihilism', 'A new grand narrative &ndash; a cultural paradigm-shift &ndash; that economy and technology will follow', 'Hegel&rsquo;s <em>Geist</em>'],
    ['Economism', 'Structure (interstructure)', 'Political economy is the base; ideology, psychology and culture emerge from it', 'Inequality, ecological crisis and existential risk as &lsquo;capitalogenic&rsquo;: the life-blind logic of capital', 'A new political economy, beyond money, markets, states and corporations', 'Marxist materialism'],
    ['Technologism', 'Infrastructure', 'Technology constrains economics, and economics constrains culture', 'The industrial-technological system as the root of unfreedom and ecological peril', 'The next technology as the mechanism that remakes the world in its image', 'Ellul, Kaczynski, the primitivists; the Futurists, techno-optimists'],
    ['Naturalisation', 'Biostructure, substructure, ecostructure', 'Evolved human nature, geography and Darwinian selection fix the range of possible societies', 'The mismatch thesis: &lsquo;Palaeolithic emotions, medieval institutions and god-like technology&rsquo;; ecological overshoot', 'Institutions designed around our biases; living within ecological limits; re-engineering human nature', 'Sociobiology, evolutionary psychology, Jared Diamond, E. O. Wilson'],
    ['Physicalisation', 'Cosmostructure', 'Civilisation as a thermodynamic phenomenon, advancing with the energy it harnesses', 'For accelerationists, whatever impedes the cosmic gradient; for ecological economists, the entropy law itself', 'Accelerate and climb the Kardashev scale, or return within thermodynamic limits', 'Leslie White, Kardashev, e/acc, Georgescu-Roegen'],
    ['Individualisation', 'Microstructure', 'The Great Man theory: individuals bend events to their will', 'Villainisation: particular bad actors whose removal would set things right', 'Heroism: the right leader or founder; or every individual&rsquo;s choices', 'Carlyle; the personal carbon footprint'],
    ['Collectivisation', 'Mesostructure', 'Groups, not persons or impersonal structures, steer history', 'A power elite steering civilisation in its own interest; or &lsquo;humanity as a whole&rsquo;', 'Expose, regulate, displace or overthrow the elite; or collectively change course', 'C. Wright Mills, Eisenhower; Anthropocene discourse'],
    ['Historicisation', 'Macrostructure', 'The historical process itself has a shape and logic no participant intends', 'A phase in a process: the late stage of a cycle, an overshoot of complexity, a destructive selection pressure', 'Read the process correctly: prepare for the coming phase, steer the transition, design the variants selection will favour', 'Ibn Khaldun, Spengler, Toynbee, Turchin, Tilly, Henrich'],
    ['Neoidealism', 'Superstructure (cultural paradigm)', 'The metacrisis is a crisis of consciousness: of meaning, perception or developmental stage', 'A reductive, atomised, instrumentalist paradigm generating the crises downstream', 'Inner development: wisdom, sense-making, higher stages of consciousness', 'Vervaeke, McGilchrist, integral and metamodern traditions, Inner Development Goals'],
    ['Neorealism', 'Metastructure (evolutionary game theory)', 'Competitive selection dynamics across structures; institutions, technologies and cultures as their epiphenomena', 'Multipolar traps, arms races and tragedies of the commons', 'New coordination mechanisms and game designs that change the payoffs, not the players', 'Thucydides, Hobbes, Machiavelli, Malthus; Schmachtenberger&rsquo;s generator functions, Alexander&rsquo;s &lsquo;Moloch&rsquo;'],
  ]))
M.append(dict(
  id='generative-dynamics', kicker='Matrix 3 · Sections 6–7', title='Generative Dynamics Decomposed',
  desc='Schmachtenberger&rsquo;s generator functions read through the Complex Emergence Model: how each is co-produced across the structures and scales of human agency.',
  read='../#generative-dynamics',
  cols=['Structure', 'The Multi-Polar Trap', 'Exponential Technological Acceleration', 'Narrow-Boundary Problem-Solving'],
  lead=['', 'Competing actors each do what, if all do it, leaves all worse off &ndash; and none can refrain alone', 'Technological power grows exponentially, outpacing the wisdom and governance to wield it', 'Problems solved in narrow, isolated ways, pushing harm elsewhere and creating new problems'],
  rows=[
    ['Microstructure <span>Individual Agency</span>', 'Individually reasonable choices: &lsquo;if I don&rsquo;t, someone else will&rsquo;; responsibility diffused', 'Unprecedented leverage: a researcher, hacker or small team now wields capacities once reserved for states', 'Specialists rewarded for narrow objectives, rarely placed to see second-order effects'],
    ['Mesostructure <span>Collective Agency</span>', 'Firms and states as the principal players &ndash; yet coalitions, treaties and standards can escape the trap', 'Labs, firms and defence establishments favour speed over safety; regulators lag behind', 'Organisations siloed by design, solving their problem by exporting its costs'],
    ['Macrostructure <span>Historical Process</span>', 'A selection process: cooperators are outcompeted, ratcheting rivalry into institutions', 'Acceleration as history&rsquo;s long-run signature; the gap with institutional change widening', 'Layered fixes accumulate into complexity, with diminishing returns (Tainter)'],
    ['Infrastructure <span>Tech Stack</span>', 'Raises the stakes and speed of rivalry &ndash; but verification and transparency tools can enforce cooperation', 'Compounding compute, near-free replication and AI accelerating research itself', 'Technologies built for specified functions, their side effects outside the brief; tech fixing tech'],
    ['Interstructure <span>Political Economy</span>', 'Markets, sovereign states and growth imperatives write the payoff matrix; unpriced externalities make defection cheap', 'Capital, intellectual property and state investment reward acceleration; regulation slow and captured', 'Markets price only what is traded; single metrics &ndash; GDP, shareholder value &ndash; institutionalise the isolated view'],
    ['Superstructure <span>Cultural Psychology</span>', 'Defines what counts as winning and supplies us-and-them narratives &ndash; or shared norms that underwrite cooperation (Ostrom)', 'Narratives of progress and disruption legitimise speed; sense-making lags', 'The analytic paradigm of modernity: problems broken into parts, each to an expert'],
    ['Substructure <span>Evolutionary Psychology</span>', 'Status competition, in-group loyalty, short-term discounting &ndash; alongside reciprocity and norm enforcement', 'Evolved for local, linear worlds: we intuit exponential growth and distant risks poorly', 'Cognition tuned to immediate, local threats; a preference for simple causes and single culprits'],
  ],
  note='These generator functions belong to the metastructure and macrostructure: not located in any one structure, but recurring system dynamics that emerge from and operate through all of them.'))

def thumb(i):
    # a small matrix: a header row and column in violet, cells in tints
    rows, cols = [(6, 6), (8, 6), (8, 4)][i]
    W, H, x0, y0 = 220, 140, 40, 20
    cw, ch = W / cols, H / rows
    out = ''
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0: f = 'var(--h0)'
            elif r == 0 or c == 0: f = 'var(--h1)'
            else: f = 'var(--h2)' if (r + c) % 2 else 'var(--h3)'
            out += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x0 + c * cw + 1.5, y0 + r * ch + 1.5, cw - 3, ch - 3, f)
    return '<svg class="mx-thumb" viewBox="0 0 300 180" aria-hidden="true">' + out + '</svg>'

cards = ''
views = ''
for i, m in enumerate(M):
    cards += '<a class="mx-card" href="#%s">%s<p class="mx-kicker">%s</p><h2 class="mx-title">%s</h2><p class="mx-desc">%s</p></a>' % (m['id'], thumb(i), m['kicker'], m['title'], m['desc'])
    t = '<table class="mx-table"><thead><tr>' + ''.join('<th scope="col">%s</th>' % c for c in m['cols']) + '</tr>'
    if m.get('lead'):
        t += '<tr class="mx-lead">' + ''.join('<td>%s</td>' % c for c in m['lead']) + '</tr>'
    t += '</thead><tbody>'
    for r in m['rows']:
        t += '<tr><th scope="row">%s</th>%s</tr>' % (r[0], ''.join('<td>%s</td>' % c for c in r[1:]))
    t += '</tbody></table>'
    views += ('<section class="mx-view" id="%s" hidden><h1 class="page-title mx-view-title">%s</h1><p class="mx-kicker mx-view-kicker">%s</p><p class="mx-view-desc">%s</p>'
              '<div class="mx-scroll">%s</div>%s<p class="mx-read"><a href="%s">Read the section</a></p></section>') % (
              m['id'], m['title'], m['kicker'], m['desc'], t, ('<p class="mx-note">%s</p>' % m['note']) if m.get('note') else '', m['read'])

STYLE = '''<style>
    /* no band at the top and no footer, as on the Models page: the corner
       controls and the top menu in the page's own colours */
    .site-footer {
      display: none;
    }

    html:not([data-theme]) body.no-band :is(.back-arrow, .theme-toggle, .top-nav, .over-band) {
      --canvas-ink: #000000;
      --muted: #8c8c8c;
      --link-blue: #1a3a9c;
    }

    /* the site name in the top-right corner, as on the Overviews */
    .site-title,
    body.footer-in-view .site-title {
      position: absolute;
      z-index: 10;
      top: 32px;
      right: 40px;
      left: auto;
      bottom: auto;
      margin: 0;
      text-align: right;
      opacity: 1;
      pointer-events: auto;
    }

    @media (max-width: 960px) {
      .site-title,
      body.footer-in-view .site-title {
        top: 26px;
        right: 24px;
      }
    }

    @media (max-width: 600px) {
      .site-title,
      body.footer-in-view .site-title {
        top: 22px;
      }
    }

    /* the cards, as the Models page has them */
    .mx-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 32px;
      margin-top: 72px;
    }

    .mx-card {
      display: flex;
      flex-direction: column;
      padding: 26px 26px 28px;
      border: 1.5px solid color-mix(in srgb, currentColor 28%, transparent);
      color: inherit;
      text-decoration: none;
      transition: background-color 0.2s ease, border-color 0.2s ease;
    }

    .mx-card:hover,
    .mx-card:focus-visible {
      border-color: var(--link-blue);
      background: color-mix(in srgb, var(--link-blue) 8%, transparent);
      outline: none;
    }

    .mx-thumb {
      display: block;
      width: 100%;
      height: 170px;
      margin-bottom: 24px;
      --h0: #37206f;
      --h1: #6a3fc4;
      --h2: color-mix(in srgb, #6a3fc4 22%, var(--canvas-bg));
      --h3: color-mix(in srgb, #6a3fc4 12%, var(--canvas-bg));
    }

    .mx-kicker {
      margin: 0 0 8px;
      font-family: var(--mono-caps);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }

    .mx-title {
      margin: 0 0 12px;
      font-family: var(--serif);
      font-size: 27px;
      font-weight: 400;
      line-height: 1.15;
    }

    .mx-desc {
      margin: 0;
      font-size: 18px;
      line-height: 1.4;
    }

    @media (max-width: 1100px) {
      .mx-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    @media (max-width: 640px) {
      .mx-grid { grid-template-columns: 1fr; }
    }

    /* a matrix: its own view, its name the page's title; the cards, the
       page's own title and introduction hidden */
    body.mx-one :is(.mx-grid, .mx-main-title, .mx-top > .page-intro) {
      display: none;
    }

    .mx-view-title {
      margin-bottom: 14px;
    }

    .mx-view-kicker {
      margin-bottom: 28px;
    }

    /* the menu of matrices, as the Models page has its own: a row above
       the page, or in the margin to the left wherever it fits there */
    .mx-top {
      position: relative;
    }

    .mx-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 18px 28px;
      margin: 0 0 48px;
      font-family: var(--mono-caps);
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .mx-tabs a {
      padding: 0 0 6px;
      border-bottom: 1.5px solid transparent;
      color: var(--muted);
      text-decoration: none;
      white-space: nowrap;
      transition: color 0.2s ease, border-color 0.2s ease;
    }

    .mx-tabs a:hover,
    .mx-tabs a[aria-current="true"] {
      color: var(--canvas-ink);
    }

    .mx-tabs a[aria-current="true"] {
      border-bottom-color: currentColor;
    }

    @media (min-width: 1440px) {
      .mx-tabs {
        position: absolute;
        top: 12px;
        left: calc((var(--wide-col) - 100vw) / 2 + 24px);
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
        margin: 0;
        font-size: 11px;
        /* (as wide as the margin allows, a longer name over two lines) */
        width: calc((100vw - var(--wide-col)) / 2 - 48px);
      }

      .mx-tabs a {
        width: fit-content;
        white-space: normal;
        line-height: 1.4;
      }
    }

    .mx-view[hidden] {
      display: none;
    }

    .mx-view {
      margin-top: 0;
      /* (room beneath, with no footer to follow) */
      padding-bottom: 160px;
    }

    .mx-back {
      margin: 0 0 40px;
      font-family: var(--mono-caps);
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .mx-back a,
    .mx-read a {
      color: var(--link-blue);
      text-decoration: none;
      border-bottom: 1px solid currentColor;
    }

    .mx-view-desc {
      max-width: 760px;
      margin: 0 0 48px;
      font-size: 22px;
      line-height: 1.4;
    }

    /* the table: the full width, its first column the row's name in IBM,
       the cells in the serif; scrolling sideways on narrow screens */
    .mx-scroll {
      overflow-x: auto;
      margin: 0 calc(-1 * min(24px, 2vw));
      padding: 0 min(24px, 2vw);
    }

    .mx-table {
      width: 100%;
      min-width: 980px;
      border-collapse: collapse;
      font-size: 17px;
      line-height: 1.38;
    }

    .mx-table th,
    .mx-table td {
      padding: 16px 18px 18px 0;
      text-align: left;
      vertical-align: top;
      border-top: 1px solid color-mix(in srgb, currentColor 16%, transparent);
    }

    /* the header row and the first column in two light tints of the
       accent: the header the deeper, the first column the paler */
    .mx-table {
      --mx-head: color-mix(in srgb, var(--link-blue) 16%, var(--canvas-bg));
      --mx-side: color-mix(in srgb, var(--link-blue) 7%, var(--canvas-bg));
    }

    /* (deeper in the dark theme, so the two still read apart) */
    html[data-theme="dark"] .mx-table {
      --mx-head: color-mix(in srgb, var(--link-blue) 30%, var(--canvas-bg));
      --mx-side: color-mix(in srgb, var(--link-blue) 14%, var(--canvas-bg));
    }

    .mx-table th:first-child,
    .mx-table td:first-child {
      padding-left: 18px;
    }

    .mx-table thead th {
      padding-top: 16px;
      padding-bottom: 14px;
      border-top: none;
      font-family: var(--mono-caps);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--canvas-ink);
      background: var(--mx-head);
    }

    .mx-table tbody th {
      background: var(--mx-side);
    }

    .mx-table tbody th {
      width: 15%;
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 16px;
      font-weight: 600;
      line-height: 1.3;
    }

    .mx-table tbody th span {
      display: block;
      margin-top: 4px;
      font-weight: 400;
      font-size: 14px;
      color: var(--muted);
    }

    .mx-table tbody tr:first-child > * {
      border-top: none;
    }

    .mx-table td {
      padding-left: 18px;
    }

    .mx-table .mx-lead td {
      padding-top: 4px;
      border-top: none;
      font-style: italic;
      background: var(--mx-head);
    }

    .mx-table tbody tr:hover > td {
      background: color-mix(in srgb, var(--link-blue) 4%, transparent);
    }

    .mx-note {
      max-width: 760px;
      margin: 40px 0 0;
      font-size: 19px;
      font-style: italic;
      line-height: 1.4;
    }

    .mx-read {
      margin: 40px 0 0;
      font-family: var(--mono-caps);
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
  </style>
</head>
'''

i = HEAD.index('<body>')
j = HEAD.index('<main class="page-main">')
body_top = HEAD[i:j].replace('<body>', '<body class="no-band">')
foot_i = HEAD.index('<footer class="site-footer">')
foot_j = HEAD.index('<script>', foot_i)
footer = HEAD[foot_i:foot_j]
tail_i = HEAD.index('<a class="site-title"')
tail = HEAD[tail_i:]
tail = tail.replace('data-search-scope=".ov-sections" data-hide-until=".ov-top"', 'data-search-scope=".page-main"')
footer = re.sub(r'<div class="progress-pill.*?</div>\s*</div>\s*', '', footer, flags=re.S)
footer = footer.replace('data-show-after=".ov-top"', 'data-show-after=".page-title"')

tabs = '<nav class="mx-tabs" aria-label="Matrices"><a href="#" data-view="">All Matrices</a>' + ''.join('<a href="#%s" data-view="%s">%s</a>' % (m['id'], m['id'], m['title']) for m in M) + '</nav>'
main = '''<main class="page-main">
    <div class="wide-top mx-top">
    ''' + tabs + '''
    <h1 class="page-title mx-main-title"><a class="heading-link title-top" href="#">Matrices</a></h1>
    <p class="page-intro">The arguments of <a class="plain-link" href="../"><em>The Complex Emergence Model</em></a> set out as tables: its genealogy of models, its structural reductionisms, and the generative dynamics read through its structures.</p>
    <div class="mx-grid">''' + cards + '''</div>
    ''' + views + '''
    </div>
  </main>

  '''
script = '''<script>
    // a card opens its matrix (named in the address); All Matrices returns
    (function () {
      function route() {
        var id = location.hash.slice(1), view = id && document.getElementById(id);
        var one = !!(view && view.classList.contains('mx-view'));
        document.querySelectorAll('.mx-view').forEach(function (v) { v.hidden = v !== view; });
        document.body.classList.toggle('mx-one', one);
        document.querySelectorAll('.mx-tabs a').forEach(function (a) { a.setAttribute('aria-current', a.dataset.view === (one ? id : '') ? 'true' : 'false'); });
        if (one) window.scrollTo(0, 0);
      }
      window.addEventListener('hashchange', route);
      document.addEventListener('click', function (e) {
        var a = e.target.closest('.mx-tabs a[data-view=""]');
        if (!a) return;
        e.preventDefault();
        history.pushState(null, '', location.pathname);
        route();
      });
      window.addEventListener('popstate', route);
      route();
      // (arriving with a matrix named in the address: from the top of the page)
      if (document.body.classList.contains('mx-one')) setTimeout(function () { window.scrollTo(0, 0); }, 0);
    })();
  </script>

  '''
html = head + STYLE + body_top + main + footer + script + tail
open('matrices/index.html', 'w').write(html)
print('ok', len(html))
