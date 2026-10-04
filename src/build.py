# Builds the mini site from one place. Edit the CASES below, then run:
#   python3 src/build.py            (pages only)
#   python3 src/build.py --images   (pages, then the share images and card thumbnails)
# Every claim traces to infra/record/cases/<case>/facts.md. Mock-ups use fictional data.
import html, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
EDGE = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
NAME = 'Mike Oustamanolakis, PhD'
LINE = 'I give shape to complicated issues.'

# ── mock-ups (HTML + CSS, fictional data) ─────────────────────────────────────

MOCK_REPOSITORY = '''
<div class="mk mk-repo" role="img" aria-label="The document search: filters for company, document type, sub-type, active project and signatory on the left; a search box and three results on the right, each with its code, company, type, status, place and date of signing.">
  <aside>
    <h5>Company</h5>
    <ul class="mk-list"><li>Zenithasia Corp. <i>8</i></li><li>Blue Lotus Solutions <i>7</i></li><li>Kinetica Innovations Ltd. <i>6</i></li><li>Jade Mountain Holdings <i>3</i></li><li>Dragonfly Enterprises Inc. <i>2</i></li></ul>
    <h5>Document type</h5>
    <div class="mk-chips"><b>Legal 45</b><b class="on">Financial 20</b><b>HR 30</b><b>Strategic 12</b><b>Operational 12</b></div>
    <h5>Financial</h5>
    <div class="mk-chips"><b>Statements 5</b><b>Reports 4</b><b>Tax returns 3</b><b>Purchase orders 1</b></div>
    <h5>Active project</h5>
    <div class="mk-chips"><b class="on">EU green grant</b><b>Lab equipment</b></div>
    <h5>Signatory</h5>
    <div class="mk-chips"><b>Company</b><b>Individual</b><b>Government</b></div>
  </aside>
  <section>
    <div class="mk-search"><span>Search documents</span><b>Search</b></div>
    <p class="mk-meta">3 results · Financial · sorted by date signed</p>
    <article><h6>Zenithasia Corp. 2020 Financial Statement</h6>
      <p><code>ZC.F.20200923.0</code> · Zenithasia Corp. · Statements · <u>Completed</u></p>
      <p class="mk-where">Signed in Hong Kong · 23 Sep 2020</p></article>
    <article><h6>Social Responsibility Audit Report for EU Green Investment Grant</h6>
      <p><code>BLS.F.20200921.0</code> · Blue Lotus Solutions · Reports · <u>Completed</u></p>
      <p class="mk-where">Signed in Singapore · 21 Sep 2020 · <em>Active: EU green grant</em></p></article>
    <article><h6>Procurement for Robotic Lab Equipment</h6>
      <p><code>KI.F.20200819.0</code> · Kinetica Innovations Ltd. · Purchase orders · <u>Completed</u></p>
      <p class="mk-where">Signed in Hong Kong · 19 Aug 2020</p></article>
  </section>
</div>'''

def poster(en, zh, left, right):
    return f'<div class="mk-poster"><span class="en">{en}</span><span class="zh">{zh}</span><span class="ex">← {left}<br>→ {right}</span></div>'

MOCK_FACTORY = '''
<div class="mk mk-factory" role="img" aria-label="Four place-name posters — Shenyang, Nanjing, Guiyang and Nanchang — each with arrows to the two nearest exits, named after classical poets; beside them, the phone screen for welding machine 372, with its inspection date, status, manuals in two languages, supervisors and checklists.">
  <div class="mk-posters">''' + \
    poster('Shenyang', '沈陽', '陸遊 Lu You', '王維 Wang Wei') + \
    poster('Nanjing', '南京', '杜牧 Du Mu', '李煜 Li Houzhu') + \
    poster('Guiyang', '貴陽', '王維 Wang Wei', '韓愈 Han Yu') + \
    poster('Nanchang', '南昌', '杜甫 Du Fu', '白居易 Bai Juyi') + '''
  </div>
  <div class="mk-phone">
    <p class="mk-crumb">← 南京 Nanjing · Floor 2</p>
    <h6>焊接机器 372<br>Welding</h6>
    <p class="mk-tags"><b>Inspected 2020-09-23</b><b>2% wear</b><b class="ok">Good</b></p>
    <p class="mk-label">Manuals</p>
    <div class="mk-docs"><span>PDF<br>English</span><span>PDF<br>中文</span><span>PDF<br>Safety</span></div>
    <p class="mk-label">Supervisors</p>
    <p class="mk-people"><span>Shift: 張 Zhang</span><span>Line: 王 Wang</span></p>
    <p class="mk-label">Checklists</p>
    <div class="mk-chips"><b class="on">Operations</b><b>Maintenance</b><b>Receiving</b></div>
    <p class="mk-size">A− A A+</p>
  </div>
</div>'''

ROOMS = [('GW G.03', 'Ground', 'Lecture Theatre 1', 'Lecture theatre', '180', '120'),
         ('GW G.04', 'Ground', 'Seminar Room', 'Teaching room', '55', '30'),
         ('GW 1.01', '1', 'Seminar Room', 'Teaching room', '60', '40'),
         ('GW 1.02', '1', 'Seminar Room', 'Teaching room', '61', '40'),
         ('GW 1.04', '1', 'Computer Room', 'Computer lab', '95', '40'),
         ('GW 2.01', '2', 'Design Studio', 'Studio', '120', '30')]
MOCK_ROOMS = '''
<div class="mk mk-rooms" role="img" aria-label="Room Finder on Castlegate, a fictional campus: a search for Glassworks returns 28 rooms, 12 learning spaces and 546 seats, listed with floor, name, use, area and seats, with filters for seats and function.">
  <div class="mk-bar"><b>RF</b><span class="mk-search"><span>Glassworks</span></span></div>
  <div class="mk-chips mk-filters"><b class="on">Teaching spaces</b><b>Timetabled</b><b>30+ seats</b><b>Computer lab</b><b>Studio</b></div>
  <p class="mk-stats"><b>28</b> rooms <b>12</b> learning spaces <b>546</b> seats <b>1,599</b> m²</p>
  <table><thead><tr><th>Room</th><th>Floor</th><th class="opt">Known as</th><th>Use</th><th class="opt num">m²</th><th class="num">Seats</th></tr></thead><tbody>''' + \
    ''.join(f'<tr><td><b>{r}</b></td><td>{f}</td><td class="opt">{k}</td><td>{u}</td><td class="opt num">{a}</td><td class="num">{s}</td></tr>' for r, f, k, u, a, s in ROOMS) + \
    '''</tbody></table>
  <p class="mk-conflict"><b>1 conflict</b> GW 1.04: layout shows 40 seats, timetable lists 36. Listed for correction.</p>
</div>'''

# ── cases ─────────────────────────────────────────────────────────────────────

CASES = [
 dict(slug='repository', n=1,
  title='A failing programme back on track, and 15–20 hours a week down to two',
  card_k='Group of companies · Greater China',
  card_s='Six contributors, four jurisdictions, one way to file and find everything.',
  short='A failing programme, back on track',
  lead='A group of companies had no shared way to file or find its contracts, patents and agreements. The programme meant to fix it was failing.',
  ba=[('No shared way to name or file documents across five companies and a board',
       'One naming rule: a file’s name says whose it is, what it is, and when', ''),
      ('15–20 hours a week searching, calling and meeting about documents',
       'About 2 hours a week', 'big'),
      ('Companies in the group duplicating work without knowing',
       '“Active projects” visible to all: duplicated work stopped', ''),
      ('A programme failing under its previous manager',
       'Back on track, and adopted immediately', '')],
  ba_note='Hours: estimate, combined across the group.',
  mock=MOCK_REPOSITORY, mock_cap='Re-created from the original design. Company and project names are fictional.',
  who=[('Client', 'The board of a group of five companies'),
       ('Region', 'Macau, Taiwan, Guangzhou and Hong Kong: four legal systems'),
       ('People', 'About 50, of whom about 40 in mainland China and Macau'),
       ('My role', 'Brought in to rescue the programme')],
  what='Each company kept its documents its own way. Finding one agreement for an audit meant asking around, calling and meeting. Companies in the group sometimes worked on the same thing without knowing. The programme to fix this had stalled: designers wanted freedom, engineers wanted structure, management wanted savings, and nobody held them together.',
  how=[('Started with the board, not the backlog.', 'We went through the brief line by line, cut what they did not need, and agreed what could actually be delivered.'),
       ('Gave each team its own brief', 'inside the shared plan, with short check-ins every three days, under strict confidentiality.'),
       ('Made one rule for naming every document', 'in every company, so a file’s name alone says whose it is, what kind it is and when it was made.'),
       ('Added one field everyone could see: active projects.', 'Each company could now see what the others were working on.')],
  diagram='repository', diagram_in='impact', diagram_cap='Estimate, combined across the group.',
  impact=[('15–20 hours → about 2', 'a week across the group, searching and meeting about documents'),
          ('Duplicated work stopped', 'the active-projects field showed who was already doing what'),
          ('Chat channels closed', 'the ones that existed only to find documents'),
          ('Adopted immediately', 'the one objection came from the person whose manual filing the system replaced')],
  see=None),
 dict(slug='factory', n=2,
  title='Two factory campuses anyone can find their way around, delivered in half the time',
  card_k='Manufacturing · China',
  card_s='Agreed in two months, delivered in one, then extended by the client.',
  short='Two factory campuses, navigable by anyone',
  lead='Visitors, inspectors and officials kept getting lost. Architects and interior designers had tried signage before; none of it had stuck.',
  ba=[('Places known by codes only insiders could read',
       'Places named after cities, safety exits after classical poets', ''),
      ('Visitors, inspectors and officials getting lost',
       'Found their way unaided', 'big'),
      ('Signage schemes by architects that had not stuck',
       'Both languages on every sign, with arrows to the two nearest exits', ''),
      ('Two months agreed for delivery',
       'Delivered in one', 'big')],
  ba_note='Two campuses, five to six buildings each. 2018–2020.',
  mock=MOCK_FACTORY, mock_cap='Re-created from the original designs: four posters from the series, and the phone screen for one machine. Sites withheld.',
  who=[('Client', 'A state-owned manufacturer'),
       ('Region', 'Mainland China, 2018–2020'),
       ('Scale', 'Two campuses of five to six buildings each'),
       ('My role', 'Led the work through my consultancy')],
  what='Staff moved between buildings by bicycle, scooter and golf cart. Workers, engineers, visitors, health inspectors and government officials all needed to find a place, a machine or a safe way out, and the numbering made sense only to the people who already knew it.',
  how=[('Named places instead of numbering them.', 'Areas took the names of cities, safety exits the names of classical poets: names people already carry in their heads.'),
       ('Put both languages on every sign,', 'with arrows to the two nearest exits.'),
       ('Put every machine’s manuals, checklists and supervisors one tap away,', 'in a simple bilingual web app, with directions between buildings.'),
       ('Proved it small, then scaled it.', 'One floor in the first week, one building live in the second, a one-week pilot, then every required floor on both campuses.')],
  diagram='factory', diagram_in='how', diagram_cap='Redrawn from the original designs. The factories and their locations are withheld.',
  impact=[('1 month, not 2', 'delivered in half the agreed time'),
          ('Found their way unaided', 'visitors, inspectors and government officials, without an escort'),
          ('Extended', 'the client commissioned a follow-up project')],
  see=('prototypes/factory.html', 'See the directory working (prototype, sample data) →')),
 dict(slug='room-finder', n=3,
  title='15,000 rooms, one answer',
  card_k='Higher education · UK',
  card_s='An estate’s scattered records joined into one search, with their contradictions listed.',
  short='15,000 rooms, one answer',
  lead='Finding a suitable room took anything from half an hour to weeks, and the institution’s own records disagreed about what its rooms held.',
  ba=[('Half an hour to weeks to find a suitable room',
       'One search across 15,000+ rooms in 40+ buildings', 'big'),
      ('Four sets of records that disagreed with each other',
       'Joined into one, with every conflict listed for correction', ''),
      ('No single source anyone trusted',
       'One place to look, built only from existing files', '')],
  ba_note='Working prototype; a six-week pilot is proposed, measured on time to answer.',
  mock=MOCK_ROOMS, mock_cap='Re-created from the working prototype, on Castlegate, a fictional campus built for teaching.',
  who=[('Client', 'A large UK university'),
       ('Scale', 'More than 15,000 rooms in over 40 buildings'),
       ('My role', 'Designed and built it'),
       ('Status', 'Working prototype; pilot proposed')],
  what='To find a room that fitted a class, staff asked colleagues (about half an hour), searched booking systems (about 45 minutes), walked the campus (about two hours), or raised a ticket (hours to weeks). The records behind those systems did not agree with each other: a room’s furniture count and its timetabled seats could differ.',
  how=[('Used what already existed.', 'Floor plans, furniture layouts, teaching profiles and occupancy surveys, joined into one place, with nothing new to collect.'),
       ('Made one search answer the real question:', 'which room, where, how many seats, set up for what kind of teaching.'),
       ('Listed every contradiction instead of hiding it.', 'Where two records disagree, the system does not pick a winner; it lists the conflict so the owner can fix it at source.'),
       ('Proposed how to prove it:', 'a six-week pilot, measured on how long it takes to answer real questions.')],
  diagram='room-finder', diagram_in='how', diagram_cap='Built only from files the institution already had. No new data was collected.',
  impact=[('One search', 'across more than 15,000 rooms in over 40 buildings'),
          ('Contradictions visible', 'conflicts between records listed for correction at source'),
          ('Next: a pilot', 'six weeks, measured on time to answer')],
  see=('prototypes/room-finder.html', 'See it working: a teaching version with a fictional campus →')),
]

# ── templates ─────────────────────────────────────────────────────────────────

def page(title, body, extra_head=''):
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="robots" content="noindex">
{extra_head}<link rel="stylesheet" href="site.css">
</head>
<body>
<div class="wrap">
{body}
</div>
</body>
</html>
'''

def ba_block(c, share=False):
    rows = ''.join(f'''
  <div class="ba-row{' big' if k else ''}"><div class="ba-b">{b}</div><div class="ba-arrow" aria-hidden="true">→</div><div class="ba-a">{a}</div></div>''' for b, a, k in c['ba'])
    head = f'<p class="ba-title">{c["short"]}</p>' if share else ''
    foot = f'<p class="ba-foot"><b>{NAME}</b> · {LINE}</p>' if share else ''
    return f'''<div class="ba{' ba-share' if share else ''}">
  {head}<div class="ba-head"><span>Before</span><span></span><span>After</span></div>{rows}
  <p class="ba-note">{c['ba_note']}</p>{foot}
</div>'''

def case_page(c, i):
    prev_ = CASES[i - 1] if i else None
    next_ = CASES[i + 1] if i + 1 < len(CASES) else None
    diagram = (SRC / 'diagrams' / f'{c["diagram"]}.svg').read_text()
    fig = f'<figure>{diagram}<figcaption>{c["diagram_cap"]}</figcaption></figure>'
    who = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in c['who'])
    how = ''.join(f'<li><b>{b}</b> {t}</li>' for b, t in c['how'])
    imp = ''.join(f'<li><b>{b}</b><span>{t}</span></li>' for b, t in c['impact'])
    see = f'<p class="see"><a href="{c["see"][0]}">{c["see"][1]}</a></p>' if c['see'] else ''
    nav_l = f'<a href="{prev_["slug"]}.html">← Previous</a>' if prev_ else '<a href="index.html">← All cases</a>'
    nav_r = f'<a href="{next_["slug"]}.html">Next: {next_["short"].lower() if next_["short"][0].islower() else next_["short"]} →</a>' if next_ else '<a href="index.html">All cases →</a>'
    body = f'''<header class="top"><a href="index.html">{NAME}</a><span>Case {c['n']} of {len(CASES)}</span></header>

<h1>{c['title']}</h1>
<p class="lead">{c['lead']}</p>

{ba_block(c)}
<p class="ba-get"><a href="img/share-{c['slug']}.png" download>Download this summary as an image</a></p>

<figure class="mock">{c['mock']}<figcaption>{c['mock_cap']}</figcaption></figure>

<h2>Who</h2>
<dl class="facts">{who}</dl>

<h2>What</h2>
<p>{c['what']}</p>

<h2>How</h2>{fig if c['diagram_in'] == 'how' else ''}
<ol class="did">{how}</ol>

<h2>Impact</h2>{fig if c['diagram_in'] == 'impact' else ''}
<ul class="changed">{imp}</ul>
{see}
<nav class="next">{nav_l}{nav_r}</nav>'''
    og = f'<meta property="og:title" content="{html.escape(c["title"])}">\n<meta property="og:image" content="img/share-{c["slug"]}.png">\n'
    return page(f'{c["short"]} — {NAME}', body, og)

def home():
    cards = ''.join(f'''
  <a class="case-card" href="{c['slug']}.html">
    <img src="img/thumb-{c['slug']}.png" alt="" loading="lazy">
    <span class="k">{c['card_k']}</span>
    <span class="t">{c['title']}</span>
    <span class="s">{c['card_s']}</span>
    <span class="go">Read the case →</span>
  </a>''' for c in CASES)
    body = f'''<header class="top"><a href="index.html">{NAME}</a><span>Selected work</span></header>

<p class="name">{NAME}</p>
<h1>{LINE}</h1>
<p class="lead">For leadership teams in Hong Kong, mainland China and the UK, when an organisation’s
information, rules or services no longer fit the people who use them.</p>

<ul class="creds">
  <li><b>20+ years</b>across Europe and Asia</li>
  <li><b>7 years</b>running a design consultancy in Hong Kong</li>
  <li><b>PhD</b>The Hong Kong Polytechnic University</li>
  <li><b>Now</b>in UK higher education</li>
</ul>

<h2>When leaders bring me in</h2>
<ul class="when">
  <li>A programme is failing, and the people in it no longer agree what it is for.</li>
  <li>People cannot find what they need, so they ask, wait, or do the work twice.</li>
  <li>Two systems say different things, and the organisation follows the wrong one.</li>
</ul>

<h2>Three cases</h2>
<div class="cases">{cards}
</div>
<p class="note">Client names are withheld. Figures are measured, or marked as estimates; where there
is no figure, none is given. Screens are re-created with fictional data.</p>

<h2>Contact</h2>
<ul class="contact">
  <li><a href="mailto:mike@mikko.gr">mike@mikko.gr</a></li>
  <li><a href="https://www.linkedin.com/in/oustamanolakis">LinkedIn</a></li>
</ul>'''
    return page(f'{NAME} — selected work', body)

def bare(title, inner, cls):
    return f'''<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="../../site.css"></head><body class="{cls}">{inner}</body></html>
'''

def build():
    (ROOT / 'index.html').write_text(home())
    gen = ROOT / 'src' / 'gen'; gen.mkdir(exist_ok=True)
    for i, c in enumerate(CASES):
        (ROOT / f'{c["slug"]}.html').write_text(case_page(c, i))
        (gen / f'share-{c["slug"]}.html').write_text(bare(c['short'], ba_block(c, share=True), 'shot-share'))
        (gen / f'thumb-{c["slug"]}.html').write_text(bare(c['short'], c['mock'], 'shot-thumb'))
    print('pages written')

def images():
    out = ROOT / 'img'; out.mkdir(exist_ok=True)
    for c in CASES:
        for kind, size in (('share', '1200,630'), ('thumb', '1200,675')):
            src = ROOT / 'src' / 'gen' / f'{kind}-{c["slug"]}.html'
            subprocess.run([EDGE, '--headless', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                            f'--window-size={size}', f'--screenshot={out / f"{kind}-{c["slug"]}.png"}', src.as_uri()],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('images written')

if __name__ == '__main__':
    build()
    if '--images' in sys.argv:
        images()
