import os
import hashlib
from icons import apply_icons

ROOT = os.path.dirname(os.path.abspath(__file__))
NAV = open(os.path.join(ROOT, 'assets/_nav.html')).read().strip()
FOOTER = open(os.path.join(ROOT, 'assets/_footer.html')).read().strip()
# Cache-busting query string for style.css, derived from the file's own content so it only
# changes when the CSS actually changes (not on every build) -- browsers were serving stale
# cached CSS across edits during development even after a hard refresh. Same deal for site.js.
CSS_VERSION = hashlib.md5(open(os.path.join(ROOT, 'assets/style.css'), 'rb').read()).hexdigest()[:10]
JS_VERSION = hashlib.md5(open(os.path.join(ROOT, 'assets/site.js'), 'rb').read()).hexdigest()[:10]

SHELL = """<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta_desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://www.mananbhullar.com{path}">
<meta name="theme-color" content="#1E5FD9">
<meta name="format-detection" content="telephone=yes">

<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Manan Bhullar Real Estate">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://www.mananbhullar.com{path}">
<meta property="og:locale" content="en_CA">
<meta property="og:image" content="https://www.mananbhullar.com/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Manan Bhullar \u2014 Fraser Valley &amp; Lower Mainland Real Estate">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://www.mananbhullar.com/assets/og-image.jpg">

<link rel="preload" href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&f[]=switzer@400,500,600,700&display=swap" as="style">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&f[]=switzer@400,500,600,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css?v={css_version}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"RealEstateAgent","name":"Manan Bhullar","image":"https://www.mananbhullar.com/assets/og-image.jpg","url":"https://www.mananbhullar.com{path}","telephone":"+1-604-727-9542","email":"mb_realestate@outlook.com","areaServed":[{{"@type":"City","name":"Surrey"}},{{"@type":"City","name":"Langley"}},{{"@type":"City","name":"Delta"}},{{"@type":"City","name":"Burnaby"}}],"address":{{"@type":"PostalAddress","addressRegion":"BC","addressCountry":"CA"}}}}
</script>
</head>
<body>

{nav}

<div class="wrap crumbs">{crumbs}</div>

{body}

{footer}

<div class="mobile-cta-bar">
  <a class="cta-text" href="sms:+16047279542">\U0001F4AC Text</a>
  <a class="cta-primary" href="/contact/">Get In Touch</a>
</div>

<script src="/assets/site.js?v={js_version}" defer></script>
</body>
</html>
"""

def crumbs(*pairs):
    parts = ['<a href="/">Home</a>']
    for i, (label, href) in enumerate(pairs):
        parts.append('<span class="sep">/</span>')
        if href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span class="cur">{label}</span>')
    return ''.join(parts)

def write_page(path, title, meta_desc, crumb_html, body):
    full_html = SHELL.format(
        title=title, meta_desc=meta_desc, og_title=title.split(' | ')[0],
        path=path, nav=NAV, footer=FOOTER, crumbs=crumb_html, body=body,
        css_version=CSS_VERSION, js_version=JS_VERSION
    )
    full_html = apply_icons(full_html)
    if path.endswith('/'):
        out_dir = os.path.join(ROOT, path.lstrip('/'))
        out_file = os.path.join(out_dir, 'index.html')
    else:
        out_file = os.path.join(ROOT, path.lstrip('/'))
        out_dir = os.path.dirname(out_file)
    os.makedirs(out_dir, exist_ok=True)
    with open(out_file, 'w') as f:
        f.write(full_html)
    print('wrote', path)

# ---------- Reusable body-fragment builders ----------

def subhero(eyebrow, h1, lead, ctas=None):
    ctas_html = ctas or ''
    return f"""<header class="subhero">
  <div class="wrap">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="hero-ctas">{ctas_html}</div>
  </div>
</header>"""

CALL_CTA = '<a class="btn-outline-light" href="tel:+16047279542">\U0001F4DE Call (604) 727-9542</a>'
TEXT_CTA = '<a class="btn-outline-light" href="sms:+16047279542">\U0001F4AC Text Manan</a>'

def google_follow_card():
    return f"""<a class="google-follow-card" href="https://www.google.com/search?q=Manan+Bhullar+Coldwell+Banker+Universe+Realty" target="_blank" rel="noopener">
      <svg class="g-icon" viewBox="0 0 48 48" width="26" height="26"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3c-1.6 4.7-6.1 8-11.3 8-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.1 8 3l6-6C34.5 6 29.5 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.7-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.6 15.6 18.9 13 24 13c3.1 0 5.8 1.1 8 3l6-6C34.5 6 29.5 4 24 4c-7.4 0-13.8 4.2-17 10.3z"/><path fill="#4CAF50" d="M24 44c5.4 0 10.3-1.8 14-4.9l-6.4-5.4C29.6 35.5 26.9 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.9 39.6 16.4 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.3-2.2 4.2-4.1 5.6l6.4 5.4C39.9 36.9 44 31 44 24c0-1.3-.1-2.7-.4-3.5z"/></svg>
      <div class="txt"><strong>Follow us on Google</strong><span>Add Manan Bhullar Real Estate as a preferred source to see our updates in Search</span></div>
    </a>"""
EVAL_CTA = '<a class="btn-solid-warm" href="/sellers/home-evaluation/">Free Home Evaluation</a>'
CONTACT_CTA = '<a class="btn-solid-warm" href="/contact/">Get In Touch</a>'

def cta_band(heading, sub, ctas):
    return f"""<section class="cta-band">
  <div class="wrap">
    <h2>{heading}</h2>
    <p>{sub}</p>
    <div class="hero-ctas">{ctas}</div>
  </div>
</section>"""

def simple_cards(title, sub, cards, cols=3, raised=True):
    cls = 'raised' if raised else ''
    grid_cls = 'grid-cards' if cols == 3 else f'grid-cards cols-{cols}'
    cards_html = ''
    for c in cards:
        href = c.get('href', '#')
        icon_html = f'<span class="card-icon">{c["icon"]}</span>' if c.get('icon') else ''
        cards_html += f"""<a class="simple-card" href="{href}">
        {icon_html}<strong>{c['title']}</strong>
        <span>{c['desc']}</span>
        <span class="go">Learn More \u2192</span>
      </a>"""
    return f"""<section class="content-section {cls}">
  <div class="wrap">
    <div class="content-head center">
      <h2>{title}</h2>
      <p>{sub}</p>
    </div>
    <div class="{grid_cls}">
      {cards_html}
    </div>
  </div>
</section>"""

def info_cards(title, sub, cards, cols=3, raised=True):
    cls = 'raised' if raised else ''
    grid_cls = 'grid-cards' if cols == 3 else f'grid-cards cols-{cols}'
    cards_html = ''
    for c in cards:
        icon_html = f'<span class="card-icon">{c["icon"]}</span>' if c.get('icon') else ''
        cards_html += f"""<div class="simple-card no-link">
        {icon_html}<strong>{c['title']}</strong>
        <span>{c['desc']}</span>
      </div>"""
    return f"""<section class="content-section {cls}">
  <div class="wrap">
    <div class="content-head center">
      <h2>{title}</h2>
      <p>{sub}</p>
    </div>
    <div class="{grid_cls}">
      {cards_html}
    </div>
  </div>
</section>"""

FORMSPREE_ENDPOINT = "https://formspree.io/f/mzepnvwn"

def lead_form(title, subject, extra_fields='', message_placeholder='Your Message', note=None):
    note_html = f'<p class="form-disclaimer">{note}</p>' if note else ''
    return f"""<form class="consult-form" action="{FORMSPREE_ENDPOINT}" method="POST" data-lead-form>
      <h3>{title}</h3>
      <p class="form-trust">REALTOR® · BBA Marketing, SFU Beedie School of Business</p>
      <input type="hidden" name="_subject" value="{subject}">
      <input type="text" name="_gotcha" style="display:none">
      <input type="text" name="name" placeholder="Full Name" required style="margin-bottom:12px;">
      <input type="email" name="email" placeholder="Email Address" required style="margin-bottom:12px;">
      <input type="tel" name="phone" placeholder="Phone Number" required style="margin-bottom:12px;">
      {extra_fields}
      <textarea name="message" placeholder="{message_placeholder}"></textarea>
      <button type="submit" class="btn-block-dark">✈️ Send Message</button>
      <p class="form-error" hidden>Something went wrong — please call or email directly instead.</p>
      {note_html}
    </form>"""

REAL_PHOTOS = {
    'manan-bhullar-portrait': ('/assets/photos/manan-headshot.jpg', 1170, 1529),
    'surrey-buyer-agent': ('/assets/photos/modern-home-dusk-mountain.jpg', 1920, 950),
    'first-time-buyer-keys': ('/assets/photos/entrance-dusk-stone.jpg', 1920, 1066),
    'buyers-luxury': ('/assets/photos/dark-estate-daylight.jpg', 1920, 744),
    'buyers-condos-townhomes': ('/assets/photos/courtyard-entrance-dusk.jpg', 1920, 1169),
    'buyers-investment': ('/assets/photos/reflecting-pool-building.jpg', 1920, 942),
    'buyers-relocation': ('/assets/photos/whistler-pool-mountain.jpg', 1700, 1135),
    'area-langley': ('/assets/photos/acreage-langley.jpg', 2000, 933),
    'area-salmon-river': ('/assets/photos/acreage-langley.jpg', 2000, 933),
    'area-campbell-valley': ('/assets/photos/acreage-langley.jpg', 2000, 933),
    'area-otter-district': ('/assets/photos/acreage-langley.jpg', 2000, 933),
    'area-glen-valley': ('/assets/photos/acreage-langley.jpg', 2000, 933),
}

def point_list_section(dark, eyebrow, heading, lead, points, img_first=False, img_seed='surrey-real-estate', img_alt=''):
    dot_html = ''
    for p in points:
        dot_html += f"""<div class="point">
        <div class="dot">{p['icon']}</div>
        <div><strong>{p['title']}</strong><span>{p['desc']}</span></div>
      </div>"""
    text_block = f"""<div>
      <div class="eyebrow" style="margin-bottom:16px;">{eyebrow}</div>
      <h2>{heading}</h2>
      <p style="color:{'#C7C5C0' if dark else 'var(--ink-soft)'};margin-top:14px;">{lead}</p>
      <div class="point-list">{dot_html}</div>
    </div>"""
    alt = img_alt or f"Sample placeholder photo — {heading}"
    if img_seed in REAL_PHOTOS:
        src, w, h = REAL_PHOTOS[img_seed]
        img_block = f'<img class="imgblock" src="{src}" alt="{alt.replace(" (sample photo)", "")}" loading="lazy" width="{w}" height="{h}">'
    else:
        img_block = f'<img class="imgblock" src="https://picsum.photos/seed/{img_seed}/800/600" alt="{alt}" loading="lazy" width="800" height="600">'
    order = [img_block, text_block] if img_first else [text_block, img_block]
    cls = 'content-section dark' if dark else 'content-section'
    return f"""<section class="{cls}">
  <div class="wrap two-col">
    {order[0]}
    {order[1]}
  </div>
</section>"""

def step_section(title, sub, steps, raised=False):
    cls = 'content-section raised' if raised else 'content-section'
    steps_html = ''
    for i, s in enumerate(steps, 1):
        steps_html += f"""<div class="step-card">
        <div class="num">{i:02d}</div>
        <strong>{s['title']}</strong>
        <span>{s['desc']}</span>
      </div>"""
    return f"""<section class="{cls}">
  <div class="wrap">
    <div class="content-head center">
      <h2>{title}</h2>
      <p>{sub}</p>
    </div>
    <div class="step-grid">{steps_html}</div>
  </div>
</section>"""

def faq_section(title, items):
    items_html = ''
    for q, a in items:
        items_html += f"""<div class="faq-item">
        <button class="faq-q"><span>{q}</span><span class="chev">\u25BE</span></button>
        <div class="faq-a"><p>{a}</p></div>
      </div>"""
    return f"""<section class="content-section">
  <div class="wrap">
    <div class="content-head center">
      <h2>{title}</h2>
    </div>
    <div class="faq">{items_html}</div>
  </div>
</section>"""

def community_grid_section(title, sub, areas):
    cards = ''
    for a in areas:
        cards += f"""<a class="community-card" href="{a['href']}">
        <div><div class="name">{a['name']}</div><div class="note">{a['note']}</div></div>
        <span class="arrow">\u2192</span>
      </a>"""
    return f"""<section class="content-section raised">
  <div class="wrap">
    <div class="content-head center"><h2>{title}</h2><p>{sub}</p></div>
    <div class="community-grid">{cards}</div>
  </div>
</section>"""

def stat_strip(items):
    cards = ''.join(f'<div class="stat-card"><strong>{v}</strong><span>{l}</span></div>' for v, l in items)
    return f"""<section class="content-section stat-strip">
  <div class="wrap"><div class="grid-cards cols-4">{cards}</div></div>
</section>"""

# Real, verifiable facts about Manan \u2014 used in place of generic "30+ years" stat callouts
MANAN_STATS = [
    ("SFU Beedie", "School of Business Grad"),
    ("BBA Marketing", "Beedie School, SFU"),
    ("Residential +", "Commercial &amp; Industrial"),
    ("Fleetwood", "Record Price-Per-Sqft Sale"),
]

def market_snapshot_section():
    return f"""<section class="content-section raised">
  <div class="wrap">
    <div class="content-head center">
      <h2>Fraser Valley Market Snapshot</h2>
      <p>Real numbers from the Fraser Valley Real Estate Board's most recent monthly report \u2014 not estimates.</p>
    </div>
    <div class="grid-cards cols-4">
      <div class="simple-card"><strong>$877,600</strong><span>Composite benchmark price, all residential types</span></div>
      <div class="simple-card"><strong>$1,350,200</strong><span>Benchmark price, single-family detached</span></div>
      <div class="simple-card"><strong>$764,100</strong><span>Benchmark price, townhomes</span></div>
      <div class="simple-card"><strong>$469,500</strong><span>Benchmark price, apartments &amp; condos</span></div>
    </div>
    <p style="font-size:0.8rem;color:var(--ink-soft);margin-top:20px;text-align:center;">Source: Fraser Valley Real Estate Board, July 2026 MLS\u00ae &amp; Home Price Index statistics. The Fraser Valley market is currently favouring buyers, with inventory near decade highs \u2014 Manan can walk you through what that means for your specific situation.</p>
  </div>
</section>"""

def local_info_section(name, schools=None, shopping=None, recreation=None, entertainment=None):
    def col(title, icon, items):
        lis = ''.join(f'<li>{i}</li>' for i in items)
        return f"""<div class="local-info-col">
          <div class="local-info-head"><span class="ico">{icon}</span><strong>{title}</strong></div>
          <ul>{lis}</ul>
        </div>"""
    cols = ''
    if schools: cols += col("Schools", "\U0001F3EB", schools)
    if shopping: cols += col("Shopping &amp; Grocery", "\U0001F6D2", shopping)
    if entertainment: cols += col("Entertainment &amp; Dining", "\U0001F37D\uFE0F", entertainment)
    if recreation: cols += col("Recreation &amp; Parks", "\U0001F3DE\uFE0F", recreation)
    return f"""<section class="content-section raised">
  <div class="wrap">
    <div class="content-head center"><h2>Life in {name}</h2><p>Real schools, shopping, dining, and recreation \u2014 not a generic list. Always confirm current school catchments directly with the school district before making a decision based on address.</p></div>
    <div class="local-info-grid">{cols}</div>
  </div>
</section>"""

def pro_tip(heading, text):
    return f"""<div class="pro-tip"><strong>{heading}</strong><p>{text}</p></div>"""

def price_range_grid(title, sub, items, tip_heading=None, tip_text=None):
    cards = ''.join(f'<div class="simple-card"><strong>{n}</strong><span>{d}</span></div>' for n, d in items)
    tip_html = pro_tip(tip_heading, tip_text) if tip_heading else ''
    return f"""<section class="content-section raised">
  <div class="wrap">
    <div class="content-head center"><h2>{title}</h2><p>{sub}</p></div>
    <div class="grid-cards cols-2">{cards}</div>
    {tip_html}
  </div>
</section>"""

print("helpers ready")

# ============================================================
# AREAS DATA (reused by /communities/ index + individual pages)
# ============================================================
AREAS = [
    dict(slug='surrey', name='Surrey', note='BC\'s second-largest city',
         tags=['SkyTrain Connectivity', 'Cultural Diversity', 'Growing Tech Hub'],
         desc="Surrey is British Columbia's second-largest city, offering diverse neighbourhoods, excellent transit connectivity, and a booming local economy. From established family neighbourhoods to rapidly densifying town centres, Surrey covers an enormous range of housing types and price points.",
         schools=["SFU Surrey and KPU Civic Plaza campuses in City Centre", "School District 36 Surrey \u2014 the province's largest, with 50+ elementary and nearly 30 secondary schools"],
         shopping=["Central City Shopping Centre", "Guildford Town Centre", "Willowbrook and King's Cross Shopping Centres"],
         recreation=["Bear Creek Park", "Green Timbers Urban Forest", "Tynehead and Surrey Bend Regional Parks", "Surrey Sport &amp; Leisure Complex"],
         area_faq=[
            ("What makes Surrey attractive compared to Vancouver?", "Meaningfully more affordable housing across every property type, strong SkyTrain connectivity via the Expo Line with the Surrey-Langley extension underway, and genuine neighbourhood diversity \u2014 from high-rise City Centre living to acreage properties in the south."),
         ],
         entertainment=["Landmark Cinemas 12 Guildford", "Diverse dining along the King George Boulevard and Fraser Highway corridor"]),
    dict(slug='fleetwood', name='Fleetwood', note='Established residential, strong schools',
         tags=['Tree-Lined Streets', 'Family Homes', 'Fraser Hwy Access'],
         desc="Fleetwood is one of Surrey's long-established residential neighbourhoods, known for tree-lined streets, a mix of single-family homes and newer townhome developments, and easy access to Fraser Highway and Highway 1. It's a popular choice for families looking for more space without leaving Surrey.",
         schools=["Surrey Christian School (private, K-12)", "Multiple SD36 Surrey elementary and secondary schools serve Fleetwood \u2014 confirm your specific catchment with the district"],
         shopping=["Fleetwood Park Village", "Evergreen Mall", "Fresh St Market", "Guildford Town Centre (10 min drive)"],
         recreation=["Surrey Sport &amp; Leisure Complex (pools, ice rinks, 10,000 sq ft weight room)", "Fleetwood Community Centre &amp; Library", "Green Timbers Urban Forest", "Tynehead Regional Park", "Guildford Golf &amp; Country Club", "25+ neighbourhood parks"],
         area_faq=[
            ("Is Fleetwood a good area for families?", "Yes \u2014 Fleetwood is one of Surrey's most established family neighbourhoods, with tree-lined streets, over 25 parks, and the Surrey Sport &amp; Leisure Complex right in the community."),
            ("What's the commute like from Fleetwood?", "Fleetwood sits centrally along Fraser Highway with direct access to Highway 1. The upcoming Surrey-Langley SkyTrain extension along Fraser Highway will bring rapid transit directly through the neighbourhood."),
            ("Where do Fleetwood residents shop for groceries?", "Fresh St Market and other grocers are within Fleetwood Park Village and Evergreen Mall, with Guildford Town Centre a short drive away for larger-format shopping."),
         ],
         entertainment=["Landmark Cinemas 12 Guildford (10 min drive)", "Restaurants and cafes along Fraser Highway"]),
    dict(slug='south-surrey', name='White Rock / South Surrey', note='Oceanfront & premium market',
         tags=['Oceanfront Living', 'Iconic Pier', 'Upscale Dining'],
         desc="White Rock and South Surrey \u2014 including Grandview Heights \u2014 offer oceanfront living along Semiahmoo Bay, upscale dining, and a relaxed seaside lifestyle. The iconic White Rock pier and promenade anchor a market generally regarded as Surrey's premium residential tier, popular with commuters, downsizers, and retirees alike.",
         schools=["Earl Marriott Secondary", "Semiahmoo Secondary", "Elgin Park Secondary", "Grandview Heights Secondary (opened 2021, capacity 1,500+)", "South Surrey/White Rock Learning Centre", "Peace Arch Elementary", "White Rock Elementary", "Morgan Elementary", "Pacific Heights Elementary", "Rosemary Heights Elementary", "Sunnyside Elementary \u2014 confirm your specific catchment with SD36 Surrey"],
         shopping=["Semiahmoo Shopping Centre", "Ocean Park Shopping Centre", "Grandview Corners", "Downtown White Rock's independent retailers along Marine Drive"],
         recreation=["The White Rock pier &amp; promenade", "South Surrey Athletic Park", "South Surrey Recreation &amp; Arts Centre", "White Rock Community Centre", "Grandview Heights Aquatic Centre", "8km of sandy beach along Semiahmoo Bay"],
         area_faq=[
            ("What makes White Rock / South Surrey different from the rest of Surrey?", "It's Surrey's premium residential tier \u2014 8km of oceanfront along Semiahmoo Bay, the iconic White Rock pier, and generally larger homes on tree-lined streets, at a different price point than North Surrey."),
            ("Are there good schools in the area?", "Yes \u2014 Earl Marriott, Semiahmoo, Elgin Park, and the newer Grandview Heights Secondary are the area's main public high schools, all within SD36 Surrey, with Morgan, Pacific Heights, Rosemary Heights, and Sunnyside Elementary feeding into Grandview Heights specifically. Catchments vary by exact address, so confirm directly with the district before buying."),
            ("Is this a walkable, retiree-friendly area?", "Downtown White Rock's promenade and Marine Drive shops are very walkable, and the area sees strong interest from downsizers and retirees drawn to the beach lifestyle and slower pace."),
         ],
         entertainment=["Restaurants and cafes along White Rock's Marine Drive promenade", "Semiahmoo Shopping Centre dining"]),
    dict(slug='cloverdale', name='Cloverdale', note='Heritage charm, growing fast',
         tags=['Small-Town Charm', 'Annual Rodeo', 'New Development'],
         desc="Cloverdale blends small-town, heritage character — it's home to the Cloverdale Rodeo and Country Fair — with rapid new-home development. Newer townhome and single-family communities continue to expand around the historic downtown core, making it a popular entry point for growing families.",
         schools=["Lord Tweedsmuir Secondary", "Salish Secondary", "Multiple SD36 Surrey elementary schools feed into these two \u2014 confirm your specific catchment with the district"],
         shopping=["Willowbrook Shopping Centre", "Central City Shopping Centre (SkyTrain-accessible)", "Cloverdale's historic downtown, home to 200+ independent businesses"],
         recreation=["Cloverdale Recreation Centre (three gymnasiums, fitness/weight room)", "Clayton Community Centre (arts, recreation &amp; library)", "Cloverdale Athletic Park", "Cloverdale Fairgrounds &amp; Museum of Surrey", "Cloverdale Rodeo &amp; Country Fair (annual)"],
         area_faq=[
            ("Is Cloverdale a good area for families?", "Yes \u2014 Cloverdale is widely considered one of Surrey's best family neighbourhoods, with highly regarded schools like Lord Tweedsmuir Secondary, large sports complexes including Cloverdale Athletic Park, and a safe, community-oriented atmosphere."),
            ("What's the difference between Cloverdale and Clayton Heights?", "Historic Cloverdale is the established southern section with heritage buildings, larger residential lots, and a traditional small-town feel. Clayton Heights, to the north, is the modern, master-planned community with higher-density housing and coach homes."),
            ("What recreation facilities does Cloverdale have?", "The Cloverdale Recreation Centre offers three full gymnasiums and a large fitness/weight room, and the newer Clayton Community Centre adds an integrated arts, recreation, and library hub \u2014 both reflect the city's ongoing investment in the area as it grows."),
         ],
         entertainment=["Restaurants and cafes in Cloverdale's historic downtown"]),
    dict(slug='city-centre', name='City Centre', note='Urban core, SkyTrain access',
         tags=['High-Rise Living', 'Transit Hub', 'SFU Surrey'],
         desc="Surrey City Centre is the municipality's designated downtown, anchored by Central City Mall, Simon Fraser University's Surrey campus, and direct SkyTrain access via the Expo Line. It's the epicentre of Surrey's high-rise condo development and continues to densify rapidly.",
         schools=["SFU Surrey (Central City campus)", "KPU Civic Plaza campus", "Multiple SD36 Surrey elementary and secondary schools serve City Centre \u2014 confirm your specific catchment with the district"],
         shopping=["Central City Shopping Centre (T&amp;T Supermarket, Walmart, Best Buy, Winners, 130+ stores)", "Holland Park farmers market and events"],
         recreation=["Chuck Bailey Recreation Centre", "City Centre Library", "Holland Park", "Green Timbers Urban Forest nearby", "Surrey Memorial Hospital", "Two Expo Line SkyTrain stations \u2014 Surrey Central and King George"],
         area_faq=[
            ("What makes City Centre different from the rest of Surrey?", "It's Surrey's designated downtown \u2014 the highest concentration of high-rise condos, direct SkyTrain access via two Expo Line stations, and the SFU Surrey and KPU campuses within walking distance."),
            ("Is City Centre a good spot for investors or first-time condo buyers?", "Yes \u2014 strong rental demand from SFU and KPU students plus young professionals, direct transit access, and ongoing City investment (new city hall, library, and continued high-rise development) support both rental income and long-term appreciation."),
            ("What's within walking distance in City Centre?", "Central City Shopping Centre, Holland Park, Surrey City Hall and Library, Surrey Memorial Hospital, and both SkyTrain stations \u2014 it's one of the most walkable, transit-connected pockets of Surrey."),
         ],
         entertainment=["Dining at Central City Shopping Centre", "Cafes serving the SFU Surrey and KPU campuses"]),
    dict(slug='newton', name='Newton', note='Diverse, accessible entry point',
         tags=['Cultural Diversity', 'First-Time Buyers', 'Central Location'],
         desc="Newton is one of Surrey's most diverse and densely populated neighbourhoods, offering a mix of older single-family homes, townhomes, and newer condo development. Its central location and relative affordability make it a popular starting point for first-time buyers.",
         schools=["Multiple SD36 Surrey elementary and secondary schools serve Newton \u2014 confirm your specific catchment with the district, as East and West Newton fall into different school zones"],
         shopping=["King's Cross Shopping Centre", "Newton Town Centre (anchored by Chalo FreshCo grocery)", "Strawberry Hill Shopping Centre", "Payal Plaza and the Scott Road corridor's South Asian grocers, sweet shops, and jewellers"],
         recreation=["Newton Recreation Centre (wave pool \u2014 the only one in Surrey \u2014 plus mat room)", "Bear Creek Park (miniature railway, mini-golf)", "Unwin Park (Surrey's largest fully accessible playground)", "Bell Performing Arts Centre", "Newton Cultural Centre", "The new $310M Newton Community Centre, currently under construction"],
         area_faq=[
            ("Is Newton a good area for first-time buyers?", "Yes \u2014 Newton is one of Surrey's more accessible entry points, with a mix of older single-family homes, townhomes, and condos at relatively lower price points than City Centre or South Surrey."),
            ("What recreation does Newton offer?", "Newton Recreation Centre has Surrey's only wave pool, and Bear Creek Park \u2014 one of the city's most-used parks \u2014 includes a miniature railway and mini-golf. A major new $310M Newton Community Centre is currently under construction with a 50-metre pool and expanded library."),
            ("What's the shopping and dining scene like in Newton?", "Newton has one of the largest concentrations of South Asian businesses in Canada along the Scott Road corridor \u2014 grocers, sweet shops, jewellers, and restaurants \u2014 plus everyday shopping at King's Cross and Newton Town Centre."),
         ],
         entertainment=["A large concentration of South Asian restaurants, sweet shops, and cafes along the Scott Road corridor"]),
    dict(slug='industrial-corridor', name='Industrial Corridor', note='Leasing & investment',
         tags=['Warehousing', 'Highway Access', 'US Border Proximity'],
         desc="Surrey's industrial corridor — including areas like Campbell Heights and the Cloverdale industrial parks — has become one of the Lower Mainland's fastest-growing hubs for warehouse, distribution, and light-industrial space, driven by its highway access and proximity to the US border.",
         area_faq=[
            ("What areas make up Surrey's industrial corridor?", "Campbell Heights is the flagship large-format industrial park, alongside established industrial land around Cloverdale and the Highway 10 corridor \u2014 see Manan's dedicated Industrial &amp; Warehouse commercial page for full detail on this market."),
         ]),
    dict(slug='delta', name='Delta', note='Three distinct communities',
         tags=['Waterfront Living', 'BC Ferries Terminal', 'Ladner & Tsawwassen'],
         desc="Delta is a diverse municipality comprising three distinct communities — Ladner, Tsawwassen, and North Delta — offering everything from waterfront living and rural acreages to the Tsawwassen ferry terminal connecting to Vancouver Island.",
         schools=["Delta School District (SD37) \u2014 24 elementary and 7 secondary schools, including District French Immersion"],
         recreation=["Ladner Leisure Centre", "North Delta Recreation Centre", "Sungod Recreation Centre", "Centennial Beach and Boundary Bay"],
         entertainment=["Restaurants in Ladner Village and dining at Tsawwassen Mills"],
         shopping=["Ladner Village shops", "Tsawwassen Mills and Tsawwassen Commons"]),
    dict(slug='langley', name='Langley', note='Small-town charm, modern amenities',
         tags=['Fort Langley Heritage', 'Wine Country', 'Equestrian Community'],
         desc="Langley combines small-town charm with modern amenities, featuring the historic Fort Langley village, an established wine and agritourism scene, and a strong equestrian community alongside newer master-planned residential development.",
         schools=["School District 35 Langley covers all of Langley Township and City", "Willoughby's newer schools include Lynn Fripps, Richard Bulpitt, and Yorkson Creek Middle \u2014 confirm your specific catchment with SD35"],
         shopping=["Willowbrook Shopping Centre", "Willoughby Town Centre", "Langley City's downtown (600+ shops and services)", "Tsawwassen and Cascades Casino nearby for entertainment"],
         recreation=["Langley Events Centre &amp; Willoughby Community Centre (fitness studio, weight room, triple gymnasium)", "Fort Langley National Historic Site", "Campbell Valley Regional Park", "Aldergrove Regional Park &amp; the Aldergrove Credit Union Community Centre (pool + outdoor water park)", "Trinity Western University"],
         area_faq=[
            ("What's the fastest-growing part of Langley?", "Willoughby (sometimes called Willoughby-Willowbrook) is Langley's largest and fastest-growing neighbourhood, home to roughly a quarter of the Township's population and its three newest schools, with the Langley Events Centre and Willoughby Town Centre as its amenity hub."),
            ("Is Fort Langley a good area to live, or mainly for visiting?", "Both \u2014 Fort Langley is a genuine residential village as well as a heritage tourist destination, with museums, shops, restaurants, and the Langley Rowing and Paddling Centre along the Fraser River, all within a walkable historic core."),
            ("What recreation options does Langley offer?", "A strong mix: the Langley Events Centre and Willoughby Community Centre for fitness and sport, Campbell Valley and Aldergrove Regional Parks for hiking and horseback riding, and the Aldergrove Credit Union Community Centre's pool and outdoor water park for families."),
         ],
         entertainment=["Cineplex Cinemas Langley", "Restaurants in Fort Langley's historic village and Willoughby Town Centre"]),
    dict(slug='burnaby', name='Burnaby', note='Geographic centre of Metro Vancouver',
         tags=['Metrotown', 'SFU & BCIT', 'SkyTrain Lines'],
         desc="Burnaby sits at the geographic centre of Metro Vancouver, offering everything from Metrotown's high-rise energy to quieter, tree-lined family neighbourhoods, with two major universities (SFU and BCIT) and extensive SkyTrain coverage.",
         schools=["Burnaby South Secondary (IB Diploma Programme &amp; French Immersion)", "Simon Fraser University (Burnaby Mountain campus)", "British Columbia Institute of Technology (BCIT)", "School District 41 Burnaby covers the whole city \u2014 elementary catchment depends on exact address"],
         shopping=["Metropolis at Metrotown \u2014 BC's largest shopping centre, 330+ stores", "The Amazing Brentwood (major grocery, dining, and fitness under one development)", "Crystal Mall (food and grocery)", "Brentwood Town Centre"],
         recreation=["Central Park (90-hectare park with Swangard Stadium, trails, and sports fields)", "Deer Lake Park", "Burnaby Lake Regional Park", "Burnaby Mountain &amp; the SFU Loop Trail", "Confederation Park (miniature railway)"],
         area_faq=[
            ("What's the difference between Metrotown and Brentwood?", "Metrotown is Burnaby's largest and densest town centre, anchored by Metropolis at Metrotown with the greatest volume and variety of shopping. Brentwood, anchored by The Amazing Brentwood, is newer and more curated, with a self-contained mixed-use feel and strong transit connections via the Millennium Line."),
            ("Is Burnaby a good choice for families with university connections?", "Yes \u2014 Burnaby is home to both Simon Fraser University (on Burnaby Mountain) and BCIT, giving the city a genuine university-town character in parts, alongside established family neighbourhoods in North Burnaby and around Deer Lake."),
            ("What green space does Burnaby offer?", "A lot for a city this dense \u2014 Central Park's 90 hectares include a stadium, forest trails, and a pitch-and-putt course; Deer Lake and Burnaby Lake both offer extensive trail networks; and Burnaby Mountain provides hiking with regional views."),
         ],
         entertainment=["Cineplex Cinemas Metropolis at Metrotown", "Cineplex VIP Cinemas &amp; The Rec Room (bowling, arcade, dining) at The Amazing Brentwood"]),
    dict(slug='coquitlam', name='Coquitlam', note='SkyTrain-connected, mountain-backed',
         tags=['Evergreen SkyTrain Line', 'Coquitlam Centre', 'Lafarge Lake'],
         desc="Coquitlam pairs SkyTrain-connected town centres with mountain-backed family neighbourhoods, from Burquitlam's newer towers to the established communities around Lafarge Lake and Westwood Plateau.",
         shopping=["Coquitlam Centre Mall (200+ shops, restaurants, and services)", "Austin Heights, Sunwood Square, and Burquitlam Plaza shopping areas", "Como Lake Village and Pinetree Village"],
         recreation=["City Centre Aquatic Centre", "Westwood Plateau Golf and Country Club", "Lafarge Lake", "Bramble Park and extensive trail networks on Westwood Plateau"],
         area_faq=[
            ("What's Westwood Plateau like as a neighbourhood?", "A master-planned community on Eagle Mountain, home to around 20,000 people, known for golf, hiking, good schools, and a quieter, more established feel than denser parts of Coquitlam \u2014 though it sees noticeably more snow in winter than lower-elevation parts of the city."),
            ("Where's the retail hub of Coquitlam?", "Coquitlam Centre Mall is the heart of it, with 200+ shops and services, complemented by smaller plazas like Austin Heights, Burquitlam Plaza, and Sunwood Square scattered through the surrounding neighbourhoods."),
         ],
         entertainment=["Cineplex Cinemas Coquitlam", "Extensive dining at Coquitlam Centre Mall"]),
    dict(slug='port-coquitlam', name='Port Coquitlam', note='Tri-Cities value',
         tags=['Traboulay PoCo Trail', 'Walkable Downtown', 'West Coast Express'],
         desc="Port Coquitlam offers a genuine community feel and some of the Tri-Cities' better relative value, with family neighbourhoods, a walkable downtown core, and West Coast Express commuter rail access.",
         schools=["School District 43 (Tri-Cities) \u2014 2 public secondary, 5 middle, and 14 elementary schools serve Port Coquitlam specifically"],
         shopping=["Downtown along Shaughnessy Street and McAllister Avenue", "Local shops and a summer farmers' market"],
         recreation=["Port Coquitlam Community Centre (205,000 sq ft \u2014 three arenas, gymnasium, leisure pool, fitness centre)", "Traboulay PoCo Trail (25km loop around the city)", "Lions Park"],
         area_faq=[
            ("What makes Port Coquitlam different from Coquitlam or Port Moody?", "PoCo retains a working-class, community-oriented character from its railway-town roots, with a compact low-rise downtown and generally 10-20% lower home prices than neighbouring Coquitlam \u2014 popular with first-time buyers and young families."),
            ("What's the Traboulay PoCo Trail?", "A 25km trail loop connecting parks, forests, and riverfront around the entire city \u2014 a genuine outdoor amenity residents use regularly, not just a weekend destination."),
         ],
         entertainment=["Restaurants and cafes along downtown Shaughnessy Street"]),
    dict(slug='new-westminster', name='New Westminster', note="BC's original capital",
         tags=['Five SkyTrain Stations', 'Riverfront Living', 'Heritage Character'],
         desc="New Westminster, BC's historic first capital, offers riverfront living, heritage character, and one of the region's more attainable inner-Metro condo markets, backed by five SkyTrain stations across the city.",
         schools=["Royal Columbian Hospital and Douglas College anchor major employment in Sapperton", "New Westminster Schools (SD40) serve the whole city \u2014 confirm your specific catchment"],
         shopping=["Uptown's shops, cafés, and restaurants", "Columbia Street's historic downtown retail"],
         recreation=["Parks and riverfront paths throughout the city", "New Westminster Parks and Recreation programs and facilities"],
         area_faq=[
            ("What's the difference between Uptown and Sapperton in New West?", "Uptown is a vibrant, modern hub with high-rises, shops, and dining, popular with young professionals and downsizers. Sapperton is home to Royal Columbian Hospital, one of BC's major medical centres, giving that neighbourhood a strong healthcare-employment character."),
            ("Why is New Westminster known for good transit?", "It's served by five SkyTrain stations across the Expo and Millennium Lines, unusually good coverage for its size, on top of walkable riverfront paths and a compact, historic street grid."),
         ],
         entertainment=["Restaurants throughout Uptown and along Columbia Street"]),
    dict(slug='vancouver', name='Vancouver', note="BC's largest city",
         tags=['Diverse Neighbourhoods', 'Downtown Core', 'Transit-Connected'],
         desc="Vancouver real estate spans an enormous range, from dense downtown condo towers to established east-side and west-side neighbourhoods, each with its own character, price point, and community feel.",
         area_faq=[
            ("Does Manan work in Vancouver specifically, or mainly the Fraser Valley?", "Manan's core practice is centred in Surrey and the Fraser Valley, but he works with buyers and sellers across the Lower Mainland, including Vancouver. Given how varied Vancouver's dozens of neighbourhoods are, it's worth a direct conversation about the specific area you're considering."),
         ]),
    dict(slug='richmond', name='Richmond', note='Historic charm meets urban energy',
         tags=['Steveston Village', 'Canada Line', 'YVR Access'],
         desc="Richmond pairs the historic charm of Steveston Village with City Centre's urban energy along the Canada Line, plus proximity to YVR and Highway 99 — a diverse, well-connected city on the Fraser River delta.",
         schools=["Steveston-London Secondary (public, grades 8-12)", "School District 38 Richmond serves the whole city \u2014 confirm your specific catchment"],
         shopping=["CF Richmond Centre Mall", "Steveston Village's shops, restaurants, and Fisherman's Wharf fresh seafood"],
         recreation=["Richmond Olympic Oval", "Steveston Community Centre (pool, library, martial arts centre)", "Garry Point Park &amp; Britannia Shipyards Park (waterfront)", "47.5km perimeter cycling/walking trail around the whole city"],
         area_faq=[
            ("What makes Steveston different from the rest of Richmond?", "It's a historic fishing village with a genuinely walkable waterfront core \u2014 Fisherman's Wharf, the Britannia Heritage Shipyards, and a 1km boardwalk \u2014 alongside newer townhomes and condos in Steveston North, giving it a distinct small-village feel within the larger city."),
            ("What recreation does Richmond offer beyond Steveston?", "The Richmond Olympic Oval is a major legacy facility from the 2010 Games, and the city's 47.5km perimeter trail is popular for cycling and walking around the entire island."),
         ],
         entertainment=["CF Richmond Centre dining", "Fisherman's Wharf fresh seafood and Steveston Village restaurants"]),
    dict(slug='port-moody', name='Port Moody', note='City of the Arts',
         tags=['Rocky Point Park', 'Brewers Row', 'Two SkyTrain Stations'],
         desc="Port Moody wraps the end of Burrard Inlet with Rocky Point Park's waterfront, the craft-brewery scene along Brewers Row, and mountain-side family neighbourhoods served by two SkyTrain stations.",
         schools=["SD43 covers Port Moody \u2014 2 secondary, 2 middle, and 6 elementary schools citywide"],
         recreation=["Rocky Point Park (recreational pier, outdoor pool, spray park, Shoreline Trail, kayak/paddleboard rentals)", "Port Moody Recreation Complex (weight room, two gymnasiums, two arenas, curling centre)", "Buntzen Lake and Belcarra Regional Park nearby", "Port Moody Station Museum &amp; Arts Centre"],
         area_faq=[
            ("What is Port Moody's Rocky Point Park known for?", "It's the city's best-known park \u2014 a recreational pier on Burrard Inlet, an outdoor pool, spray park, skateboard park, and the Shoreline Trail, plus kayak and paddleboard rentals and waterfront dining."),
            ("What outdoor destinations are near Port Moody beyond the city itself?", "Buntzen Lake and Belcarra Regional Park are both close by for hiking and swimming, and Golden Ears Provincial Park is reachable via the Lougheed Highway corridor through Coquitlam and Pitt Meadows."),
         ],
         entertainment=["Several craft breweries along Brewers Row", "Waterfront dining near Rocky Point Park"],
         shopping=["Suter Brook Village shops"]),
    dict(slug='pitt-meadows', name='Pitt Meadows', note='Rivers, dykes & farmland',
         tags=['West Coast Express', 'Golden Ears Bridge', 'Dyke Trails'],
         desc="Rivers, dykes, and farmland frame one of the region's more liveable small cities, with West Coast Express commuter rail, Golden Ears Bridge access, and extensive dyke trail networks for an outdoor-oriented lifestyle.",
         recreation=["West Coast Express station", "Extensive dyke trail network along the Pitt and Fraser Rivers"],
         entertainment=["Restaurants along the Harris Road commercial strip"],
         shopping=["Pitt Meadows' town centre shops along Harris Road"]),
    dict(slug='abbotsford', name='Abbotsford', note="'City in the Country'",
         tags=['Mountain Views', 'University Town', 'International Airport'],
         desc="Known as the 'City in the Country,' Abbotsford offers mountain views and relatively more affordable housing than Vancouver, alongside a growing urban centre, University of the Fraser Valley, and its own international airport.",
         schools=["Abbotsford Senior Secondary", "Robert Bateman Secondary", "University of the Fraser Valley (UFV)", "SD34 Abbotsford runs 46 schools \u2014 note that popular schools like Yale and Robert Bateman restrict non-catchment enrolment when over capacity, so confirm your specific catchment"],
         shopping=["Seven Oaks Shopping Centre", "Highstreet Shopping Centre", "Historic downtown shopping district"],
         recreation=["Abbotsford Recreation Centre (pool, ice rink, gym, weight room, indoor track)", "Matsqui Recreation Centre", "Mill Lake Park (walking trails, playgrounds, MSA Museum nearby)", "Sumas Mountain &amp; Glen Valley (hiking, biking)"],
         area_faq=[
            ("Does it matter exactly where I buy in Abbotsford for school access?", "Yes, increasingly so \u2014 the school district has restricted non-catchment requests for over-capacity schools like Yale and Robert Bateman, meaning your specific address determines eligibility for these popular schools rather than general area proximity."),
            ("What recreation does Abbotsford offer?", "Two full recreation centres (Abbotsford and Matsqui) with pools, ice rinks, and fitness facilities, plus Mill Lake Park as a central outdoor gathering spot and Sumas Mountain for hiking and biking."),
         ],
         entertainment=["Restaurants at Seven Oaks and Highstreet Shopping Centres", "Historic downtown dining"]),
    dict(slug='maple-ridge', name='Maple Ridge', note='Mountain scenery, family amenities',
         tags=['Golden Ears Park', 'Mountain Scenery', 'Growing Town Centre'],
         desc="Maple Ridge offers mountain scenery via Golden Ears Provincial Park, strong family amenities, and a growing urban town centre, while maintaining a relatively relaxed, small-community feel.",
         recreation=["Golden Ears Provincial Park (55,000 hectares, 65km of hiking/biking/horseback trails, Alouette Lake)", "West Coast Express commuter rail into Vancouver"],
         area_faq=[
            ("What makes Golden Ears Provincial Park a draw for Maple Ridge residents?", "It's one of the largest provincial parks accessible from Metro Vancouver \u2014 55,000 hectares with 65km of trails, plus Alouette Lake for swimming and picnicking, all under an hour from downtown Vancouver."),
         ],
         entertainment=["Restaurants in Maple Ridge's town centre"],
         shopping=["Haney Place Mall and downtown Maple Ridge shops"]),
    dict(slug='mission', name='Mission', note='North bank of the Fraser',
         tags=['West Coast Express', 'Heritage Downtown', 'River Views'],
         desc="Mission is a charming community on the north bank of the Fraser River, offering a small-town atmosphere with excellent transit connections into Metro Vancouver via West Coast Express.",
         schools=["University of the Fraser Valley (UFV) has a Mission campus location"],
         area_faq=[
            ("What's the commute like from Mission into Metro Vancouver?", "West Coast Express commuter rail runs from Mission City Station into downtown Vancouver, giving Mission genuine rail transit access despite being one of the furthest-out Fraser Valley communities."),
         ],
         entertainment=["Restaurants in downtown Mission"],
         shopping=["Downtown Mission's shops along First Avenue"]),
    dict(slug='chilliwack', name='Chilliwack', note='Mountains, rivers & lakes',
         tags=['Outdoor Recreation', 'Agricultural Hub', 'Growing Community'],
         desc="Chilliwack is surrounded by mountains, rivers, and lakes, offering exceptional outdoor recreation and increasingly attractive relative affordability for buyers priced out of markets closer to Vancouver.",
         schools=["University of the Fraser Valley (UFV) Chilliwack campus", "SD33 Chilliwack schools serve the city"],
         shopping=["Cottonwood Shopping Mall", "Chilliwack Landing (the city's recreational and commercial heart)"],
         recreation=["Cheam Leisure Centre", "Chilliwack Landing Leisure Centre (aquatic centre, fitness centre, spray park, skateboard facility)", "Chilliwack Museum (National Historic Site)", "Chilliwack Cultural Centre", "Nine golf courses in the area, plus hiking, biking, kayaking, and whitewater rafting nearby"],
         area_faq=[
            ("What outdoor recreation is Chilliwack known for?", "It's genuinely exceptional \u2014 nine golf courses, hiking and biking in the surrounding Cascade Mountains, kayaking and whitewater rafting, and sport fishing for salmon and sturgeon on the Fraser River, all within city limits or a short drive."),
            ("Does Chilliwack have post-secondary options?", "Yes \u2014 University of the Fraser Valley has a dedicated Chilliwack campus, alongside the district's public school system (SD33)."),
         ],
         entertainment=["Restaurants at Cottonwood Shopping Mall and Chilliwack Landing"]),
    dict(slug='hope', name='Hope', note='Gateway to the Fraser Canyon',
         tags=['Mountain Gateway', 'Outdoor Recreation', 'Affordable Living'],
         desc="Hope is the gateway to the Fraser Canyon and BC interior, offering spectacular mountain scenery, more affordable real estate, and a tight-knit community feel at the eastern edge of the Fraser Valley.",
         schools=["University of the Fraser Valley has a Hope-area campus location, within walking distance of downtown"],
         shopping=["Downtown Hope's shops and cafés, walkable from most residential areas"],
         recreation=["Hope Recreation Centre (Dan Sharrers Aquatic Centre, arena, weight/cardio rooms)", "Hope Golf Club", "Sasquatch Caves and Flood Falls nearby", "Extensive river and mountain trail access"],
         area_faq=[
            ("Is downtown Hope walkable?", "Yes \u2014 shops, schools, and the UFV campus location are all within walking distance of the downtown core, giving Hope a genuine small-town, walkable character despite its remote-feeling mountain setting."),
         ],
         entertainment=["Cafes and restaurants throughout walkable downtown Hope"]),
    dict(slug='harrison-hot-springs', name='Harrison Hot Springs', note='Resort-style living',
         tags=['Hot Springs Resort', 'Harrison Lake', 'Year-Round Tourism'],
         desc="Harrison Hot Springs offers resort-style living with natural hot springs, stunning Harrison Lake, and the charm of a small year-round tourism destination at the edge of the Fraser Valley.",
         recreation=["Natural hot springs and public pools", "Harrison Lake (beach, boating)", "Waterpark and artisan shops downtown"],
         entertainment=["Resort dining and artisan cafes throughout the downtown waterpark area"],
         shopping=["Artisan and gift shops throughout the downtown waterpark area"]),

    # -------- Surrey neighbourhoods (expanded) --------
    dict(slug='guildford', name='Guildford', note='Retail hub, established homes',
         tags=['Guildford Town Centre', 'Established Homes', 'Central Surrey'],
         desc="Guildford is anchored by Guildford Town Centre and offers a mix of established single-family homes, townhomes, and newer condo development in a central, well-connected part of Surrey.",
         schools=["School District 36 Surrey (50+ elementary and nearly 30 secondary schools district-wide)", "Confirm your specific catchment with SD36 \u2014 zoning varies by subdivision"],
         shopping=["Guildford Town Centre (one of BC's largest shopping malls)", "Guildford's restaurant and café strip along 104 Avenue"],
         recreation=["Guildford Recreation Centre (pool, gym, sauna, indoor track, attached library)", "Fraser Heights Recreation Centre (tennis courts, sports fields)", "Tynehead Regional Park", "Surrey Bend Regional Park (Fraser River access)", "Green Timbers Urban Forest nearby"],
         area_faq=[
            ("What makes Guildford a convenient place to live?", "Guildford Town Centre \u2014 one of BC's largest shopping malls \u2014 sits at its centre, with two full recreation centres (Guildford and Fraser Heights), regional parks, and strong highway access to Surrey City Centre and Langley."),
            ("What recreation is available in Guildford?", "The Guildford Recreation Centre has a pool, gym, sauna, and indoor track and is attached to the Guildford library branch. Nearby Tynehead and Surrey Bend Regional Parks add Fraser River access and natural trails."),
            ("Is Guildford good for families?", "Yes \u2014 it's one of Surrey's busiest and most established areas, with a wide age range of housing stock, strong transit connections, and easy access to Green Timbers Urban Forest and Tynehead Regional Park for outdoor time."),
         ],
         entertainment=["Landmark Cinemas 12 Guildford", "Restaurants and food court at Guildford Town Centre"]),
    dict(slug='east-newton', name='East Newton', note='Family homes near amenities',
         tags=['Family-Friendly', 'Central Newton', 'Established Streets'],
         desc="East Newton offers a mix of single-family homes and townhomes close to Newton's shopping and recreation amenities, appealing to families wanting central Surrey access at good relative value.",
         recreation=["Bear Creek Park and Newton Recreation Centre both within reach"],
         entertainment=["Restaurants along the nearby Scott Road corridor"],
         shopping=["King's Cross Shopping Centre nearby"]),
    dict(slug='west-newton', name='West Newton', note='Diverse, central Surrey',
         tags=['Central Location', 'Diverse Community', 'Established Homes'],
         desc="West Newton is a diverse, densely built part of Surrey with a mix of older single-family homes and newer townhome and condo infill close to Scott Road and King George Boulevard.",
         shopping=["Scott Road corridor's South Asian grocers, sweet shops, and jewellers"],
         entertainment=["South Asian restaurants and cafes along Scott Road, within West Newton itself"]),
    dict(slug='east-clayton', name='East Clayton', note='Newer townhomes, walkable design',
         tags=['Newer Townhomes', 'Walkable Streets', 'Master-Planned'],
         desc="East Clayton is a newer, master-planned pocket of Surrey known for walkable street grids, laneway homes, and modern townhome development.",
         recreation=["Clayton Community Centre nearby"],
         entertainment=["Restaurants at nearby Willowbrook Shopping Centre (Langley)"],
         shopping=["Willowbrook Shopping Centre nearby (Langley)"]),
    dict(slug='clayton', name='Clayton', note='Newer master-planned community',
         tags=['Newer Townhomes', 'Master-Planned', 'Near Langley'],
         desc="Clayton is one of Surrey's newer master-planned communities, known for modern townhome and single-family development, walking trails, and proximity to the Langley border.",
         recreation=["Clayton Community Centre (arts, recreation &amp; library hub, opened at 7155 187A Street)"],
         entertainment=["Cafes and restaurants at Clayton Community Centre's surrounding retail"],
         shopping=["Willowbrook Shopping Centre nearby"]),
    dict(slug='fraser-heights', name='Fraser Heights', note='Forested, family-oriented',
         tags=['Forested Setting', 'Fraser River Views', 'Top-Rated Schools'],
         desc="Fraser Heights sits along the Fraser River in a forested, hillside setting, known for larger lots, well-regarded schools, and easy access to Highway 1.",
         schools=["Fraser Heights Secondary (Science Academy partnership with SFU, AP courses, ~1,400 students)", "SD36 Surrey elementary schools serve the area \u2014 confirm your specific catchment"],
         shopping=["Guildford Town Centre (5 minutes away)", "Local restaurants, cafés, and bars along the Guildford corridor"],
         recreation=["Fraser Heights Recreation Centre (tennis courts, sports fields, weight room, fitness studio)", "Fraser Heights Youth Park (skate park)", "Green spaces and trails throughout the neighbourhood"],
         area_faq=[
            ("Is Fraser Heights a good school catchment?", "Fraser Heights Secondary is well regarded, with a two-year Science Academy pathway run in partnership with SFU, Advanced Placement courses, and over 50 student clubs \u2014 it sits right next to the neighbourhood's recreation centre."),
            ("What's it like living in Fraser Heights day-to-day?", "It's been described as an 'island within a city' \u2014 self-contained with its own recreation centre, healthcare services, and gated communities, while still being five minutes from Guildford Town Centre for shopping and dining."),
            ("What housing types are available in Fraser Heights?", "Primarily detached single-family homes on larger lots, with some townhomes and condos. It's popular with families wanting more space and forested surroundings while staying within Surrey and close to Highway 1."),
         ],
         entertainment=["Restaurants at Guildford Town Centre, five minutes away"]),
    dict(slug='panorama-ridge', name='Panorama Ridge', note='Elevated views, established homes',
         tags=['Elevated Views', 'Established Homes', 'Family Neighbourhood'],
         desc="Panorama Ridge is an established, family-oriented Surrey neighbourhood known for elevated lots with valley views and a quiet, residential feel.",
         recreation=["Close to Bear Creek Park and Newton's recreation facilities"],
         entertainment=["Restaurants in nearby Newton and Bear Creek"],
         shopping=["Newton Town Centre nearby"]),
    dict(slug='sullivan-heights', name='Sullivan Heights', note='Established community near Cloverdale',
         tags=['Established Community', 'Near Cloverdale', 'Family Homes'],
         desc="Sullivan Heights is an established South Surrey-area community bordering Cloverdale, offering a mix of single-family homes and a quiet, residential feel.",
         shopping=["Willowbrook and Central City Shopping Centres nearby via Cloverdale"],
         entertainment=["Restaurants in nearby Cloverdale's historic downtown"]),
    dict(slug='grandview-heights', name='Grandview Heights', note="South Surrey's newest premium community",
         tags=['Newer Custom Homes', 'South Surrey', 'Walking Trails'],
         desc="Grandview Heights is South Surrey's newest premium community, featuring modern custom homes and newer townhomes on generous lots, with walking trails and mountain and valley views.",
         schools=["Grandview Heights Secondary", "Rosemary Heights Elementary", "SD36 Surrey elementary schools serve the area \u2014 confirm your specific catchment"],
         shopping=["Grandview Corners", "Morgan Crossing (nearby)"],
         recreation=["Grandview Heights Aquatic Centre (indoor pool, weight room, drop-in aquatic fitness)", "Extensive walking trails throughout the newer subdivisions"],
         area_faq=[
            ("Why is Grandview Heights considered a premium South Surrey market?", "It's one of the most active newer-construction luxury markets in the Lower Mainland, with modern custom homes on generous lots, mountain and valley views from the Highway 99 corridor lots, and strong demand from move-up buyers and Vancouver expats."),
            ("What schools serve Grandview Heights?", "Grandview Heights Secondary and Rosemary Heights Elementary serve much of the area, with additional SD36 Surrey elementary schools depending on exact address \u2014 confirm your specific catchment with the district."),
            ("What amenities are nearby?", "Grandview Corners and neighbouring Morgan Crossing cover everyday shopping and dining, and the Grandview Heights Aquatic Centre offers an indoor pool and fitness facilities within the neighbourhood."),
         ],
         entertainment=["Restaurants at Grandview Corners and nearby Morgan Crossing"]),
    dict(slug='morgan-creek', name='Morgan Creek', note='Golf course community, estate homes',
         tags=['Golf Course Community', 'Estate Homes', 'Gated Enclaves'],
         desc="Morgan Creek is a South Surrey estate community built around the Morgan Creek Golf Course, known for large lots, custom builds, and a strong sense of community.",
         schools=["Morgan Elementary", "Rosemary Heights Elementary", "Grandview Heights Secondary", "SouthRidge (private K-12)"],
         shopping=["Morgan Crossing", "Grandview Corners nearby"],
         recreation=["Morgan Creek Golf Course", "Walking trails throughout the community"],
         area_faq=[
            ("What defines Morgan Creek as a community?", "It's a South Surrey estate community built around the private Morgan Creek Golf Course, with a gated section commanding the highest values and backing onto the golf course adding a meaningful premium."),
            ("What schools serve Morgan Creek?", "Morgan Elementary, Rosemary Heights Elementary, and Grandview Heights Secondary are the public options, and SouthRidge offers K-12 private education within the broader area."),
            ("Is Morgan Creek mostly estate homes, or is there other housing?", "It's known primarily for larger custom and estate homes, though the surrounding area includes townhomes and condos at more accessible price points \u2014 Morgan Creek itself skews toward larger detached lots."),
         ],
         entertainment=["Dining at Morgan Crossing"]),
    dict(slug='elgin-chantrell', name='Elgin Chantrell', note='Acreage estates, rural feel',
         tags=['Acreage Properties', 'Equestrian Estates', 'Rural Feel'],
         desc="Elgin Chantrell is a quiet, rural-feel enclave in South Surrey known for large acreage properties, equestrian estates, and custom homes with easy access to Highway 99 and the US border.",
         schools=["Elgin Park Secondary", "SD36 Surrey elementary schools serve the area \u2014 confirm your specific catchment"],
         shopping=["Ocean Park and Semiahmoo Shopping Centres nearby"],
         recreation=["Equestrian facilities throughout the acreage properties", "Crescent Beach and Blackie Spit nearby for waterfront access"],
         area_faq=[
            ("What kind of properties are typical in Elgin Chantrell?", "Half-acre to multi-acre estate properties, many with equestrian setups, custom homes, and a genuinely rural feel despite being within Surrey and close to Highway 99 and the US border."),
            ("Is Elgin Chantrell close to amenities despite feeling rural?", "Yes \u2014 it's a short drive to Ocean Park and Semiahmoo Shopping Centres and to Crescent Beach, so the rural feel doesn't come at the cost of everyday convenience."),
         ],
         entertainment=["Restaurants at nearby Ocean Park and Semiahmoo Shopping Centres"]),
    dict(slug='sunnyside', name='Sunnyside', note='Established homes near White Rock',
         tags=['Coastal Proximity', 'Established Homes', 'Near White Rock'],
         desc="Sunnyside is an established South Surrey neighbourhood close to White Rock's beaches and amenities, offering a mix of single-family homes and newer infill.",
         schools=["Elgin Park Secondary serves much of the area \u2014 confirm your specific catchment with SD36 Surrey"],
         shopping=["Semiahmoo Shopping Centre nearby"],
         recreation=["Close proximity to White Rock's beach and promenade", "South Surrey Athletic Park nearby"],
         entertainment=["Restaurants along White Rock's Marine Drive promenade, nearby"]),
    dict(slug='ocean-park', name='Ocean Park', note='Village feel near the beach',
         tags=['Village Feel', 'Beach Proximity', 'Heritage Character'],
         desc="Ocean Park is a mature, established South Surrey neighbourhood with a village feel, tree-lined streets, heritage character, and proximity to the beach.",
         schools=["Elgin Park Secondary", "Ocean Cliff Elementary", "SD36 Surrey elementary schools serve the area \u2014 confirm your specific catchment"],
         shopping=["Ocean Park Shopping Centre"],
         recreation=["Ocean Park beach access", "Crescent Beach and Blackie Spit nearby"],
         area_faq=[
            ("What makes Ocean Park feel different from other South Surrey neighbourhoods?", "Its village atmosphere \u2014 tree-lined streets, heritage character, and larger lots \u2014 combined with proximity to the beach, gives it a quieter, more established coastal feel than newer South Surrey developments."),
         ],
         entertainment=["Cafes and restaurants at Ocean Park Shopping Centre"]),
    dict(slug='crescent-beach', name='Crescent Beach', note='Waterfront village lifestyle',
         tags=['Waterfront Village', 'Beach Lifestyle', 'Boardwalk'],
         desc="Crescent Beach is a small waterfront village in South Surrey known for its boardwalk, beach lifestyle, and tight-knit community feel.",
         recreation=["Crescent Beach boardwalk", "Blackie Spit Park (birdwatching, waterfront trails)", "Crescent Beach Marina"],
         area_faq=[
            ("What kind of homes are available in Crescent Beach?", "A mix of smaller heritage character homes and newer builds on compact lots, trading premium beach proximity for smaller lot sizes compared to nearby Elgin Chantrell or Morgan Creek."),
         ],
         entertainment=["Waterfront cafes and restaurants along the Crescent Beach boardwalk"],
         shopping=["A small strip of local shops along the boardwalk"]),
    dict(slug='king-george-corridor', name='King George Corridor', note='Transit-connected, mixed commercial',
         tags=['Transit Access', 'Commercial Mix', 'Central Location'],
         desc="The King George Corridor runs through the heart of Surrey, offering strong transit access along with a mix of residential and commercial properties.",
         shopping=["Central City Shopping Centre and Surrey City Centre amenities along the corridor"],
         entertainment=["Restaurants along the King George corridor into City Centre"]),
    dict(slug='port-kells', name='Port Kells', note='Rural-residential, industrial proximity',
         tags=['Industrial Proximity', 'Rural-Residential Mix', 'Highway Access'],
         desc="Port Kells is a rural-residential pocket of North Surrey bordering major industrial land, offering larger lots and easy highway access.",
         shopping=["Guildford and Cloverdale shopping within a short drive"],
         entertainment=["Restaurants in nearby Cloverdale and Guildford"]),
    dict(slug='bridgeview', name='Bridgeview', note='Affordable entry, riverfront industrial',
         tags=['Industrial Access', 'Affordable Entry', 'Riverfront'],
         desc="Bridgeview is a North Surrey neighbourhood along the Fraser River, offering some of the more affordable residential entry points in the city alongside nearby industrial land.",
         recreation=["Bridgeview Community Centre"],
         entertainment=["Restaurants in nearby Guildford"],
         shopping=["Guildford Town Centre nearby"]),
    dict(slug='bolivar-heights', name='Bolivar Heights', note='Established North Surrey homes',
         tags=['Established Homes', 'North Surrey', 'Central Location'],
         desc="Bolivar Heights is an established North Surrey neighbourhood offering a mix of older single-family homes with good access to Scott Road and transit.",
         shopping=["Scott Road corridor shops nearby"],
         entertainment=["Restaurants along the nearby Scott Road corridor"]),
    dict(slug='cedar-hills', name='Cedar Hills', note='Established homes, transit access',
         tags=['North Surrey', 'Established Homes', 'Transit Access'],
         desc="Cedar Hills is a North Surrey neighbourhood of established single-family homes with convenient access to transit and the Guildford area.",
         shopping=["Guildford Town Centre nearby"],
         entertainment=["Restaurants at nearby Guildford Town Centre"]),
    dict(slug='royal-heights', name='Royal Heights', note='Elevated views, North Surrey',
         tags=['Elevated Views', 'North Surrey', 'Established Homes'],
         desc="Royal Heights is a North Surrey neighbourhood known for elevated lots with city and mountain views and a mix of established and newer homes.",
         shopping=["North Surrey shopping via Scott Road corridor"],
         entertainment=["Restaurants along the nearby Scott Road corridor"]),
    dict(slug='johnston-heights', name='Johnston Heights', note='Central Surrey, near Guildford',
         tags=['Central Surrey', 'Established Homes', 'Near Guildford'],
         desc="Johnston Heights is a central Surrey neighbourhood of established homes bordering Guildford, offering good access to shopping and transit.",
         shopping=["Guildford Town Centre nearby"],
         recreation=["Guildford and Fraser Heights Recreation Centres both within reach"],
         entertainment=["Restaurants and food court at nearby Guildford Town Centre"]),
    dict(slug='green-timbers', name='Green Timbers', note='Urban forest, central Surrey',
         tags=['Green Timbers Urban Forest', 'Central Surrey', 'Established Homes'],
         desc="Green Timbers takes its name from the adjacent urban forest and park, offering established homes in a central, well-treed part of Surrey.",
         recreation=["Green Timbers Urban Forest (trails through second-growth forest)"],
         entertainment=["Restaurants at nearby Guildford Town Centre"],
         shopping=["Guildford Town Centre nearby"]),
    dict(slug='tynehead', name='Tynehead', note='Semi-rural, larger lots',
         tags=['Tynehead Regional Park', 'Semi-Rural', 'Larger Lots'],
         desc="Tynehead is a semi-rural pocket of Surrey bordering Tynehead Regional Park, known for larger lots and a quieter, nature-oriented setting.",
         recreation=["Tynehead Regional Park (Fraser River access, off-leash dog area, salmon-bearing streams)"],
         entertainment=["Restaurants at nearby Guildford Town Centre"],
         shopping=["Guildford Town Centre nearby"]),
    dict(slug='hazelmere', name='Hazelmere', note='Rural acreage, golf courses',
         tags=['Rural Acreage', 'Golf Courses', 'Agricultural Land'],
         desc="Hazelmere is a rural South Surrey area known for acreage properties, several golf courses, and agricultural land near the US border.",
         recreation=["Several golf courses in the surrounding acreage land"],
         entertainment=["Restaurants in nearby South Surrey and Semiahmoo Shopping Centre"],
         shopping=["Semiahmoo Shopping Centre nearby"]),
    dict(slug='campbell-heights', name='Campbell Heights', note="Surrey's premier industrial park",
         tags=['Industrial Park', 'Investment Potential', 'Highway Access'],
         desc="Campbell Heights is Surrey's premier industrial park, home to modern large-format warehouses and manufacturing operations with strong demand and highway access.",
         shopping=["Primarily industrial; nearby South Surrey shopping via Highway 99"],
         entertainment=["Limited on-site dining; South Surrey restaurants a short drive away"]),
    dict(slug='chimney-hill', name='Chimney Hill', note='Established Newton-area homes',
         tags=['Established Homes', 'Newton Area', 'Family Neighbourhood'],
         desc="Chimney Hill is an established, family-oriented neighbourhood in the Newton area of Surrey with a mix of single-family homes.",
         recreation=["Newton Recreation Centre and Bear Creek Park both nearby"],
         entertainment=["Restaurants in nearby Newton"],
         shopping=["Newton Town Centre nearby"]),
    dict(slug='bear-creek', name='Bear Creek', note='Parkside, central Surrey',
         tags=['Bear Creek Park', 'Central Surrey', 'Family Amenities'],
         desc="Bear Creek is a central Surrey neighbourhood named for the adjacent Bear Creek Park, offering family amenities and established housing.",
         recreation=["Bear Creek Park (152 acres \u2014 outdoor pool, water park, mini golf, miniature train, Bear Creek Gardens, Surrey Art Gallery)"],
         area_faq=[
            ("What can families do at Bear Creek Park?", "A lot \u2014 a free outdoor pool with diving board, a water spray park, mini golf, the well-known Bear Creek Miniature Train, an exercise circuit and running track, plus the Bear Creek Gardens and Surrey Art Gallery, all within one 152-acre park."),
         ],
         entertainment=["Restaurants in nearby Guildford and Newton"],
         shopping=["Guildford Town Centre nearby"]),
    dict(slug='strawberry-hill', name='Strawberry Hill', note='Central location, established homes',
         tags=['Central Location', 'Established Homes', 'Newton Proximity'],
         desc="Strawberry Hill is a central Surrey neighbourhood bordering Newton, offering established homes and convenient access to shopping and transit.",
         shopping=["Strawberry Hill Shopping Centre", "Newton Town Centre nearby"],
         entertainment=["Restaurants at Strawberry Hill Shopping Centre and nearby Newton"]),
    dict(slug='south-westminster', name='South Westminster', note='Riverfront industrial, North Surrey',
         tags=['Riverfront Industrial', 'North Surrey', 'Fraser River'],
         desc="South Westminster is a North Surrey area along the Fraser River with a strong industrial and logistics presence alongside pockets of residential property.",
         shopping=["North Surrey shopping via the King George corridor"],
         entertainment=["Restaurants along the nearby Scott Road corridor"]),

    # -------- Langley neighbourhoods (expanded) --------
    dict(slug='fort-langley', name='Fort Langley', note='Historic riverside village',
         tags=['Historic Village', 'National Historic Site', 'Fraser River'],
         desc="Fort Langley is a historic riverside village known for its national historic site, boutique shops, and charming small-town atmosphere along the Fraser River.",
         shopping=["Fort Langley's historic village core \u2014 museums, boutique shops, art galleries, restaurants"],
         recreation=["Fort Langley National Historic Site (Hudson's Bay Company fort)", "Langley Rowing and Paddling Centre", "Fort Langley Library", "Riverfront parks and trails along the Fraser River"],
         area_faq=[
            ("Is Fort Langley just a tourist spot, or a real place to live?", "Both \u2014 it's a genuine residential village as well as a heritage destination. Residents get walkable access to museums, shops, and the Fraser River waterfront, alongside the tourist traffic that comes with being the birthplace of BC."),
         ],
         entertainment=["Cafes, pubs, and restaurants throughout Fort Langley's historic village core"]),
    dict(slug='willoughby', name='Willoughby', note="Langley's fastest-growing area",
         tags=['Fast-Growing', 'New Townhomes', 'SkyTrain Extension'],
         desc="Willoughby is one of the fastest-growing communities in the Fraser Valley, with new townhome and condo development serving a rapidly expanding population and benefiting from the SkyTrain extension to Langley.",
         schools=["Lynn Fripps Elementary", "Richard Bulpitt Elementary", "Yorkson Creek Middle School (Langley's three newest schools, all opened in this area since 2012)"],
         shopping=["Willoughby Town Centre", "The Township of Langley Civic Centre (council chambers, Muriel Arnason Library)"],
         recreation=["Langley Events Centre", "Willoughby Community Centre (fitness studio, weight room, triple gymnasium)", "Willoughby Community Park"],
         area_faq=[
            ("Why is Willoughby considered Langley's top growth area?", "It's the Township's largest neighbourhood by population \u2014 roughly a quarter of all Langley Township residents \u2014 with the most new home construction, the newest schools, and the greatest concentration of shopping and dining in the Township."),
            ("What schools were built to serve Willoughby's growth?", "Lynn Fripps Elementary (2012), Richard Bulpitt Elementary (2013), and Yorkson Creek Middle School (2014) were all built specifically to serve the area's rapid population growth, with further expansions announced since."),
         ],
         entertainment=["Restaurants and cafes at Willoughby Town Centre"]),
    dict(slug='walnut-grove', name='Walnut Grove', note='Established, family-friendly',
         tags=['Established Community', 'Parks & Trails', 'Family-Friendly'],
         desc="Walnut Grove is an established, family-friendly Langley community known for its parks, trails, and mix of single-family homes and townhomes.",
         recreation=["Walnut Grove's extensive park and trail network", "Community centres and recreation facilities throughout the neighbourhood"],
         area_faq=[
            ("What makes Walnut Grove a popular family choice?", "It's known for strong schools, established parks and trails, and safe, residential streets, with easy highway access for commuting to Surrey, Burnaby, or Vancouver \u2014 a favourite among families prioritizing stability over newer construction."),
         ],
         entertainment=["Restaurants in nearby Langley City and Willowbrook"],
         shopping=["Walnut Grove Shopping Centre"]),
    dict(slug='langley-city', name='Langley City', note='Compact, walkable downtown',
         tags=['Compact Downtown', 'Transit Access', 'Walkable'],
         desc="Langley City offers a compact, walkable downtown core with transit access and a mix of older and newer condo and townhome development.",
         shopping=["Langley City's downtown \u2014 600+ unique shops and services"],
         recreation=["Langley Sportsplex", "Douglas Park and over 300 acres of city parkland", "Cascades Casino", "Annual Langley Good Times Cruise-In"],
         area_faq=[
            ("How is Langley City different from Langley Township?", "Langley City is its own separate, smaller municipality \u2014 a compact, walkable downtown with 600+ shops and services and over 300 acres of parkland \u2014 while the Township surrounding it covers Willoughby, Fort Langley, Walnut Grove, and the other larger, more suburban communities."),
         ],
         entertainment=["600+ shops and restaurants throughout Langley City's walkable downtown", "Cascades Casino entertainment"]),
    dict(slug='brookswood', name='Brookswood', note='Treed lots, semi-rural feel',
         tags=['Treed Lots', 'Established Homes', 'Semi-Rural Feel'],
         desc="Brookswood is known for larger, treed lots and a semi-rural feel within Langley, popular with buyers wanting more space and privacy.",
         recreation=["Close to Langley City's Douglas Park and Langley Sportsplex"],
         entertainment=["Restaurants in nearby Langley City"],
         shopping=["Langley City shops nearby"]),
    dict(slug='murrayville', name='Murrayville', note='Village feel, historic character',
         tags=['Village Feel', 'Historic Character', 'Established Homes'],
         desc="Murrayville offers a village feel with historic character, established homes, and a small commercial core within the Township of Langley.",
         shopping=["Murrayville's small commercial core, including nearby schools, parks, and a public library"],
         area_faq=[
            ("What's the appeal of Murrayville specifically?", "Everyday ease in a quiet, walkable setting \u2014 nearby schools, parks, a public library, and a recreation centre, without the density of Willoughby or Langley City."),
         ],
         entertainment=["Cafes and restaurants in Murrayville's small commercial core"]),
    dict(slug='aldergrove', name='Aldergrove', note='Affordable entry, small-town feel',
         tags=['Border Proximity', 'Affordable Entry', 'Small-Town Feel'],
         desc="Aldergrove offers a more affordable entry point into the Langley market with a small-town feel and proximity to the US border.",
         recreation=["Aldergrove Regional Park (hiking, birdwatching)", "Greater Vancouver Zoo", "Aldergrove Credit Union Community Centre (pool and outdoor water park)", "Aldergrove Athletic Park"],
         area_faq=[
            ("What outdoor amenities does Aldergrove offer?", "A lot for an affordable-entry community \u2014 Aldergrove Regional Park for hiking and birdwatching, the Greater Vancouver Zoo, and the Aldergrove Credit Union Community Centre, which includes both an indoor pool and an outdoor water park."),
         ],
         entertainment=["Restaurants along Aldergrove's main commercial strip"],
         shopping=["Aldergrove's main commercial strip"]),
    dict(slug='willowbrook', name='Willowbrook', note='Shopping hub, central Langley',
         tags=['Shopping Hub', 'Central Langley', 'Established Homes'],
         desc="Willowbrook is a central Langley area anchored by Willowbrook Shopping Centre, offering established homes with convenient access to amenities.",
         shopping=["Willowbrook Shopping Centre"],
         entertainment=["Restaurants and food court at Willowbrook Shopping Centre"]),
    dict(slug='yorkson', name='Yorkson', note='Newer development, Willoughby area',
         tags=['Newer Development', 'Family Homes', 'Willoughby Area'],
         desc="Yorkson is a newer residential pocket within the Willoughby area of Langley, offering modern single-family and townhome development.",
         recreation=["Yorkson Community Parks North and South", "Willoughby Community Centre and Langley Events Centre nearby"],
         entertainment=["Restaurants at nearby Willoughby Town Centre"],
         shopping=["Willoughby Town Centre nearby"]),
    dict(slug='salmon-river', name='Salmon River', note='Rural acreage, equestrian properties',
         tags=['Rural Acreage', 'Agricultural Land', 'Equestrian Properties'],
         desc="Salmon River is a rural area of Langley known for acreage properties, agricultural land, and equestrian estates.",
         recreation=["Salmon River itself (a Fraser River tributary running through the district)"],
         entertainment=["Restaurants in nearby Aldergrove and Langley City"],
         shopping=["Aldergrove's commercial strip nearby"]),
    dict(slug='campbell-valley', name='Campbell Valley', note='Regional park, rural estates',
         tags=['Regional Park', 'Rural Estates', 'Nature Access'],
         desc="Campbell Valley is a rural Langley area bordering Campbell Valley Regional Park, offering larger estate properties and easy access to nature.",
         recreation=["Campbell Valley Regional Park (hiking, horseback riding, picnicking)"],
         entertainment=["Restaurants in nearby Langley City"],
         shopping=["Langley City shops nearby"]),
    dict(slug='highpoint', name='Highpoint', note='Central Langley, established homes',
         tags=['Established Homes', 'Central Langley', 'Family Neighbourhood'],
         desc="Highpoint is an established, family-oriented neighbourhood in central Langley with a mix of single-family homes.",
         shopping=["Willowbrook Shopping Centre and Langley City's downtown nearby"],
         entertainment=["Restaurants at nearby Willowbrook Shopping Centre"]),
    dict(slug='otter-district', name='Otter District', note='Rural acreage, border proximity',
         tags=['Rural Acreage', 'Agricultural Land', 'US Border Proximity'],
         desc="The Otter District is a rural part of Langley known for acreage and agricultural land close to the US border.",
         shopping=["Aldergrove and Langley City shopping within reach"],
         entertainment=["Restaurants in nearby Aldergrove"]),
    dict(slug='milner', name='Milner', note='Rural-residential, future growth area',
         tags=['Rural-Residential', 'Agricultural Land', 'Future Growth Area'],
         desc="Milner is a rural-residential area of Langley with agricultural land that continues to see interest as municipal growth plans evolve.",
         shopping=["Willowbrook and Fort Langley shopping nearby"],
         entertainment=["Restaurants in nearby Fort Langley and Willowbrook"]),
    dict(slug='glen-valley', name='Glen Valley', note='Fraser River acreage, rural setting',
         tags=['Fraser River Acreage', 'Agricultural Land', 'Rural Setting'],
         desc="Glen Valley sits along the Fraser River in Langley, offering acreage and agricultural properties in a quiet, rural setting.",
         recreation=["Fraser River access for rural, low-density living"],
         entertainment=["Restaurants in nearby Fort Langley"],
         shopping=["Fort Langley shops nearby"]),
    dict(slug='uplands', name='Uplands', note='Established homes, central Langley',
         tags=['Established Homes', 'Central Langley', 'Family Neighbourhood'],
         desc="Uplands is an established, family-oriented neighbourhood in central Langley offering a mix of single-family homes.",
         shopping=["Willowbrook Shopping Centre nearby"],
         entertainment=["Restaurants at nearby Willowbrook Shopping Centre"]),

    # -------- Delta neighbourhoods (expanded) --------
    dict(slug='ladner', name='Ladner', note='Historic village on the Fraser River',
         tags=['Historic Village', 'Fraser River', 'Small-Town Charm'],
         desc="Ladner is a historic riverside village within Delta, known for its small-town charm, waterfront setting, and established residential streets. It includes the sub-areas of Ladner Village, Hawthorne, and Westham Island.",
         schools=["Ladner Elementary", "Delta Secondary School", "Sacred Heart Elementary", "Delta School District has 24 elementary and 7 secondary schools, including a District French Immersion program \u2014 confirm your specific catchment with SD37"],
         shopping=["Ladner Village's historic downtown along 47A Avenue (independent shops, cafés, the Ladner Village Market)", "Trenant Park Square", "Tsawwassen Mills and Tsawwassen Commons, a short drive away"],
         recreation=["Ladner Leisure Centre (ice rink, two pools, weight room, sauna)", "Ladner Community Centre", "Ladner Harbour Park &amp; Memorial Park", "George C. Reifel Migratory Bird Sanctuary on Westham Island", "Deas Island Regional Park", "Delta Nature Reserve &amp; Burns Bog nearby"],
         area_faq=[
            ("What's the difference between Ladner and Tsawwassen?", "Ladner is Delta's historic administrative centre \u2014 a Fraser River fishing village turned small-town community with a walkable heritage downtown. Tsawwassen is the coastal, beach-oriented community to the south, home to the ferry terminal and Tsawwassen Mills."),
            ("Is Ladner good for birdwatching and nature access?", "Yes \u2014 the George C. Reifel Migratory Bird Sanctuary on nearby Westham Island is internationally known for birdwatching, and Deas Island Regional Park and the Delta Nature Reserve both offer riverside and wetland trails within a short drive."),
            ("What recreation facilities does Ladner have?", "The Ladner Leisure Centre is the community hub \u2014 an ice rink, two pools including a six-lane competition pool, a weight room, and a sauna. It's also the official training facility of the WHL's Vancouver Giants."),
         ],
         entertainment=["Cafes, pubs, and restaurants along Ladner Village's historic 47A Avenue"]),
    dict(slug='tsawwassen', name='Tsawwassen', note='Ferry terminal, beachfront living',
         tags=['Ferry Terminal', 'Beachfront', 'Tsawwassen Mills'],
         desc="Tsawwassen offers beachfront and near-beach living in Delta, home to the BC Ferries terminal and Tsawwassen Mills. It includes the sub-areas of Tsawwassen Central, Beach Grove, English Bluff, and Pebble Hill.",
         schools=["Beach Grove Elementary", "English Bluff Elementary", "Delta Secondary School (Ladner) serves much of South Delta \u2014 confirm your specific catchment with SD37"],
         shopping=["Tsawwassen Mills (one of BC's largest retail centres, on Tsawwassen First Nation lands)", "Tsawwassen Commons"],
         recreation=["Centennial Beach", "Beach Grove Golf Club", "Splashdown Waterslide Park", "Tsawwassen Arts Centre", "Winskill Aquatic and Fitness Centre", "The Tsawwassen Ferry Terminal, the largest of its kind in North America"],
         area_faq=[
            ("Is Tsawwassen good for beach and outdoor lifestyle?", "Yes \u2014 Tsawwassen is known as one of the sunniest spots in Metro Vancouver, with Centennial Beach, a large stretch of waterfront homes, and easy access to Boundary Bay for paddleboarding and kitesurfing."),
            ("What should I know about buying property on Tsawwassen First Nation land?", "The Tsawwassen First Nation holds treaty lands adjacent to the community, including Tsawwassen Mills and a growing residential program. TFN fee-simple lots and leasehold properties involve different title structures than standard freehold purchases \u2014 Manan can walk you through what that means for a specific property."),
            ("How far is Tsawwassen from the ferry terminal and how does that affect living there?", "The BC Ferries terminal is within Tsawwassen itself, making Vancouver Island and the Gulf Islands a genuine day trip \u2014 a real lifestyle draw, though ferry traffic can affect specific routes and times near sailings."),
         ],
         entertainment=["Dining options at Tsawwassen Mills"]),
    dict(slug='north-delta', name='North Delta', note='Elevated views, established homes',
         tags=['Elevated Views', 'Established Homes', 'Scott Road Corridor'],
         desc="North Delta offers established homes on elevated lots with valley and mountain views, along the Scott Road corridor bordering Surrey.",
         schools=["North Delta Secondary", "Seaquam Secondary", "Delta School District (SD37) covers multiple elementary schools \u2014 confirm your specific catchment"],
         shopping=["Scottsdale Centre", "Scott 72 Centre", "Delta Shoppers Mall", "Sunshine Village shopping area"],
         recreation=["North Delta Recreation Centre (weight room, ice arena, curling rink, gymnasiums, outdoor pool, art gallery)", "Sungod Recreation Centre (four pools, ice rink, weight room)", "Watershed Park", "McKittrick Park"],
         area_faq=[
            ("Is North Delta a good area for families?", "Yes \u2014 it offers strong schools (North Delta Secondary and Seaquam Secondary), large parks like Watershed Park, and more attainable housing than Vancouver proper, with direct access across the Fraser River via the Alex Fraser Bridge."),
            ("What recreation facilities does North Delta have?", "Two major centres \u2014 North Delta Recreation Centre with a curling rink, ice arena, and outdoor pool, and Sungod Recreation Centre with four pools and an ice rink \u2014 plus Watershed Park for green space."),
            ("Where do North Delta residents shop?", "Scottsdale Centre, Scott 72 Centre, and the renovated Delta Shoppers Mall cover most everyday needs, with Surrey's larger malls a short drive away."),
         ],
         entertainment=["Restaurants at Scottsdale Centre"]),
    dict(slug='sunshine-hills', name='Sunshine Hills', note='Treed streets, established homes',
         tags=['Treed Streets', 'Established Homes', 'North Delta'],
         desc="Sunshine Hills is a well-treed, established North Delta neighbourhood known for its quiet, residential character.",
         shopping=["Sunshine Village shopping area (shops, restaurants)"],
         recreation=["Watershed Park", "Delta Golf Club nearby"],
         entertainment=["Restaurants at nearby Scottsdale Centre"]),
    dict(slug='annieville', name='Annieville', note='Riverfront industrial, North Delta',
         tags=['Riverfront Industrial', 'North Delta', 'Fraser River'],
         desc="Annieville is a North Delta area along the Fraser River with a mix of residential streets and nearby industrial land.",
         recreation=["Several neighbourhood parks with rinks, ball fields, playgrounds, outdoor pools, and walking trails"],
         area_faq=[
            ("What's Annieville known for as a community?", "It's grown steadily since the 1950s into a well-parked residential area \u2014 its many neighbourhood parks together offer a wide range of recreation, from ball fields to outdoor pools, while retaining its historic riverside character."),
         ],
         entertainment=["Restaurants at nearby Scottsdale Centre"],
         shopping=["Scottsdale Centre nearby"]),
    dict(slug='scottsdale', name='Scottsdale', note='Commercial corridor, North Delta',
         tags=['Commercial Corridor', 'North Delta', 'Transit Access'],
         desc="Scottsdale is a North Delta area anchored by the Scottsdale commercial corridor, offering convenient shopping and transit access.",
         shopping=["Scottsdale Centre (grocery, food court, retail)"],
         entertainment=["Restaurants and dining at Scottsdale Centre"]),
    dict(slug='boundary-bay', name='Boundary Bay', note='Beachfront, rural-residential',
         tags=['Beachfront', 'Rural-Residential', 'Agricultural Land'],
         desc="Boundary Bay is a quiet, beachfront and rural-residential area of Delta known for its shoreline, agricultural land, and relaxed pace of life.",
         recreation=["Boundary Bay beach and dyke trails"],
         entertainment=["Restaurants in nearby Tsawwassen"],
         shopping=["Tsawwassen Mills nearby"]),

    # -------- Burnaby neighbourhoods (expanded) --------
    dict(slug='metrotown', name='Metrotown', note="Burnaby's high-rise urban core",
         tags=['Shopping Hub', 'High-Rise Living', 'SkyTrain Access'],
         desc="Metrotown is Burnaby's high-rise urban core, anchored by Metropolis at Metrotown mall and dense condo development with direct SkyTrain access.",
         schools=["Burnaby South Secondary (IB Diploma Programme &amp; French Immersion)", "Maywood Community School (French Immersion)", "Marlborough, Twelfth Avenue, and Chaffey-Burke Elementary \u2014 feeder school depends on exact address, confirm with SD41 Burnaby"],
         shopping=["Metropolis at Metrotown (330+ stores, Whole Foods, T&amp;T Supermarket)", "Crystal Mall (food and grocery)"],
         recreation=["Central Park (90 hectares \u2014 Swangard Stadium, trails, sports fields, Pitch-and-Putt golf)", "Bonsor area recreation amenities"],
         area_faq=[
            ("What schools serve Metrotown addresses?", "Most fall within the Burnaby South Secondary catchment, which runs an IB Diploma Programme and French Immersion. Elementary feeders vary by exact address between Maywood, Marlborough, Twelfth Avenue, and Chaffey-Burke \u2014 confirm with SD41 Burnaby, since IB admission is an application stream, not automatic even for in-catchment students."),
            ("What green space is near Metrotown despite the density?", "Central Park \u2014 90 hectares including Swangard Stadium, a Pitch-and-Putt course, sports fields, and forest trails \u2014 sits right next to the high-rise core, an unusual combination at this density."),
         ],
         entertainment=["Cineplex Cinemas Metropolis", "300+ dining options and a large food court at Metropolis at Metrotown"]),
    dict(slug='brentwood', name='Brentwood', note='Major redevelopment, SkyTrain access',
         tags=['Redevelopment Hub', 'SkyTrain Access', 'New Towers'],
         desc="Brentwood is one of Burnaby's major redevelopment hubs, with new residential towers and retail rising around the SkyTrain station.",
         shopping=["The Amazing Brentwood (major grocery, dining, fitness \u2014 self-contained mixed-use development)"],
         recreation=["Brentwood Town Centre SkyTrain station (Millennium Line)", "Nearby parks, walking trails, and forested areas with North Shore Mountain views"],
         area_faq=[
            ("How does Brentwood compare to Metrotown for day-to-day living?", "Brentwood is newer and more curated \u2014 The Amazing Brentwood is genuinely self-contained with grocery, dining, and fitness in one development, versus Metrotown's larger overall retail volume. Brentwood also offers newer building stock and a community-oriented feel with strong Millennium Line transit."),
         ],
         entertainment=["Cineplex VIP Cinemas &amp; The Rec Room (bowling, arcade, dining) at The Amazing Brentwood", "Tap &amp; Barrel and 30+ other restaurants"]),
    dict(slug='lougheed', name='Lougheed', note='Town centre redevelopment',
         tags=['Town Centre Redevelopment', 'SkyTrain Access', 'Shopping'],
         desc="Lougheed Town Centre is undergoing major redevelopment, with new condo towers and retail complementing SkyTrain access at the Burnaby-Coquitlam border.",
         shopping=["Lougheed Town Centre mall (undergoing major redevelopment)"],
         recreation=["Lougheed SkyTrain station (Expo and Millennium Lines interchange)"],
         entertainment=["Restaurants at nearby Metrotown and Brentwood"]),
    dict(slug='deer-lake', name='Deer Lake', note='Parks, arts & culture',
         tags=['Deer Lake Park', 'Arts & Culture', 'Established Homes'],
         desc="The Deer Lake area is home to Burnaby's arts and culture precinct and Deer Lake Park, surrounded by established, higher-value homes.",
         recreation=["Deer Lake Park (trails, lake, Burnaby Art Gallery, Shadbolt Centre for the Arts)"],
         entertainment=["Restaurants at nearby Metrotown"],
         shopping=["Metrotown shopping nearby"]),
    dict(slug='capitol-hill', name='Capitol Hill', note='Elevated views, North Burnaby',
         tags=['Elevated Views', 'Established Homes', 'North Burnaby'],
         desc="Capitol Hill is a North Burnaby neighbourhood known for elevated lots with city and mountain views.",
         shopping=["Nearby Burnaby Heights' Hastings Street shops and Brentwood's The Amazing Brentwood"],
         entertainment=["Restaurants along nearby Hastings Street in Burnaby Heights"]),
    dict(slug='edmonds', name='Edmonds', note='Transit access, affordable entry',
         tags=['Transit Access', 'Affordable Entry', 'South Burnaby'],
         desc="Edmonds is a South Burnaby neighbourhood offering relatively more affordable entry points alongside good SkyTrain access.",
         shopping=["Edmonds Town Centre area shops and services"],
         entertainment=["Restaurants at nearby Metrotown"]),
    dict(slug='burnaby-heights', name='Burnaby Heights', note='Heritage character, Hastings Street',
         tags=['Heritage Character', 'Hastings Street', 'North Burnaby'],
         desc="Burnaby Heights is known for its heritage character and the Hastings Street commercial strip, offering established North Burnaby homes.",
         shopping=["Hastings Street's independent shops, cafés, and restaurants"],
         entertainment=["Independent restaurants and cafes along Hastings Street"]),
    dict(slug='south-slope', name='South Slope', note='Established South Burnaby homes',
         tags=['Established Homes', 'South Burnaby', 'Family Neighbourhood'],
         desc="South Slope is an established, family-oriented South Burnaby neighbourhood with a mix of single-family homes.",
         shopping=["Close to Metrotown's Metropolis mall and Crystal Mall"],
         entertainment=["Restaurants at nearby Metrotown"]),
    dict(slug='highgate', name='Highgate', note='Shopping centre, condo living',
         tags=['Shopping Centre', 'Condo Living', 'South Burnaby'],
         desc="Highgate is a South Burnaby area anchored by Highgate Village shopping centre, offering condo and townhome living.",
         shopping=["Highgate Village shopping centre"],
         entertainment=["Restaurants at Highgate Village shopping centre"]),
    dict(slug='central-park-burnaby', name='Central Park', note='Parkside, SkyTrain access',
         tags=['Central Park', 'Established Homes', 'SkyTrain Access'],
         desc="The Central Park neighbourhood borders Burnaby's largest park, offering established homes with good SkyTrain access.",
         recreation=["Central Park (90 hectares \u2014 Swangard Stadium, forest trails, Pitch-and-Putt course, duck ponds)"],
         entertainment=["Restaurants at nearby Metrotown"],
         shopping=["Metrotown shopping nearby"]),
    dict(slug='government-road', name='Government Road', note='North Burnaby, industrial proximity',
         tags=['Industrial Proximity', 'North Burnaby', 'Established Homes'],
         desc="Government Road is a North Burnaby neighbourhood offering established homes near industrial and light-commercial land.",
         shopping=["Lougheed Town Centre and Brentwood shopping nearby"],
         entertainment=["Restaurants at nearby Lougheed and Brentwood"]),
    dict(slug='cariboo', name='Cariboo', note='North Burnaby, near Lougheed',
         tags=['North Burnaby', 'Established Homes', 'Near Lougheed'],
         desc="Cariboo is a North Burnaby neighbourhood bordering Lougheed Town Centre, offering established housing.",
         shopping=["Lougheed Town Centre nearby"],
         entertainment=["Restaurants at nearby Lougheed Town Centre"]),
    dict(slug='big-bend', name='Big Bend', note='Industrial area, Fraser River',
         tags=['Industrial Area', 'Fraser River', 'South Burnaby'],
         desc="Big Bend is a South Burnaby area along the Fraser River known primarily for its industrial and commercial land base.",
         shopping=["Primarily industrial; Metrotown shopping a short drive away"],
         entertainment=["Restaurants at nearby Metrotown"]),
    dict(slug='sperling-duthie', name='Sperling-Duthie', note='SFU proximity, established homes',
         tags=['SFU Proximity', 'Established Homes', 'Near Lougheed'],
         desc="Sperling-Duthie is a North Burnaby neighbourhood offering established homes within reach of SFU and the Lougheed corridor.",
         schools=["Close to Simon Fraser University"],
         entertainment=["Restaurants at nearby Brentwood and Lougheed"],
         shopping=["Brentwood and Lougheed shopping nearby"]),
    dict(slug='willingdon-heights', name='Willingdon Heights', note='Central Burnaby, transit access',
         tags=['Central Burnaby', 'Established Homes', 'Transit Access'],
         desc="Willingdon Heights is a central Burnaby neighbourhood offering established homes and convenient transit access.",
         shopping=["Brentwood and Metrotown shopping both within reach"],
         entertainment=["Restaurants at nearby Brentwood and Metrotown"]),
    dict(slug='forest-grove', name='Forest Grove', note='Established homes, central Burnaby',
         tags=['Established Homes', 'Central Burnaby', 'Family Neighbourhood'],
         desc="Forest Grove is a central Burnaby neighbourhood with a mix of established, family-oriented homes.",
         shopping=["Central Burnaby shopping via Kingsway"],
         entertainment=["Restaurants at nearby Metrotown"]),
    dict(slug='suncrest', name='Suncrest', note='South Burnaby, family neighbourhood',
         tags=['South Burnaby', 'Established Homes', 'Family Neighbourhood'],
         desc="Suncrest is a South Burnaby neighbourhood offering established, family-oriented homes.",
         shopping=["Metrotown shopping nearby"],
         entertainment=["Restaurants at nearby Metrotown"]),
    dict(slug='montecito', name='Montecito', note='North Burnaby, near Burnaby Mountain',
         tags=['North Burnaby', 'Established Homes', 'Near Burnaby Mountain'],
         desc="Montecito is a North Burnaby neighbourhood near Burnaby Mountain, offering established homes and mountain proximity.",
         recreation=["Burnaby Mountain and the SFU Loop Trail nearby"],
         entertainment=["Restaurants at nearby Brentwood"],
         shopping=["Brentwood shopping nearby"]),
    dict(slug='univercity-sfu', name='UniverCity (SFU)', note='Mountain-top campus community',
         tags=['SFU Campus', 'Mountain Views', 'Sustainable Community'],
         desc="UniverCity is a planned community atop Burnaby Mountain beside Simon Fraser University, known for sustainable design and mountain views.",
         schools=["Simon Fraser University (Burnaby Mountain campus)"],
         recreation=["Burnaby Mountain Park &amp; the SFU Loop Trail"],
         entertainment=["Campus dining at Simon Fraser University", "Nesters Market and a handful of local cafes in the UniverCity village"],
         shopping=["Nesters Market and small shops within the UniverCity village"]),
    dict(slug='lochdale', name='Lochdale', note='North Burnaby, established homes',
         tags=['North Burnaby', 'Established Homes', 'Near Burnaby Mountain'],
         desc="Lochdale is a North Burnaby neighbourhood offering established homes near Burnaby Mountain and Hastings Street.",
         shopping=["Hastings Street shops nearby"],
         entertainment=["Restaurants at nearby Brentwood"]),
    dict(slug='westridge', name='Westridge', note='North Burnaby, waterfront proximity',
         tags=['North Burnaby', 'Waterfront Proximity', 'Established Homes'],
         desc="Westridge is a North Burnaby neighbourhood offering established homes with proximity to Burrard Inlet.",
         recreation=["Burrard Inlet waterfront access nearby"],
         entertainment=["Restaurants at nearby Brentwood"],
         shopping=["Brentwood shopping nearby"]),
    dict(slug='sullivan-heights-burnaby', name='Sullivan Heights', note='North Burnaby, family neighbourhood',
         tags=['North Burnaby', 'Established Homes', 'Family Neighbourhood'],
         desc="Sullivan Heights is a North Burnaby neighbourhood offering established, family-oriented homes.",
         shopping=["Lougheed Town Centre and Brentwood shopping nearby"],
         entertainment=["Restaurants at nearby Lougheed and Brentwood"]),

    # -------- Extended service area --------
    dict(slug='kelowna', name='Kelowna', note="Heart of BC's Okanagan wine country",
         tags=['Okanagan Lake', 'Wine Country', 'Tourism & Lifestyle'],
         desc="Kelowna is the heart of BC's Okanagan wine country, offering lakeside living, a thriving tourism economy, and a lifestyle-driven real estate market.",
         schools=["UBC Okanagan (North Glenmore)", "Kelowna Secondary", "Aberdeen Hall (private)"],
         shopping=["South Pandosy's shops and restaurants", "Downtown Kelowna's waterfront dining and retail"],
         recreation=["Okanagan Lake beaches, marinas, and Waterfront Park", "Knox Mountain Park", "Myra Canyon", "Parkinson Recreation Centre", "Numerous wineries and golf courses (Gallagher's Canyon, Harvest Golf Club, Black Mountain Golf Club)"],
         area_faq=[
            ("What are the best-known Kelowna neighbourhoods for families?", "Lower Mission, Glenmore, Kettle Valley, Upper Mission, and Black Mountain are commonly cited as the strongest family areas, each combining schools, parks, and recreation facilities with a slightly different mix of price point and setting."),
            ("How does Kelowna's lifestyle differ from the Fraser Valley?", "It's a genuinely different market \u2014 lakeside living on Okanagan Lake, an established wine and tourism economy, and a hotter, drier climate, versus the Fraser Valley's Metro Vancouver-commuter orientation."),
         ],
         entertainment=["Restaurants and cafes in South Pandosy and downtown Kelowna's waterfront dining strip"]),
    dict(slug='kamloops', name='Kamloops', note='Thompson Rivers confluence',
         tags=['Thompson Rivers', 'Semi-Arid Climate', 'University Town'],
         desc="Kamloops sits at the confluence of the Thompson Rivers, offering a semi-arid climate, relative affordability, and a growing economy anchored by Thompson Rivers University.",
         schools=["Thompson Rivers University (TRU)", "Sa-Hali Secondary", "Kamloops-Thompson School District (SD73)"],
         shopping=["Tranquille Road's local shops and restaurants (North Kamloops)", "Sahali's shopping centres near TRU"],
         recreation=["Tournament Capital Centre", "Riverside Park &amp; Pioneer Park", "Sun Peaks skiing nearby", "Dunes at Westsyde golf course", "Over 2,000 hours of sunshine annually"],
         area_faq=[
            ("What is Kamloops known for as a place to live?", "A major-centre mix of amenities \u2014 a university, professional arts scene, and shopping \u2014 combined with small-city ease, generally no more than a 15-minute drive across town, plus over 2,000 hours of sunshine a year and easy access to skiing at Sun Peaks."),
            ("Which Kamloops neighbourhoods are most central?", "Sahali is the largest and most central, home to TRU, major shopping, and a range of housing from condos to single-family homes, just minutes from downtown."),
         ],
         entertainment=["Restaurants along Tranquille Road (North Kamloops) and at Sahali"]),
]

def _oxford_join(items):
    items = list(items)
    if len(items) == 1: return items[0]
    if len(items) == 2: return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"

def _housing_type(desc, tags):
    text = (desc + ' ' + ' '.join(tags)).lower()
    types = []
    if 'acreage' in text or 'estate' in text or 'equestrian' in text: types.append("acreage and estate properties")
    if 'townhome' in text or 'townhouse' in text: types.append("townhomes")
    if 'condo' in text or 'high-rise' in text or 'tower' in text: types.append("condos")
    if 'detached' in text or 'single-family' in text: types.append("single-family detached homes")
    if not types:
        if 'industrial' in text: types.append("industrial and commercial properties, not primarily residential")
        elif 'rural' in text or 'agricultural' in text or 'farm' in text: types.append("larger rural and agricultural-zoned properties")
        else: types.append("a mix of established housing")
    return _oxford_join(types)

def _good_fit(name, note, tags):
    text = (note + ' ' + ' '.join(tags)).lower()
    fits = []
    if 'family' in text or 'families' in text or 'school' in text: fits.append("families")
    if 'newer' in text or 'master-planned' in text or 'growing' in text: fits.append("buyers wanting newer construction")
    if 'established' in text or 'heritage' in text or 'village' in text: fits.append("buyers who want a turnkey home in an established community")
    if 'affordable' in text or 'entry' in text or 'value' in text: fits.append("first-time buyers and investors watching their budget")
    if 'luxury' in text or 'estate' in text or 'premium' in text: fits.append("move-up and luxury buyers")
    if 'industrial' in text or 'investment' in text or 'warehousing' in text: fits.append("investors and business owners rather than residential buyers")
    if 'rural' in text or 'acreage' in text or 'agricultural' in text: fits.append("buyers wanting space, privacy, or acreage over urban convenience")
    if not fits: fits.append("a range of buyers depending on budget and lifestyle priorities")
    return _oxford_join(sorted(set(fits), key=fits.index))

def _auto_supplement_faqs(area, target=6):
    faqs = list(area.get('area_faq') or [])
    existing_q = ' '.join(q.lower() for q, _ in faqs)
    name = area['name']
    candidates = []
    if area.get('schools') and 'school' not in existing_q:
        candidates.append((
            f"What schools serve {name}?",
            f"{_oxford_join(area['schools'])}."
        ))
    if area.get('shopping') and 'shop' not in existing_q and 'grocery' not in existing_q:
        candidates.append((
            f"Where do {name} residents shop?",
            f"{_oxford_join(area['shopping'])}."
        ))
    if area.get('recreation') and 'recreation' not in existing_q and 'park' not in existing_q:
        candidates.append((
            f"What recreation and parks are near {name}?",
            f"{_oxford_join(area['recreation'])}."
        ))
    if 'type of home' not in existing_q and 'kind of home' not in existing_q and 'housing' not in existing_q:
        candidates.append((
            f"What type of homes will I find in {name}?",
            f"{name} is mainly known for {_housing_type(area['desc'], area['tags'])}. {area['desc']}"
        ))
    if 'good fit' not in existing_q and 'good choice' not in existing_q and 'good area' not in existing_q and 'good for' not in existing_q:
        candidates.append((
            f"Who is {name} a good fit for?",
            f"Based on the area's character \u2014 {area['note'].lower()} \u2014 {name} tends to suit {_good_fit(name, area['note'], area['tags'])}. Manan can talk through whether it fits your specific situation."
        ))
    candidates.append((
        f"Is Manan familiar with {name} specifically?",
        f"Yes \u2014 as a licensed REALTOR\u00ae in British Columbia, Manan works with clients across the province, not just one sub-region, and can speak directly to {name}'s current inventory, pricing, and what makes it different from its neighbours."
    ))
    candidates.append((
        f"How does pricing in {name} compare to the wider Fraser Valley market?",
        f"As a general reference point, the Fraser Valley's composite benchmark price was $877,600 as of the most recent Fraser Valley Real Estate Board report, with detached homes at $1,350,200, townhomes at $764,100, and condos at $469,500. Where {name} sits relative to those figures depends on housing type, lot size, and age of construction \u2014 Manan can pull current comparables specific to this area."
    ))
    candidates.append((
        f"Is now a good time to buy or sell in {name}?",
        "Market conditions across the Fraser Valley have recently favoured buyers, with inventory near decade highs and sales activity below year-ago levels \u2014 which can mean more negotiating room for buyers and a need for sharper pricing and presentation for sellers. Conditions shift, so it's worth a direct, current conversation with Manan rather than relying on general trends alone."
    ))
    for q, a in candidates:
        if len(faqs) >= target:
            break
        faqs.append((q, a))
    area['area_faq'] = faqs

for _area in AREAS:
    _auto_supplement_faqs(_area)

def area_href(slug):
    return f'/communities/{slug}/'

COMMUNITY_CARDS = [dict(name=a['name'], href=area_href(a['slug']), note=a['note']) for a in AREAS]


# ============================================================
# /buyers/  — Buy a Home hub
# ============================================================
buyers_body = subhero(
    "Buyer Representation",
    'Your <span class="accent-warm">Home Buying</span> Journey',
    "A clear, guided process from first conversation to key handover \u2014 with full buyer representation across Surrey and the Lower Mainland.",
    TEXT_CTA + CONTACT_CTA
)
buyers_body += step_section(
    "A Clear, Guided Process",
    "Here's what to expect when you buy a home with Manan.",
    [
        dict(title="Get Pre-Approved", desc="Before you start searching, get mortgage pre-approval. Manan connects you with trusted lenders and helps you understand your budget and purchasing power."),
        dict(title="Define Your Needs", desc="A conversation about your must-haves, nice-to-haves, lifestyle preferences, and long-term goals \u2014 this shapes your tailored property search."),
        dict(title="Property Search", desc="Access to MLS\u00ae listings plus local market insight. Showings are scheduled around your schedule, with honest assessments of every property."),
        dict(title="Make an Offer", desc="A competitive offer with the right conditions to protect your interests, negotiated skillfully on your behalf."),
        dict(title="Due Diligence", desc="Inspections, strata documents, title review \u2014 you're guided through every subject so you can move forward with confidence."),
        dict(title="Close &amp; Move In", desc="From final walkthrough to key handover, Manan ensures a smooth completion \u2014 and stays available whenever you need him after."),
    ]
)
buyers_body += point_list_section(
    True, "Buyer Representation",
    'Why Buy With <span class="accent-warm">Manan</span>?',
    "Your buyer's agent should be your advocate, your guide, and your trusted advisor. Here's what that means in practice.",
    [
        dict(icon="\U0001F4C8", title="Deep Local Expertise", desc="Manan knows the neighbourhoods, streets, and market trends across Surrey and the Lower Mainland \u2014 residential and commercial alike."),
        dict(icon="\U0001F4A1", title="Your Interests First", desc="As your buyer's agent, Manan's loyalty is to you. He'll tell you when a property isn't right, even if it means more time searching."),
        dict(icon="\U0001F91D", title="Extensive Network", desc="Beyond MLS\u00ae, Manan's relationships across the industry can surface opportunities before they're widely known."),
        dict(icon="\U0001F4C4", title="Buyer Representation", desc="In most transactions, the seller's side pays the buyer's agent commission \u2014 you get full professional representation with no direct cost to you."),
    ],
    img_seed='surrey-buyer-agent', img_alt="Manan Bhullar meeting with buyer clients (sample photo)"
)
buyers_body += market_snapshot_section()
buyers_body += f"""<section class="content-section raised">
  <div class="wrap two-col">
    <div>
      <div class="eyebrow" style="margin-bottom:16px;">First-Time Buyer?</div>
      <h2>Programs for First-Time Buyers</h2>
      <p style="color:var(--ink-soft);margin-top:14px;max-width:48ch;">There are real, current programs to help first-time buyers get into the market. Manan will walk you through every option available to your specific situation.</p>
      <div style="margin-top:22px;"><a class="btn-outline-dark" href="/buyers/first-time/">See the Full First-Time Buyer Guide \u2192</a></div>
    </div>
    <div class="calc-card" id="mortgageCalc">
      <h3>Mortgage Calculator</h3>
      <div class="sub">Estimate your monthly payments</div>
      <div class="calc-row"><label for="calcPrice">Purchase Price ($)</label><input type="number" id="calcPrice" value="800000"></div>
      <div class="calc-row-split">
        <div class="calc-row"><label for="calcDown">Down Payment (%)</label><input type="number" id="calcDown" value="20"></div>
        <div class="calc-row"><label for="calcRate">Interest Rate (%)</label><input type="number" step="0.01" id="calcRate" value="5.25"></div>
      </div>
      <div class="calc-row">
        <label for="calcAmort">Amortization (years)</label>
        <select id="calcAmort">
          <option value="25">25 years</option>
          <option value="30">30 years</option>
          <option value="20">20 years</option>
          <option value="15">15 years</option>
        </select>
      </div>
      <div class="calc-result">
        <div class="amt" id="calcResult">~$0</div>
        <div class="note" id="calcResultNote"></div>
      </div>
      <a class="btn-solid-warm calc-cta" id="calcCta" href="sms:+16047279542">\U0001F4AC Text Manan About This Number</a>
      <div class="calc-disclaimer">For illustration only. Contact a mortgage broker for accurate figures.</div>
    </div>
  </div>
</section>"""
buyers_body += simple_cards(
    "Explore Buyer Services", "Detailed guides for every kind of buyer.",
    [
        dict(title="First-Time Buyers", desc="Government programs, step-by-step guidance, and everything you need to buy your first home.", href="/buyers/first-time/"),
        dict(title="Condos &amp; Townhomes", desc="Navigate strata documents, fees, and bylaws with confidence.", href="/buyers/condos-townhomes/"),
        dict(title="Investment Properties", desc="Rental homes, multi-family, and secondary suites. Build wealth through Fraser Valley real estate.", href="/buyers/investment/"),
        dict(title="Luxury Homes", desc="Estate properties in South Surrey, White Rock, and beyond. Discretion and premium service.", href="/buyers/luxury/"),
        dict(title="Relocating to BC", desc="Moving from out of province? Manan helps remote buyers find the right community and home.", href="/buyers/relocation/"),
    ],
    raised=False
)
buyers_body += f"""<section class="content-section raised">
  <div class="wrap">
    <div class="content-head center"><h2>Popular Communities</h2><p>A few places to start — explore all {len(AREAS)} communities Manan serves for the full picture.</p></div>
    <div class="community-grid">
      <a class="community-card" href="/communities/surrey/"><div><div class="name">Surrey</div><div class="note">BC's second-largest city</div></div><span class="arrow">→</span></a>
      <a class="community-card" href="/communities/delta/"><div><div class="name">Delta</div><div class="note">Three distinct communities</div></div><span class="arrow">→</span></a>
      <a class="community-card" href="/communities/south-surrey/"><div><div class="name">White Rock / South Surrey</div><div class="note">Oceanfront & premium market</div></div><span class="arrow">→</span></a>
      <a class="community-card" href="/communities/langley/"><div><div class="name">Langley</div><div class="note">Small-town charm, modern amenities</div></div><span class="arrow">→</span></a>
      <div class="community-card-group">
        <div class="name">Metro Vancouver</div>
        <div class="group-links"><a href="/communities/vancouver/">Vancouver →</a><a href="/communities/burnaby/">Burnaby →</a><a href="/communities/coquitlam/">Coquitlam →</a></div>
      </div>
      <div class="community-card-group">
        <div class="name">Out of Town</div>
        <div class="group-links"><a href="/communities/kamloops/">Kamloops →</a><a href="/communities/kelowna/">Kelowna →</a><a href="/communities/hope/">Hope →</a></div>
      </div>
    </div>
    <div style="text-align:center;margin-top:24px;"><a class="btn-outline-dark" href="/communities/">View All Areas →</a></div>
  </div>
</section>"""
buyers_body += cta_band(
    'Ready to Start Your <span class="accent-warm">Home Search</span>?',
    "A free, no-pressure consultation is the best place to start.",
    TEXT_CTA + EVAL_CTA
)
write_page(
    '/buyers/',
    'Buy a Home | Surrey & Fraser Valley Buyer Representation | Manan Bhullar',
    "Full buyer representation across Surrey and the Lower Mainland \u2014 guided process, mortgage calculator, and first-time buyer programs with Manan Bhullar.",
    crumbs(("Buy a Home", None)),
    buyers_body
)

# ============================================================
# /buyers/first-time/  — First-Time Home Buyers
# ============================================================
ft_body = subhero(
    "Your First Home Awaits",
    'First-Time Home Buyers <br>Surrey &amp; Fraser Valley',
    "Buying your first home is one of the biggest decisions you'll make. Manan guides first-time buyers through every step \u2014 from government programs to keys in hand.",
    TEXT_CTA + '<a class="btn-solid-warm" href="/contact/">Book a Free Consultation</a>'
)
ft_body += point_list_section(
    False, "Getting Started", "Why Work With a Buyer's Agent as a First-Timer",
    "Your first purchase comes with the steepest learning curve \u2014 financing rules, strata documents, subject conditions, closing costs. A dedicated buyer's agent means someone in your corner who explains every decision in plain language, at no direct cost to you in most transactions.",
    [
        dict(icon="\U0001F4CB", title="No Pressure, No Rush", desc="Manan takes a hands-on, personal approach \u2014 you'll never feel pushed into a decision before you're ready."),
        dict(icon="\U0001F50D", title="Every Document Explained", desc="Inspection reports, strata minutes, title search \u2014 explained clearly so you know exactly what you're buying."),
        dict(icon="\u2696\uFE0F", title="Honest Opinions", desc="If a property isn't right for you, Manan will tell you \u2014 even if it means more time searching."),
    ],
    img_first=True, img_seed='first-time-buyer-keys', img_alt="First-time buyers receiving keys (sample photo)"
)
ft_body += f"""<section class="content-section raised">
  <div class="wrap">
    <div class="content-head center">
      <h2>Programs &amp; Incentives for First-Time Buyers</h2>
      <p>Current federal and provincial programs available to eligible first-time buyers in BC. Manan will help confirm exactly what you qualify for.</p>
    </div>
    <div class="grid-cards cols-2">
      <div class="simple-card">
        <strong>BC First-Time Home Buyers' Property Transfer Tax Exemption</strong>
        <span>Eligible first-time buyers pay no Property Transfer Tax on homes up to $835,000, with a partial exemption phasing out up to $860,000.</span>
      </div>
      <div class="simple-card">
        <strong>First Home Savings Account (FHSA)</strong>
        <span>Contribute up to $8,000 per year, to a $40,000 lifetime maximum, in a tax-advantaged account designed specifically for a first home purchase.</span>
      </div>
      <div class="simple-card">
        <strong>RRSP Home Buyers' Plan (HBP)</strong>
        <span>Withdraw RRSP savings tax-free toward your first home, repayable over 15 years. Can be combined with the FHSA.</span>
      </div>
      <div class="simple-card">
        <strong>Bill C-4 GST Rebate for New Builds</strong>
        <span>First-time buyers pay no GST on qualifying new construction up to $1 million, with the rebate phasing out between $1 million and $1.5 million \u2014 a saving of up to $50,000. Applies to purchase agreements signed on or after May 27, 2025, through the end of 2030.</span>
      </div>
      <div class="simple-card">
        <strong>CMHC Mortgage Insurance</strong>
        <span>Allows qualified buyers to purchase with less than 20% down, insuring the lender against default on higher-ratio mortgages.</span>
      </div>
    </div>
    <p style="font-size:0.8rem;color:var(--ink-soft);margin-top:24px;text-align:center;">Program thresholds and eligibility rules change \u2014 Manan will help you confirm current details and whether you qualify.</p>
  </div>
</section>"""
ft_body += market_snapshot_section()
ft_body += step_section(
    "What Your Budget Actually Buys Right Now",
    "Real Fraser Valley benchmark prices by property type \u2014 a starting point for setting expectations before you shop.",
    [
        dict(title="Under the Condo Benchmark", desc="At a $469,500 benchmark, apartments in Surrey City Centre, Whalley, and parts of Newton remain the most accessible entry point, especially near SkyTrain."),
        dict(title="Around the Townhome Benchmark", desc="At a $764,100 benchmark, townhomes in Cloverdale, Clayton, and parts of Langley offer more space than a condo without stretching to a detached home."),
        dict(title="Approaching the Detached Benchmark", desc="At a $1,350,200 benchmark, detached homes are within reach in Abbotsford, Chilliwack, and select North Surrey pockets, particularly with a larger down payment."),
    ],
    raised=True
)
ft_body += faq_section("First-Time Buyer Questions, Answered", [
    ("What is the minimum down payment for a first home in BC?", "In Canada, the minimum down payment is 5% on the first $500,000 of the purchase price and 10% on any portion between $500,000 and $1.5 million. Homes priced above $1.5 million require 20% down. For a $750,000 Fraser Valley townhome, that's $50,000 minimum, plus closing costs. If you put down less than 20%, you'll also pay CMHC mortgage default insurance, which is added to your mortgage rather than paid up front."),
    ("How much should I save for closing costs?", "Budget roughly 1.5\u20134% of the purchase price. The largest single item is usually BC's Property Transfer Tax \u2014 1% on the first $200,000 and 2% above that, so $14,000 on an $800,000 home \u2014 unless you qualify for the first-time buyer exemption, which fully eliminates it up to $835,000. Beyond that: legal or notary fees, home inspection, title insurance, and adjustments for prepaid property taxes. Manan will walk through a full estimate specific to your purchase."),
    ("Can I use the FHSA and Home Buyers' Plan together?", "Yes \u2014 and you should if you can. The FHSA lets you contribute up to $8,000 per year to a $40,000 lifetime maximum, with contributions tax-deductible and qualifying withdrawals completely tax-free. The RRSP Home Buyers' Plan lets you withdraw up to $60,000 tax-free, repayable over 15 years starting the second year after withdrawal. Used together, a couple can access a substantial down payment. Start the FHSA early \u2014 contribution room only begins once the account is opened."),
    ("What is the difference between pre-approved and pre-qualified?", "Pre-qualification is a rough estimate based on numbers you self-report \u2014 it takes minutes and carries little weight with sellers. Pre-approval means a lender has verified your income, credit, and down payment documentation, and typically includes a rate hold of 90 to 120 days. In a competitive situation, a pre-approval is what makes your offer credible. Get it before you start seriously viewing."),
    ("Should I buy a condo or detached home as my first place?", "It comes down to budget, lifestyle, and how much maintenance you want. A condo gets you into the market at a lower price with exterior maintenance handled, but you pay monthly strata fees and live by strata bylaws. A detached home gives you land, freedom, and more space, with all upkeep and higher carrying costs on you. Townhomes sit in between. Given current Fraser Valley benchmarks \u2014 roughly $469,500 for apartments versus $1,350,200 for detached \u2014 the gap is significant for most first-time buyers."),
    ("How long does the buying process usually take?", "From first conversation to possession, most first-time purchases run six to twelve weeks, though it varies widely. Getting pre-approved takes a few days to a week. The search itself is the most variable part \u2014 anywhere from a few weeks to several months depending on your criteria and inventory. Once an offer is accepted, subject removal typically takes one to two weeks, and completion is usually 30 to 60 days after that."),
])
ft_body += simple_cards(
    "Related Buyer Services", "Other ways Manan helps buyers across the Fraser Valley.",
    [
        dict(title="Condos &amp; Townhomes", desc="Strata living guide \u2014 fees, bylaws, and depreciation reports.", href="/buyers/condos-townhomes/"),
        dict(title="Investment Properties", desc="Rental homes, multi-family, and secondary suites for investors.", href="/buyers/investment/"),
        dict(title="Luxury Homes", desc="Estate properties in South Surrey and White Rock.", href="/buyers/luxury/"),
        dict(title="Relocating to BC", desc="Moving from out of province? Remote-buyer support.", href="/buyers/relocation/"),
    ], cols=4, raised=False
)
ft_body += cta_band(
    'Ready to Buy Your <span class="accent-warm">First Home</span>?',
    "Let's start with a free, no-pressure consultation. Manan will walk you through the programs you qualify for and help you understand your budget.",
    TEXT_CTA + CONTACT_CTA
)
write_page(
    '/buyers/first-time/',
    "First-Time Home Buyers | Surrey & Fraser Valley | Manan Bhullar",
    "A complete guide for first-time home buyers in Surrey and the Fraser Valley \u2014 current BC programs, FAQs, and step-by-step guidance from Manan Bhullar.",
    crumbs(("Buy a Home", "/buyers/"), ("First-Time Buyers", None)),
    ft_body
)

# ============================================================
# Remaining Buyers sub-pages
# ============================================================
def area_cards(slugs):
    lookup = {a['slug']: a for a in AREAS}
    return [dict(name=lookup[s]['name'], href=area_href(s), note=lookup[s]['note']) for s in slugs if s in lookup]

def simple_service_page(path, crumb_label, eyebrow, h1, lead, points, extra="", faq=None, related=None, area_slugs=None):
    body = subhero(eyebrow, h1, lead, TEXT_CTA + CONTACT_CTA)
    body += point_list_section(False, eyebrow, "What This Means For You", "", points, img_first=True, img_seed=path.strip('/').replace('/', '-'), img_alt=f"{crumb_label} (sample photo)")
    body += extra
    if area_slugs:
        body += community_grid_section(
            f"Where to Look for {crumb_label}", "Real neighbourhood guides, not just a generic city page.",
            area_cards(area_slugs)
        )
    if faq:
        body += faq_section(f"{crumb_label} Questions, Answered", faq)
    if related:
        body += simple_cards("Related Buyer Services", "Other ways Manan helps buyers across the Fraser Valley.", related, cols=3, raised=True)
    body += cta_band(
        'Let\'s Talk It <span class="accent-warm">Through</span>',
        "Every situation is different \u2014 a short call is the fastest way to figure out the right approach for yours.",
        TEXT_CTA + CONTACT_CTA
    )
    return body

write_page(
    '/buyers/condos-townhomes/',
    "Condos & Townhomes | Strata Buying Guide | Manan Bhullar",
    "Buying a condo or townhome in Surrey and the Fraser Valley? Manan Bhullar guides buyers through strata documents, fees, and bylaws.",
    crumbs(("Buy a Home", "/buyers/"), ("Condos & Townhomes", None)),
    simple_service_page(
        '/buyers/condos-townhomes/', 'Condos & Townhomes', 'Strata Living',
        'Condos &amp; Townhomes',
        "Strata living comes with its own rulebook \u2014 fees, bylaws, depreciation reports, and meeting minutes that can make or break a purchase. Manan helps buyers read between the lines before they commit.",
        [
            dict(icon="\U0001F4C4", title="Strata Document Review", desc="A close read of meeting minutes, financials, and depreciation reports to flag any red flags before your subjects expire."),
            dict(icon="\U0001F4B0", title="Understanding Fees", desc="What's included in monthly strata fees, and what isn't \u2014 so there are no surprises after you move in."),
            dict(icon="\U0001F4CB", title="Bylaws &amp; Rentals", desc="Rental restrictions, pet policies, and renovation rules reviewed up front, especially important for investors."),
        ],
        faq=[
            ("What is the difference between a condo and a townhouse?", "Both are strata-titled in BC, meaning you own your unit and share ownership of common property through a strata corporation. A condo is typically an apartment-style unit inside a larger building, with shared interior hallways, elevators, and amenities. A townhouse is a multi-level home sharing one or two walls with neighbours, usually with its own front door, attached garage, and a small private yard or patio. Townhouses feel closer to a detached home; condos generally cost less for the same bedroom count."),
            ("What are strata fees and what do they cover?", "Strata fees are monthly payments funding shared building costs \u2014 typically building insurance, common area maintenance and cleaning, landscaping, management fees, and contributions to the contingency reserve fund. What's included varies a lot: some buildings cover heat and hot water, others don't. Amenity-heavy buildings with pools, gyms, and concierge carry higher fees. Fees are set by the strata based on its budget and aren't negotiable by individual owners."),
            ("What is a depreciation report and why does it matter?", "A depreciation report is a professional assessment projecting a building's major component lifespans and repair costs over 30 years \u2014 roof, windows, plumbing, elevators, building envelope. It tells you whether the contingency reserve fund is adequate or whether a large special levy is likely. A building without a current depreciation report, or one showing a badly underfunded reserve, is a genuine risk worth understanding before your subjects expire."),
            ("What is a special levy and can I be stuck paying one?", "A special levy is a one-time charge to owners when the strata needs funds beyond its reserve \u2014 typically for major repairs like re-roofing or envelope remediation. Yes, you can inherit one: if a levy is approved after you take possession, you pay it as the current owner, even if the underlying problem predates your purchase. This is exactly why reviewing minutes and the depreciation report before subject removal matters so much."),
            ("Can I rent out my condo in BC?", "BC removed strata rental restriction bylaws in November 2022 under Bill 44, so stratas can no longer ban long-term rentals \u2014 any existing rental restriction bylaw is unenforceable. Stratas can still restrict short-term rentals of under 30 days (Airbnb-style), and 55+ age restrictions remain permitted. Municipal zoning and provincial short-term rental rules apply on top of strata bylaws, so confirm all three layers for the specific building and city."),
            ("How do I evaluate strata documents before buying?", "Request at least two years of council meeting minutes, the current budget and financial statements, the depreciation report, the bylaws and rules, and the Form B Information Certificate. Look for recurring maintenance complaints, envelope or water ingress issues, contentious council disputes, upcoming projects mentioned but not yet funded, and the reserve fund balance relative to the building's age. Manan reviews these with every strata buyer and flags what stands out."),
        ],
        related=[
            dict(title="First-Time Buyers", desc="Government programs and step-by-step guidance for your first purchase.", href="/buyers/first-time/"),
            dict(title="Investment Properties", desc="Considering a condo or townhome as a rental? Start here.", href="/buyers/investment/"),
            dict(title="Buy a Home", desc="Back to the full buyer representation overview.", href="/buyers/"),
        ],
        area_slugs=['city-centre', 'fleetwood', 'cloverdale', 'grandview-heights', 'langley', 'abbotsford']
    )
)

write_page(
    '/buyers/investment/',
    "Investment Properties | Fraser Valley Real Estate | Manan Bhullar",
    "Build wealth through Fraser Valley real estate \u2014 rental homes, multi-family, and secondary suites with Manan Bhullar.",
    crumbs(("Buy a Home", "/buyers/"), ("Investment Properties", None)),
    simple_service_page(
        '/buyers/investment/', 'Investment Properties', 'Build Wealth',
        'Investment Properties',
        "Rental homes, multi-family buildings, and secondary suites \u2014 Manan works with investors to identify properties that fit their financial goals across Surrey and the Lower Mainland.",
        [
            dict(icon="\U0001F4CA", title="Rental &amp; Cash-Flow Analysis", desc="Realistic rental income estimates and expense breakdowns to evaluate a property as an investment, not just a home."),
            dict(icon="\U0001F3E0", title="Secondary Suite Potential", desc="Identifying properties with legal or conforming secondary-suite potential to help offset your mortgage."),
            dict(icon="\U0001F4BC", title="Multi-Family &amp; Land", desc="For larger investment goals, Manan also works alongside the commercial side of his practice for multi-family and development opportunities."),
        ],
        extra=price_range_grid(
            "Real Numbers from the Fraser Valley Rental Market",
            "What to expect when you run the numbers on a rental property here \u2014 scenarios, not guarantees. Manan runs actual leased comparables, not asking rents, before you write an offer.",
            [
                ("Suited Home in Newton or Whalley", "A detached home with a legal or conforming secondary suite is the most common entry point for Fraser Valley investors. Upper floor plus basement suite gives you two income streams from one mortgage, and Surrey has been comparatively progressive on secondary suite regulation. Verify suite legality with the City before you write \u2014 an unpermitted suite affects both financing and insurance."),
                ("One-Bedroom Condo Near SkyTrain", "Surrey City Centre condos near King George and Gateway stations draw steady tenant demand from students at SFU Surrey and young professionals. At current rates, a high-leverage condo purchase often runs slightly cash-flow negative, with the investment case resting on appreciation and the SkyTrain extension rather than monthly income."),
                ("Cloverdale or Langley Townhome", "Three-bedroom townhomes rent to families who tend to stay long-term and maintain the property well. Strata fees eat into the return, so factor them into your cap rate rather than treating rent as net. Since Bill 44, strata rental restriction bylaws are no longer enforceable, though short-term rentals under 30 days can still be restricted."),
                ("Abbotsford or Chilliwack Detached", "The strongest cash-flow-positive opportunities in the region, particularly with a suite. Entry prices are meaningfully lower than Surrey, and rents hold up well. The trade-off is generally slower appreciation than Surrey or Langley over a long horizon \u2014 a cash-flow play rather than a growth play."),
            ],
            tip_heading="How Manan underwrites an investment property",
            tip_text="Most new investors anchor on the rent number in the listing and never check what comparable units actually leased for. Manan pulls recently-leased comparables \u2014 not asking rents \u2014 and underwrites conservatively, budgeting for vacancy, maintenance, and the first major repair. Cleaner numbers going in means fewer surprises in year two."
        ),
        faq=[
            ("What is a good cap rate for Surrey rental properties?", "Cap rate is net operating income divided by purchase price. In the Lower Mainland, residential cap rates are generally compressed compared to the national average \u2014 investors here have historically accepted thinner yields because appreciation did the heavy lifting. Suited detached homes in Newton or Whalley typically sit at the higher end of the local range; condos at the lower end once strata fees are deducted. Manan will run the actual numbers on any specific property rather than working from a rule of thumb."),
            ("What is the minimum down payment for an investment property in Canada?", "Non-owner-occupied rental properties require a minimum 20% down payment. They don't qualify for CMHC-insured high-ratio mortgages, which are only available on owner-occupied homes. If you live in one unit of a two-to-four unit property, different rules can apply \u2014 worth confirming with your broker early, since it materially changes what you can afford."),
            ("Can I get a mortgage for an investment property?", "Yes, though qualification is stricter than for a principal residence. Lenders apply the mortgage stress test, and most will only count a portion of projected rental income (commonly 50\u201380%) toward your qualifying income. Rates on rental properties are typically slightly higher. Expect more documentation \u2014 leases, rental history, and often a rental appraisal."),
            ("What are the tax implications of investment properties in BC?", "Rental income is taxable and must be reported, offset by deductible expenses including mortgage interest, property tax, insurance, maintenance, and property management fees. On sale, capital gains apply to non-principal-residence property. BC also has the Speculation and Vacancy Tax and, in some municipalities, an Empty Homes Tax \u2014 both generally avoided if the property is genuinely tenanted long-term. This is accountant territory, not realtor territory; Manan will flag when to bring yours in."),
            ("What is the difference between a legal and a non-conforming secondary suite?", "A legal suite is permitted and registered with the municipality, meeting current building code and bylaw requirements. A non-conforming or unpermitted suite may function fine day-to-day but isn't registered. The difference matters concretely: lenders may not count income from an unpermitted suite, insurers may decline coverage, and the city can order it removed. Always verify status with the municipality before removing subjects."),
            ("Should I buy a single-family rental or a multi-family property?", "Suited detached homes are the usual starting point \u2014 lower entry price, residential financing, and simpler management. Multi-family (typically 5+ units) shifts you into commercial financing, where lenders underwrite the building's income rather than primarily your personal income, and where returns are driven by NOI. Multi-family generally means better economies of scale but a larger down payment and more operational involvement. Manan works both sides and can talk through where your capital fits."),
        ],
        related=[
            dict(title="Condos &amp; Townhomes", desc="Strata rules and rental restrictions to check before buying to rent out.", href="/buyers/condos-townhomes/"),
            dict(title="Commercial Real Estate", desc="For larger multi-family or commercial income properties.", href="/commercial/"),
            dict(title="Buy a Home", desc="Back to the full buyer representation overview.", href="/buyers/"),
        ],
        area_slugs=['newton', 'city-centre', 'guildford', 'langley-city', 'north-delta', 'campbell-heights']
    )
)

write_page(
    '/buyers/luxury/',
    "Luxury Homes | South Surrey & White Rock Estates | Manan Bhullar",
    "Estate properties in South Surrey, White Rock, and beyond \u2014 discretion, experience, and premium service with Manan Bhullar.",
    crumbs(("Buy a Home", "/buyers/"), ("Luxury Homes", None)),
    simple_service_page(
        '/buyers/luxury/', 'Luxury Homes', 'Estate Properties',
        'Luxury Homes',
        "South Surrey, White Rock, and other premium pockets of the Lower Mainland call for a different level of service \u2014 discretion, market fluency, and a network that extends beyond the public MLS\u00ae.",
        [
            dict(icon="\U0001F510", title="Discretion", desc="Confidential searches and, where appropriate, off-market conversations handled with privacy in mind."),
            dict(icon="\U0001F3E1", title="Market Fluency", desc="A close read on what distinguishes comparable luxury properties \u2014 lot, finishes, view, and location \u2014 beyond the listing photos."),
            dict(icon="\u2728", title="White-Glove Process", desc="From private showings to coordinating trades and stagers, every detail is managed with the same care as the transaction itself."),
        ],
        extra=price_range_grid(
            "South Surrey &amp; White Rock Price Ranges",
            "A snapshot of where the South Surrey, White Rock, and Fraser Valley luxury market sits right now.",
            [
                ("Morgan Creek", "Estate homes generally run $2.5M\u2013$5M+ depending on lot size, condition, and golf-course frontage. Larger custom builds on premium lots have traded above $6M. The gated section commands the highest values; backing onto the golf course adds a meaningful premium. Catchment schools include Morgan Elementary, Rosemary Heights Elementary, and Grandview Heights Secondary, plus SouthRidge private school (K-12)."),
                ("Grandview Heights", "Newer custom homes typically range from $2.2M\u2013$4.5M. The newest builds on the larger Highway 99 view lots can reach $5M+. Grandview is one of the most active luxury markets in the Lower Mainland, with strong demand from move-up buyers and Vancouver expats. Shopping at Morgan Crossing and Grandview Corners is nearby."),
                ("White Rock Waterfront &amp; Hillside", "Direct ocean-view properties along the hillside typically range from $2.5M\u2013$6M, with the few true waterfront lots commanding $7M\u2013$12M+. View preservation, slope conditions, and lot configuration are critical factors that change values dramatically within a single block."),
                ("Elgin Chantrell &amp; Crescent Beach", "Acreage estates in Elgin Chantrell start around $3M and climb past $8M for premier multi-acre properties with custom homes, equestrian setups, or cottage compounds. Crescent Beach itself offers smaller lots but premium beach proximity at $2.5M\u2013$5M for renovated character homes and new builds."),
            ],
            tip_heading="A note on how Manan prices luxury property",
            tip_text="Land \u2014 lot size, location, view corridor, and zoning \u2014 is the most durable driver of value in this market. Finishes and floor plans get renovated every 15\u201320 years; the lot doesn't change. When evaluating a luxury purchase or listing, Manan weighs the land first and the structure second."
        ),
        faq=[
            ("What defines a luxury home in South Surrey?", "In the South Surrey and White Rock market, the luxury threshold typically starts around $2 million and runs well into the $5\u201310 million range for waterfront, acreage, and architect-designed estates. Beyond price, luxury here means custom construction, premium finishes, larger lots (often half-acre to multi-acre in Elgin Chantrell or Morgan Creek), specialty features like wine cellars, theatre rooms, and gated entries, and irreplaceable locations such as ocean frontage, golf course backing, or panoramic mountain views."),
            ("Are luxury homes a good investment in BC?", "Luxury property tends to behave differently from the broader market \u2014 it's less liquid, with fewer qualified buyers and longer average days on market, but the land component is highly durable. Irreplaceable attributes like ocean frontage or a large lot in an established estate pocket hold value in ways that finishes and floor plans don't. Manan's view is that the land drives long-term value; treat the house as a depreciating asset sitting on an appreciating one."),
            ("What is the buying process for a $2M+ home?", "The mechanics are similar to any purchase, but the details carry more weight. Expect a longer due-diligence window, a private (rather than public open house) showing schedule, a more detailed inspection scope covering things like building envelope, drainage, and specialty systems, and closer coordination with your lawyer and lender. Financing conditions typically need more time than a standard purchase, so build that into your subject removal dates."),
            ("Should I get a private inspection for a luxury property?", "Yes \u2014 and often more than one. Large custom homes frequently warrant specialists beyond a general inspector: building envelope consultants for stucco or flat-roof construction, geotechnical review for hillside and slope lots (particularly relevant along the White Rock hillside), and specialty trades for pools, elevators, and home automation systems. The cost is minor relative to the purchase price."),
            ("How does luxury home financing differ?", "Above roughly $1.5 million, mortgages are uninsurable in Canada, meaning a minimum 20% down payment and no CMHC insurance option. Many lenders apply tighter qualification and appraisal scrutiny at higher price points, and some cap their exposure on a single property. Buyers at this level often work with lenders or private financing that specialize in high-value residential. Manan can point you toward brokers who work in this segment regularly."),
            ("What is the typical commission structure on luxury sales?", "Commission in BC is negotiable on every transaction and isn't set by any board or regulator. On higher-value properties, the structure is typically discussed up front as part of the listing conversation, alongside the marketing budget \u2014 professional photography, video, and targeted exposure cost more on an estate property than a standard listing. Manan will lay out exactly what's proposed and what it covers before you sign anything."),
        ],
        related=[
            dict(title="Relocating to BC", desc="Moving from out of province for a luxury purchase? Start here.", href="/buyers/relocation/"),
            dict(title="White Rock / South Surrey", desc="Explore the community most associated with the region's premium market.", href="/communities/south-surrey/"),
            dict(title="Buy a Home", desc="Back to the full buyer representation overview.", href="/buyers/"),
        ],
        area_slugs=['morgan-creek', 'grandview-heights', 'ocean-park', 'south-surrey', 'elgin-chantrell', 'panorama-ridge']
    )
)

write_page(
    '/buyers/relocation/',
    "Relocating to BC | Remote Buyer Support | Manan Bhullar",
    "Moving to Surrey or the Lower Mainland from out of province? Manan Bhullar helps remote buyers find the right community and home.",
    crumbs(("Buy a Home", "/buyers/"), ("Relocating to BC", None)),
    simple_service_page(
        '/buyers/relocation/', 'Relocating to BC', 'Moving to BC',
        'Relocating to BC',
        "Moving from Alberta, Ontario, or anywhere else? Manan helps out-of-province and remote buyers understand BC's market and find the right community \u2014 often before they've had a chance to visit in person.",
        [
            dict(icon="\U0001F310", title="Virtual Tours &amp; Video Walkthroughs", desc="Detailed video walkthroughs and live video calls for buyers who can't view properties in person before an offer."),
            dict(icon="\U0001F4CD", title="Neighbourhood Orientation", desc="An honest breakdown of each community's character, commute, and lifestyle fit \u2014 not just the listing sheet."),
            dict(icon="\U0001F4C5", title="Coordinated Timelines", desc="Aligning your move, financing, and closing dates so the transition to BC is as seamless as possible."),
        ],
        faq=[
            ("Can I buy a home in BC if I am not yet living here?", "Yes \u2014 Canadian citizens and permanent residents can buy property anywhere in BC regardless of where they currently live. The federal foreign buyer ban applies to non-Canadians, not to someone relocating from Alberta, Ontario, or another province. You can sign documents remotely through electronic signature or with a notary in your home province, and your BC lawyer or notary coordinates closing whether or not you've arrived."),
            ("How do I qualify for a mortgage when relocating?", "Most national lenders will work with you before you've moved, but they'll want to see employment continuity \u2014 a signed offer letter from your new BC employer, or evidence your existing income continues (remote work, a transfer, self-employment history). If you're between jobs during the move, that's the piece most likely to complicate approval, so get pre-approved before you resign anything."),
            ("What should I know about BC's foreign buyer tax and other property taxes?", "BC's Additional Property Transfer Tax is 20% and applies to foreign nationals purchasing in designated regions including Metro Vancouver and parts of the Fraser Valley \u2014 it does not apply to Canadian citizens or permanent residents relocating from another province. Separately, BC's Speculation and Vacancy Tax applies to properties left vacant, which is worth understanding if there's a gap between your purchase and your move."),
            ("How do BC's closing costs compare to other provinces?", "BC charges Property Transfer Tax on purchase \u2014 1% on the first $200,000, 2% from $200,000 to $2 million, 3% from $2 million to $3 million, and an additional 2% on the residential portion above $3 million (a 5% marginal rate on that slice). On a $900,000 home that's $16,000. First-time buyers may be fully exempt up to $835,000 and partially up to $860,000; there's a separate newly-built-home exemption up to $1.1 million. Beyond PTT, budget for legal or notary fees, title insurance, adjustments, and inspection."),
            ("How long should my relocation house hunt take?", "Most out-of-province buyers spend a few weeks narrowing communities remotely, then plan one focused in-person trip covering their shortlist. If your timeline is tight, that trip can be compressed into a few days of back-to-back showings. If you have flexibility, more time in the market almost always produces a better decision."),
            ("Should I rent first or buy right away when moving to BC?", "If your move isn't immediate, renting for three to six months is often the cheapest market research you can buy. Neighbourhoods that look ideal online can turn out to have a commute, school catchment, or feel that doesn't fit. That said, if you're confident about the area and the market is moving in your favour, buying directly avoids two moves and two sets of costs. Manan will give you a straight read either way."),
        ],
        related=[
            dict(title="First-Time Buyers", desc="Moving to BC for your first home purchase? Check the current programs.", href="/buyers/first-time/"),
            dict(title="Areas I Serve", desc="Get a feel for Surrey and Lower Mainland communities before you visit.", href="/communities/"),
            dict(title="Buy a Home", desc="Back to the full buyer representation overview.", href="/buyers/"),
        ]
    )
)

# ============================================================
# /sellers/  — Sell Your Property hub
# ============================================================
sellers_body = subhero(
    "Seller Representation",
    'Sell Your Property for <span class="accent-warm">Top Dollar</span>',
    "A clear pricing, marketing, and negotiation strategy \u2014 built around your property and your timeline.",
    TEXT_CTA + EVAL_CTA
)
sellers_body += market_snapshot_section()
sellers_body += step_section(
    "How Manan Sells Your Home",
    "A straightforward process from first conversation to closing.",
    [
        dict(title="Free Home Evaluation", desc="A market-based assessment of your property's value, backed by current comparable sales."),
        dict(title="Pricing &amp; Prep Strategy", desc="A conversation about pricing strategy and any prep work \u2014 staging, minor repairs, photography \u2014 that will maximize your return."),
        dict(title="Marketing Launch", desc="Professional photography, MLS\u00ae listing, and targeted marketing to reach qualified buyers."),
        dict(title="Showings &amp; Offers", desc="Coordinated showings and skilled negotiation on every offer that comes in, always with your interests first."),
        dict(title="Subject Removal", desc="Guidance through the buyer's inspection, financing, and any other subject conditions."),
        dict(title="Closing", desc="Coordination with your lawyer or notary through to completion and possession day."),
    ]
)
sellers_body += simple_cards(
    "Seller Services", "Whatever stage you're at in the selling process.",
    [
        dict(title="Free Home Evaluation", desc="Find out what your home is worth in today's market \u2014 no cost, no obligation.", href="/sellers/home-evaluation/"),
        dict(title="Downsizing", desc="A thoughtful, well-paced plan for empty nesters and retirees moving to their next chapter.", href="/sellers/downsizing/"),
    ],
    cols=2, raised=True
)
sellers_body += faq_section("Selling Questions, Answered", [
    ("How much does it cost to sell a home in BC?", "The main cost is commission, which is negotiable and agreed with your realtor before listing \u2014 there's no fixed rate set by any board. Beyond that, budget for any prep or staging costs, a lawyer or notary for closing, and mortgage discharge fees if applicable. Unlike buying, there's no property transfer tax on the sale side; that's a buyer's cost."),
    ("Do I pay tax on the sale of my home?", "If it was your principal residence for the entire time you owned it, the gain is generally exempt from federal capital gains tax under the Principal Residence Exemption. If you sell within 730 days of buying, BC's home flipping tax may also apply \u2014 up to 20% of the profit in year one, sliding to zero at the two-year mark, with only a capped $20,000 deduction for primary residences, not a full exemption. This is accountant territory for anything beyond a straightforward long-held principal residence."),
    ("How long does it typically take to sell a home in the Fraser Valley?", "It depends heavily on price point, condition, and current market conditions \u2014 inventory has been elevated recently, which tends to lengthen days on market compared to a tighter seller's market. Manan will give you a realistic estimate based on current activity for your specific property type and area, not a generic average."),
    ("Should I renovate before selling, or sell as-is?", "It depends on the return. Cosmetic work \u2014 paint, decluttering, minor repairs \u2014 almost always pays for itself. Major renovations rarely return their full cost at resale and can delay your listing. Manan will walk your property and tell you honestly what's worth doing and what isn't before you spend a dollar."),
    ("What's the difference between list price and assessed value?", "BC Assessment values are calculated once a year for property tax purposes and often lag the current market by months. List price is based on recent comparable sales and current demand, which is what your home will actually transact at. The two numbers can differ significantly, especially in a fast-moving market \u2014 don't anchor your expectations to your assessment notice."),
    ("Can I sell and buy at the same time without ending up homeless in between?", "Yes \u2014 this is common, and there are a few ways to structure it: a subject-to-sale offer on your purchase, a rent-back arrangement with your buyer after closing, bridge financing to cover the gap, or timing both completion dates to align. Manan coordinates this regularly for sellers who are also buying and will walk through which option fits your situation."),
])
sellers_body += cta_band(
    'Curious What Your <span class="accent-warm">Home Is Worth</span>?',
    "Start with a free, no-obligation home evaluation.",
    TEXT_CTA + EVAL_CTA
)
write_page(
    '/sellers/',
    "Sell Your Property | Surrey & Lower Mainland | Manan Bhullar",
    "Sell your home for top dollar with a clear pricing, marketing, and negotiation strategy from Manan Bhullar.",
    crumbs(("Sell Your Property", None)),
    sellers_body
)

# /sellers/home-evaluation/
he_body = subhero(
    "Free & No-Obligation",
    'What Is Your Home <span class="accent-warm">Worth?</span>',
    "Get a market-based home evaluation from Manan Bhullar \u2014 free, no obligation, no pressure.",
    TEXT_CTA + CONTACT_CTA
)
he_body += f"""<section class="content-section">
  <div class="wrap two-col">
    <div>
      <h2>How the Evaluation Works</h2>
      <p style="color:var(--ink-soft);margin-top:14px;">Manan reviews current comparable sales, active listings, and your property's specific features and condition to give you a realistic, market-based estimate \u2014 not an inflated number designed to win your listing.</p>
      <div class="point-list">
        <div class="point"><div class="dot">\U0001F4CA</div><div><strong>Comparable Sales Review</strong><span>Recent, relevant sales in your immediate area and property type.</span></div></div>
        <div class="point"><div class="dot">\U0001F3E0</div><div><strong>Property Walkthrough</strong><span>An in-person or video walkthrough to account for condition, upgrades, and unique features.</span></div></div>
        <div class="point"><div class="dot">\U0001F4DD</div><div><strong>Written Summary</strong><span>A clear written estimate with the reasoning behind it, so you understand exactly how the number was reached.</span></div></div>
      </div>
    </div>
    <img class="imgblock" src="https://picsum.photos/seed/home-evaluation/800/600" alt="Free home evaluation walkthrough (sample photo)" loading="lazy" width="800" height="600">
  </div>
</section>"""
he_body += market_snapshot_section()
he_body += faq_section("Home Evaluation Questions, Answered", [
    ("Is the evaluation really free, with no obligation?", "Yes. There's no cost and no requirement to list with Manan afterward \u2014 it's a genuine starting point for homeowners who want a realistic sense of value, whether they're selling soon, refinancing, or just curious."),
    ("How accurate is a home evaluation compared to a formal appraisal?", "A realtor's evaluation is based on current comparable sales and live market activity, which is generally reliable for setting a list price. A formal bank appraisal is a separate, more rigid process typically required for financing, often using slightly different criteria, and can land somewhat differently than a market evaluation."),
    ("Does my home need to be tidy or staged for the evaluation?", "Not for the evaluation itself \u2014 Manan can account for condition and clutter mentally during the walkthrough. If you decide to sell, that's when prep and staging conversations become worth having, before photos and showings."),
    ("How long does the evaluation process take?", "The walkthrough typically takes well under an hour. A written estimate follows shortly after, once comparable sales in your immediate area have been pulled and reviewed."),
    ("What factors affect my home's value the most?", "Location and comparable recent sales carry the most weight, followed by size, lot, condition, and updates \u2014 kitchens and bathrooms especially. Market timing matters too: the same home can evaluate differently a few months apart if inventory or interest rates shift. Manan will walk through what's specifically driving your number, not just hand you a figure."),
    ("How often should I get my home evaluated if I'm not selling yet?", "Roughly once a year is reasonable if you're tracking equity for planning purposes \u2014 refinancing, an eventual sale, or just staying informed. Market conditions can move meaningfully within 12 months, so a number from a couple of years ago may no longer reflect reality."),
])
he_eval_form = lead_form(
    "Get My Free Evaluation",
    "New Home Evaluation Request \u2014 mananbhullar.com",
    extra_fields='<input type="text" name="property_address" placeholder="Property Address" required style="margin-bottom:12px;"><select name="timeline"><option>What\u2019s your timeline?</option><option>Just curious</option><option>Selling in 3\u201312 months</option><option>Ready to list now</option></select>',
    message_placeholder="Anything else Manan should know? (optional)"
)
he_body += f"""<section class="cta-form-band">
  <div class="wrap cta-form-grid">
    <div class="cta-form-left">
      <h2>Request Your <span class="accent-warm">Free Evaluation</span></h2>
      <p>Share your address and Manan will follow up with a realistic, market-based estimate \u2014 free, no obligation, no pressure.</p>
      <div class="phone-line">\U0001F4DE <a href="tel:+16047279542">(604) 727-9542</a></div>
    </div>
    {he_eval_form}
  </div>
</section>"""
write_page(
    '/sellers/home-evaluation/',
    "Free Home Evaluation | Manan Bhullar",
    "Get a free, no-obligation home evaluation from Manan Bhullar, Surrey BC.",
    crumbs(("Sell Your Property", "/sellers/"), ("Free Home Evaluation", None)),
    he_body
)

# /sellers/downsizing/
ds_body = subhero(
    "Empty Nesters & Retirees",
    'A Thoughtful Approach to <span class="accent-warm">Downsizing</span>',
    "Selling the family home and moving to your next chapter is a big transition \u2014 Manan helps make it a well-paced, low-stress one.",
    TEXT_CTA + CONTACT_CTA
)
ds_body += point_list_section(
    False, "Downsizing", "What Sets a Downsizing Sale Apart", "",
    [
        dict(icon="\u23F1\uFE0F", title="A Timeline That Works For You", desc="Downsizing sales often need to be coordinated with a purchase, a move, or family logistics \u2014 Manan plans around your timeline, not a generic template."),
        dict(icon="\U0001F91D", title="Trusted Referrals", desc="Recommendations for movers, estate sale services, and other trades that many downsizing sellers find helpful."),
        dict(icon="\U0001F4AC", title="Patient, Clear Communication", desc="No pressure, no jargon \u2014 every step explained clearly, with as much or as little involvement from family as you'd like."),
    ],
    img_first=True, img_seed='downsizing-move', img_alt="Downsizing to a new home (sample photo)"
)
ds_body += faq_section("Downsizing Questions, Answered", [
    ("Should I sell my current home before buying the next one?", "It depends on your equity, financing options, and risk tolerance. Manan can walk through the trade-offs of selling first versus buying first, including options like a subject-to-sale offer, a rent-back after your sale closes, or bridge financing, based on your specific numbers."),
    ("What happens to belongings I'm not taking with me?", "Many downsizing sellers work with an estate sale company, donation services, or family members to handle belongings ahead of a move. Manan can share names of services other clients have found helpful, and plan the listing timeline around when the home will actually be clear."),
    ("Do I need to renovate before selling?", "Usually not extensively \u2014 for most downsizing sales, a clean, decluttered, well-maintained home shows well without a major renovation budget. Manan can advise on what's actually worth doing versus skipping, since over-improving before a downsize rarely pays for itself."),
    ("How much say can family members have in the process?", "As much or as little as you'd like. Some sellers want family closely involved in decisions; others prefer to keep it simple and stay informed after the fact. Manan follows your lead and can loop in adult children on pricing or timeline conversations if that's helpful."),
    ("Is downsizing to a condo or townhome a good financial move?", "Often, yes \u2014 selling a larger home and moving to a smaller condo or townhome typically releases equity, and can eliminate or significantly reduce a mortgage. Weigh that against ongoing strata fees, which replace some maintenance costs but aren't nothing. Manan can run the numbers on your specific scenario before you decide."),
    ("What's the best time of year to sell when downsizing?", "There's no single right answer \u2014 spring and early fall tend to see more buyer activity in the Fraser Valley, but the better question is usually what fits your timeline and your next home's availability, rather than chasing a seasonal peak. Manan will tell you honestly if waiting a season would meaningfully help, or if it's not worth the delay."),
])
ds_body += cta_band(
    'Thinking About Your <span class="accent-warm">Next Chapter</span>?',
    "A relaxed, no-obligation conversation is a good place to start.",
    TEXT_CTA + CONTACT_CTA
)
write_page(
    '/sellers/downsizing/',
    "Downsizing | Empty Nesters & Retirees | Manan Bhullar",
    "A thoughtful, well-paced downsizing process for empty nesters and retirees in Surrey and the Lower Mainland, with Manan Bhullar.",
    crumbs(("Sell Your Property", "/sellers/"), ("Downsizing", None)),
    ds_body
)

# ============================================================
# /commercial/  — Commercial Real Estate hub
# ============================================================
def market_context_section(heading, paragraphs, img_seed, img_alt, fact_label=None, fact_value=None):
    paras_html = ''.join(f'<p style="color:var(--ink-soft);margin-top:14px;">{p}</p>' for p in paragraphs)
    if img_seed in REAL_PHOTOS:
        src, w, h = REAL_PHOTOS[img_seed]
    else:
        src, w, h = f"https://picsum.photos/seed/{img_seed}/900/675", 900, 675
    badge_html = ''
    if fact_label:
        badge_html = f'<div class="market-fact-badge"><span>{fact_label}</span><strong>{fact_value}</strong></div>'
    return f"""<section class="content-section">
  <div class="wrap two-col">
    <div>
      <h2>{heading}</h2>
      {paras_html}
    </div>
    <div class="market-context-photo">
      <img src="{src}" alt="{img_alt}" loading="lazy" width="{w}" height="{h}">
      {badge_html}
    </div>
  </div>
</section>"""

comm_body = subhero(
    "Commercial & Industrial",
    'Commercial Real Estate <span class="accent-warm">Across the Lower Mainland</span>',
    "From industrial and warehouse leasing to retail, hospitality, and land \u2014 Manan brings the same client-first approach to commercial transactions across 17 specialized categories.",
    TEXT_CTA + CONTACT_CTA
)

COMMERCIAL_CATEGORIES = [
    dict(slug='industrial', title='Industrial &amp; Warehouse', icon='\U0001F3ED', desc="Leasing and distribution space across the Surrey industrial corridor."),
    dict(slug='retail', title='Retail Spaces', icon='\U0001F6CD\uFE0F', desc="Storefronts and strip-mall units for owner-operators and investors."),
    dict(slug='hotels-motels', title='Hotels &amp; Motels', icon='\U0001F3E8', desc="Hospitality property sales across the region."),
    dict(slug='liquor-stores', title='Liquor Stores', icon='\U0001F943', desc="Licensed retail business sales, including asset and share transactions."),
    dict(slug='land', title='Land &amp; Subdivisions', icon='\U0001F4D0', desc="Development land and subdivision opportunities."),
    dict(slug='gas-stations', title='Gas Stations', icon='\u26FD', desc="Branded and independent fuel retail sites, with environmental due diligence."),
    dict(slug='convenience-stores', title='Convenience Stores', icon='\U0001F3EA', desc="Independent c-stores \u2014 tobacco, lottery, and lease-based business sales."),
    dict(slug='restaurants', title='Restaurants', icon='\U0001F37D\uFE0F', desc="Independent and franchise food businesses, from lease review to licence transfer."),
    dict(slug='apartment-buildings', title='Apartment Buildings', icon='\U0001F3D9\uFE0F', desc="4-plex to 60+ unit purpose-built rental buildings and value-add opportunities."),
    dict(slug='self-storage', title='Self-Storage', icon='\U0001F4E6', desc="Climate-controlled and drive-up facilities, valued on occupancy and rate growth."),
    dict(slug='truck-yards', title='Truck Yards', icon='\U0001F69B', desc="Fleet and trailer drop yards across the Surrey, Delta, and Langley industrial corridor."),
    dict(slug='banquet-halls', title='Banquet Halls', icon='\U0001F382', desc="Event venues and reception halls, including South Asian wedding venues."),
    dict(slug='auto-dealerships', title='Auto Dealerships', icon='\U0001F697', desc="New car franchise and used car dealership real estate and business sales."),
    dict(slug='daycares-childcare', title='Daycares &amp; Childcare', icon='\U0001F9F8', desc="Licensed child care and preschool businesses, including $10/Day program sites."),
    dict(slug='car-washes', title='Car Washes', icon='\U0001F697', desc="Tunnel, in-bay automatic, and self-serve wash facilities."),
    dict(slug='farms-alr-land', title='Farms &amp; ALR Land', icon='\U0001F69C', desc="Agricultural properties, ALR compliance, and quota considerations."),
]
def cc_href(slug): return f"/commercial/{slug}/"

def commercial_cta_form(category_name, related_slugs, form_title=None):
    ft = form_title or f"{category_name} Inquiry"
    pills = ''.join(f'<a href="{cc_href(s)}">{next(c["title"] for c in COMMERCIAL_CATEGORIES if c["slug"]==s)} \u2192</a>' for s in related_slugs)
    pills += '<a href="/commercial/">All Commercial \u2192</a>'
    form = lead_form(ft, f"New {category_name} Inquiry \u2014 mananbhullar.com")
    return f"""<section class="cta-form-band">
  <div class="wrap cta-form-grid">
    <div class="cta-form-left">
      <h2>Buying or Selling <span class="accent-warm">{category_name}</span>?</h2>
      <p>Every transaction in this category has its own rhythm and considerations \u2014 let's have a direct conversation about yours.</p>
      <div class="phone-line">\U0001F4DE <a href="tel:+16047279542">(604) 727-9542</a></div>
      <div class="cta-form-pills">{pills}</div>
    </div>
    {form}
  </div>
</section>"""

comm_body += point_list_section(
    False, "Why Manan", "Why Choose Manan for Commercial Real Estate?",
    "Commercial real estate requires specialized knowledge across a wide range of property and business types. Manan brings Fraser Valley market knowledge, thorough due diligence, and a network built across residential and commercial alike.",
    [
        dict(icon="\U0001F4CA", title="Market Analysis", desc="Comparable sales data and market studies specific to the property type in question."),
        dict(icon="\U0001F6E1\uFE0F", title="Due Diligence", desc="Thorough evaluation covering zoning, environmental, licensing, and financial factors relevant to each category."),
        dict(icon="\U0001F91D", title="Investor Network", desc="Access to a network of commercial buyers, sellers, and industry professionals across the Lower Mainland."),
        dict(icon="\U0001F4C8", title="Investment Strategy", desc="Straight advice on property selection and what a given deal means for your broader portfolio."),
    ],
    img_first=False, img_seed='commercial-hub-office', img_alt="Modern commercial interior"
)
comm_body += simple_cards(
    "Commercial Real Estate Markets I Serve", "Deep familiarity with the specific corridors and submarkets that matter in each city.",
    [
        dict(title="Surrey", desc="City Centre development, King George corridor, Newton industrial.", href="/communities/surrey/", icon="\U0001F4CD"),
        dict(title="Langley", desc="Gloucester Industrial, Willoughby retail, City of Langley downtown.", href="/communities/langley/", icon="\U0001F4CD"),
        dict(title="Abbotsford", desc="Clearbrook Road retail, airport area, highway commercial.", href="/communities/abbotsford/", icon="\U0001F4CD"),
        dict(title="Chilliwack", desc="Downtown revitalization, Yale Road corridor, Vedder crossing.", href="/communities/chilliwack/", icon="\U0001F4CD"),
        dict(title="Mission", desc="Development land, downtown commercial, junction area.", href="/communities/mission/", icon="\U0001F4CD"),
        dict(title="Maple Ridge", desc="Town centre, Lougheed Highway, Albion industrial.", href="/communities/maple-ridge/", icon="\U0001F4CD"),
    ],
    cols=3, raised=True
)
comm_body += simple_cards(
    "Explore Our Commercial Services", "Specialized real estate representation across 17 commercial property and business categories, each with its own valuation, due diligence, and financing approach.",
    [dict(title=c['title'], desc=c['desc'], href=cc_href(c['slug']), icon=c['icon']) for c in COMMERCIAL_CATEGORIES],
    cols=4, raised=False
)
comm_body += commercial_cta_form("Commercial Property", ['industrial', 'retail'], form_title="Commercial Property Inquiry")
write_page(
    '/commercial/',
    "Commercial Real Estate | Surrey & Lower Mainland | Manan Bhullar",
    "Commercial and industrial real estate services across Surrey and the Lower Mainland \u2014 industrial, retail, hospitality, and land, with Manan Bhullar.",
    crumbs(("Commercial &amp; Industrial", None)),
    comm_body
)

def commercial_sub(path, label, icon, eyebrow_tag, h1, lead,
                    market_heading, market_paragraphs, market_photo_seed,
                    valued_title, valued_sub, valued_items,
                    dd_title, dd_sub, dd_items,
                    middle_section="", faq=None, related_slugs=None):
    slug = path.strip('/').split('/')[-1]
    body = f"""<section class="subhero">
  <div class="wrap">
    <div class="eyebrow">{icon} {eyebrow_tag}</div>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="hero-ctas">{TEXT_CTA}{CONTACT_CTA}</div>
  </div>
</section>"""
    body += market_context_section(market_heading, market_paragraphs, market_photo_seed, f"{label} (sample photo)")
    body += info_cards(valued_title, valued_sub, valued_items, cols=2, raised=True)
    body += middle_section
    body += info_cards(dd_title, dd_sub, dd_items, cols=3, raised=False)
    if faq:
        body += faq_section(f"{label} Questions, Answered", faq)
    rel = related_slugs or [c['slug'] for c in COMMERCIAL_CATEGORIES if c['slug'] != slug][:2]
    body += commercial_cta_form(label, rel)
    write_page(
        path,
        f"{label} | Commercial Real Estate | Manan Bhullar",
        f"{label} across Surrey and the Lower Mainland, part of Manan Bhullar's commercial and industrial real estate practice.",
        crumbs(("Commercial &amp; Industrial", "/commercial/"), (label, None)),
        body
    )

def dd(icon, title, desc): return dict(icon=icon, title=title, desc=desc)
def vv(icon, title, desc): return dict(icon=icon, title=title, desc=desc)

COMMERCIAL_PAGES = [
dict(slug='industrial', label='Industrial &amp; Warehouse', icon='\U0001F3ED', tag='Industrial Specialist',
    lead="Warehouse, distribution, and light-industrial space across Surrey's fast-growing industrial corridor \u2014 for both tenants and owners.",
    m_heading="Surrey's Industrial Market: Tight Supply, Strong Demand",
    m_paras=["Surrey's industrial corridor \u2014 anchored by Campbell Heights and the Highway 10 corridor \u2014 has become one of the Lower Mainland's fastest-growing hubs for warehouse, distribution, and light-industrial space, driven by e-commerce growth and the city's position between the port and inland markets.",
             "Industrial zoning is limited and municipalities have been tightening permissions for outdoor and lower-intensity uses, keeping vacancy tight for modern, high-ceiling, dock-loading space. Older or smaller-format buildings see more availability, but at a real trade-off in functionality."],
    m_photo='industrial-warehouse-interior',
    valued=[vv("\U0001F4CF","Clear Height & Configuration","Modern distribution tenants often want 28\u201336 feet of clear height for racking; manufacturing users may prioritize power capacity and floor drains instead."),
            vv("\U0001F69B","Highway & Loading Access","Proximity to major highways and dock-level loading configuration directly affect both lease rates and resale value."),
            vv("\U0001F4DD","Lease Structure","Net (NNN) leases are standard in this market \u2014 tenant pays base rent plus their share of taxes, insurance, and CAM."),
            vv("\U0001F3D7\uFE0F","Building Age & Systems","Sprinkler coverage, power capacity, and envelope condition all factor into value alongside pure square footage.")],
    dd_items=[dd("🧪","Environmental History","Checking for contamination risk, especially on older sites or former manufacturing use \u2014 a Phase I assessment is standard due diligence."),
              dd("🗺️","Zoning Compliance","Confirming the property's zoning explicitly permits your intended use, not assumed from how a similar building nearby is used."),
              dd("🛣️","Loading & Access","Verifying truck turning radius, dock configuration, and clear height match your operational needs."),
              dd("⚡","Power Capacity","Confirming available electrical service is adequate for your equipment \u2014 upgrades can be a significant unplanned cost."),
              dd("📄","Lease Cost History","Reviewing actual CAM costs from recent years, not just landlord estimates, before comparing net-lease options."),
              dd("📐","Easements & Right-of-Way","Checking for any registered easements or right-of-way restrictions affecting usable yard space.")],
    faq=[
        ("What clear height do most industrial tenants look for?", "It varies by use \u2014 modern distribution and logistics tenants often want 28\u201336 feet of clear height for racking, while lighter industrial or manufacturing users may need less but more power capacity or floor drains instead. Manan matches a space's specs to your actual operation rather than a generic checklist."),
        ("Is it better to lease or buy industrial space?", "Owning builds equity, locks in occupancy costs, and can generate rental income from surplus space \u2014 but ties up capital and limits flexibility to relocate. Leasing preserves capital for operations and lets you resize as the business grows, at the cost of rent escalations and no equity buildup."),
        ("How competitive is Surrey's industrial market right now?", "Surrey's industrial corridor \u2014 particularly Campbell Heights and the Highway 10 corridor \u2014 has seen strong demand driven by e-commerce growth and its position between the port and inland markets, keeping vacancy tight for modern, high-ceiling, dock-loading space."),
        ("What's the difference between a net lease and a gross lease for industrial space?", "In a net (or triple net/NNN) lease, the tenant pays base rent plus their share of property tax, insurance, and common area maintenance \u2014 the standard structure for industrial space in this market. In a gross lease, the landlord bundles those costs into one rent figure."),
        ("What due diligence is specific to buying industrial property?", "Beyond a standard building inspection, industrial buyers should check for environmental contamination history, zoning compliance for your specific use, loading and truck turning radius adequacy, power capacity for your equipment, and any easements affecting yard space."),
        ("Can I convert a warehouse to include office or retail space?", "Sometimes, but it depends entirely on the municipal zoning designation \u2014 industrial zoning often caps the allowable office or retail component as a percentage of total floor area. This needs confirmation with the municipality before you count on it."),
    ], related=['retail','land']),

dict(slug='retail', label='Retail Spaces', icon='\U0001F6CD\uFE0F', tag='Retail Specialist',
    lead="Storefronts and strip-mall units for owner-operators, franchisees, and investors across the Lower Mainland.",
    m_heading="Location Is Everything in Retail",
    m_paras=["Retail success depends heavily on location. Evaluating a retail property means looking at foot traffic patterns, vehicle counts, visibility from the road, parking adequacy, and the surrounding tenant mix \u2014 a space that works for one business may not work for another.",
             "The Fraser Valley's rapid population growth is creating new retail demand across established and emerging corridors, from King George Boulevard to Willoughby's newer developments. Understanding where growth is concentrated helps identify the strongest retail opportunities."],
    m_photo='retail-storefront-strip',
    valued=[vv("\U0001F6B6","Foot Traffic & Visibility","Corner locations and high vehicle counts command meaningful rent premiums over interior strip-mall units."),
            vv("\U0001F3EA","Tenant Mix","The surrounding tenant mix affects draw \u2014 anchor tenants like grocery stores support smaller shops nearby."),
            vv("\U0001F4C4","Lease Structure","Triple net (NNN) is the standard structure in Fraser Valley retail, with tenants covering their share of operating costs."),
            vv("\U0001F17F\uFE0F","Parking & Access","Adequate parking and drive-through capability matter significantly for specific retail categories.")],
    dd_items=[dd("🗺️","Permitted Use","Confirming your business matches the zoning and lease's use clause before signing."),
              dd("🚫","Exclusivity Clauses","Checking whether a competing tenant could move in next door under the existing lease terms."),
              dd("💰","CAM Cost History","Reviewing actual common-area-maintenance costs from recent years, not just landlord estimates."),
              dd("🅿️","Parking Allocation","Verifying your allotted parking stalls match what your business actually needs."),
              dd("🔧","Maintenance Responsibility","Clarifying who's responsible for HVAC, roof, and structural repairs under the lease."),
              dd("🛣️","Traffic & Demographic Data","Reviewing vehicle counts and neighbourhood demographics relevant to your specific retail category.")],
    faq=[
        ("What lease term is typical for a retail space?", "Terms commonly run three to five years for a strip-mall unit, with renewal options built in, and longer for standalone or anchor-tenant space."),
        ("What's a tenant improvement allowance?", "It's a landlord contribution toward your build-out costs \u2014 flooring, fixtures, HVAC modifications, signage \u2014 negotiated as part of the lease. Not every landlord offers one."),
        ("Should I buy or lease a retail space for my business?", "Leasing offers flexibility and lower upfront capital \u2014 the right call for a newer or unproven business. Buying builds equity if you're confident in the location long-term."),
        ("What's the difference between triple net (NNN) and gross retail leases?", "In a triple net lease, the tenant pays base rent plus a proportional share of property tax, insurance, and CAM. A gross lease bundles everything into one monthly payment, usually at a higher base rent."),
        ("How much does foot traffic and visibility actually affect retail value or rent?", "Significantly \u2014 corner locations and high vehicle counts command meaningful premiums over interior strip-mall units for comparable square footage."),
        ("What should I check before signing a retail lease?", "Permitted use match, exclusivity clauses, CAM cost history, parking allocation, and maintenance responsibility split."),
    ], related=['industrial','land']),

dict(slug='hotels-motels', label='Hotels &amp; Motels', icon='\U0001F3E8', tag='Hospitality Specialist',
    lead="Hospitality property sales across the region \u2014 a specialized asset class that calls for discretion and market-specific experience.",
    m_heading="Buying a Hotel Means Buying a Business, Not Just Real Estate",
    m_paras=["Purchasing a hotel or motel is fundamentally different from buying other commercial real estate \u2014 you are buying both a property and a business. Every aspect requires specialized due diligence, from financial performance to licensing to zoning.",
             "The Fraser Valley benefits from year-round tourism around Harrison Hot Springs and Cultus Lake, growing agri-tourism in the eastern valley, and steady Highway 1 corridor motel demand from travellers between Vancouver and the Interior."],
    m_photo='hospitality-pool-resort',
    valued=[vv("\U0001F4CA","Revenue & Occupancy","Reviewing at least three years of financials, seasonal occupancy rates, ADR, and RevPAR to assess true profitability."),
            vv("\U0001F4DC","Licensing & Permits","Business licences, health authority permits, liquor licences if applicable, and Tourism BC compliance requirements."),
            vv("\U0001F4CD","Zoning & Land Use","Confirming proper zoning for hospitality use and understanding any restrictions on expansion or rezoning potential."),
            vv("\U0001F4B5","Commercial Financing","Hospitality financing evaluates business income, not just the real estate \u2014 a different lender conversation than standard commercial.")],
    dd_items=[dd("📊","Financial Statements","At least three years of statements, occupancy by season, ADR, and RevPAR trends."),
              dd("📋","Licensing Transfer","Understanding what business licences and permits transfer with the sale versus need reapplication."),
              dd("👥","Staff & Operations","Reviewing staffing levels, management structure, and operational continuity through a transition."),
              dd("🤝","Brand & Franchise Agreements","If flagged, confirming franchise agreement terms, fees, and approval requirements for a change of ownership."),
              dd("🔧","Physical Condition","PIP (Property Improvement Plan) requirements for branded properties, deferred maintenance, and capital reserve adequacy."),
              dd("🤫","Confidentiality Process","Discreet marketing to protect ongoing operations and staff during the sale process.")],
    faq=[
        ("Is a hotel or motel sale handled differently from other commercial real estate?", "Yes \u2014 you're buying both a property and a business. Financial review typically covers at least three years of statements, occupancy rates by season, ADR, and RevPAR, on top of standard property due diligence."),
        ("How is confidentiality maintained during a hotel sale?", "Marketing is typically handled discreetly, often without a public listing, to avoid disrupting ongoing operations, staff morale, or guest relationships during the sale process."),
        ("What licensing is required to buy a hotel or motel in BC?", "Requirements vary by property but can include a business licence, health authority permits, a liquor licence if applicable, and compliance with tourism accommodation regulations."),
        ("How is a motel or hotel valued?", "Primarily on income \u2014 a capitalization rate applied to net operating income, informed by occupancy, ADR, and RevPAR trends, plus the real estate's underlying value and condition."),
        ("Is hospitality financing harder to get than standard commercial financing?", "It's different rather than strictly harder \u2014 lenders evaluate the operating business's income and management track record alongside the real estate."),
        ("What's driving demand for Fraser Valley hospitality properties right now?", "Year-round tourism around Harrison Hot Springs and Cultus Lake, growing agri-tourism in the eastern Fraser Valley, and steady Highway 1 corridor motel demand."),
    ], related=['banquet-halls','retail']),

dict(slug='liquor-stores', label='Liquor Stores', icon='\U0001F943', tag='Licensed Retail Specialist',
    lead="Licensed retail business sales, including both asset and share transactions, for a category with its own regulatory considerations.",
    m_heading="Why Liquor Stores Are a Sought-After Investment in BC",
    m_paras=["British Columbia operates a controlled liquor distribution system where the number of Liquor Retail Store (LRS) licences is limited by the provincial government, and new licences are rarely issued. That scarcity means existing licensed stores hold real value beyond just their sales figures.",
             "For investors and entrepreneurs, a well-located liquor store in a growing community represents a stable, cash-flowing business, while the limited supply of licences protects existing operators from excessive new competition."],
    m_photo='liquor-retail-shelves',
    valued=[vv("\U0001F4CA","Revenue & Profitability","Annual gross sales, net profit margins, and revenue trends over the past three to five years drive valuation."),
            vv("\U0001F4CD","Location & Demographics","Proximity to residential areas, competition density, and neighbourhood demographics all influence value."),
            vv("\U0001F4DC","Licence Value","LRS licences are limited by government policy, making an existing licence inherently valuable on its own."),
            vv("\U0001F4C4","Lease Terms & Real Estate","A long-term lease with favourable renewal options increases business value; owning the building adds stability.")],
    dd_items=[dd("📊","Financial Review","Tax returns, POS reports, supplier invoices, and bank statements cross-checked against each other."),
              dd("📋","Licence Verification","Confirming the LRS licence is in good standing with no outstanding violations before closing."),
              dd("📄","Lease & Property Review","Reviewing lease terms, renewal options, and rent escalation clauses in detail."),
              dd("📦","Inventory Assessment","Evaluating current inventory levels, value, and supplier relationships."),
              dd("🎯","Competitive Analysis","Assessing nearby competition and any upcoming developments that could affect future sales."),
              dd("⚖️","Asset vs. Share Structure","Understanding the tax and liability implications of each deal structure before deciding which to pursue.")],
    faq=[
        ("What's the difference between an asset sale and a share sale?", "An asset sale transfers the business's assets \u2014 inventory, fixtures, the lease, and the licence \u2014 to a new entity. A share sale transfers ownership of the existing corporate entity itself, including its licence."),
        ("Does the liquor licence transfer automatically with a sale?", "No \u2014 licence transfers go through a provincial approval process through the BC Liquor and Cannabis Regulation Branch, which can take weeks to months."),
        ("Why are BC liquor store licences worth so much?", "BC operates a controlled liquor distribution system where LRS licences are limited by provincial policy, and new licences are rarely issued \u2014 that scarcity gives the licence real intrinsic value."),
        ("How is a liquor store valued?", "Primarily on revenue and profitability trends over the past three to five years, plus location, lease terms, and the licence value itself."),
        ("What financial documents should I review before buying a liquor store?", "Tax returns, POS reports, supplier invoices, and bank statements, cross-checked against each other \u2014 discrepancies are the most common red flag."),
        ("Can I finance a liquor store purchase, and how does that work?", "Yes, though it's its own niche \u2014 lenders evaluate both the real estate and the business's cash flow, similar to other licensed-business transactions."),
    ], related=['convenience-stores','restaurants']),

dict(slug='land', label='Land &amp; Subdivisions', icon='\U0001F4D0', tag='Development Land Specialist',
    lead="Development land and subdivision opportunities across Surrey and the Lower Mainland, for builders, developers, and land investors.",
    m_heading="Understanding Subdivision Potential Before You Buy",
    m_paras=["Whether a property can be subdivided depends on current municipal zoning, Official Community Plan (OCP) designations, minimum lot size requirements, and servicing availability \u2014 all things that require direct due diligence with the municipality.",
             "Many Fraser Valley properties fall within the Agricultural Land Reserve, which adds an additional layer of Agricultural Land Commission approval on top of standard municipal review."],
    m_photo='development-land-aerial',
    valued=[vv("\U0001F4D0","Zoning & OCP Designation","Current zoning and long-term Official Community Plan designation set the ceiling on what a site can become."),
            vv("\U0001F33E","ALR Status","Agricultural Land Reserve status significantly affects subdivision potential and requires separate provincial approval."),
            vv("\U0001F6B0","Servicing Availability","Access to water, sewer, and storm drainage \u2014 or the cost to extend it \u2014 is often the largest line item in a development budget."),
            vv("\U0001F4D0","Assembly Potential","Adjacent parcels suited to assembly can unlock development potential not available from a single lot alone.")],
    dd_items=[dd("🗺️","Feasibility Assessment","Reviewing zoning bylaws, OCP designations, lot size minimums, and servicing availability before investing in an application."),
              dd("🌾","ALR Considerations","Confirming whether Agricultural Land Commission approval is required on top of municipal review."),
              dd("📋","Municipal Application Requirements","Understanding surveys, engineering plans, and servicing agreements needed for a subdivision application."),
              dd("💰","Servicing Cost Estimates","Getting a realistic estimate for extending water, sewer, and road infrastructure to new lots."),
              dd("🧪","Environmental & Geotechnical","Assessing whether site conditions require additional studies before development can proceed."),
              dd("⏳","Development Timeline","Building realistic timeline expectations, since rezoning and servicing extensions can take considerably longer than a straightforward subdivision.")],
    faq=[
        ("How do I know if a property has subdivision potential?", "It depends on current municipal zoning, OCP designations, minimum lot size requirements, and servicing availability \u2014 all requiring direct due diligence with the municipality."),
        ("Do you handle land assembly for developers?", "Manan can help identify and approach adjacent parcels for potential assembly, working alongside your legal and development team."),
        ("What should I budget for beyond the purchase price on development land?", "Rezoning applications, servicing costs, engineering and survey fees, environmental and geotechnical studies, and holding costs during the approval process."),
        ("What is the Agricultural Land Reserve and how does it affect subdivision?", "The ALR is BC's protected farmland zone. If your land is in the ALR, subdivision or exclusion requires Agricultural Land Commission approval on top of municipal approval."),
        ("How long does the BC subdivision approval process typically take?", "It varies significantly, but a straightforward residential subdivision with no ALR involvement can take several months to a year; rezoning or ALR exclusion can take considerably longer."),
        ("What's the difference between a standard subdivision and bare land strata?", "A standard subdivision creates individually titled parcels. Bare land strata creates lots sharing ownership of common property through a strata corporation, similar to a strata condo but for land."),
    ], related=['industrial','farms-alr-land']),

dict(slug='gas-stations', label='Gas Stations', icon='\u26FD', tag='Fuel Retail Specialist',
    lead="Branded and independent fuel retail sites across the Lower Mainland \u2014 a category with real estate, business, and environmental dimensions all in play.",
    m_heading="A Category With Real Estate, Business, and Environmental Dimensions",
    m_paras=["Gas station transactions combine three distinct considerations: the underlying real estate value, the operating business (fuel volume, c-store, and add-on revenue), and environmental risk from decades of underground fuel storage.",
             "Branded stations come with supply agreements and marketing support but restrict fuel supplier flexibility; independents offer more pricing freedom but rely on their own reputation to drive traffic."],
    m_photo='gas-station-canopy',
    valued=[vv("\u26FD","Fuel Supply & Branding","Branded agreements (Esso, Shell, Petro-Canada, Chevron) versus independent supply, and what each means for flexibility."),
            vv("\U0001F4CB","Environmental Risk","Underground storage tank history and contamination risk factor directly into price and financing."),
            vv("\U0001F3EA","C-Store & Add-On Revenue","Convenience store, car wash, and liquor add-on revenue alongside fuel volume."),
            vv("\U0001F4CD","Location & Traffic","Vehicle counts and highway access drive both fuel volume and c-store performance.")],
    dd_items=[dd("🧪","Phase I Environmental Assessment","A baseline requirement to check for soil and groundwater contamination from underground storage tanks."),
              dd("🔬","Phase II Assessment","Where Phase I flags concerns, further soil and groundwater testing before closing."),
              dd("📈","Supply Agreement Terms","Understanding exclusivity terms and remaining length on any branded fuel supply agreement."),
              dd("🧾","C-Store Financials","Verifying convenience store and add-on revenue against POS reports and supplier invoices."),
              dd("📋","Municipal & Provincial Permits","Confirming fuel retail permits are current and properly transferable."),
              dd("🔧","Tank & Equipment Age","Reviewing underground storage tank age, materials, and any required upgrades under current regulations.")],
    faq=[
        ("What environmental due diligence is needed before buying a gas station?", "A Phase I Environmental Site Assessment at minimum, and often a Phase II if concerns are flagged, to check for soil and groundwater contamination from underground storage tanks."),
        ("What's the difference between branded and independent gas stations?", "Branded stations come with supply agreements and marketing support but restrict your fuel supplier. Independents have more flexibility on suppliers and pricing but rely on their own reputation."),
        ("How is a gas station valued?", "A combination of fuel volume and margin, convenience store and add-on revenue, the underlying real estate value, and remaining lease term if applicable."),
        ("What licensing is required to operate a gas station?", "Fuel retailing requires provincial and municipal permits, with separate licensing if the site includes a liquor store or convenience store component."),
        ("How does environmental liability affect financing?", "Lenders typically require a clean Phase I (and Phase II if warranted) before approving financing on a fuel retail site \u2014 environmental risk is a real, deal-specific consideration."),
        ("Can I add a car wash or convenience store to an existing gas station?", "It depends on zoning, lot size, and municipal approval \u2014 worth confirming feasibility with the municipality before counting on it as an expansion plan."),
    ], related=['convenience-stores','car-washes']),

dict(slug='convenience-stores', label='Convenience Stores', icon='\U0001F3EA', tag='Convenience Retail Specialist',
    lead="Independent c-stores across the Fraser Valley \u2014 tobacco, lottery, and lease-based businesses with their own due diligence considerations.",
    m_heading="Mostly Leasehold Businesses, With Their Own Financial Rhythm",
    m_paras=["Most convenience stores in the Fraser Valley are leasehold businesses rather than real estate sales, which makes lease terms often the single most important piece of due diligence in a transaction.",
             "Tobacco and lottery revenue carry structurally different, more predictable margins than general merchandise \u2014 understanding the mix is key to accurately valuing the business."],
    m_photo='convenience-store-interior',
    valued=[vv("\U0001F4C4","Lease Terms","Remaining term, renewal options, and rent escalation clauses, since most c-stores are leasehold businesses."),
            vv("\U0001F6AC","Tobacco & Lottery Mix","These categories carry predictable, verifiable margins distinct from general merchandise revenue."),
            vv("\U0001F4CA","Sales Verification","Cross-checked against supplier invoices and BCLC lottery statements for a realistic picture."),
            vv("\U0001F4CD","Location & Traffic","Foot and vehicle traffic patterns specific to convenience retail, not general retail assumptions.")],
    dd_items=[dd("📋","Licensing Review","Tobacco retail licence, lottery terminal agreement, and any liquor licensing tied to the business."),
              dd("📄","Lease Analysis","Term, renewal options, and rent escalation \u2014 the top due diligence priority for a leasehold business."),
              dd("🧾","Sales Cross-Verification","Comparing reported sales against supplier invoices and BCLC lottery commission statements."),
              dd("📦","Inventory & Fixtures","Assessing current inventory value and condition of coolers, shelving, and POS equipment."),
              dd("💬","Landlord Relationship","Understanding the landlord's history with the tenant and any pending disputes or rent issues."),
              dd("🎯","Competitive Landscape","Nearby convenience and grocery competition that could affect future sales.")],
    faq=[
        ("What licences does a convenience store need?", "A tobacco retail licence, a lottery terminal agreement with BCLC if applicable, and a standard municipal business licence."),
        ("Is the real estate usually included, or is this a lease?", "Most convenience stores in the Fraser Valley are leasehold businesses rather than real estate sales \u2014 reviewing the lease is often the most important due diligence step."),
        ("How is a convenience store business valued?", "Primarily on verified sales and profit margin trends, with tobacco and lottery volume assessed separately since their margins are structurally different."),
        ("What should I check in the financials before buying?", "Cross-check reported sales against supplier invoices and BCLC lottery commission statements, which are harder to misstate than general retail sales."),
        ("Can the lease be assigned to a new owner?", "Most commercial leases include an assignment clause requiring landlord consent \u2014 confirm this early, since a landlord can decline or add conditions."),
        ("What's a realistic timeline for a convenience store transaction?", "Once financials are verified and lease assignment is confirmed, these transactions typically move faster than real estate deals \u2014 often four to eight weeks to close."),
    ], related=['gas-stations','liquor-stores']),

dict(slug='restaurants', label='Restaurants', icon='\U0001F37D\uFE0F', tag='Food & Beverage Specialist',
    lead="Independent restaurants and franchise food businesses across the Lower Mainland, from lease condition to liquor licence transfer.",
    m_heading="Goodwill and Location Drive Restaurant Value",
    m_paras=["Restaurant transactions weigh goodwill and location more heavily than most other commercial categories \u2014 a strong location with an established customer base can be worth significantly more than the equipment and lease alone.",
             "Franchise purchases add another layer: franchisor approval of the buyer, ongoing royalty and marketing fees, and adherence to brand standards, versus the full operational freedom of an independent."],
    m_photo='restaurant-interior-dining',
    valued=[vv("\U0001F37D\uFE0F","Goodwill & Reputation","Established customer base and reputation can represent a meaningful share of total value."),
            vv("\U0001F4C4","Lease & Kitchen Condition","Remaining term and whether existing kitchen infrastructure suits your concept without major buildout."),
            vv("\U0001F37A","Liquor Licence","A transferable liquor licence adds real value and requires provincial approval to transfer."),
            vv("\U0001F91D","Franchise vs. Independent","Franchise brand recognition and support versus full independent operational freedom.")],
    dd_items=[dd("📊","Financial Verification","Adjusted EBITDA (seller's discretionary earnings) based on verified financials, not owner estimates."),
              dd("📋","Liquor Licence Transfer","Confirming the provincial approval timeline and requirements before counting on a specific closing date."),
              dd("🍽️","Kitchen & Equipment Condition","Assessing hood, grease trap, and equipment condition against your concept's needs."),
              dd("📄","Lease Terms & Landlord Approval","Remaining term, renewal options, and whether a change of use needs landlord sign-off."),
              dd("🤝","Franchise Agreement Review","For franchise purchases, understanding royalty structure, territory rights, and franchisor approval requirements."),
              dd("✅","Health Inspection History","Reviewing recent health authority inspection records for any outstanding compliance issues.")],
    faq=[
        ("Does a liquor licence transfer automatically with a restaurant sale?", "No \u2014 liquor licence transfers go through a provincial approval process through the BC Liquor and Cannabis Regulation Branch, and timelines vary."),
        ("What's different about buying a franchise restaurant versus independent?", "Franchise purchases require franchisor approval, come with ongoing royalty and marketing fees, and require adherence to brand standards. Independent restaurants offer full operational freedom."),
        ("What should I check on the lease before buying a restaurant?", "Remaining term, whether the kitchen and hood infrastructure suits your concept, and whether the landlord will approve a change of use."),
        ("How is a restaurant business valued?", "Generally a multiple of adjusted EBITDA based on verified financials, plus equipment value and any transferable licences. Goodwill and location weigh heavily."),
        ("What financial red flags should I watch for?", "Cash-heavy sales that are hard to verify, declining year-over-year trends, and rent that's a disproportionately high share of revenue."),
        ("Can I change the concept after buying an existing restaurant?", "Depends on zoning, the lease's use clause, and whether a change of use requires landlord or municipal approval \u2014 confirm before assuming full flexibility."),
    ], related=['liquor-stores','retail']),

dict(slug='apartment-buildings', label='Apartment Buildings', icon='\U0001F3D9\uFE0F', tag='Multi-Family Specialist',
    lead="4-plex to 60+ unit purpose-built rental buildings across the Lower Mainland \u2014 CMHC-eligible financing and value-add opportunities.",
    m_heading="Rent Roll Analysis Drives Multi-Family Value",
    m_paras=["Buildings of 5+ units generally qualify for CMHC-insured multi-family financing, which can offer better rates and longer amortization than conventional commercial financing \u2014 a meaningful factor in how a deal gets structured.",
             "BC caps annual rent increases at a province-set rate each year, and that limit carries over to a new owner \u2014 existing tenancies and their rent history don't reset with a sale, which shapes how value-add opportunities actually play out."],
    m_photo='apartment-building-exterior',
    valued=[vv("\U0001F4CA","Rent Roll vs. Market","The gap between current rents and market rents, and how quickly that gap can close under BC's rent rules."),
            vv("\U0001F3E6","Financing Eligibility","CMHC-insured financing availability for 5+ unit buildings versus conventional commercial financing."),
            vv("\U0001F527","Value-Add Potential","Dated suites or inefficient operations that could support a renovation-driven NOI increase."),
            vv("\U0001F4CB","Tenancy History","Start dates and rent history for each unit, which determine allowable rent increase timing.")],
    dd_items=[dd("📑","Rent Roll Review","Current versus market rents, tenancy start dates, and any below-market long-term tenancies."),
              dd("📉","Vacancy History","Recent vacancy trends and typical time-to-lease for the building."),
              dd("🔧","Building Condition Report","Roof, envelope, mechanical, and electrical systems condition and remaining useful life."),
              dd("🏦","CMHC Financing Eligibility","Confirming the building and buyer qualify for CMHC-insured multi-family financing if pursuing that route."),
              dd("✅","Rent Increase Compliance","Verifying past rent increases followed BC's allowable annual rate."),
              dd("📊","Operating Expense History","Actual utility, maintenance, and management costs versus what's represented in the offering.")],
    faq=[
        ("What's the difference between financing a small versus large apartment building?", "Buildings of 5+ units generally qualify for CMHC-insured multi-family financing, offering better rates and longer amortization than conventional commercial financing."),
        ("What should I review in the rent roll before buying?", "Current versus market rents, tenancy start dates, below-market long-term tenancies, and recent vacancy history."),
        ("What are BC's rules on raising rent after a purchase?", "BC caps annual rent increases at a province-set rate, and a change of ownership doesn't reset that limit \u2014 existing tenancy rent history carries over."),
        ("What is a value-add apartment opportunity?", "A building where rents sit below market or operations are inefficient, offering a path to increase NOI through renovation or better management."),
        ("What's the typical down payment for a multi-family purchase?", "CMHC-insured multi-family financing can allow lower down payments than conventional commercial \u2014 typically starting around 15\u201325% depending on the program and building profile, worth confirming current terms with a lender."),
        ("Should I self-manage or hire a property manager?", "Depends on portfolio size, your availability, and comfort with tenant relations \u2014 professional management costs typically run 4\u20138% of gross rent but can improve retention and reduce vacancy."),
    ], related=['self-storage','land']),

dict(slug='self-storage', label='Self-Storage', icon='\U0001F4E6', tag='Storage Facility Specialist',
    lead="Climate-controlled and drive-up self-storage facilities across the Lower Mainland, valued on occupancy, rate growth, and submarket supply.",
    m_heading="Self-Storage: A Supply-Constrained Asset Class",
    m_paras=["Self-storage demand is driven by life events that happen in every economic cycle \u2014 moves, downsizing, business inventory, seasonal storage \u2014 which gives the category a defensive quality other commercial asset types don't always have.",
             "Building new self-storage requires municipal approval and land use permissions that are limited in cities like Surrey and Burnaby, which protects existing operators from the kind of new-supply pressure that affects faster-growing US markets."],
    m_photo='self-storage-facility',
    valued=[vv("\U0001F4CA","Occupancy & Rate Growth","Net operating income driven by occupancy rate, average rate per square foot, and expense ratio."),
            vv("\U0001F321\uFE0F","Facility Type Mix","Climate-controlled units command higher rents; drive-up units cost less to build and operate."),
            vv("\U0001F4CD","Site Quality & Access","Visibility, ease of access, and demographics within a 3-mile trade area drive demand."),
            vv("\U0001F4CA","Submarket Supply","Checking current development applications nearby before assuming stable occupancy going forward.")],
    dd_items=[dd("📑","Rent Roll & Concession Audit","Full rent roll with move-in dates, current rates, and any active promotional concessions."),
              dd("📊","Trailing Financials","Recent operating income and expenses compared against industry benchmarks for stabilized facilities."),
              dd("📈","Submarket Supply Analysis","All competing facilities within a reasonable radius and any approved or under-construction new supply."),
              dd("🔍","Site Inspection","Roof condition, gate and access systems, security cameras, and pavement condition."),
              dd("💻","Technology & Automation","Property management software, online rental capability, and automated kiosk or gate systems."),
              dd("🗺️","Zoning & Environmental","Confirming zoning permits self-storage use and no contamination history, particularly on former industrial sites.")],
    faq=[
        ("How is a self-storage facility valued?", "Primarily on net operating income, driven by occupancy rate, average rate per square foot, and expense ratio, capitalized at a rate reflecting facility quality and location."),
        ("What's the difference between climate-controlled and drive-up self-storage?", "Climate-controlled units command higher rents but cost more to build and operate. Drive-up units are cheaper but rent for less. Most facilities blend both."),
        ("How much new self-storage supply is coming to my submarket?", "This changes regularly and varies by municipality \u2014 checking current development applications nearby is essential before assuming stable occupancy going forward."),
        ("What operational factors matter beyond the real estate itself?", "Management software, gate access security, insurance or tenant protection plan revenue, and unit mix matching local demand."),
        ("Is self-storage a good hedge in an economic downturn?", "Historically yes \u2014 demand is driven by life events (moves, downsizing, business storage) that occur in every economic cycle, giving the category a defensive quality."),
        ("What's a realistic hold period for a self-storage investment?", "Many private investors target a multi-year hold to allow rate growth and stabilization to play out \u2014 worth discussing your specific return goals and timeline directly."),
    ], related=['apartment-buildings','industrial']),

dict(slug='truck-yards', label='Truck Yards', icon='\U0001F69B', tag='Trucking Yard Specialist',
    lead="Tractor-trailer drop yards, multi-tenant trucking yards, and full-service trucking company facilities in Surrey, Delta, Langley, and the Fraser Valley industrial corridor.",
    m_heading="BC's Trucking Yard Market: Tight Supply, Strong Demand",
    m_paras=["The Surrey-Delta-Langley industrial corridor handles a substantial portion of BC's containerized cargo and long-haul trucking activity. Drop yards, fleet yards, and multi-tenant trucking facilities along Highway 91, the South Fraser Perimeter Road, and surrounding industrial zones serve fleets ranging from owner-operators to large trucking enterprises.",
             "Supply is genuinely constrained \u2014 industrial zoning permitting trucking use is limited, ALR restrictions rule out many otherwise-suitable parcels, and growing residential-adjacent zones face increasing noise and traffic complaints. Existing zoned-and-permitted truck yards trade at a real premium over comparable industrial land without that specific permission."],
    m_photo='truck-yard-highway',
    valued=[vv("\U0001F4CD","Acreage & Highway Access","Pricing is fundamentally per-acre with highway access as the multiplier. Sites with direct Highway 91, 17, 1, or 99 access command real premiums."),
            vv("\U0001F4CB","Zoning & Permitted Use","Zoning varies dramatically by municipality \u2014 most yards require heavy industrial or specific transportation/logistics zoning."),
            vv("\U0001F527","Surface, Drainage & Fencing","Yard surface (gravel, crushed asphalt, concrete) directly affects capacity and operating cost. Poor drainage causes mud and unusability."),
            vv("\U0001F4CA","Tenant Mix & Lease Structure","Yards operate as multi-tenant (fleet operators paying monthly per-trailer fees) or single-tenant to a larger trucking company.")],
    dd_items=[dd("🗺️","Zoning & Permitted Use","Confirming the municipality permits trucking use, no temporary use permit dependency, no expiring grandfathered status. Surrey, Delta, and Langley each have distinct zoning regimes for industrial/transportation uses."),
              dd("🌾","ALR Status & Soil","If the property is in or near the ALR, reviewing BC Agricultural Land Commission status and confirming no soil restrictions that would prevent surface treatment upgrades."),
              dd("🧪","Environmental & Stormwater","Phase I ESA with particular attention to historical use (fuel storage, mechanical, container repair) and stormwater management plan compliance with municipal requirements."),
              dd("🔧","Capacity & Surface Condition","Documented trailer/parking capacity, surface condition (gravel depth, paving, drainage), gates, fencing height and condition, and lighting infrastructure."),
              dd("📇","Tenant Roster & Income Verification","Current tenants, lease terms, rate per stall or per acre, payment history, and any tenant-installed improvements that affect ownership."),
              dd("🛡️","Title, Financing & Insurance","Clean title, no expropriation notices (highway widening risk), and commercial financing terms typical for industrial land.")],
    faq=[
        ("What zoning allows a truck yard or fleet yard?", "Typically heavy industrial zoning with specific allowance for outdoor storage. Municipalities have been tightening these permissions as industrial land values rise, so confirming current zoning \u2014 not assuming based on existing use \u2014 is essential."),
        ("Why is yard space getting harder to find in the Fraser Valley?", "Rising industrial land values and municipal pressure to intensify industrial land use, favouring buildings over open storage, have reduced available yard space across Surrey, Delta, and Langley's industrial corridors."),
        ("What condition issues matter most for a truck yard?", "Paving condition and drainage are the biggest factors \u2014 inadequate drainage causes standing water and accelerates pavement degradation under heavy vehicle loads."),
        ("Is truck yard real estate usually bought or leased?", "Both are common. Owner-operators with stable, growing fleets often prefer to buy given the limited supply, while smaller operators frequently lease to preserve capital for their fleet."),
        ("Are truck yard transactions typically public listings?", "Often not \u2014 many trucking yard transactions in BC happen quietly between known operators or through direct introductions, rather than public MLS listings."),
        ("What financing is available for truck yard purchases?", "Commercial financing for industrial land, typically through credit unions or lenders experienced with industrial property \u2014 loan-to-value terms depend on the specific site and buyer profile, worth a direct conversation with a commercial lender."),
    ], related=['industrial','land']),

dict(slug='banquet-halls', label='Banquet Halls', icon='\U0001F382', tag='Event Venue Specialist',
    lead="South Asian wedding venues, corporate event spaces, and reception halls across Surrey, Langley, Abbotsford, and the Fraser Valley. From boutique 200-guest venues to flagship 800+ capacity facilities.",
    m_heading="Surrey: One of Canada's Largest Wedding Markets",
    m_paras=["Surrey hosts one of the largest South Asian wedding markets in North America. With weddings routinely involving 400\u20131,200 guests, multi-day celebrations spanning Sangeet, Mehndi, Reception, and Anand Karaj ceremonies, demand for premium banquet hall capacity has grown faster than supply for over two decades.",
             "Banquet hall transactions in BC are intensely relationship-driven. Many properties sell quietly between known operators or to first-time buyers introduced by existing venue owners. Understanding the cultural nuances, family dynamics, and operational rhythms of the business is critical to a successful acquisition."],
    m_photo='banquet-hall-event',
    valued=[vv("\U0001F465","Capacity & Configuration","Value scales with maximum guest capacity, flexibility to split into multiple events, and ancillary spaces like mandap area, bridal suite, and dance floor size."),
            vv("\U0001F4C5","Booking Calendar & Forward Revenue","Established halls carry 6\u201324 months of forward bookings. The deposit roster, payment terms, and contract assignability all affect deal value."),
            vv("\U0001F37D\uFE0F","Commercial Kitchen & Catering Model","Halls run either in-house catering, exclusive caterer arrangements, or open-caterer models. Kitchen size and BC Health Authority compliance affect flexibility and value."),
            vv("\U0001F4DC","Liquor Licensing & Permits","BC Liquor-Primary licence or Special Event Permit eligibility, parking capacity ratios, and occupant load certification from BC Fire Office.")],
    dd_items=[dd("📅","Booking Pipeline Verification","Full forward booking schedule, deposit roster including transferability to new ownership, and any cancellation/refund liability already accrued."),
              dd("📊","Revenue Analysis by Event Type","Mix between weddings, corporate events, religious celebrations, and other functions. Per-event revenue trends, food and beverage minimums, and ancillary revenue from bar service, decor, and DJ rentals."),
              dd("🍽️","Kitchen & Catering Audit","BC Health Authority inspection history, equipment inventory and condition, gas service capacity for high-BTU South Asian cooking, walk-in cooler/freezer condition, and any pending compliance upgrades."),
              dd("🧯","Occupancy & Fire Compliance","BC Fire Office certified occupant load for hall configuration, exit capacity, sprinkler coverage, and any open fire safety issues. Mismatch between marketed and certified capacity is a common red flag."),
              dd("✅","Parking & Municipal Compliance","On-site parking count, shared parking agreements, municipal banquet hall parking ratio compliance, and any noise bylaw issues. Surrey, Langley, and Abbotsford each apply different requirements."),
              dd("⚖️","Real Estate vs. Business Structure","Most banquet halls are sold as combined real estate + business. Verify allocation between the two for tax purposes, equipment ownership separately from the building, and any tenant-installed leasehold improvements.")],
    faq=[
        ("How is a banquet hall business valued?", "On booking revenue history, forward booking pipeline (deposits and confirmed dates), profit margins after catering and staffing costs, and the underlying real estate or lease terms."),
        ("What licensing does a banquet hall need for alcohol service?", "A liquor licence appropriate to the venue type, which may be a standing licence or event-specific permits depending on how the venue operates \u2014 worth confirming directly with the provincial liquor branch."),
        ("What's driving demand for banquet halls in the Fraser Valley?", "A significant South Asian wedding and event market drives strong demand for larger-capacity venues in Surrey and Abbotsford specifically, alongside steady corporate event and community usage."),
        ("What should I check on parking and capacity before buying?", "Municipal occupancy limits (fire code capacity) and required parking stalls per capacity directly cap your usable event size \u2014 confirm these before assuming a venue can host your planned event sizes."),
        ("Are banquet hall bookings transferable to a new owner?", "Often, but not automatically \u2014 confirm whether existing contracts and deposits are assignable to a new ownership entity as part of the purchase agreement, not assumed."),
        ("Is real estate typically included, or are these leasehold businesses?", "Both structures exist in this market \u2014 some banquet halls own their building, others operate on a long-term commercial lease. Manan can walk through what's available for your specific search."),
    ], related=['restaurants','retail']),

dict(slug='auto-dealerships', label='Auto Dealerships', icon='\U0001F697', tag='Automotive Retail Specialist',
    lead="New car franchise and used car dealership real estate and business sales across the Lower Mainland.",
    m_heading="A Business Valuation Exercise as Much as a Real Estate One",
    m_paras=["Dealership transactions weigh the franchise agreement value, inventory financing arrangements, and service department profitability separately from the real estate \u2014 fundamentally a business valuation exercise more than a pure property sale.",
             "New car franchise purchases require manufacturer approval of any ownership change, a separate process from the real estate transaction that can take significant time and needs to be factored into your overall timeline."],
    m_photo='auto-dealership-lot',
    valued=[vv("\U0001F4DC","Franchise Agreement","For new-car stores, the franchise agreement itself carries significant value, subject to manufacturer approval of any transfer."),
            vv("\U0001F527","Service Department","Service and parts profitability often represents a stable, recurring revenue stream separate from vehicle sales."),
            vv("\U0001F4B0","Inventory Financing","Floor plan financing arrangements and inventory value factor into the overall transaction structure."),
            vv("\U0001F3E2","Purpose-Built Real Estate","Dealership real estate is often purpose-built and may need retrofitting if the franchise changes or terminates.")],
    dd_items=[dd("🤝","Manufacturer Approval Process","Understanding the timeline and requirements for manufacturer sign-off on any change of dealer principal or ownership."),
              dd("📋","VSA Licensing Status","Confirming BC Vehicle Sales Authority licensing is current, with bonding requirements verified for used dealers."),
              dd("📊","Service Department Financials","Reviewing service and parts revenue and profitability separately from vehicle sales performance."),
              dd("🏦","Floor Plan Financing Review","Understanding existing inventory financing arrangements and how they transfer or need restructuring."),
              dd("🔧","Real Estate Condition & Use","Assessing whether the purpose-built facility suits a continuing franchise or would need retrofitting."),
              dd("📜","Franchise Agreement Terms","Reviewing territory rights, performance requirements, and remaining term on the franchise agreement.")],
    faq=[
        ("What's required to buy a new car franchise dealership?", "The manufacturer must approve any change of dealer principal or ownership structure \u2014 a separate process from the real estate transaction that can take significant time."),
        ("What is VSA licensing?", "BC's Vehicle Sales Authority licenses all motor dealers in the province. Both new and used dealerships need an active VSA licence, with additional bonding for used dealers."),
        ("How is a dealership valued differently from other commercial real estate?", "Dealership valuations weigh the franchise agreement value, inventory financing, and service department profitability separately from the real estate."),
        ("Can I buy just the real estate without the dealership business?", "Yes \u2014 some dealership real estate trades independently of the business, particularly when a dealer is relocating or a franchise is being terminated."),
        ("How long does manufacturer approval typically take?", "It varies by manufacturer and can take several weeks to a few months \u2014 factor this into your closing timeline rather than assuming a standard commercial transaction pace."),
        ("What happens to existing inventory in a dealership sale?", "Inventory is typically addressed separately from the real estate and franchise, often through existing floor plan financing arrangements that need to be assumed or restructured."),
    ], related=['car-washes','retail']),

dict(slug='daycares-childcare', label='Daycares &amp; Childcare', icon='\U0001F9F8', tag='Childcare Business Specialist',
    lead="Licensed group child care, preschool, and out-of-school care businesses across the Fraser Valley. Both standalone real estate-and-business sales and business-only transactions in leased space.",
    m_heading="A Recession-Resistant, Demand-Constrained Asset",
    m_paras=["BC has a severe and structural shortage of licensed childcare spaces. Waitlists at quality daycares across Surrey, Langley, Burnaby, and Vancouver routinely stretch 12\u201324 months for infant/toddler spots. This supply-demand imbalance means a well-run licensed daycare with strong parent retention is one of the most reliably cash-flowing small businesses in the province.",
             "BC's $10/Day ChildCareBC initiative has reshaped the economics. Participating centres trade reduced parent fees for provincial funding, with overall margins similar to \u2014 and sometimes better than \u2014 non-participating centres because of the volume guarantee. Understanding which model fits your acquisition is one of the most important strategic decisions."],
    m_photo='daycare-classroom-toys',
    valued=[vv("\U0001F4CA","Licensed Capacity & Utilization","BC daycares are licensed for a specific maximum capacity by age group. Valuation tracks closely with licensed capacity \u00d7 utilization rate \u00d7 monthly fee."),
            vv("\U0001F4C4","$10/Day Program Status","Participation in the province's $10 a Day program substantially affects fee structures and operating economics, and affects buyer pool and financing options."),
            vv("\U0001F9D1\u200D\U0001F3EB","Staff Retention & ECE Qualifications","BC requires specific ECE-to-child ratios. Tenured ECE staff with continuity through a transition is a core value factor."),
            vv("\U0001F3E0","Real Estate Configuration","Licensed group child care requires specific outdoor play area square footage per child, dedicated sleeping areas for infants, and Health Authority-compliant washrooms.")],
    dd_items=[dd("📋","Licence in Good Standing","Current BC Community Care Licence confirmed by age group, capacity confirmed, no open compliance concerns, and confirmation the licence transfers cleanly."),
              dd("📝","Enrolment & Waitlist Audit","Current enrolment by age group, attendance records over the past 12 months, waitlist depth, and parent retention data."),
              dd("👥","Staff & ECE Roster","ECE certifications on file, staff retention plan, current wages relative to BC ECE wage grid, and participation in the ECE wage enhancement program."),
              dd("✅","Building Compliance","Most recent fire inspection, Health Authority inspection, outdoor play space square footage, washroom counts, and confirmation the building meets current licensing standards."),
              dd("💲","$10/Day Program Documentation","If participating: provincial funding agreement, fee reduction confirmation, and parent fee structure. If not: market fee comparison and competitive positioning analysis."),
              dd("📄","Real Estate vs. Lease Analysis","If freehold: zoning permits childcare use, no covenants prohibiting use. If leased: term remaining, landlord consent on transfer, and renewal options that accommodate the long-term nature of childcare operations.")],
    faq=[
        ("What licensing does a daycare need in BC?", "Licensing under the Community Care and Assisted Living Act, with requirements covering staff-to-child ratios, facility safety, and ECE certification for staff, administered through the local health authority."),
        ("What is the $10 a Day program and does it affect value?", "It's a provincial funding program that caps parent fees at $10/day for participating licensed facilities in exchange for provincial funding \u2014 participation affects the facility's revenue model directly."),
        ("What staffing considerations matter when buying a daycare?", "ECE staffing shortages are a real, ongoing constraint across BC, so understanding whether existing staff will stay through a transition is often as important as the physical facility."),
        ("Does the licence transfer with a sale?", "Facility licensing is tied to both the operator and the physical space meeting requirements. A change of ownership typically requires a new licence application review rather than an automatic transfer."),
        ("How long does a licence transfer typically take?", "Licence transfer review can take 30\u201360 days depending on the health authority's workload \u2014 closing is typically synchronized with licensing approval rather than happening before it."),
        ("Can I expand capacity after buying an existing daycare?", "Possibly, but it requires a new licensing application and confirmation that the physical space meets requirements for the expanded capacity \u2014 not something to assume without health authority sign-off."),
    ], related=['apartment-buildings','restaurants']),

dict(slug='car-washes', label='Car Washes', icon='\U0001F697', tag='Car Wash Specialist',
    lead="Tunnel (express) car washes, in-bay automatic, and self-serve facilities across the Fraser Valley. Established operations with membership programs and well-maintained equipment.",
    m_heading="Why Tunnel Car Washes Are One of BC's Best Hidden Investments",
    m_paras=["The car wash industry has transformed over the past decade with the rise of express tunnel washes and unlimited monthly membership programs. A well-located modern tunnel car wash with a strong membership base generates better margins, more predictable cash flow, and higher real estate appreciation than most commercial categories.",
             "BC's wet climate is paradoxically good for the business \u2014 year-round vehicle dirt, road salt in interior regions, and an active consumer culture of vehicle maintenance support steady demand. Surrey, Langley, Abbotsford, and the Tri-Cities have all actively traded car wash markets with new development continuing."],
    m_photo='car-wash-tunnel',
    valued=[vv("\U0001F4CA","Wash Volume & Revenue Mix","Annual wash count is the headline metric. Revenue mix between single washes, multi-packs, and unlimited memberships is critical."),
            vv("\U0001F4C8","Membership Program","Modern tunnel car washes generate a growing share of revenue from unlimited-wash monthly membership programs \u2014 conversion rate of new customers to memberships is a leading indicator of operator quality."),
            vv("\U0001F527","Equipment Age & Brand","Industry equipment brands have very different reliability and parts-availability profiles. Tunnel equipment typically lasts 12\u201318 years with ongoing maintenance."),
            vv("\U0001F4A7","Water Reclamation & Compliance","BC car wash facilities must comply with municipal sewer use bylaws and environmental regulations on detergent discharge. Modern facilities use reclaimed water systems.")],
    dd_items=[dd("🧾","Wash Volume Verification","Daily/monthly wash count by service tier, cross-referenced against POS reports, member-card scans, and water/electricity consumption patterns as an independent check."),
              dd("📊","Membership Cohort Analysis","Total active members, monthly recurring revenue, churn rate, average tenure, and price point. Membership conversion rate of new customers is a strong forward indicator."),
              dd("🔧","Equipment Audit","Equipment make/model/age inventory, maintenance log review, vacuum capacity, dryer effectiveness, and any pending replacements. Tunnel equipment over 12 years old needs replacement reserves budgeted."),
              dd("💧","Water & Environmental","Reclamation system efficiency, municipal sewer use compliance, any open environmental notices, and the cost to upgrade to current standards if the facility is older."),
              dd("📄","Real Estate vs. Lease","Most modern tunnel washes own their real estate (purpose-built and not easily relocatable). Verify zoning, lot configuration, queuing capacity, and any redevelopment potential for the future."),
              dd("🎯","Local Competition","Competing car washes within a reasonable radius, their membership pricing, and any approved or under-construction new supply that could affect market saturation.")],
    faq=[
        ("What are the main types of car wash businesses?", "Tunnel (express) washes process the highest volume and increasingly rely on membership revenue. In-bay automatics serve one vehicle at a time. Self-serve bays require the least capital and labour but generate the least revenue per square foot."),
        ("How is a car wash valued?", "Primarily on wash volume, membership subscriber count and retention, and equipment age and condition, since major equipment replacement is a significant capital cost."),
        ("What should I check on equipment before buying a car wash?", "Age and maintenance history of the wash tunnel or automatic equipment, condition of the water reclamation system, and any pending major repairs."),
        ("Is membership or subscription revenue a good sign?", "Generally yes \u2014 recurring membership revenue is more stable and considered more valuable than pay-per-wash volume alone."),
        ("What financing is typically used for car wash acquisitions?", "BDC, credit unions, and life insurance companies are active lenders for well-performing car washes \u2014 SBA-style commercial mortgages with 20\u201325 year amortization are typical, worth confirming current terms with a lender."),
        ("How competitive is the Fraser Valley car wash market?", "Actively traded, with Surrey, Langley, Abbotsford, and the Tri-Cities all seeing new development \u2014 competing within 5km matters for membership pricing and volume, worth reviewing for any specific site."),
    ], related=['gas-stations','self-storage']),

dict(slug='farms-alr-land', label='Farms &amp; ALR Land', icon='\U0001F69C', tag='Agricultural Property Specialist',
    lead="Blueberry farms, dairy operations, hobby farms, and Agricultural Land Reserve acreages across the Fraser Valley.",
    m_heading="Agricultural Land Comes With Its Own Regulatory Layer",
    m_paras=["The Agricultural Land Reserve protects Fraser Valley farmland from non-agricultural development, which means property within it faces real restrictions on subdivision, non-farm use, and residential footprint \u2014 all governed by the Agricultural Land Commission separately from municipal zoning.",
             "For supply-managed sectors like dairy and poultry, production quota is typically a separate, valuable asset from the real estate itself, and understanding whether it's included in a sale materially changes what you're actually buying."],
    m_photo='farmland-fraser-valley',
    valued=[vv("\U0001F69C","ALR Status","Agricultural Land Reserve status and Agricultural Land Commission rules significantly affect what a property can be used for."),
            vv("\U0001F414","Quota (Where Applicable)","Dairy and poultry production quota is typically valued and transferred separately from the real estate."),
            vv("\U0001F4A7","Water Rights & Soil","A valid, properly registered water licence for irrigation, and soil quality relevant to the specific agricultural use."),
            vv("\U0001F3E0","Residential Footprint","Principal residence allowances on ALR land are subject to size restrictions that vary by farm size and municipality.")],
    dd_items=[dd("🌾","ALR Status Verification","Confirming Agricultural Land Reserve status and any exclusion or subdivision applications, past or pending."),
              dd("💧","Water Licence Review","Verifying any water licence attached to the property is valid, adequate, and properly registered under BC's Water Sustainability Act."),
              dd("📜","Quota Transfer Requirements","For dairy or poultry operations, understanding whether quota is included and its transfer process through the relevant marketing board."),
              dd("🧪","Soil & Environmental Assessment","Soil quality testing relevant to the intended agricultural use, and any environmental contamination history."),
              dd("🔧","Farm Structure Condition","Assessing barns, outbuildings, and agricultural infrastructure condition and remaining useful life."),
              dd("✅","Residential Use Compliance","Confirming any existing residence complies with ALR principal-residence size restrictions for the property's farm classification.")],
    faq=[
        ("What is the Agricultural Land Reserve and how does it affect a purchase?", "The ALR is a provincial land-use zone protecting farmland from non-agricultural development, with restrictions governed by the Agricultural Land Commission separately from municipal zoning."),
        ("Do I need farm quota to buy a working farm?", "For supply-managed sectors like dairy and poultry, production quota is typically a separate, valuable asset from the real estate \u2014 verify whether it's included and understand transfer requirements."),
        ("What water rights considerations matter for Fraser Valley farmland?", "BC's Water Sustainability Act governs licensed water use for irrigation \u2014 confirm any attached water licence is valid, adequate, and properly registered."),
        ("Can I build a house on ALR land?", "Generally yes for a principal residence tied to farm use, subject to size restrictions and Agricultural Land Commission rules that vary by farm size and municipality."),
        ("Does farm status affect property taxes?", "BC's Farm Class assessment can significantly reduce property taxes for qualifying working farms \u2014 eligibility depends on income thresholds and active use, worth confirming with BC Assessment for a specific property."),
        ("What farm types are most common in the Fraser Valley?", "Blueberry and cranberry farms, dairy operations, and poultry are especially prominent in the region, alongside smaller hobby farms and equestrian properties."),
    ], related=['land','truck-yards']),
]

for p in COMMERCIAL_PAGES:
    commercial_sub(
        f"/commercial/{p['slug']}/", p['label'], p['icon'], p['tag'], p['label'], p['lead'],
        p['m_heading'], p['m_paras'], p['m_photo'],
        f"How {p['label'].replace('&amp;','&')} Are Valued", "Key drivers of value in this category",
        p['valued'],
        f"{p['label'].replace('&amp;','&')} Due Diligence", "What to verify before you commit",
        p['dd_items'],
        faq=p['faq'],
        related_slugs=p['related']
    )

# ============================================================
# /communities/  — index + individual area pages
# ============================================================
comm_idx_body = subhero(
    "Areas I Serve",
    'Communities Across <span class="accent-warm">Surrey &amp; the Lower Mainland</span>',
    "Get to know the neighbourhoods Manan works in \u2014 residential and commercial alike.",
    TEXT_CTA + CONTACT_CTA
)
comm_idx_body += community_grid_section(
    "Browse by Community", "Explore each area's character before you start your search.", COMMUNITY_CARDS
)
comm_idx_body += cta_band(
    'Not Sure Which <span class="accent-warm">Area Fits</span>?',
    "Manan can walk you through the trade-offs based on what matters most to you.",
    TEXT_CTA + CONTACT_CTA
)
write_page(
    '/communities/',
    "Areas Served | Surrey & Lower Mainland Communities | Manan Bhullar",
    "Explore the communities Manan Bhullar serves across Surrey and the Lower Mainland, residential and commercial.",
    crumbs(("Areas I Serve", None)),
    comm_idx_body
)

for a in AREAS:
    others = [c for c in COMMUNITY_CARDS if c['href'] != area_href(a['slug'])][:3]
    tags_html = ''.join(f'<span>{t}</span>' for t in a.get('tags', []))
    body = subhero(
        "Areas I Serve",
        a['name'],
        a['note'] + ".",
        TEXT_CTA + CONTACT_CTA
    )
    # picsum seeds are opaque hashes, not content-aware -- "surrey" happened to hash to an
    # unrelated astronaut/spacewalk stock photo, so it needs a pinned override (see also index.html's
    # homepage area card, which had the same seed).
    _picsum_seed_overrides = {"surrey": "surrey-lowermainland"}
    _photo_seed = _picsum_seed_overrides.get(a['slug'], a['slug'])
    area_photo_src = REAL_PHOTOS.get(f"area-{a['slug']}", (f"https://picsum.photos/seed/{_photo_seed}/800/600", 800, 600))
    body += f"""<section class="content-section" style="padding:48px 0 56px;">
  <div class="wrap two-col">
    <div>
      <h2>About {a['name']}</h2>
      <p style="color:var(--ink-soft);margin-top:14px;">{a['desc']}</p>
      <div class="tags" style="margin-top:18px;display:flex;gap:8px;flex-wrap:wrap;">{tags_html}</div>
      <div style="margin-top:24px;display:flex;gap:14px;flex-wrap:wrap;"><a class="btn-outline-dark" href="/property-search/">Search Properties in {a['name']} \u2192</a><a class="btn-outline-dark" href="/contact/">Ask Manan About {a['name']} \u2192</a></div>
    </div>
    <img class="imgblock" style="aspect-ratio:16/11;" src="{area_photo_src[0]}" alt="{a['name']} neighbourhood" loading="lazy" width="{area_photo_src[1]}" height="{area_photo_src[2]}">
  </div>
</section>"""
    if a.get('schools') or a.get('shopping') or a.get('recreation'):
        body += local_info_section(a['name'], a.get('schools'), a.get('shopping'), a.get('recreation'), a.get('entertainment'))
    body += f"""<section class="content-section">
  <div class="wrap two-col">
    <img class="imgblock" src="https://picsum.photos/seed/{a['slug']}-street/800/600" alt="{a['name']} street view (sample photo)" loading="lazy" width="800" height="600">
    <div>
      <h2>Buying or Selling in {a['name']}</h2>
      <p style="color:var(--ink-soft);margin-top:14px;">Whether you're searching for a home in {a['name']} or thinking about listing one, local context matters \u2014 what a property is actually worth here, how quickly comparable homes have been moving, and which streets or buildings tend to hold their value. Manan works across both the residential and commercial sides of {a['name']}'s market and can walk you through what's realistic for your specific goals.</p>
      <div class="point-list">
        <div class="point"><div class="dot">\U0001F3E1</div><div><strong>Buyers</strong><span>A tailored search and honest guidance on what {a['name']} actually offers for your budget and lifestyle.</span></div></div>
        <div class="point"><div class="dot">\U0001F511</div><div><strong>Sellers</strong><span>A free evaluation grounded in current comparable activity in {a['name']}, not a generic estimate.</span></div></div>
      </div>
      <div style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap;">
        <a class="btn-solid-warm" href="/property-search/">\U0001F50D Search Homes in {a['name']}</a>
        <a class="btn-outline-dark" href="/sellers/home-evaluation/">\U0001F4CB Free Home Evaluation</a>
      </div>
      <p style="margin-top:14px;font-size:0.85rem;color:var(--ink-soft);">Prefer to talk now? Call <a href="tel:+16047279542" style="color:var(--accent-deep);font-weight:600;">(604) 727-9542</a></p>
    </div>
  </div>
</section>"""
    if a.get('area_faq'):
        body += faq_section(f"{a['name']} Real Estate FAQs", a['area_faq'])
    body += community_grid_section("Other Communities", "Explore more of the areas Manan serves.", others)
    body += cta_band(
        f'Thinking About {a["name"]}?',
        "Manan can share more on pricing, inventory, and what to expect in this market.",
        TEXT_CTA + CONTACT_CTA
    )
    title_name = a['name']
    if a['slug'] == 'sullivan-heights':
        title_name = 'Sullivan Heights (Surrey)'
    elif a['slug'] == 'sullivan-heights-burnaby':
        title_name = 'Sullivan Heights (Burnaby)'
    write_page(
        f"/communities/{a['slug']}/",
        f"{title_name} Real Estate | Manan Bhullar",
        f"{title_name} real estate with Manan Bhullar \u2014 {a['note'].lower()}. Local knowledge across Surrey and the Lower Mainland.",
        crumbs(("Areas I Serve", "/communities/"), (a['name'], None)),
        body
    )

# ============================================================
# /why-manan/ (formerly split across /about/ + /why-manan/ -- merged into one
# page; the standalone /about/ page was removed), /contact/, /property-search/, /listings/
# ============================================================
why_body = subhero(
    "About Manan",
    'Why Work With <span class="accent-warm">Manan</span>?',
    "A marketing-trained, dual-market REALTOR\u00AE who treats residential and commercial clients with the same level of care.",
    TEXT_CTA + CONTACT_CTA
)
why_body += f"""<section class="content-section why-dark-section">
  <div class="wrap two-col">
    <img class="bio-photo" style="width:100%;" src="/assets/photos/manan-headshot.jpg" alt="Manan Bhullar headshot" loading="lazy" width="1170" height="1529">
    <div>
      <h2>Background</h2>
      <p style="margin-top:14px;">Serving the Fraser Valley and Lower Mainland, Manan brings personal attention to every client and expertise across residential, commercial, and industrial real estate \u2014 always focused on what it takes to reach your goals.</p>
      <p style="margin-top:14px;">Manan knows the region's neighbourhoods and its real estate market well. Clients aren't just transactions to him \u2014 his approach is honest, dedicated service that puts your interests first.</p>
      <div class="bio-credential" style="margin-top:24px;max-width:100%;">
        <strong>BBA, Marketing Specialist</strong>
        <span>Beedie School of Business, Simon Fraser University</span>
      </div>
    </div>
  </div>
</section>"""
_why_points = [
    dict(icon="\U0001F393", title="Marketing-Trained Approach", desc="A BBA in Marketing from SFU's Beedie School of Business shapes how every property is positioned and presented."),
    dict(icon="\U0001F3E2", title="Residential &amp; Commercial Fluency", desc="Few agents work seriously in both markets \u2014 that dual perspective often helps clients see opportunities others miss."),
    dict(icon="\U0001F4AC", title="Direct, Honest Communication", desc="Clear answers, realistic expectations, and no pressure \u2014 whether you're buying your first condo or leasing an industrial unit."),
    dict(icon="\U0001F91D", title="Full Representation", desc="Backed by full brokerage support on every transaction, from offer to closing."),
]
_why_points_html = ''.join(
    f"""<div class="point">
        <div class="dot">{p['icon']}</div>
        <div><strong>{p['title']}</strong><span>{p['desc']}</span></div>
      </div>""" for p in _why_points
)
# Single-column (no photo -- the Background section above already carries the one headshot
# this page needs) unlike the shared point_list_section() helper, which always pairs the list
# with a second photo in a two-col layout.
why_body += f"""<section class="content-section raised">
  <div class="wrap" style="max-width:640px;">
    <div class="content-head center">
      <div class="eyebrow" style="margin-bottom:16px;">Why Manan</div>
      <h2>What Clients Can Expect</h2>
    </div>
    <div class="point-list" style="margin-top:32px;">{_why_points_html}</div>
  </div>
</section>"""
why_body += cta_band(
    'See It For <span class="accent-warm">Yourself</span>',
    "A short call is the easiest way to find out if it's a good fit.",
    TEXT_CTA + CONTACT_CTA
)
write_page(
    '/why-manan/',
    "About &amp; Why Manan | Manan Bhullar, Surrey Real Estate",
    "Meet Manan Bhullar \u2014 BBA Marketing from SFU's Beedie School of Business, and why work with a marketing-trained, dual-market REALTOR\u00AE serving the Fraser Valley and Lower Mainland.",
    crumbs(("About &amp; Why Manan", None)),
    why_body
)

contact_body = subhero(
    "Contact",
    'Get In Touch',
    "Whether you're buying, selling, or leasing \u2014 reach out any time.",
    ''
)
contact_interested_options = "<option>I'm interested in...</option><option>Buying a Home</option><option>Selling My Property</option><option>Commercial Real Estate</option><option>Free Home Evaluation</option><option>Investment Properties</option><option>Other</option>"
contact_lead_form = lead_form(
    "Send a Message",
    "New Contact Form Message — mananbhullar.com",
    extra_fields=f'<select name="interested_in">{contact_interested_options}</select>',
    message_placeholder="Your Message (optional)"
)
contact_body += f"""<section class="content-section">
  <div class="wrap two-col">
    <div>
      <h2>Contact Details</h2>
      <div class="point-list">
        <div class="point"><div class="dot">\U0001F4DE</div><div><strong>Phone</strong><span><a href="tel:+16047279542" style="color:var(--accent-deep);">(604) 727-9542</a></span></div></div>
        <div class="point"><div class="dot">\U0001F4CD</div><div><strong>Office</strong><span>201-2010 E 48th Ave, Vancouver, BC V5P 1R8</span></div></div>
        <div class="point"><div class="dot">\u2709\uFE0F</div><div><strong>Email</strong><span><a href="mailto:mb_realestate@outlook.com" style="color:var(--accent-deep);">mb_realestate@outlook.com</a></span></div></div>
        <div class="point"><div class="dot">\U0001F3E2</div><div><strong>Service Area</strong><span>Surrey &amp; the Lower Mainland</span></div></div>
      </div>
    </div>
    {contact_lead_form}
  </div>
</section>"""
write_page(
    '/contact/',
    "Contact Manan Bhullar | Fraser Valley Real Estate",
    "Contact Manan Bhullar, REALTOR\u00AE, for residential, commercial, and industrial real estate in Surrey and the Lower Mainland.",
    crumbs(("Contact", None)),
    contact_body
)

ps_body = subhero(
    "Property Search",
    'Search Properties Across <span class="accent-warm">Surrey &amp; the Lower Mainland</span>',
    "Browse current MLS\u00AE listings by area. Call Manan when you find something you love.",
    ''
)
ps_body += f"""<section class="content-section">
  <div class="wrap" style="max-width:640px;">
    <div class="calc-card">
      <h3>Find Your Next Property</h3>
      <div class="sub">Choose an area and search type</div>
      <div class="search-tabs" style="margin-bottom:16px;">
        <button class="search-tab active" data-tab="res">Residential</button>
        <button class="search-tab" data-tab="com">Commercial</button>
      </div>
      <div class="calc-row">
        <label for="psAreaSelect">Area</label>
        <select id="psAreaSelect">
          <option value="49.1913,-122.8490">All Fraser Valley</option>
          <option value="49.0847,-123.0587">Delta</option>
          <option value="49.1913,-122.8490">Surrey</option>
          <option value="49.1042,-122.6604">Langley</option>
          <option value="49.0189,-122.8025">White Rock / South Surrey</option>
          <option value="49.2488,-122.9805">Burnaby</option>
          <option value="49.2838,-122.7932">Coquitlam</option>
          <option value="49.2057,-122.9110">New Westminster</option>
          <option value="49.2827,-123.1207">Vancouver</option>
          <option value="49.1666,-123.1336">Richmond</option>
          <option value="49.0504,-122.3045">Abbotsford</option>
          <option value="49.2193,-122.6019">Maple Ridge</option>
          <option value="49.1337,-122.3255">Mission</option>
          <option value="49.1579,-121.9514">Chilliwack</option>
        </select>
      </div>
      <button type="button" class="btn-block-dark" data-realtor-search="psAreaSelect">\U0001F50D Search Properties \u2197</button>
      <p class="calc-disclaimer">Opens current listings for your selected area in a new tab.</p>
    </div>
  </div>
</section>"""
ps_body += cta_band(
    'Found Something You <span class="accent-warm">Love</span>?',
    "Text Manan to book a showing.",
    TEXT_CTA
)
write_page(
    '/property-search/',
    "Property Search | Manan Bhullar",
    "Search MLS\u00AE listings across the Fraser Valley and Lower Mainland with Manan Bhullar.",
    crumbs(("Property Search", None)),
    ps_body
)

listings_body = subhero(
    "My Listings",
    'Current Listings',
    "Manan's active listings will appear here. In the meantime, reach out directly or search current MLS\u00AE inventory.",
    '<a class="btn-solid-warm" href="/property-search/">\U0001F50D Search Properties \u2197</a>' + CONTACT_CTA
)
listings_body += f"""<section class="content-section">
  <div class="wrap" style="text-align:center;max-width:52ch;">
    <p style="color:var(--ink-soft);">This page is ready for listing data once an MLS\u00AE feed is connected \u2014 for now, call or message Manan directly for current inventory.</p>
  </div>
</section>"""
write_page(
    '/listings/',
    "My Listings | Manan Bhullar",
    "Current listings from Manan Bhullar, REALTOR\u00AE.",
    crumbs(("My Listings", None)),
    listings_body
)

# ============================================================
# /blog/  — index + articles
# ============================================================
ARTICLES = [
    dict(slug='first-time-buyer-programs-bc', tag='Buying',
         title="BC First-Time Buyer Programs, Explained",
         desc="A plain-language walkthrough of the PTT exemption, FHSA, and RRSP Home Buyers' Plan.",
         img='blog-first-time-buyers'),
    dict(slug='preparing-your-home-to-sell', tag='Selling',
         title="Preparing Your Home to Sell: A Practical Checklist",
         desc="The prep work that actually helps a listing perform, without an unnecessary renovation budget.",
         img='blog-selling-checklist'),
]

blog_cards = ''
for art in ARTICLES:
    blog_cards += f"""<a class="blog-card" href="/updates/{art['slug']}/">
      <img class="thumb" src="https://picsum.photos/seed/{art['img']}/500/310" alt="{art['title']} (sample photo)" loading="lazy" width="500" height="310" style="width:100%;object-fit:cover;">
      <div class="body">
        <span class="tag">{art['tag']}</span>
        <strong>{art['title']}</strong>
        <span>{art['desc']}</span>
        <span class="go">Read More \u2192</span>
      </div>
    </a>"""

blog_idx_body = f"""<header class="subhero">
  <div class="wrap">
    <div class="eyebrow">Updates</div>
    <h1>Real Estate Insight for <span class="accent-warm">Surrey &amp; the Lower Mainland</span></h1>
    <p class="lead">In-depth guides and current market analysis from your trusted Fraser Valley expert.</p>
    {google_follow_card()}
  </div>
</header>"""
blog_idx_body += f"""<section class="content-section">
  <div class="wrap">
    <div class="blog-grid">{blog_cards}</div>
  </div>
</section>"""
write_page(
    '/updates/',
    "Updates | Manan Bhullar Real Estate",
    "Real estate guides and articles for buyers, sellers, and investors in Surrey and the Lower Mainland, from Manan Bhullar.",
    crumbs(("Updates", None)),
    blog_idx_body
)

def article_page(art, body_html):
    sidebar_form = lead_form(
        "Have Questions? Ask Manan",
        f"New Article Question \u2014 {art['title']} \u2014 mananbhullar.com",
        message_placeholder="Your Question"
    )
    full = f"""<header class="subhero" style="padding:48px 0;">
  <div class="wrap" style="text-align:center;">
    <div class="eyebrow">{art['tag']}</div>
    <h1 style="max-width:32ch;margin:0 auto;">{art['title']}</h1>
  </div>
</header>
<img class="article-hero-img" src="https://picsum.photos/seed/{art['img']}/1200/480" alt="{art['title']} (sample photo)" loading="lazy" width="1200" height="480">
<section class="content-section">
  <div class="wrap article-layout">
    <div class="article-body">
      {body_html}
      <div style="margin-top:48px;padding-top:24px;border-top:1px solid var(--line);text-align:center;">
        <a class="btn-outline-dark" href="/updates/">\u2190 Back to Updates</a>
      </div>
    </div>
    <aside class="article-sidebar">
      {sidebar_form}
      <div class="sidebar-call-box">
        <strong>Speak with Manan Directly</strong>
        <p>Prefer to talk it through? Reach out any time \u2014 free, no-obligation.</p>
        {TEXT_CTA}
      </div>
    </aside>
  </div>
</section>"""
    write_page(
        f"/updates/{art['slug']}/",
        f"{art['title']} | Manan Bhullar",
        art['desc'],
        crumbs(("Updates", "/updates/"), (art['title'], None)),
        full
    )

article_page(ARTICLES[0], """
<p>Buying a first home in BC comes with more financial moving parts than most buyers expect. Here's a plain-language summary of the main programs currently available \u2014 always confirm current details with your mortgage broker or lawyer before relying on them.</p>
<h2>BC Property Transfer Tax First-Time Home Buyers' Exemption</h2>
<p>Eligible first-time buyers can receive a full exemption from BC's Property Transfer Tax on homes valued up to $835,000, with a partial exemption phasing out up to $860,000. To qualify, you generally need to be a Canadian citizen or permanent resident, have lived in BC or filed BC tax returns for a minimum period, and never have owned a principal residence anywhere in the world.</p>
<h2>First Home Savings Account (FHSA)</h2>
<p>The FHSA lets eligible Canadians contribute up to $8,000 per year, to a $40,000 lifetime maximum, toward a first home. Contributions are tax-deductible, and qualifying withdrawals are tax-free \u2014 combining features of an RRSP and a TFSA.</p>
<h2>RRSP Home Buyers' Plan (HBP)</h2>
<p>The Home Buyers' Plan allows eligible first-time buyers to withdraw funds from an RRSP tax-free toward a home purchase, repayable back into the RRSP over 15 years. The FHSA and HBP can generally be used together on the same purchase.</p>
<h2>CMHC Mortgage Insurance</h2>
<p>Buyers putting down less than 20% will typically require mortgage default insurance through CMHC or a similar insurer, which is added to the mortgage rather than paid upfront.</p>
<p>Every buyer's situation is different, and program rules do change. Manan can help you confirm exactly what you qualify for as part of a free, no-pressure consultation.</p>
""")

article_page(ARTICLES[1], """
<p>Good prep work doesn't have to mean a major renovation. Here's what actually tends to move the needle when it comes to how a home shows and how buyers respond to it.</p>
<h2>Start With a Deep Clean and Declutter</h2>
<p>Before anything else, a genuinely thorough clean and a significant decluttering pass \u2014 including closets and storage areas buyers will open \u2014 makes the single biggest visual difference for the least cost.</p>
<h2>Handle Small Repairs</h2>
<p>Sticking doors, leaky faucets, chipped paint, and burnt-out bulbs are inexpensive to fix and can otherwise plant doubt about how well the rest of the home has been maintained.</p>
<h2>Neutralize, Don't Necessarily Renovate</h2>
<p>Bold paint colours and heavy personalization can make it harder for buyers to picture themselves in the space. Neutral, fresh paint in key rooms is often a better return than a full renovation.</p>
<h2>Let the Light In</h2>
<p>Clean windows, open curtains, and well-placed lighting for showings make a measurable difference in how bright and welcoming a home feels in photos and in person.</p>
<h2>Talk to Your Agent Before Spending Money</h2>
<p>Not every property benefits from the same prep work. Before committing to any repairs or upgrades, a conversation with Manan can help prioritize what's actually likely to affect your sale price versus what won't.</p>
""")

# ============================================================
# Legal / footer pages
# ============================================================
def legal_page(path, title, heading, body_text):
    body = subhero("Legal", heading, "", '')
    body += f"""<section class="content-section">
  <div class="wrap article-body">
    <p>{body_text}</p>
  </div>
</section>"""
    write_page(path, f"{title} | Manan Bhullar", body_text, crumbs((heading, None)), body)

legal_page('/privacy-policy/', 'Privacy Policy', 'Privacy Policy',
    "This page will outline how personal information submitted through this site is collected, used, and protected. Full policy text to be finalized with Manan before launch.")
legal_page('/terms-of-use/', 'Terms of Use', 'Terms of Use',
    "This page will outline the terms governing use of this website. Full policy text to be finalized with Manan before launch.")
legal_page('/fair-housing-notice/', 'Fair Housing Notice', 'Fair Housing Notice',
    "Manan Bhullar is committed to fair housing practices, in compliance with applicable BC and Canadian human rights legislation. Full notice text, including brokerage details, to be finalized before launch.")

# ============================================================
# 404 page \u2014 standalone, sleek dark treatment
# ============================================================
NOT_FOUND_HTML = """<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 \u2014 Page Not Found | Manan Bhullar</title>
<meta name="robots" content="noindex, follow">
<link rel="preconnect" href="https://api.fontshare.com">
<link href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#0A0A0A;color:#FAFAF8;font-family:'General Sans',-apple-system,BlinkMacSystemFont,sans-serif;min-height:100vh;display:flex;flex-direction:column;}
.nf-main{flex:1;display:flex;align-items:center;justify-content:center;padding:40px 24px;}
.nf-inner{display:flex;align-items:center;gap:28px;}
.nf-code{font-size:clamp(3rem,8vw,4.5rem);font-weight:600;letter-spacing:-0.03em;line-height:1;}
.nf-rule{width:1px;align-self:stretch;background:rgba(250,250,248,0.28);}
.nf-msg{font-size:clamp(1rem,2.4vw,1.35rem);font-weight:400;line-height:1.5;color:rgba(250,250,248,0.92);}
.nf-links{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px;}
.nf-links a{color:rgba(250,250,248,0.62);text-decoration:none;font-size:0.85rem;border:1px solid rgba(250,250,248,0.22);padding:8px 15px;transition:all .18s ease;}
.nf-links a:hover{color:#0A0A0A;background:#FAFAF8;border-color:#FAFAF8;}
.nf-foot{padding:26px 24px;border-top:1px solid rgba(250,250,248,0.12);text-align:center;font-size:0.78rem;color:rgba(250,250,248,0.45);}
.nf-foot a{color:rgba(250,250,248,0.72);text-decoration:none;}
@media (max-width:520px){
  .nf-inner{flex-direction:column;align-items:flex-start;gap:16px;}
  .nf-rule{width:52px;height:1px;align-self:auto;}
}
</style>
</head>
<body>
<main class="nf-main">
  <div class="nf-inner">
    <div class="nf-code">404</div>
    <div class="nf-rule"></div>
    <div>
      <p class="nf-msg">This page could not be found.</p>
      <div class="nf-links">
        <a href="/">Home</a>
        <a href="/buyers/">Buy a Home</a>
        <a href="/sellers/">Sell Your Property</a>
        <a href="/communities/">Areas I Serve</a>
        <a href="/contact/">Contact</a>
      </div>
    </div>
  </div>
</main>
<div class="nf-foot">Manan Bhullar \u00b7 <a href="tel:+16047279542">(604) 727-9542</a></div>
</body>
</html>
"""
with open(os.path.join(ROOT, '404.html'), 'w') as f:
    f.write(NOT_FOUND_HTML)
print('wrote /404.html')

# ============================================================
# sitemap.xml \u2014 auto-generated from every index.html on disk
# ============================================================
import datetime
today = datetime.date.today().isoformat()
url_paths = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in ('assets',)]
    if 'index.html' in filenames:
        rel = os.path.relpath(dirpath, ROOT)
        url_paths.append('/' if rel == '.' else '/' + rel.replace(os.sep, '/') + '/')
url_paths.sort()

sitemap_entries = ''.join(
    f"""  <url>
    <loc>https://www.mananbhullar.com{p}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{'weekly' if p == '/' else 'monthly'}</changefreq>
    <priority>{'1.0' if p == '/' else '0.6'}</priority>
  </url>
"""
    for p in url_paths
)
sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}</urlset>
"""
with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
    f.write(sitemap_xml)
print(f'wrote /sitemap.xml ({len(url_paths)} urls)')

robots_txt = """User-agent: *
Allow: /

Sitemap: https://www.mananbhullar.com/sitemap.xml
"""
with open(os.path.join(ROOT, 'robots.txt'), 'w') as f:
    f.write(robots_txt)
print('wrote /robots.txt')

print("BUILD COMPLETE")
