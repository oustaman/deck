# Builds the mini site from one place. Edit the CASES below, then run:
#   python3 src/build.py            (pages only)
#   python3 src/build.py --images   (pages, then the share images used for link previews)
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
    <ul class="mk-list"><li>Zenithasia Corp. <i>8</i></li><li>Quorivale Ltd. <i>7</i></li><li>Talverin Group <i>6</i></li><li>Jade Mountain Holdings <i>3</i></li><li>Merovane Holdings <i>2</i></li></ul>
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
      <p><code>QL.F.20200921.0</code> · Quorivale Ltd. · Reports · <u>Completed</u></p>
      <p class="mk-where">Signed in Singapore · 21 Sep 2020 · <em>Active: EU green grant</em></p></article>
    <article><h6>Procurement for Robotic Lab Equipment</h6>
      <p><code>TG.F.20200819.0</code> · Talverin Group · Purchase orders · <u>Completed</u></p>
      <p class="mk-where">Signed in Hong Kong · 19 Aug 2020</p></article>
  </section>
</div>'''

MOCK_NAMING = '''
<div class="mk mk-naming" role="img" aria-label="The naming rule, broken down: ZC, the company; F, the document family; 20200923, the date signed; 0, the sequence number for that day; then the title in plain words.">
  <p class="mk-file">ZC.F.20200923.0_Zenithasia_Corp._2020_Financial_Statement.pdf</p>
  <div class="mk-code"><span>ZC</span><i>.</i><span>F</span><i>.</i><span>20200923</span><i>.</i><span>0</span><i>_</i><span class="t">Title in plain words</span></div>
  <p class="mk-rule">Read left to right: <b>whose · what kind · when · which one · what it says</b>, before anyone opens the file.</p>
  <div class="mk-parts">
    <div><b>ZC</b><span>Company</span><em>Its initials: Zenithasia Corp. One code per company, six in all.</em></div>
    <div><b>F</b><span>Family</span><em>L legal · F financial · H HR · S strategic · O operational. More than fifty kinds of document, five letters.</em></div>
    <div><b>20200923</b><span>Date signed</span><em>Year, month, day: names sort in time order on any computer.</em></div>
    <div><b>0</b><span>Sequence</span><em>The first document that company signed that day; the next is 1.</em></div>
    <div><b>Title</b><span>In plain words</span><em>What the document is, readable by anyone.</em></div>
  </div>
</div>'''

def poster(en, zh, left, right):
    return f'<div class="mk-poster"><span class="en">{en}</span><span class="zh">{zh}</span><span class="ex"><span>← {left}</span><span>→ {right}</span></span></div>'

MOCK_POSTERS = '''
<div class="mk mk-posters" role="img" aria-label="Four place-name posters: Shenyang, Nanjing, Guiyang and Nanchang, each in large Chinese characters with the English name above, and arrows to the two nearest exits, named after classical poets.">''' + \
    poster('Shenyang', '沈陽', '陸遊 Lu You', '王維 Wang Wei') + \
    poster('Nanjing', '南京', '杜牧 Du Mu', '李煜 Li Houzhu') + \
    poster('Guiyang', '貴陽', '王維 Wang Wei', '韓愈 Han Yu') + \
    poster('Nanchang', '南昌', '杜甫 Du Fu', '白居易 Bai Juyi') + '</div>'

def machine(zh, en, n, insp, wear):
    return f'<li><b>{zh} {n} {en}</b><span class="mk-tags"><em>Inspection {insp}</em><em>{wear} wear</em><em>Good</em></span></li>'

def screen(phone, question, notes, label):
    lis = ''.join(f'<li>{n}</li>' for n in notes)
    return (f'<div class="mk mk-screen" role="img" aria-label="{label}"><div class="mk-phone">{phone}</div>'
            f'<div class="mk-notes"><p class="mk-q">{question}</p><ul>{lis}</ul></div></div>')

SCREEN_PLACE = screen('''
    <p class="mk-top"><span>地點 Location</span><span>方向 Directions →</span></p>
    <div class="mk-place"><small>Factory 工廠 02</small><b>南京 Nanjing</b></div>
    <p class="mk-label">機器在這裡 Machines here</p>
    <ul class="mk-machines">''' +
      machine('焊接机器', 'Welding', 372, '2019/09/23', '2%') +
      machine('工業機器人', 'Industrial robot', 16, '2020/01/14', '0%') +
      machine('注塑机', 'Injection moulding', '09', '2017/02/20', '31%') +
      machine('傳送帶', 'Conveyor belt', 87, '2019/11/18', '4%') +
      machine('傳送帶', 'Conveyor belt', '02', '2015/07/09', '77%') +
      machine('生産線機器', 'Assembly line', 238, '2020/04/15', '22%') + '''
    </ul>''',
  'Where am I, and what is here?',
  ['The place name on screen matches the poster on the wall: scan it, or look it up.',
   'Every machine in this place, with its last inspection, wear and status at a glance.',
   'One tap to directions to anywhere else on either campus.'],
  'Phone screen: Factory 02, Nanjing, with the machines there and their inspection date, wear and status.')

SCREEN_MACHINE = screen('''
    <p class="mk-top"><span>← Factory 工廠 02 南京 Nanjing</span></p>
    <h6>焊接机器 372<br>Welding</h6>
    <p class="mk-tags"><em>Inspection 2019/09/23</em><em>2% wear</em><em>Good</em></p>
    <p class="mk-label">Manuals</p>
    <div class="mk-docs"><span>PDF<br>操作手冊</span><span>PDF<br>安全手冊</span><span>PDF<br>Operational manual</span></div>
    <p class="mk-label">Who to ask</p>
    <p class="mk-people"><span><small>導師 Supervisor</small>張 Zhang</span><span><small>值班主任 Shift supervisor</small>王 Wang</span></p>
    <p class="mk-label">清單 Checklists</p>
    <div class="mk-chips"><b class="on">操作 Operations</b><b>機器維修 Maintenance</b><b>進貨程序 Receiving</b></div>
    <div class="mk-step"><b>Operations · 1</b> Wear the right safety gear: welding helmet, gloves and safety glasses.</div>
    <div class="mk-step"><b>Operations · 2</b> Check the machine and cables for damage; make sure every connection is tight.</div>
    <p class="mk-size">A− A A+</p>''',
  'How do I run this machine safely?',
  ['Manuals in both languages, one tap away, instead of a binder somewhere on the floor.',
   'The supervisor and shift supervisor, by name: who to ask, right now.',
   'Checklists for operations, maintenance and receiving, step by step, with larger text when needed.'],
  'Phone screen: welding machine 372, with its manuals in two languages, supervisors and checklists.')

SCREEN_ROUTE = screen('''
    <p class="mk-top"><span>← 焊接机器 372 Welding</span></p>
    <p class="mk-label">從 From</p><div class="mk-field">Factory 工廠 02 南京 Nanjing</div>
    <p class="mk-label">到 To</p><div class="mk-field">Factory 工廠 05 合肥 Hefei</div>
    <ol class="mk-dir"><li>Exit the building from gate C.</li><li>Take a golf cart to Factory 05.</li><li>Enter Factory 05 from gate B.</li><li>Take lift 03 to the 7th floor.</li><li>Turn left; walk 100 metres to 合肥 Hefei.</li></ol>
    <ol class="mk-dir zh"><li>從 C 門離開建築物。</li><li>乘坐高爾夫車前往工廠 05。</li><li>從 B 門進入工廠 05。</li><li>乘坐 03 號電梯到達 7 樓。</li><li>左轉步行 100 米，直到看到合肥。</li></ol>''',
  'How do I get to the next building?',
  ['Step by step between buildings: gates, golf cart, lift and floor.',
   'In English and Chinese, for visitors and staff alike.',
   'It ends at a named place: the same name printed on the poster when you arrive.'],
  'Phone screen: directions from Factory 02 to Factory 05, in English and Chinese.')

ROOMS = [('GW G.03', 'Ground', 'Lecture Theatre 1', 'Lecture theatre', '180', '120'),
         ('GW G.04', 'Ground', 'Seminar Room', 'Teaching room', '55', '30'),
         ('GW 1.01', '1', 'Seminar Room', 'Teaching room', '60', '40'),
         ('GW 1.02', '1', 'Seminar Room', 'Teaching room', '61', '40'),
         ('GW 1.04', '1', 'Computer Room', 'Computer lab', '95', '40'),
         ('GW 2.01', '2', 'Design Studio', 'Studio', '120', '30')]
MOCK_ROOMS = '''
<div class="mk mk-rooms" role="img" aria-label="Room Finder, with sample data: a search for Glassworks returns 28 rooms, 12 learning spaces and 546 seats, listed with floor, name, use, area and seats, with filters for seats and function.">
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
 dict(slug='factory', n=1, nav='Case: Factory',
  title='Two factory campuses anyone can find their way around, delivered in half the time',
  card_k='Electronics manufacturing · China',
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
  stat=('1', 'month, not 2', 'from the first floor to every required floor on both campuses'),
  figs=[(MOCK_POSTERS, 'Four posters from the series, re-created. Each names a place after a city and points to the two nearest exits, named after poets. These sit alongside the mandated green exit signs; they do not replace them.'),
        (SCREEN_PLACE, ''), (SCREEN_MACHINE, ''), (SCREEN_ROUTE, 'Three screens from the phone app, re-created with sample data. Sites withheld.')],
  how_fig=None,
  who=[('Client', 'NDA · Electronics manufacturer'),
       ('Region', 'Mainland China, 2018–2020'),
       ('Scale', 'Two campuses of five to six buildings each'),
       ('My role', 'Led the work through my consultancy')],
  what='Staff moved between buildings by bicycle, scooter and golf cart. Workers, engineers, visitors, health inspectors and government officials all needed to find a place, a machine or a safe way out, and the numbering made sense only to the people who already knew it.',
  how=[('Named places instead of numbering them.', 'Areas took the names of cities, safety exits the names of classical poets: names people already carry in their heads. The named exits sit alongside the mandated green exit signs; they do not replace them.'),
       ('Put both languages on every sign,', 'with arrows to the two nearest exits.'),
       ('Put every machine’s manuals, checklists and supervisors one tap away,', 'in a simple bilingual web app, with directions between buildings.'),
       ('Proved it small, then scaled it.', 'One floor in the first week, one building live in the second, a one-week pilot, then every required floor on both campuses.')],
  diagram='factory', diagram_in='how', diagram_cap='Redrawn from the original designs. The factories and their locations are withheld.',
  impact=[('1 month, not 2', 'delivered in half the agreed time'),
          ('Found their way unaided', 'visitors, inspectors and government officials, without an escort'),
          ('Extended', 'the client commissioned a follow-up project')],
  see=('prototypes/factory.html', 'See the directory working (prototype, sample data) →')),
 dict(slug='repository', n=2, nav='Case: Conglomerate',
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
  stat=('~18h/w → 2h/w', 'searching and meeting about documents', 'combined across the group; 15–20 hours a week before (estimate)'),
  figs=[(MOCK_REPOSITORY, 'The search, re-created from the original design. Company and project names are invented.')],
  how_fig=(MOCK_NAMING, 'The naming rule that makes the search work: every company files the same way.'),
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
 dict(slug='room-finder', n=3, nav='Case: University',
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
  stat=('15,000+', 'rooms, one search', 'across more than 40 buildings, built from records the institution already had'),
  figs=[(MOCK_ROOMS, 'Re-created from the working prototype, with sample data.')],
  how_fig=None,
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
  see=('prototypes/room-finder.html', 'See the working prototype (sample data) →')),
]

# ── templates ─────────────────────────────────────────────────────────────────

def page(title, body, extra_head='', active='home'):
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="robots" content="noindex">
{extra_head}<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css">
</head>
<body>
<div class="wrap">
{body}
{site_nav(active)}
</div>
</body>
</html>
'''

def site_nav(active):
    items = [('home', 'index.html', 'Home')] + [(c['slug'], f"{c['slug']}.html", c['nav']) for c in CASES]
    links = ''.join(f'<a href="{href}"{" class=\"on\" aria-current=\"page\"" if key == active else ""}>{label}</a>' for key, href, label in items)
    return f'<footer class="site-nav"><nav aria-label="Pages">{links}</nav></footer>'

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

<div class="stat"><p class="stat-n">{' '.join(f'<span>{t}</span>' for t in c['stat'][0].replace(' → ', ' →\u00a0').split(' '))}</p><p class="stat-u">{c['stat'][1]}</p><p class="stat-c">{c['stat'][2]}</p></div>

{ba_block(c)}
{''.join(f'<figure class="mock">{m}' + (f'<figcaption>{cap}</figcaption>' if cap else '') + '</figure>' for m, cap in c['figs'])}

<h2>Who</h2>
<dl class="facts">{who}</dl>

<h2>What</h2>
<p>{c['what']}</p>

<h2>How</h2>{fig if c['diagram_in'] == 'how' else ''}{f'<figure class="mock">{c["how_fig"][0]}<figcaption>{c["how_fig"][1]}</figcaption></figure>' if c['how_fig'] else ''}
<ol class="did">{how}</ol>

<h2>Impact</h2>{fig if c['diagram_in'] == 'impact' else ''}
<ul class="changed">{imp}</ul>
{see}
<nav class="next">{nav_l}{nav_r}</nav>'''
    og = f'<meta property="og:title" content="{html.escape(c["title"])}">\n<meta property="og:image" content="img/share-{c["slug"]}.png">\n'
    return page(f'{c["short"]} — {NAME}', body, og, active=c['slug'])

def home():
    cards = ''.join(f'''
  <a class="case-card" href="{c['slug']}.html">
    <span class="k">{c['card_k']}</span>
    <span class="t">{c['title']}</span>
    <span class="s">{c['card_s']}</span>
    <span class="go">Read the case →</span>
  </a>''' for c in CASES)
    body = f'''<header class="top"><a href="index.html">{NAME}</a><span>Selected work</span></header>

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
is no figure, none is given. Screens are re-created with sample data.</p>

<h2>Contact</h2>
<ul class="contact">
  <li><a href="mailto:mike@mikko.gr">mike@mikko.gr</a></li>
  <li><a href="https://www.linkedin.com/in/oustamanolakis">LinkedIn</a></li>
</ul>'''
    return page(f'{NAME} — selected work', body, active='home')

def bare(title, inner, cls):
    return f'''<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../site.css"></head><body class="{cls}">{inner}</body></html>
'''

def build():
    (ROOT / 'index.html').write_text(home())
    gen = ROOT / 'src' / 'gen'; gen.mkdir(exist_ok=True)
    for i, c in enumerate(CASES):
        (ROOT / f'{c["slug"]}.html').write_text(case_page(c, i))
        (gen / f'share-{c["slug"]}.html').write_text(bare(c['short'], ba_block(c, share=True), 'shot-share'))
    print('pages written')

def images():
    out = ROOT / 'img'; out.mkdir(exist_ok=True)
    for c in CASES:
        for kind, size in (('share', '1200,630'),):
            src = ROOT / 'src' / 'gen' / f'{kind}-{c["slug"]}.html'
            subprocess.run([EDGE, '--headless', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                            f'--window-size={size}', f'--screenshot={out / f"{kind}-{c["slug"]}.png"}', src.as_uri()],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('images written')

if __name__ == '__main__':
    build()
    if '--images' in sys.argv:
        images()
