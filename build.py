import os
import hashlib
from icons import apply_icons

ROOT = os.path.dirname(os.path.abspath(__file__))

# Google Maps Embed API key -- get one free at https://console.cloud.google.com/
# Enable "Maps Embed API", create a key, restrict to mananbhullar.com/*, paste here.
# Leave empty to skip map embeds.
GOOGLE_MAPS_KEY = "AIzaSyD-SmCc6jn7X2w2IUI6P0lk90c5KVOUBZo"
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
  <a class="cta-text" href="tel:+16047279542">\U0001F4DE Call Manan</a>
  <a class="cta-primary" href="/contact/">Message</a>
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

def subhero(eyebrow, h1, lead, ctas=None, flat_dark=False):
    ctas_html = ctas or ''
    cls = 'subhero flat-dark' if flat_dark else 'subhero'
    eyebrow_html = f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''
    return f"""<header class="{cls}">
  <div class="wrap">
    {eyebrow_html}
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

def simple_cards(title, sub, cards, cols=3, raised=True, dark=False):
    cls = 'dark' if dark else ('raised' if raised else '')
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

def info_cards(title, sub, cards, cols=3, raised=True, dark=False):
    cls = 'dark' if dark else ('raised' if raised else '')
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
      <p class="form-trust">Manan Bhullar REALTOR® | Marketing Specialist</p>
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
    'commercial-hub-office': ('/assets/photos/commercial-hub-office.jpg', 800, 600),
    'industrial-warehouse-interior': ('/assets/photos/industrial-warehouse-interior.jpg', 900, 675),
    'retail-storefront-strip': ('/assets/photos/retail-storefront-strip.jpg', 900, 675),
    'hospitality-pool-resort': ('/assets/photos/hospitality-pool-resort.jpg', 900, 675),
    'liquor-retail-shelves': ('/assets/photos/liquor-retail-shelves.jpg', 900, 675),
    'development-land-aerial': ('/assets/photos/development-land-aerial.jpg', 900, 675),
    'gas-station-canopy': ('/assets/photos/gas-station-canopy.jpg', 900, 675),
    'convenience-store-interior': ('/assets/photos/convenience-store-interior.jpg', 900, 675),
    'restaurant-interior-dining': ('/assets/photos/restaurant-interior-dining.jpg', 900, 675),
    'apartment-building-exterior': ('/assets/photos/apartment-building-exterior.jpg', 900, 675),
    'self-storage-facility': ('/assets/photos/self-storage-facility.jpg', 900, 675),
    'truck-yard-highway': ('/assets/photos/truck-yard-highway.jpg', 900, 675),
    'banquet-hall-event': ('/assets/photos/banquet-hall-event.jpg', 900, 675),
    'auto-dealership-lot': ('/assets/photos/auto-dealership-lot.jpg', 900, 675),
    'daycare-classroom-toys': ('/assets/photos/daycare-classroom-toys.jpg', 900, 675),
    'car-wash-tunnel': ('/assets/photos/car-wash-tunnel.jpg', 900, 675),
    'farmland-fraser-valley': ('/assets/photos/farmland-fraser-valley.jpg', 900, 675),
    'abbotsford-street': ('/assets/photos/abbotsford-street.jpg', 800, 600),
    'aldergrove-street': ('/assets/photos/aldergrove-street.jpg', 800, 600),
    'annieville-street': ('/assets/photos/annieville-street.jpg', 800, 600),
    'bear-creek-street': ('/assets/photos/bear-creek-street.jpg', 800, 600),
    'big-bend-street': ('/assets/photos/big-bend-street.jpg', 800, 600),
    'bolivar-heights-street': ('/assets/photos/bolivar-heights-street.jpg', 800, 600),
    'boundary-bay-street': ('/assets/photos/boundary-bay-street.jpg', 800, 600),
    'brentwood-street': ('/assets/photos/brentwood-street.jpg', 800, 600),
    'bridgeview-street': ('/assets/photos/bridgeview-street.jpg', 800, 600),
    'brookswood-street': ('/assets/photos/brookswood-street.jpg', 800, 600),
    'burnaby-heights-street': ('/assets/photos/burnaby-heights-street.jpg', 800, 600),
    'burnaby-street': ('/assets/photos/burnaby-street.jpg', 800, 600),
    'campbell-heights-street': ('/assets/photos/campbell-heights-street.jpg', 800, 600),
    'campbell-valley-street': ('/assets/photos/campbell-valley-street.jpg', 800, 600),
    'capitol-hill-street': ('/assets/photos/capitol-hill-street.jpg', 800, 600),
    'cariboo-street': ('/assets/photos/cariboo-street.jpg', 800, 600),
    'cedar-hills-street': ('/assets/photos/cedar-hills-street.jpg', 800, 600),
    'central-park-burnaby-street': ('/assets/photos/central-park-burnaby-street.jpg', 800, 600),
    'chilliwack-street': ('/assets/photos/chilliwack-street.jpg', 800, 600),
    'chimney-hill-street': ('/assets/photos/chimney-hill-street.jpg', 800, 600),
    'city-centre-street': ('/assets/photos/city-centre-street.jpg', 800, 600),
    'clayton-street': ('/assets/photos/clayton-street.jpg', 800, 600),
    'cloverdale-street': ('/assets/photos/cloverdale-street.jpg', 800, 600),
    'coquitlam-street': ('/assets/photos/coquitlam-street.jpg', 800, 600),
    'crescent-beach-street': ('/assets/photos/crescent-beach-street.jpg', 800, 600),
    'deer-lake-street': ('/assets/photos/deer-lake-street.jpg', 800, 600),
    'delta-street': ('/assets/photos/delta-street.jpg', 800, 600),
    'downsizing-move': ('/assets/photos/downsizing-move.jpg', 800, 600),
    'downtown-vancouver-street': ('/assets/photos/downtown-vancouver-street.jpg', 800, 600),
    'east-clayton-street': ('/assets/photos/east-clayton-street.jpg', 800, 600),
    'east-newton-street': ('/assets/photos/east-newton-street.jpg', 800, 600),
    'edmonds-street': ('/assets/photos/edmonds-street.jpg', 800, 600),
    'elgin-chantrell-street': ('/assets/photos/elgin-chantrell-street.jpg', 800, 600),
    'fleetwood-street': ('/assets/photos/fleetwood-street.jpg', 800, 600),
    'forest-grove-street': ('/assets/photos/forest-grove-street.jpg', 800, 600),
    'fort-langley-street': ('/assets/photos/fort-langley-street.jpg', 800, 600),
    'fraser-heights-street': ('/assets/photos/fraser-heights-street.jpg', 800, 600),
    'glen-valley-street': ('/assets/photos/glen-valley-street.jpg', 800, 600),
    'government-road-street': ('/assets/photos/government-road-street.jpg', 800, 600),
    'grandview-heights-street': ('/assets/photos/grandview-heights-street.jpg', 800, 600),
    'green-timbers-street': ('/assets/photos/green-timbers-street.jpg', 800, 600),
    'guildford-street': ('/assets/photos/guildford-street.jpg', 800, 600),
    'harrison-hot-springs-street': ('/assets/photos/harrison-hot-springs-street.jpg', 800, 600),
    'hazelmere-street': ('/assets/photos/hazelmere-street.jpg', 800, 600),
    'highgate-street': ('/assets/photos/highgate-street.jpg', 800, 600),
    'highpoint-street': ('/assets/photos/highpoint-street.jpg', 800, 600),
    'home-evaluation': ('/assets/photos/home-evaluation.jpg', 800, 600),
    'hope-street': ('/assets/photos/hope-street.jpg', 800, 600),
    'industrial-corridor-street': ('/assets/photos/industrial-corridor-street.jpg', 800, 600),
    'johnston-heights-street': ('/assets/photos/johnston-heights-street.jpg', 800, 600),
    'kamloops-street': ('/assets/photos/kamloops-street.jpg', 800, 600),
    'kelowna-street': ('/assets/photos/kelowna-street.jpg', 800, 600),
    'king-george-corridor-street': ('/assets/photos/king-george-corridor-street.jpg', 800, 600),
    'kitsilano-street': ('/assets/photos/kitsilano-street.jpg', 800, 600),
    'ladner-street': ('/assets/photos/ladner-street.jpg', 800, 600),
    'langley-city-street': ('/assets/photos/langley-city-street.jpg', 800, 600),
    'langley-street': ('/assets/photos/langley-street.jpg', 800, 600),
    'lochdale-street': ('/assets/photos/lochdale-street.jpg', 800, 600),
    'lougheed-street': ('/assets/photos/lougheed-street.jpg', 800, 600),
    'maple-ridge-street': ('/assets/photos/maple-ridge-street.jpg', 800, 600),
    'marketing-global-reach': ('/assets/photos/marketing-global-reach.jpg', 800, 600),
    'metrotown-street': ('/assets/photos/metrotown-street.jpg', 800, 600),
    'milner-street': ('/assets/photos/milner-street.jpg', 800, 600),
    'mission-street': ('/assets/photos/mission-street.jpg', 800, 600),
    'montecito-street': ('/assets/photos/montecito-street.jpg', 800, 600),
    'morgan-creek-street': ('/assets/photos/morgan-creek-street.jpg', 800, 600),
    'mount-pleasant-street': ('/assets/photos/mount-pleasant-street.jpg', 800, 600),
    'murrayville-street': ('/assets/photos/murrayville-street.jpg', 800, 600),
    'new-westminster-street': ('/assets/photos/new-westminster-street.jpg', 800, 600),
    'newton-street': ('/assets/photos/newton-street.jpg', 800, 600),
    'north-delta-street': ('/assets/photos/north-delta-street.jpg', 800, 600),
    'north-vancouver-street': ('/assets/photos/north-vancouver-street.jpg', 800, 600),
    'ocean-park-street': ('/assets/photos/ocean-park-street.jpg', 800, 600),
    'otter-district-street': ('/assets/photos/otter-district-street.jpg', 800, 600),
    'panorama-ridge-street': ('/assets/photos/panorama-ridge-street.jpg', 800, 600),
    'pitt-meadows-street': ('/assets/photos/pitt-meadows-street.jpg', 800, 600),
    'point-grey-street': ('/assets/photos/point-grey-street.jpg', 800, 600),
    'port-coquitlam-street': ('/assets/photos/port-coquitlam-street.jpg', 800, 600),
    'port-kells-street': ('/assets/photos/port-kells-street.jpg', 800, 600),
    'port-moody-street': ('/assets/photos/port-moody-street.jpg', 800, 600),
    'prince-george-street': ('/assets/photos/prince-george-street.jpg', 800, 600),
    'richmond-street': ('/assets/photos/richmond-street.jpg', 800, 600),
    'royal-heights-street': ('/assets/photos/royal-heights-street.jpg', 800, 600),
    'salmon-river-street': ('/assets/photos/salmon-river-street.jpg', 800, 600),
    'scottsdale-street': ('/assets/photos/scottsdale-street.jpg', 800, 600),
    'shaughnessy-street': ('/assets/photos/shaughnessy-street.jpg', 800, 600),
    'south-slope-street': ('/assets/photos/south-slope-street.jpg', 800, 600),
    'south-surrey-street': ('/assets/photos/south-surrey-street.jpg', 800, 600),
    'south-westminster-street': ('/assets/photos/south-westminster-street.jpg', 800, 600),
    'sperling-duthie-street': ('/assets/photos/sperling-duthie-street.jpg', 800, 600),
    'strawberry-hill-street': ('/assets/photos/strawberry-hill-street.jpg', 800, 600),
    'sullivan-heights-burnaby-street': ('/assets/photos/sullivan-heights-burnaby-street.jpg', 800, 600),
    'sullivan-heights-street': ('/assets/photos/sullivan-heights-street.jpg', 800, 600),
    'suncrest-street': ('/assets/photos/suncrest-street.jpg', 800, 600),
    'sunnyside-street': ('/assets/photos/sunnyside-street.jpg', 800, 600),
    'sunshine-hills-street': ('/assets/photos/sunshine-hills-street.jpg', 800, 600),
    'surrey-street': ('/assets/photos/surrey-street.jpg', 800, 600),
    'tsawwassen-street': ('/assets/photos/tsawwassen-street.jpg', 800, 600),
    'tynehead-street': ('/assets/photos/tynehead-street.jpg', 800, 600),
    'univercity-sfu-street': ('/assets/photos/univercity-sfu-street.jpg', 800, 600),
    'uplands-street': ('/assets/photos/uplands-street.jpg', 800, 600),
    'vancouver-street': ('/assets/photos/vancouver-street.jpg', 800, 600),
    'walnut-grove-street': ('/assets/photos/walnut-grove-street.jpg', 800, 600),
    'west-newton-street': ('/assets/photos/west-newton-street.jpg', 800, 600),
    'west-vancouver-street': ('/assets/photos/west-vancouver-street.jpg', 800, 600),
    'westridge-street': ('/assets/photos/westridge-street.jpg', 800, 600),
    'williams-lake-street': ('/assets/photos/williams-lake-street.jpg', 800, 600),
    'willingdon-heights-street': ('/assets/photos/willingdon-heights-street.jpg', 800, 600),
    'willoughby-street': ('/assets/photos/willoughby-street.jpg', 800, 600),
    'willowbrook-street': ('/assets/photos/willowbrook-street.jpg', 800, 600),
    'yorkson-street': ('/assets/photos/yorkson-street.jpg', 800, 600),
}

# Real photos oversized for how small they're actually displayed -- each has a pre-generated
# "-sm.jpg" mobile variant (see assets/photos/*-sm.jpg) so phones don't download the full-res
# desktop file. Value is (sm variant width, true intrinsic width of the original file) -- the
# true width is needed for the srcset "w" descriptor even when a caller passes a smaller
# display width into the <img> width= attribute (e.g. blog thumbnails).
REAL_PHOTOS_SM = {
    '/assets/photos/homepage-cover.jpg': (900, 2000),
    '/assets/photos/manan-headshot.jpg': (700, 1170),
    '/assets/photos/modern-home-dusk-mountain.jpg': (900, 1920),
    '/assets/photos/entrance-dusk-stone.jpg': (900, 1920),
    '/assets/photos/dark-estate-daylight.jpg': (900, 1920),
    '/assets/photos/courtyard-entrance-dusk.jpg': (900, 1920),
    '/assets/photos/reflecting-pool-building.jpg': (900, 1920),
    '/assets/photos/whistler-pool-mountain.jpg': (900, 1700),
    '/assets/photos/acreage-langley.jpg': (900, 2000),
    '/assets/photos/blog-market-update.jpg': (900, 3000),
    '/assets/photos/blog-surrey-neighbourhoods.jpg': (900, 1920),
    '/assets/photos/blog-gas-station.jpg': (900, 1176),
}

def responsive_img_attrs(src, orig_w=None, sizes="(max-width:860px) 100vw, 590px"):
    if src not in REAL_PHOTOS_SM:
        return ''
    sm_w, true_w = REAL_PHOTOS_SM[src]
    sm_src = src.rsplit('.', 1)[0] + '-sm.jpg'
    return f' srcset="{sm_src} {sm_w}w, {src} {true_w}w" sizes="{sizes}"'

def point_list_section(dark, eyebrow, heading, lead, points, img_first=False, img_seed='surrey-real-estate', img_alt=''):
    dot_html = ''
    for p in points:
        dot_html += f"""<div class="point">
        <div class="dot">{p['icon']}</div>
        <div><strong>{p['title']}</strong><span>{p['desc']}</span></div>
      </div>"""
    eyebrow_html = f'<div class="eyebrow" style="margin-bottom:16px;">{eyebrow}</div>' if eyebrow else ''
    text_block = f"""<div>
      {eyebrow_html}
      <h2>{heading}</h2>
      <p style="color:{'#C7C5C0' if dark else 'var(--ink-soft)'};margin-top:14px;">{lead}</p>
      <div class="point-list">{dot_html}</div>
    </div>"""
    alt = img_alt or f"Sample placeholder photo — {heading}"
    if img_seed in REAL_PHOTOS:
        src, w, h = REAL_PHOTOS[img_seed]
        img_block = f'<img class="imgblock" src="{src}"{responsive_img_attrs(src, w)} alt="{alt.replace(" (sample photo)", "")}" loading="lazy" width="{w}" height="{h}">'
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

def checklist_section(title, sub, items, raised=False, dark=False):
    cls = 'content-section dark' if dark else ('content-section raised' if raised else 'content-section')
    rows_html = ''
    for it in items:
        rows_html += f"""<div class="point">
        <div class="dot">{it['icon']}</div>
        <div><strong>{it['title']}</strong><span>{it['desc']}</span></div>
      </div>"""
    return f"""<section class="{cls}">
  <div class="wrap">
    <div class="content-head center">
      <h2>{title}</h2>
      <p>{sub}</p>
    </div>
    <div class="point-list point-list-grid">{rows_html}</div>
  </div>
</section>"""

def step_section(title, sub, steps, raised=False, dark=False):
    cls = 'content-section dark' if dark else ('content-section raised' if raised else 'content-section')
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

def faq_section(title, items, dark=False, raised=False, charcoal=False):
    items_html = ''
    for q, a in items:
        items_html += f"""<div class="faq-item">
        <button class="faq-q"><span>{q}</span><span class="chev">\u25BE</span></button>
        <div class="faq-a"><p>{a}</p></div>
      </div>"""
    if charcoal:
        cls = 'content-section dark charcoal'
    elif dark:
        cls = 'content-section dark'
    elif raised:
        cls = 'content-section raised'
    else:
        cls = 'content-section'
    return f"""<section class="{cls}">
  <div class="wrap">
    <div class="content-head center">
      <h2>{title}</h2>
    </div>
    <div class="faq">{items_html}</div>
  </div>
</section>"""

def area_group_cards(groups):
    """groups: list of (label, [slugs]) tuples -> .community-card-group blocks, reusing real area names/hrefs."""
    lookup = {a['slug']: a for a in AREAS}
    cards = ''
    for label, slugs in groups:
        links = ''.join(f'<a href="{area_href(s)}">{lookup[s]["name"]} \u2192</a>' for s in slugs if s in lookup)
        cards += f"""<div class="community-card-group">
        <div class="name">{label}</div>
        <div class="group-links">{links}</div>
      </div>"""
    return cards

def community_grid_section(title, sub, areas, charcoal=False, dark=False, raised=True, groups=None, view_all=False):
    cards = ''
    for a in areas:
        cards += f"""<a class="community-card" href="{a['href']}">
        <div><div class="name">{a['name']}</div><div class="note">{a['note']}</div></div>
        <span class="arrow">\u2192</span>
      </a>"""
    if groups:
        cards += area_group_cards(groups)
    if charcoal:
        cls = 'content-section dark charcoal'
    elif dark:
        cls = 'content-section dark'
    elif raised:
        cls = 'content-section raised'
    else:
        cls = 'content-section'
    btn_cls = 'btn-outline-light' if (dark or charcoal) else 'btn-outline-dark'
    view_all_html = f'<div style="text-align:center;margin-top:24px;"><a class="{btn_cls}" href="/communities/">View All Areas \u2192</a></div>' if view_all else ''
    return f"""<section class="{cls}">
  <div class="wrap">
    <div class="content-head center"><h2>{title}</h2><p>{sub}</p></div>
    <div class="community-grid">{cards}</div>
    {view_all_html}
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

def market_snapshot_section(dark=False, raised=True):
    cls = 'content-section dark' if dark else ('content-section raised' if raised else 'content-section')
    note_style = 'color:#C7C5C0;' if dark else 'color:var(--ink-soft);'
    num_style = f'color:var({"--accent-on-dark" if dark else "--accent-deep"});'
    return f"""<section class="{cls}">
  <div class="wrap">
    <div class="content-head center">
      <h2>Fraser Valley Market Snapshot</h2>
      <p>Real numbers from the Fraser Valley Real Estate Board's most recent monthly report \u2014 not estimates.</p>
    </div>
    <div class="grid-cards cols-4">
      <div class="simple-card"><strong style="{num_style}">$877,600</strong><span>Composite benchmark price, all residential types</span></div>
      <div class="simple-card"><strong style="{num_style}">$1,350,200</strong><span>Benchmark price, single-family detached</span></div>
      <div class="simple-card"><strong style="{num_style}">$764,100</strong><span>Benchmark price, townhomes</span></div>
      <div class="simple-card"><strong style="{num_style}">$469,500</strong><span>Benchmark price, apartments &amp; condos</span></div>
    </div>
    <p style="font-size:0.8rem;{note_style}margin-top:20px;text-align:center;">Source: Fraser Valley Real Estate Board, July 2026 MLS\u00ae &amp; Home Price Index statistics. The Fraser Valley market is currently favouring buyers, with inventory near decade highs \u2014 Manan can walk you through what that means for your specific situation.</p>
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
    col_count = 0
    if schools: cols += col("Schools", "\U0001F3EB", schools); col_count += 1
    if shopping: cols += col("Shopping &amp; Grocery", "\U0001F6D2", shopping); col_count += 1
    if entertainment: cols += col("Entertainment &amp; Dining", "\U0001F37D\uFE0F", entertainment); col_count += 1
    if recreation: cols += col("Recreation &amp; Parks", "\U0001F3DE\uFE0F", recreation); col_count += 1
    grid_cls = 'local-info-grid even-cols' if col_count == 4 else 'local-info-grid'
    return f"""<section class="content-section">
  <div class="wrap">
    <div class="content-head center"><h2>Life in {name}</h2><p>Schools, shopping, dining, and recreation in {name}.</p></div>
    <div class="{grid_cls}">{cols}</div>
  </div>
</section>"""

def pro_tip(heading, text):
    return f"""<div class="pro-tip"><strong>{heading}</strong><p>{text}</p></div>"""

def price_range_grid(title, sub, items, tip_heading=None, tip_text=None, raised=True):
    cards = ''.join(f'<div class="simple-card"><strong>{n}</strong><span>{d}</span></div>' for n, d in items)
    tip_html = pro_tip(tip_heading, tip_text) if tip_heading else ''
    cls = 'content-section raised' if raised else 'content-section'
    return f"""<section class="{cls}">
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
         stats={'population': '732,000+', 'benchmark': '$1,350,200', 'benchmark_label': 'Detached Benchmark (FVREB Jul 2026)'},
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
         stats={'population': '115,000+', 'benchmark': '$1,350,200', 'benchmark_label': 'Detached Benchmark (FVREB Jul 2026)'},
         tags=['Waterfront Living', 'BC Ferries Terminal', 'Ladner & Tsawwassen'],
         desc="Delta is a diverse municipality comprising three distinct communities — Ladner, Tsawwassen, and North Delta — offering everything from waterfront living and rural acreages to the Tsawwassen ferry terminal connecting to Vancouver Island.",
         schools=["Delta School District (SD37) \u2014 24 elementary and 7 secondary schools, including District French Immersion"],
         recreation=["Ladner Leisure Centre", "North Delta Recreation Centre", "Sungod Recreation Centre", "Centennial Beach and Boundary Bay"],
         entertainment=["Restaurants in Ladner Village and dining at Tsawwassen Mills"],
         shopping=["Ladner Village shops", "Tsawwassen Mills and Tsawwassen Commons"]),
    dict(slug='langley', name='Langley', note='Small-town charm, modern amenities',
         stats={'population': '198,000+', 'benchmark': '$1,350,200', 'benchmark_label': 'Detached Benchmark (FVREB Jul 2026)'},
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
         stats={'population': '310,000+', 'benchmark': '$1,011,900', 'benchmark_label': 'Composite Benchmark (REBGV 2026)'},
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
         stats={'population': '160,000+', 'benchmark': '$1,088,800', 'benchmark_label': 'Composite Benchmark (REBGV Jul 2026)'},
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
         stats={'population': '700,000+', 'benchmark': '$1,088,800', 'benchmark_label': 'Composite Benchmark (REBGV Jul 2026)'},
         tags=['Diverse Neighbourhoods', 'Downtown Core', 'Transit-Connected'],
         desc="Vancouver real estate spans an enormous range, from dense downtown condo towers and Yaletown lofts to established west-side neighbourhoods like Shaughnessy and Point Grey, plus east-side communities like Mount Pleasant — each with its own character, price point, and community feel.",
         area_faq=[
            ("Does Manan work in Vancouver specifically, or mainly the Fraser Valley?", "Manan is a licensed BC REALTOR® who works with buyers and sellers across the Lower Mainland, including Vancouver and all of its neighbourhoods. Given how varied Vancouver's dozens of communities are, it's worth a direct conversation about the specific area you're considering."),
         ]),
    dict(slug='north-vancouver', name='North Vancouver', note='Mountains meet the waterfront',
         stats={'population': '170,000+', 'benchmark': '$779,700', 'benchmark_label': 'Condo Benchmark (REBGV 2026)'},
         tags=['North Shore Mountains', 'Lonsdale Quay', 'SeaBus Connected'],
         desc="North Vancouver spans the City and District of North Vancouver on the North Shore, from the urban waterfront energy of Lower Lonsdale and the SeaBus terminal to mountain-backed family neighbourhoods in Lynn Valley, Edgemont Village, and Deep Cove.",
         schools=["Carson Graham Secondary (IB World School — Middle Years and Diploma Programmes)", "Handsworth Secondary (North Vancouver's largest, ~1,600 students)", "Sutherland Secondary", "Seycove Secondary (Deep Cove area)", "Windsor Secondary", "Argyle Secondary", "SD44 North Vancouver serves the whole district"],
         shopping=["Lonsdale Quay Market (waterfront market and food hall)", "Capilano Mall", "Park &amp; Tilford Gardens shopping area", "Edgemont Village shops and restaurants", "Lower Lonsdale's independent shops and restaurants along Lonsdale Avenue"],
         recreation=["Grouse Mountain (skiing, snowboarding, skyride, ziplines)", "Mount Seymour Provincial Park (skiing, snowshoeing, hiking)", "Lynn Canyon Park &amp; Suspension Bridge (free admission)", "Lynn Headwaters Regional Park", "Deep Cove (kayaking, paddleboarding, Baden Powell Trail)", "Quarry Rock hike (one of Metro Vancouver's most popular day hikes)"],
         area_faq=[
            ("What's the difference between the City and District of North Vancouver?", "They're two separate municipalities sharing the North Shore. The City is smaller and more urban, centred around Lonsdale and the SeaBus terminal. The District is larger and more suburban, covering neighbourhoods like Lynn Valley, Edgemont, and Deep Cove, with bigger lots and a more mountain-community feel."),
            ("How do you get to downtown Vancouver from North Vancouver?", "The SeaBus runs every 10–15 minutes from Lonsdale Quay to Waterfront Station downtown — a 12-minute crossing. Highway 1 and the Lions Gate Bridge also connect, though bridge traffic during rush hour is a real factor to plan around."),
         ],
         entertainment=["Lonsdale Quay Market food hall", "Restaurants and cafés along Lonsdale Avenue", "Deep Cove's waterfront cafés (Arms Reach Bistro, Deep Cove Pizza)"]),
    dict(slug='west-vancouver', name='West Vancouver', note="Metro Vancouver's premium North Shore",
         stats={'population': '46,000+', 'benchmark': '$3,060,000', 'benchmark_label': 'Detached Benchmark (REBGV 2026)'},
         tags=['Waterfront Living', 'Park Royal', 'Cypress Mountain'],
         desc="West Vancouver is one of Metro Vancouver's most established luxury residential communities, stretching along the North Shore waterfront from Ambleside and Dundarave through the British Properties and out to Horseshoe Bay's BC Ferries terminal.",
         schools=["Rockridge Secondary (IB Middle Years Programme, Advanced Placement)", "Sentinel Secondary (French Immersion, Advanced Placement, ~1,160 students)", "West Vancouver Secondary (IB Diploma, Arts, Trades)", "West Vancouver Schools (SD45) — 14 elementary and 3 secondary schools district-wide"],
         shopping=["Park Royal Shopping Centre (Metro Vancouver's first shopping centre, major expansion)", "Ambleside Village shops and restaurants along Marine Drive", "Dundarave Village's independent boutiques and cafés", "Caulfeild Village"],
         recreation=["Cypress Mountain (skiing, snowboarding, snowshoeing — a 2010 Olympic venue)", "Lighthouse Park (old-growth forest, granite shoreline, hiking trails)", "Whytecliff Park (diving, shoreline walks, marine-protected area)", "Ambleside Beach &amp; Seawalk", "Hollyburn Country Club", "West Vancouver Aquatic Centre"],
         area_faq=[
            ("What neighbourhoods make up West Vancouver?", "The main communities run east to west along the waterfront: Ambleside and Dundarave (walkable village cores), the British Properties and Chartwell (hillside estates with views), Caulfeild and Eagle Harbour (quieter, west-end residential), and Horseshoe Bay (the BC Ferries terminal village at the western tip)."),
            ("Why are West Vancouver home prices among the highest in Metro Vancouver?", "It's a combination of waterfront and mountain-view lots, large established properties (many dating to the mid-century), proximity to downtown via the Lions Gate Bridge, top-ranked public schools, and strict zoning that has historically limited densification — supply stays very tight relative to demand."),
         ],
         entertainment=["Ambleside and Dundarave Village restaurants", "Park Royal dining", "Horseshoe Bay waterfront restaurants"]),
    dict(slug='kitsilano', name='Kitsilano', note="Vancouver's beachside village",
         tags=['Kitsilano Beach', 'West 4th Avenue', 'Outdoor Lifestyle'],
         desc="Kitsilano is one of Vancouver's most sought-after westside neighbourhoods, known for its beach lifestyle, independent shops and restaurants along West 4th Avenue and West Broadway, and a walkable, village-like feel within the city.",
         schools=["Kitsilano Secondary (grades 8–12)", "Lord Byng Secondary (nearby, at the western edge of Kitsilano/Point Grey boundary)", "Several VSB elementary schools including General Gordon, Henry Hudson, and Bayview"],
         shopping=["West 4th Avenue's independent shops, boutiques, and cafés", "West Broadway corridor retail and services", "Local grocery including Whole Foods Market Kitsilano"],
         recreation=["Kitsilano Beach &amp; Kitsilano Pool (outdoor heated saltwater pool, 137m long)", "Vanier Park (home to the Museum of Vancouver, H.R. MacMillan Space Centre, and Vancouver Maritime Museum)", "Jericho Beach Park", "Hadden Park and the Seaside Greenway cycling/walking path"],
         area_faq=[
            ("What's Kitsilano like as a neighbourhood to live in?", "Kits has a genuine village feel — walkable streets, independent coffee shops and restaurants, and beach access that residents actually use daily, not just on weekends. Housing ranges from character homes on tree-lined streets to low-rise apartments and newer infill townhomes, with prices reflecting one of Vancouver's most desirable westside locations."),
            ("Is Kitsilano good for families or more of a young-professional neighbourhood?", "Both. The eastern end closer to Broadway has more rentals and younger demographics, while the residential streets south of 4th Avenue and west toward Point Grey are full of established families. Kitsilano Secondary and the nearby elementary schools have strong reputations."),
         ],
         entertainment=["West 4th Avenue restaurants and cafés", "Jericho Beach summer concessions", "Vanier Park's museums and waterfront events"]),
    dict(slug='point-grey', name='Point Grey &amp; UBC', note='University district, Pacific Spirit Park',
         tags=['University of British Columbia', 'Pacific Spirit Park', 'Wesbrook Village'],
         desc="Point Grey and the UBC campus area sit at Vancouver's western tip, where Pacific Spirit Regional Park's 763 hectares of forest trails meet the university's growing residential neighbourhoods in Wesbrook Village and University Hill — plus some of Vancouver's most established old-money residential streets.",
         schools=["University Hill Secondary (VSB, grades 8–12, on UBC campus in Wesbrook Place)", "Lord Byng Secondary (Point Grey, grades 8–12)", "Norma Rose Point Elementary and University Hill Elementary (both serve the UBC campus area)", "University of British Columbia (Canada's third-largest university)"],
         shopping=["Wesbrook Village (UBC's on-campus commercial centre — grocery, restaurants, cafés, pharmacy)", "West 10th Avenue shops and services near the UBC gates", "West Point Grey Village along West 10th"],
         recreation=["Pacific Spirit Regional Park (763 hectares of forest trails for hiking, running, cycling, and horseback riding)", "Spanish Banks Beach (shallow wading, beach volleyball, kiteboarding)", "Wreck Beach (clothing-optional, beneath the UBC cliffs)", "UBC Botanical Garden", "Museum of Anthropology at UBC", "Nitobe Memorial Garden"],
         area_faq=[
            ("Who typically buys in the Point Grey / UBC area?", "It's a mix: established families on Point Grey's residential streets (large lots, older character homes, high price points), UBC faculty and staff in Wesbrook Village and University Hill, investors buying campus-area condos for the student rental market, and international families wanting proximity to UBC for their children's education."),
            ("What is Wesbrook Village?", "It's UBC's master-planned residential neighbourhood on the south side of campus, built over the past decade, with mid-rise condos, townhomes, a commercial village centre, and its own elementary and secondary schools — a self-contained community that didn't exist 15 years ago."),
         ],
         entertainment=["Wesbrook Village restaurants and cafés", "UBC campus events, lectures, and cultural programming", "Museum of Anthropology exhibitions"]),
    dict(slug='downtown-vancouver', name='Downtown Vancouver', note='Urban core, waterfront condos',
         tags=['Yaletown', 'Coal Harbour', 'Stanley Park'],
         desc="Downtown Vancouver is the region's urban core — dense condo towers in Yaletown and Coal Harbour, the historic character of Gastown and Chinatown, the residential West End, and Stanley Park's 400-hectare seawall loop, all on a compact, transit-connected peninsula.",
         schools=["Limited school options downtown — primarily a market for professionals, investors, and downsizers rather than families", "King George Secondary (Mount Pleasant, nearby)", "Crosstown Elementary (opened 2019, serves the growing downtown family population)"],
         shopping=["Pacific Centre Mall (200+ stores, anchored by Nordstrom and Holt Renfrew)", "Robson Street retail corridor", "Alberni Street luxury retail (Tiffany, Louis Vuitton, Hermès)", "Gastown's independent boutiques and galleries", "Yaletown's shops along Mainland and Hamilton Streets"],
         recreation=["Stanley Park (400 hectares — seawall, beaches, Vancouver Aquarium, trails, Prospect Point)", "Coal Harbour Seawall (walking and cycling path)", "Vancouver Convention Centre waterfront public spaces", "English Bay Beach and Sunset Beach"],
         area_faq=[
            ("What are the main downtown sub-areas for condos?", "Yaletown is the converted-warehouse district with a food-and-drink scene; Coal Harbour faces the waterfront and North Shore mountains with newer luxury towers; the West End is Vancouver's densest residential neighbourhood with strong rental and resale markets; and Gastown/Crosstown have character conversions and newer builds at a range of price points."),
            ("Is downtown Vancouver a good investment-property market?", "It's one of the region's strongest rental markets — low vacancy rates, strong tenant demand from downtown workers and international students, and the density and transit access that support long-term appreciation. Strata rules and rental restrictions vary building to building, so due diligence on the specific strata corporation is essential."),
         ],
         entertainment=["Rogers Arena (Canucks, concerts)", "BC Place Stadium (Whitecaps, Lions, major events)", "Granville Entertainment District", "Gastown's restaurants and bars", "Yaletown dining and nightlife"]),
    dict(slug='mount-pleasant', name='Mount Pleasant', note="Vancouver's creative hub",
         tags=['Main Street', 'Brewery Creek', 'Independent Shops'],
         desc="Mount Pleasant is one of Vancouver's most dynamic neighbourhoods, centred around Main Street's independent shops, Brewery Creek's craft beer scene, and a creative community of studios, galleries, and tech companies — with real estate ranging from heritage character homes to new-build condos.",
         schools=["SD39 Vancouver elementary schools serve the neighbourhood — confirm specific catchment based on address", "King George Secondary (nearby)", "Emily Carr University of Art + Design (Great Northern Way campus, just east)"],
         shopping=["Main Street's independent shops, vintage stores, and boutiques (roughly 2nd Ave to 30th Ave)", "Brewery Creek area shops", "Broadway corridor for larger retail and services"],
         recreation=["Mount Pleasant Community Centre (gymnasium, pool, fitness centre)", "Jonathan Rogers Park", "Dude Chilling Park", "Guelph Park (dog park)", "Brewery Creek urban trails"],
         area_faq=[
            ("What's the vibe of Mount Pleasant?", "It's Vancouver's most recognizably 'creative neighbourhood' — murals on buildings, independent coffee roasters on every other block along Main Street, craft breweries in the Brewery Creek cluster, tech companies in converted industrial space, and a weekend farmers' market. Housing prices reflect the popularity."),
            ("How does Mount Pleasant compare to Kitsilano?", "They attract different demographics: Kits is beachside, slightly more established, and westside; Mount Pleasant is east-side, more urban-gritty, younger-skewing, and known more for food, beer, and art than beaches. Both are walkable and popular — Mount Pleasant typically offers more variety at slightly lower price points than Kits."),
         ],
         entertainment=["Main Street restaurants and cafés", "Brewery Creek craft breweries (33 Acres, Brassneck, Main Street Brewing, Faculty Brewing)", "Fox Cabaret and other live-music venues"]),
    dict(slug='shaughnessy', name='Shaughnessy', note="Vancouver's grand residential neighbourhood",
         tags=['Heritage Estates', 'Tree-Lined Streets', 'First Shaughnessy'],
         desc="Shaughnessy is one of Vancouver's most prestigious residential neighbourhoods — grand heritage homes on large lots along tree-lined crescents, with First Shaughnessy designated as a heritage conservation area, and proximity to VanDusen Botanical Garden, Queen Elizabeth Park, and South Granville's shops.",
         schools=["Shaughnessy Elementary (public)", "Quilchena Elementary (public)", "York House School (independent girls' school, K–12)", "Little Flower Academy (independent girls' school, grades 8–12)", "Vancouver College (independent boys' school, K–12, nearby)", "Eric Hamber Secondary and Prince of Wales Secondary serve the surrounding catchments"],
         shopping=["South Granville shopping and dining (Granville Street between 12th and 16th Avenues)", "Kerrisdale Village nearby (41st Avenue and West Boulevard)", "Oakridge Centre (under major redevelopment into a mixed-use town centre)"],
         recreation=["VanDusen Botanical Garden (55 acres, 7,500+ plant species, Elizabethan hedge maze)", "Queen Elizabeth Park (highest point in Vancouver, Bloedel Conservatory, pitch-and-putt golf)", "Shaughnessy Park", "Crescent-shaped streets designed for walking"],
         area_faq=[
            ("What is First Shaughnessy?", "It's the original subdivision developed by the Canadian Pacific Railway starting in 1907, now a heritage conservation area with restrictions on demolition and exterior alterations — the grand homes along The Crescent, Angus Drive, and Osler Street are among Vancouver's most recognizable residential properties."),
            ("What price range does Shaughnessy typically trade at?", "Shaughnessy is consistently one of Vancouver's highest-value residential neighbourhoods, with detached homes on the larger First Shaughnessy lots typically trading well above the city-wide average. Exact pricing varies significantly by lot size, heritage status, and condition — contact Manan for current market context."),
         ],
         entertainment=["South Granville's restaurants and galleries", "VanDusen Festival of Lights (seasonal)", "Queen Elizabeth Park's Seasons in the Park restaurant"]),
    dict(slug='richmond', name='Richmond', note='Historic charm meets urban energy',
         stats={'population': '225,000+', 'benchmark': '$1,088,800', 'benchmark_label': 'Composite Benchmark (REBGV Jul 2026)'},
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
         stats={'population': '160,000+', 'benchmark': '$1,350,200', 'benchmark_label': 'Detached Benchmark (FVREB Jul 2026)'},
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
    dict(slug='williams-lake', name='Williams Lake', note='Stampede Capital of BC',
         tags=['Cariboo Region', 'Stampede Capital of BC', 'Lakeside Living'],
         desc="Williams Lake is a central Cariboo hub built around its namesake freshwater lake, known across BC as the Stampede Capital for its world-famous annual rodeo, with a real estate market spanning in-town family homes to rural acreages and ranches just beyond the city limits.",
         schools=["Williams Lake Junior Secondary (Grades 8\u201310)", "Williams Lake Secondary (Grades 11\u201312)"],
         recreation=["Williams Lake itself \u2014 boating, kayaking, paddleboarding, and fishing", "Extensive walking and trail networks", "Home of the annual Williams Lake Stampede"],
         area_faq=[
            ("What is Williams Lake known for?", "It's proudly known as the Stampede Capital of BC, home to the world-famous Williams Lake Stampede, alongside lakeside recreation and easy access to Cariboo ranch country."),
            ("What kind of properties are available in Williams Lake?", "The market spans in-town family homes close to schools and parks to expansive rural acreages and ranches just outside town \u2014 a genuinely different mix than the Lower Mainland."),
         ]),
    dict(slug='prince-george', name='Prince George', note="Northern BC's largest city",
         tags=['Northern BC Hub', 'University of Northern BC', 'Four-Season Recreation'],
         desc="Prince George is northern BC's largest city and regional hub, home to the University of Northern British Columbia, with neighbourhoods ranging from established family areas to newer developments built around the university.",
         schools=["University of Northern British Columbia (UNBC)", "Lakewood Elementary &amp; Westwood Secondary (College Heights)"],
         shopping=["College Heights' big-box retail, banks, and restaurants"],
         recreation=["Hart Highlands Ski Hill", "Aberdeen Glen Golf Course", "Extensive hiking, biking, and trail networks (Old Summit Lake area)", "Riverside parks and trails near South Fort George"],
         entertainment=["Restaurants and pubs in College Heights", "Park Drive-In (Old Summit Lake area)"],
         area_faq=[
            ("What neighbourhoods are popular for families in Prince George?", "College Heights (served by Lakewood Elementary and Westwood Secondary) and University Heights, a newer development of craftsman-style homes a short walk from UNBC, are both commonly highlighted family areas."),
            ("Is Prince George a university town?", "Yes \u2014 it's home to the University of Northern British Columbia, and the University Heights neighbourhood was built specifically around it."),
         ]),
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

# ============================================================
# Real geography groupings for "Other Communities" cross-links -- replaces a
# static first-3-in-list slice that ignored proximity entirely (e.g. Kelowna's
# page was suggesting Surrey/Fleetwood as "other communities"). Neighbourhoods
# are grouped under their real parent city; standalone cities are their own
# group. GROUP_NEIGHBORS gives real-world adjacent cities to fall back on when
# a group has too few (or zero) siblings of its own -- e.g. Hope has no
# neighbourhood pages of its own, so it falls back to Chilliwack/Harrison.
# ============================================================
AREA_GROUPS = {
    'Surrey': ['surrey', 'fleetwood', 'cloverdale', 'city-centre', 'newton', 'industrial-corridor',
               'guildford', 'east-newton', 'west-newton', 'east-clayton', 'clayton', 'fraser-heights',
               'panorama-ridge', 'sullivan-heights', 'grandview-heights', 'sunnyside',
               'king-george-corridor', 'port-kells', 'bridgeview', 'bolivar-heights', 'cedar-hills',
               'royal-heights', 'johnston-heights', 'green-timbers', 'tynehead', 'hazelmere',
               'campbell-heights', 'chimney-hill', 'bear-creek', 'strawberry-hill', 'south-westminster'],
    'South Surrey / White Rock': ['south-surrey', 'morgan-creek', 'elgin-chantrell', 'ocean-park', 'crescent-beach'],
    'Langley': ['langley', 'fort-langley', 'willoughby', 'walnut-grove', 'langley-city', 'brookswood',
                'murrayville', 'aldergrove', 'willowbrook', 'yorkson', 'salmon-river', 'campbell-valley',
                'highpoint', 'otter-district', 'milner', 'glen-valley'],
    'Delta': ['delta', 'ladner', 'tsawwassen', 'north-delta', 'sunshine-hills', 'annieville',
              'scottsdale', 'boundary-bay', 'uplands'],
    'Burnaby': ['burnaby', 'metrotown', 'brentwood', 'lougheed', 'deer-lake', 'capitol-hill', 'edmonds',
                'burnaby-heights', 'south-slope', 'highgate', 'central-park-burnaby', 'government-road',
                'cariboo', 'big-bend', 'sperling-duthie', 'willingdon-heights', 'forest-grove',
                'suncrest', 'montecito', 'univercity-sfu', 'lochdale', 'westridge', 'sullivan-heights-burnaby'],
    'Coquitlam': ['coquitlam'],
    'Port Coquitlam': ['port-coquitlam'],
    'New Westminster': ['new-westminster'],
    'Vancouver': ['vancouver', 'kitsilano', 'point-grey', 'downtown-vancouver', 'mount-pleasant', 'shaughnessy'],
    'North Vancouver': ['north-vancouver'],
    'West Vancouver': ['west-vancouver'],
    'Richmond': ['richmond'],
    'Port Moody': ['port-moody'],
    'Pitt Meadows': ['pitt-meadows'],
    'Abbotsford': ['abbotsford'],
    'Maple Ridge': ['maple-ridge'],
    'Mission': ['mission'],
    'Chilliwack': ['chilliwack'],
    'Hope': ['hope'],
    'Harrison Hot Springs': ['harrison-hot-springs'],
    'Kelowna': ['kelowna'],
    'Kamloops': ['kamloops'],
    'Williams Lake': ['williams-lake'],
    'Prince George': ['prince-george'],
}
SLUG_TO_GROUP = {slug: group for group, slugs in AREA_GROUPS.items() for slug in slugs}
# Real city-center coordinates for the hero/area-page Realtor.ca deep-link search dropdown.
GROUP_COORDS = [
    ("Delta", "49.0847,-123.0587"),
    ("Surrey", "49.1913,-122.8490"),
    ("Langley", "49.1042,-122.6604"),
    ("South Surrey / White Rock", "49.0189,-122.8025"),
    ("Burnaby", "49.2488,-122.9805"),
    ("Coquitlam", "49.2838,-122.7932"),
    ("Port Coquitlam", "49.2626,-122.7811"),
    ("Port Moody", "49.2838,-122.8519"),
    ("Pitt Meadows", "49.2213,-122.6892"),
    ("New Westminster", "49.2057,-122.9110"),
    ("Vancouver", "49.2827,-123.1207"),
    ("North Vancouver", "49.3200,-123.0724"),
    ("West Vancouver", "49.3280,-123.1598"),
    ("Richmond", "49.1666,-123.1336"),
    ("Abbotsford", "49.0504,-122.3045"),
    ("Maple Ridge", "49.2193,-122.6019"),
    ("Mission", "49.1337,-122.3255"),
    ("Chilliwack", "49.1579,-121.9514"),
    ("Hope", "49.3831,-121.4416"),
    ("Harrison Hot Springs", "49.3003,-121.7857"),
    ("Kelowna", "49.8880,-119.4960"),
    ("Kamloops", "50.6745,-120.3273"),
    ("Williams Lake", "52.1417,-122.1417"),
    ("Prince George", "53.9171,-122.7497"),
]
GROUP_COORD_MAP = dict(GROUP_COORDS)
GROUP_NEIGHBORS = {
    'Surrey': ['Delta', 'Langley', 'South Surrey / White Rock', 'New Westminster'],
    'South Surrey / White Rock': ['Surrey', 'Delta', 'Langley'],
    'Langley': ['Surrey', 'Abbotsford', 'Maple Ridge'],
    'Delta': ['Surrey', 'Richmond', 'South Surrey / White Rock'],
    'Burnaby': ['Vancouver', 'New Westminster', 'Coquitlam'],
    'Coquitlam': ['Port Coquitlam', 'Port Moody', 'Burnaby'],
    'Port Coquitlam': ['Coquitlam', 'Port Moody', 'Pitt Meadows'],
    'New Westminster': ['Burnaby', 'Coquitlam', 'Surrey'],
    'Vancouver': ['Burnaby', 'Richmond', 'New Westminster', 'North Vancouver', 'West Vancouver'],
    'North Vancouver': ['West Vancouver', 'Vancouver', 'Burnaby'],
    'West Vancouver': ['North Vancouver', 'Vancouver'],
    'Richmond': ['Vancouver', 'Delta'],
    'Port Moody': ['Coquitlam', 'Port Coquitlam', 'Burnaby'],
    'Pitt Meadows': ['Maple Ridge', 'Port Coquitlam'],
    'Abbotsford': ['Langley', 'Mission', 'Chilliwack'],
    'Maple Ridge': ['Pitt Meadows', 'Langley', 'Mission'],
    'Mission': ['Abbotsford', 'Maple Ridge', 'Chilliwack'],
    'Chilliwack': ['Abbotsford', 'Mission', 'Hope'],
    'Hope': ['Chilliwack', 'Harrison Hot Springs'],
    'Harrison Hot Springs': ['Hope', 'Chilliwack'],
    'Kelowna': ['Kamloops'],
    'Kamloops': ['Kelowna', 'Williams Lake', 'Prince George'],
    'Williams Lake': ['Kamloops', 'Prince George'],
    'Prince George': ['Williams Lake', 'Kamloops'],
}
# Areas the client called out as genuinely more remote from the Fraser Valley/
# Lower Mainland core -- these lean more commercial/investment-focused in
# content since they're less likely to be a typical Lower Mainland commuter's
# residential search, and more likely a ranch, acreage, tourism, or investment
# conversation.
OUT_OF_TOWN_GROUPS = {'Hope', 'Harrison Hot Springs', 'Kelowna', 'Kamloops', 'Williams Lake', 'Prince George'}

def _auto_supplement_faqs(area, target=6):
    faqs = list(area.get('area_faq') or [])
    existing_q = ' '.join(q.lower() for q, _ in faqs)
    name = area['name']
    is_out_of_town = SLUG_TO_GROUP.get(area['slug']) in OUT_OF_TOWN_GROUPS
    candidates = []
    if is_out_of_town and 'investment' not in existing_q and 'commercial' not in existing_q:
        # Prioritized first (not appended at the end) so it reliably survives the
        # target=6 cap even on information-rich pages like Kelowna, which already
        # fill most slots with schools/shopping/recreation/custom FAQs.
        candidates.append((
            f"What investment or commercial opportunities exist in {name}?",
            f"Areas like {name} often draw interest beyond a typical residential buyer — acreages, ranch or rural land, tourism-driven commercial space, and income properties can all be part of the picture depending on the specific property and zoning. Manan can walk through what's realistic for {name} specifically, residential or otherwise."
        ))
    if 'familiar with' not in existing_q:
        # Prioritized right after the out-of-town investment question (not appended at
        # the end) so this confident, non-limiting answer reliably survives the target=6
        # cap even on information-rich pages that already fill most slots with
        # schools/shopping/recreation -- see the out-of-town candidate above for the same
        # reasoning. Client was explicit: don't let Manan read as boxed into one sub-region.
        candidates.append((
            f"Is Manan familiar with {name} specifically?",
            f"Yes \u2014 as a licensed REALTOR\u00ae in British Columbia, Manan works with clients across the province, not just one sub-region, and can speak directly to {name}'s current inventory, pricing, and what makes it different from its neighbours."
        ))
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
    if is_out_of_town:
        candidates.append((
            f"Is now a good time to buy or sell in {name}?",
            f"Conditions in {name} can move differently than the Lower Mainland's \u2014 driven more by local tourism, resource, or agricultural economics than commuter demand. Rather than relying on general Lower Mainland trends, it's worth a direct, current conversation with Manan about what's happening specifically in {name}."
        ))
    else:
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

_AREA_CARD_BY_SLUG = {a['slug']: dict(name=a['name'], href=area_href(a['slug']), note=a['note']) for a in AREAS}

def related_area_cards(current_slug, count=3):
    """Geography-aware 'Other Communities' picks: same-city siblings first,
    then real adjacent cities, so Fleetwood (a Surrey neighbourhood) only ever
    shows up next to other Surrey pages instead of next to Kelowna or Vancouver."""
    picked, seen = [], {current_slug}
    current_group = SLUG_TO_GROUP.get(current_slug)
    if current_group:
        for slug in AREA_GROUPS[current_group]:
            if len(picked) >= count:
                break
            if slug not in seen and slug in _AREA_CARD_BY_SLUG:
                picked.append(_AREA_CARD_BY_SLUG[slug])
                seen.add(slug)
        # Round-robin one pick per neighbouring city first, so a city with no
        # sub-neighbourhood pages of its own (Vancouver, Coquitlam, etc.) gets
        # geographic variety -- e.g. Burnaby + Richmond + New Westminster --
        # instead of exhausting one neighbour's whole sub-area list first.
        neighbor_queues = [list(AREA_GROUPS.get(g, [])) for g in GROUP_NEIGHBORS.get(current_group, [])]
        while len(picked) < count and any(neighbor_queues):
            for queue in neighbor_queues:
                if len(picked) >= count:
                    break
                while queue:
                    slug = queue.pop(0)
                    if slug not in seen and slug in _AREA_CARD_BY_SLUG:
                        picked.append(_AREA_CARD_BY_SLUG[slug])
                        seen.add(slug)
                        break
    # Deliberately no generic fallback beyond real groups/neighbours -- a remote
    # area like Kelowna or Kamloops genuinely only has one or two honest
    # "nearby" picks, and padding with an unrelated Surrey neighbourhood is
    # exactly the bug this function replaces. The grid layout handles 1-3
    # cards without leaving a gap (see .community-grid's auto-fit rule).
    return picked[:count]

# ============================================================
# /buyers/  — Buy a Home hub
# ============================================================
buyers_body = subhero(
    "",
    'Your <span class="gradient-text">Home Buying</span> Journey',
    "A clear, guided process from first conversation to key handover \u2014 with full buyer representation across Surrey and the Lower Mainland.",
    TEXT_CTA + CONTACT_CTA,
    flat_dark=True
)
buyers_body += market_snapshot_section(dark=True)
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
    ],
    dark=True
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
buyers_body += f"""<section class="content-section">
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
      <a class="btn-solid-warm calc-cta" id="calcCta" href="sms:+16047279542">\U0001F4AC Contact Manan to Learn More</a>
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
buyers_body += community_grid_section(
    "Popular Communities", f'A few places to start — explore all <a href="/communities/" style="color:var(--accent-on-dark);font-weight:600;text-decoration:underline;">{len(AREAS)} communities</a> Manan serves for the full picture.',
    [],
    raised=False, dark=True, view_all=True,
    groups=[
        ('Surrey', ['city-centre', 'fleetwood', 'cloverdale', 'guildford', 'newton']),
        ('Delta', ['ladner', 'tsawwassen', 'north-delta']),
        ('South Surrey / White Rock', ['south-surrey', 'morgan-creek', 'ocean-park', 'crescent-beach']),
        ('Langley', ['langley-city', 'willoughby', 'walnut-grove', 'fort-langley']),
        ('Metro Vancouver', ['vancouver', 'burnaby', 'coquitlam']),
        ('Out of Town', ['kamloops', 'kelowna', 'hope']),
    ]
)
buyers_body += cta_band(
    'Ready to Start Your <span class="accent-warm">Home Search</span>?',
    "A free, no-pressure consultation is the best place to start.",
    EVAL_CTA
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
    "",
    '<span class="gradient-text">First-Time Home Buyers</span> <br>Surrey &amp; Fraser Valley',
    "Buying your first home is one of the biggest decisions you'll make. Manan guides first-time buyers through every step \u2014 from government programs to keys in hand.",
    '<a class="btn-solid-warm" href="/contact/">Book a Free Consultation</a>',
    flat_dark=True
)
ft_body += point_list_section(
    True, "", "Why Work With a Buyer's Agent as a First-Timer",
    "Your first purchase comes with the steepest learning curve \u2014 financing rules, strata documents, subject conditions, closing costs. A dedicated buyer's agent means someone in your corner who explains every decision in plain language, at no direct cost to you in most transactions.",
    [
        dict(icon="\U0001F4CB", title="No Pressure, No Rush", desc="Manan takes a hands-on, personal approach \u2014 you'll never feel pushed into a decision before you're ready."),
        dict(icon="\U0001F50D", title="Every Document Explained", desc="Inspection reports, strata minutes, title search \u2014 explained clearly so you know exactly what you're buying."),
        dict(icon="\u2696\uFE0F", title="Honest Opinions", desc="If a property isn't right for you, Manan will tell you \u2014 even if it means more time searching."),
    ],
    img_first=True, img_seed='first-time-buyer-keys', img_alt="First-time buyers receiving keys (sample photo)"
)
ft_body += f"""<section class="content-section">
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
ft_body += step_section(
    "What Your Budget Actually Buys Right Now",
    "Real Fraser Valley benchmark prices by property type \u2014 a starting point for setting expectations before you shop.",
    [
        dict(title="Under the Condo Benchmark", desc="At a $469,500 benchmark, apartments in Surrey City Centre, Whalley, and parts of Newton remain the most accessible entry point, especially near SkyTrain."),
        dict(title="Around the Townhome Benchmark", desc="At a $764,100 benchmark, townhomes in Cloverdale, Clayton, and parts of Langley offer more space than a condo without stretching to a detached home."),
        dict(title="Approaching the Detached Benchmark", desc="At a $1,350,200 benchmark, detached homes are within reach in Abbotsford, Chilliwack, and select North Surrey pockets, particularly with a larger down payment."),
    ],
    dark=True
)
ft_body += market_snapshot_section(dark=False, raised=False)
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
    ], cols=4, raised=False, dark=True
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

def simple_service_page(path, crumb_label, eyebrow, h1, lead, points, extra="", faq=None, related=None, area_slugs=None, area_groups=None):
    body = subhero("", f'<span class="gradient-text">{h1}</span>', lead, CONTACT_CTA, flat_dark=True)
    body += point_list_section(True, "", "What This Means For You", "", points, img_first=True, img_seed=path.strip('/').replace('/', '-'), img_alt=f"{crumb_label} (sample photo)")
    body += extra
    if area_slugs or area_groups:
        # avoid 3 light sections in a row when there's already an "extra" section before this one
        body += community_grid_section(
            f"Where to Look for {crumb_label}", "Real neighbourhood guides across the areas Manan serves.",
            area_cards(area_slugs) if area_slugs else [], raised=False, dark=bool(extra), groups=area_groups
        )
    if faq:
        body += faq_section(f"{crumb_label} Questions, Answered", faq)
    if related:
        body += simple_cards("Related Buyer Services", "Other ways Manan helps buyers across the Fraser Valley.", related, cols=3, raised=False, dark=True)
    body += cta_band(
        'Let\'s Talk It <span class="accent-warm">Through</span>',
        "Every situation is different \u2014 a short call is the fastest way to figure out the right approach for yours.",
        CONTACT_CTA
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
        area_groups=[
            ('Surrey', ['city-centre', 'fleetwood', 'cloverdale', 'guildford', 'grandview-heights']),
            ('Langley', ['langley-city', 'willoughby', 'walnut-grove']),
            ('South Surrey / White Rock', ['south-surrey']),
            ('Delta', ['ladner', 'tsawwassen']),
            ('Burnaby', ['metrotown', 'brentwood', 'lougheed', 'highgate']),
            ('Vancouver', ['downtown-vancouver', 'mount-pleasant', 'kitsilano']),
        ]
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
            tip_text="Most new investors anchor on the rent number in the listing and never check what comparable units actually leased for. Manan pulls recently-leased comparables \u2014 not asking rents \u2014 and underwrites conservatively, budgeting for vacancy, maintenance, and the first major repair. Cleaner numbers going in means fewer surprises in year two.",
            raised=False
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
        area_groups=[
            ('Surrey', ['newton', 'city-centre', 'guildford', 'east-newton', 'campbell-heights']),
            ('Langley', ['langley-city', 'willoughby']),
            ('Delta', ['north-delta', 'ladner']),
            ('Burnaby', ['metrotown', 'edmonds', 'lougheed']),
            ('Abbotsford', ['abbotsford']),
        ]
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
            tip_text="Land \u2014 lot size, location, view corridor, and zoning \u2014 is the most durable driver of value in this market. Finishes and floor plans get renovated every 15\u201320 years; the lot doesn't change. When evaluating a luxury purchase or listing, Manan weighs the land first and the structure second.",
            raised=False
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
        area_groups=[
            ('South Surrey / White Rock', ['south-surrey', 'morgan-creek', 'elgin-chantrell', 'ocean-park', 'crescent-beach']),
            ('Surrey', ['grandview-heights', 'panorama-ridge']),
            ('Vancouver', ['shaughnessy', 'point-grey']),
            ('West Vancouver', ['west-vancouver']),
        ]
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
    "",
    'Sell Your Property for <span class="gradient-text">Top Dollar</span>',
    "A clear pricing, marketing, and negotiation strategy \u2014 built around your property and your timeline.",
    EVAL_CTA,
    flat_dark=True
)
sellers_body += market_snapshot_section(dark=True)
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
    cols=2, raised=False, dark=True
)
sellers_body += community_grid_section(
    "Popular Communities", f'A few places to start — explore all <a href="/communities/" style="color:var(--accent-deep);font-weight:600;text-decoration:underline;">{len(AREAS)} communities</a> Manan serves for the full picture.',
    [],
    raised=False,
    groups=[
        ('Surrey', ['city-centre', 'fleetwood', 'cloverdale', 'guildford', 'newton']),
        ('Delta', ['ladner', 'tsawwassen', 'north-delta']),
        ('South Surrey / White Rock', ['south-surrey', 'morgan-creek', 'ocean-park', 'crescent-beach']),
        ('Langley', ['langley-city', 'willoughby', 'walnut-grove', 'fort-langley']),
        ('Metro Vancouver', ['vancouver', 'burnaby', 'coquitlam']),
        ('Out of Town', ['kamloops', 'kelowna', 'hope']),
    ]
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
    EVAL_CTA
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
    "",
    '<span class="gradient-text">What Is Your Home Worth?</span>',
    "Get a market-based home evaluation from Manan Bhullar \u2014 free, no obligation, no pressure.",
    CONTACT_CTA,
    flat_dark=True
)
he_body += f"""<section class="content-section dark">
  <div class="wrap two-col">
    <div>
      <h2>How the Evaluation Works</h2>
      <p style="color:#C7C5C0;margin-top:14px;">Manan reviews current comparable sales, active listings, and your property's specific features and condition to give you a realistic, market-based estimate \u2014 not an inflated number designed to win your listing.</p>
      <div class="point-list">
        <div class="point"><div class="dot">\U0001F4CA</div><div><strong>Comparable Sales Review</strong><span>Recent, relevant sales in your immediate area and property type.</span></div></div>
        <div class="point"><div class="dot">\U0001F3E0</div><div><strong>Property Walkthrough</strong><span>An in-person or video walkthrough to account for condition, upgrades, and unique features.</span></div></div>
        <div class="point"><div class="dot">\U0001F4DD</div><div><strong>Written Summary</strong><span>A clear written estimate with the reasoning behind it, so you understand exactly how the number was reached.</span></div></div>
      </div>
    </div>
    <img class="imgblock" src="/assets/photos/home-evaluation.jpg" alt="Free home evaluation walkthrough" loading="lazy" width="800" height="600">
  </div>
</section>"""
he_body += market_snapshot_section(raised=False)
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
    "",
    '<span class="gradient-text">A Thoughtful Approach to Downsizing</span>',
    "Selling the family home and moving to your next chapter is a big transition \u2014 Manan helps make it a well-paced, low-stress one.",
    CONTACT_CTA,
    flat_dark=True
)
ds_body += point_list_section(
    True, "", "What Sets a Downsizing Sale Apart", "",
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
def market_context_section(heading, paragraphs, img_seed, img_alt, fact_label=None, fact_value=None, dark=False, tight=False):
    para_style = ' style="color:#C7C5C0;margin-top:14px;"' if dark else ' style="color:var(--ink-soft);margin-top:14px;"'
    paras_html = ''.join(f'<p{para_style}>{p}</p>' for p in paragraphs)
    if img_seed in REAL_PHOTOS:
        src, w, h = REAL_PHOTOS[img_seed]
    else:
        src, w, h = f"https://picsum.photos/seed/{img_seed}/900/675", 900, 675
    badge_html = ''
    if fact_label:
        badge_html = f'<div class="market-fact-badge"><span>{fact_label}</span><strong>{fact_value}</strong></div>'
    cls = 'content-section dark' if dark else 'content-section'
    if tight:
        cls += ' tight'
    return f"""<section class="{cls}">
  <div class="wrap two-col">
    <div>
      <h2>{heading}</h2>
      {paras_html}
    </div>
    <div class="market-context-photo">
      <img src="{src}"{responsive_img_attrs(src, w)} alt="{img_alt}" loading="lazy" width="{w}" height="{h}">
      {badge_html}
    </div>
  </div>
</section>"""

comm_body = subhero(
    "",
    'Commercial Real Estate <span class="gradient-text">Across the Lower Mainland</span>',
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

def commercial_cta_form(category_name, related_slugs, form_title=None, gradient=False):
    ft = form_title or f"{category_name} Inquiry"
    pills = ''.join(f'<a href="{cc_href(s)}">{next(c["title"] for c in COMMERCIAL_CATEGORIES if c["slug"]==s)} \u2192</a>' for s in related_slugs)
    pills += '<a href="/commercial/">All Commercial \u2192</a>'
    form = lead_form(ft, f"New {category_name} Inquiry \u2014 mananbhullar.com")
    accent_cls = 'gradient-text' if gradient else 'accent-warm'
    return f"""<section class="cta-form-band">
  <div class="wrap cta-form-grid">
    <div class="cta-form-left">
      <h2>Buying or Selling <span class="{accent_cls}">{category_name}</span>?</h2>
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
    "Explore Our Commercial Services", "Specialized real estate representation across 17 commercial property and business categories, each with its own valuation, due diligence, and financing approach.",
    [dict(title=c['title'], desc=c['desc'], href=cc_href(c['slug']), icon=c['icon']) for c in COMMERCIAL_CATEGORIES],
    cols=4, raised=False
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
    cols=3, raised=False, dark=True
)
comm_body += commercial_cta_form("Commercial Property", ['industrial', 'retail'], form_title="Commercial Property Inquiry", gradient=True)
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
                    middle_section="", faq=None, related_slugs=None,
                    valued_raised=True, valued_dark=False, dd_dark=False, faq_dark=False, market_dark=False, faq_before_dd=False,
                    dd_as_steps=False, market_tight=False, h1_gradient=False):
    slug = path.strip('/').split('/')[-1]
    h1_html = f'<span class="gradient-text">{h1}</span>' if h1_gradient else h1
    subhero_cls = 'subhero flat-dark' if h1_gradient else 'subhero'
    body = f"""<section class="{subhero_cls}">
  <div class="wrap">
    <h1>{h1_html}</h1>
    <p class="lead">{lead}</p>
    <div class="hero-ctas">{CONTACT_CTA}</div>
  </div>
</section>"""
    body += market_context_section(market_heading, market_paragraphs, market_photo_seed, f"{label} (sample photo)", dark=market_dark, tight=market_tight)
    body += info_cards(valued_title, valued_sub, valued_items, cols=2, raised=valued_raised, dark=valued_dark)
    body += middle_section
    if dd_as_steps:
        dd_html = checklist_section(dd_title, dd_sub, dd_items, raised=False, dark=dd_dark)
    else:
        dd_html = info_cards(dd_title, dd_sub, dd_items, cols=3, raised=False, dark=dd_dark)
    faq_html = faq_section(f"{label} Questions, Answered", faq, dark=faq_dark) if faq else ''
    body += (faq_html + dd_html) if faq_before_dd else (dd_html + faq_html)
    rel = related_slugs or [c['slug'] for c in COMMERCIAL_CATEGORIES if c['slug'] != slug][:2]
    body += commercial_cta_form(label, rel, gradient=h1_gradient)
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
    # "Mostly black" theme, rolled out to all commercial category pages (approved on banquet-halls first).
    _theme_b = True
    commercial_sub(
        f"/commercial/{p['slug']}/", p['label'], p['icon'], p['tag'], p['label'], p['lead'],
        p['m_heading'], p['m_paras'], p['m_photo'],
        f"How {p['label'].replace('&amp;','&')} Are Valued", "Key drivers of value in this category",
        p['valued'],
        f"{p['label'].replace('&amp;','&')} Due Diligence", "What to verify before you commit",
        p['dd_items'],
        faq=p['faq'],
        related_slugs=p['related'],
        valued_raised=not _theme_b,
        valued_dark=_theme_b,
        dd_dark=False,
        faq_dark=False,
        market_dark=_theme_b,
        faq_before_dd=False,
        dd_as_steps=_theme_b,
        market_tight=_theme_b,
        h1_gradient=_theme_b
    )

# ============================================================
# /communities/  — index + individual area pages
# ============================================================
comm_idx_body = subhero(
    "",
    'Communities Across <span class="gradient-text">Surrey &amp; the Lower Mainland</span>',
    "Get to know the neighbourhoods Manan works in \u2014 residential and commercial alike.",
    TEXT_CTA + CONTACT_CTA
)
comm_idx_body += community_grid_section(
    "Browse by Community", "Explore each area's character before you start your search.", COMMUNITY_CARDS,
    raised=False, dark=True
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
    others = related_area_cards(a['slug'])
    tags_html = ''.join(f'<span>{t}</span>' for t in a.get('tags', []))
    _area_group = SLUG_TO_GROUP.get(a['slug'])
    _area_coord = GROUP_COORD_MAP.get(_area_group, GROUP_COORD_MAP['Surrey'])
    _area_options_html = ''.join(
        f'<option value="{coord}"{" selected" if group == _area_group else ""}>{group}</option>'
        for group, coord in GROUP_COORDS
    )
    _area_search_html = f"""<div class="hero-search">
        <select id="areaHeroSearch">
{_area_options_html}
        </select>
        <button type="button" data-realtor-search="areaHeroSearch">\U0001F50D Search</button>
      </div>"""
    _stats = a.get('stats')
    _stat_bar_html = ''
    if _stats:
        _stat_items = f'<div class="stat-item"><div class="stat-value">{_stats["population"]}</div><div class="stat-label">Population</div></div>'
        _stat_items += f'<div class="stat-item"><div class="stat-value">{_stats["benchmark"]}</div><div class="stat-label">{_stats["benchmark_label"]}</div></div>'
        _stat_bar_html = f'<div class="hero-stat-bar">{_stat_items}</div>'
    body = subhero(
        "",
        f'<span class="gradient-text">{a["name"]}</span>',
        a['note'] + ".",
        _area_search_html + _stat_bar_html
    )
    # picsum seeds are opaque hashes, not content-aware -- "surrey" happened to hash to an
    # unrelated astronaut/spacewalk stock photo, so it needs a pinned override (see also index.html's
    # homepage area card, which had the same seed).
    _picsum_seed_overrides = {"surrey": "surrey-lowermainland"}
    _photo_seed = _picsum_seed_overrides.get(a['slug'], a['slug'])
    area_photo_src = REAL_PHOTOS.get(f"area-{a['slug']}", (f"https://picsum.photos/seed/{_photo_seed}/800/600", 800, 600))
    # Amenities strip -- icon-based at-a-glance summary
    _amenity_items = []
    if a.get('schools'):   _amenity_items.append(('\U0001F3EB', 'Schools'))
    if a.get('shopping'):  _amenity_items.append(('\U0001F6D2', 'Shopping'))
    if a.get('entertainment'): _amenity_items.append(('\U0001F37D\ufe0f', 'Dining'))
    if a.get('recreation'): _amenity_items.append(('\U0001F3DE\ufe0f', 'Parks &amp; Recreation'))
    for tag in a.get('tags', []):
        tl = tag.lower()
        if 'skytrain' in tl or 'seabus' in tl or 'transit' in tl or 'canada line' in tl or 'west coast express' in tl:
            _amenity_items.append(('\U0001F689', tag))
            break
    _amenities_html = ''.join(f'<div class="amenity-item"><span class="a-icon">{ic}</span>{lb}</div>' for ic, lb in _amenity_items) if _amenity_items else ''

    _map_q = f"{a['name']}, BC, Canada".replace(' ', '+').replace('&amp;', '%26')
    if GOOGLE_MAPS_KEY:
        _area_visual_html = f'<iframe class="imgblock area-map" style="aspect-ratio:16/11;" src="https://www.google.com/maps/embed/v1/place?key={GOOGLE_MAPS_KEY}&q={_map_q}&zoom=12" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map of {a["name"]}, BC"></iframe>'
    else:
        _area_visual_html = f'<img class="imgblock" style="aspect-ratio:16/11;" src="{area_photo_src[0]}"{responsive_img_attrs(area_photo_src[0], area_photo_src[1])} alt="{a["name"]} neighbourhood" loading="lazy" width="{area_photo_src[1]}" height="{area_photo_src[2]}">'
    body += f"""<section class="content-section dark" style="padding:48px 0 56px;">
  <div class="wrap two-col">
    <div>
      <h2>About {a['name']}</h2>
      <p style="margin-top:14px;">{a['desc']}</p>
      <div class="tags" style="margin-top:18px;display:flex;gap:8px;flex-wrap:wrap;">{tags_html}</div>
      {f'<div class="amenities-strip">{_amenities_html}</div>' if _amenities_html else ''}
    </div>
    {_area_visual_html}
  </div>
</section>"""
    if a.get('schools') or a.get('shopping') or a.get('recreation'):
        body += local_info_section(a['name'], a.get('schools'), a.get('shopping'), a.get('recreation'), a.get('entertainment'))
    if a.get('area_faq'):
        body += faq_section(f"{a['name']} Real Estate FAQs", a['area_faq'])
    _is_out_of_town = SLUG_TO_GROUP.get(a['slug']) in OUT_OF_TOWN_GROUPS
    _buy_sell_lead = (
        f"Whether you're searching for a home, an acreage, or a commercial or investment opportunity in {a['name']}, local context matters \u2014 what a property is actually worth here, how quickly comparable listings have been moving, and what the market supports beyond a typical family home search. Manan works across residential, commercial, and investment opportunities in {a['name']} and can walk you through what's realistic for your specific goals."
        if _is_out_of_town else
        f"Whether you're searching for a home in {a['name']} or thinking about listing one, local context matters \u2014 what a property is actually worth here, how quickly comparable homes have been moving, and which streets or buildings tend to hold their value. Manan works across both the residential and commercial sides of {a['name']}'s market and can walk you through what's realistic for your specific goals."
    )
    _investor_point = (
        f'<div class="point"><div class="dot">\U0001F4BC</div><div><strong>Investors</strong><span>Acreage, ranch, tourism, and commercial opportunities that {a["name"]}\'s market supports beyond a typical family home search.</span></div></div>'
        if _is_out_of_town else ''
    )
    _street_seed = f"{a['slug']}-street"
    if _street_seed in REAL_PHOTOS:
        _street_src, _street_w, _street_h = REAL_PHOTOS[_street_seed]
        _street_alt = f"{a['name']} street view"
    else:
        _street_src, _street_w, _street_h = f"https://picsum.photos/seed/{_street_seed}/800/600", 800, 600
        _street_alt = f"{a['name']} street view (sample photo)"
    body += f"""<section class="content-section dark">
  <div class="wrap two-col">
    <img class="imgblock" src="{_street_src}" alt="{_street_alt}" loading="lazy" width="{_street_w}" height="{_street_h}">
    <div>
      <h2>Buying or Selling in {a['name']}</h2>
      <p style="margin-top:14px;">{_buy_sell_lead}</p>
      <div class="point-list">
        <div class="point"><div class="dot">\U0001F3E1</div><div><strong>Buyers</strong><span>A tailored search and honest guidance on what {a['name']} actually offers for your budget and lifestyle.</span></div></div>
        <div class="point"><div class="dot">\U0001F511</div><div><strong>Sellers</strong><span>A free evaluation grounded in current comparable activity in {a['name']}, not a generic estimate.</span></div></div>
        {_investor_point}
      </div>
      <div style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap;">
        <a class="btn-solid-warm" href="/property-search/">\U0001F50D Search Homes in {a['name']}</a>
        <a class="btn-outline-light" href="/sellers/home-evaluation/">\U0001F4CB Free Home Evaluation</a>
      </div>
      <p style="margin-top:14px;font-size:0.85rem;">Prefer to talk now? Call <a href="tel:+16047279542" style="color:var(--accent-on-dark);font-weight:600;">(604) 727-9542</a></p>
    </div>
  </div>
</section>"""
    # Neighbourhood Guides pills -- for cities whose AREA_GROUPS entry has
    # sub-area slugs beyond the current page itself
    _current_group = SLUG_TO_GROUP.get(a['slug'])
    _group_slugs = AREA_GROUPS.get(_current_group, []) if _current_group else []
    _sub_slugs = [s for s in _group_slugs if s != a['slug']]
    if _sub_slugs:
        _pill_html = ''
        for ss in _sub_slugs:
            _sub = _AREA_CARD_BY_SLUG.get(ss)
            if _sub:
                _pill_html += f'<a class="guide-pill" href="/communities/{ss}/"><span>{_sub["name"]}</span><span class="arrow">→</span></a>'
        if _pill_html:
            body += f"""<section class="guides-section dark">
  <div class="wrap">
    <div class="content-head center"><h2>Neighbourhood Guides</h2><p>In-depth pages for specific {a['name'] if a['slug'] == _group_slugs[0] else _current_group} communities.</p></div>
    <div class="guide-pills">{_pill_html}</div>
  </div>
</section>"""
    body += cta_band(
        f'Thinking About {a["name"]}?',
        "Manan can share more on pricing, inventory, and what to expect in this market.",
        TEXT_CTA + CONTACT_CTA
    )
    body += community_grid_section("Other Communities", "Explore more of the areas Manan serves.", others, dark=True)
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
# /marketing/
# ============================================================
marketing_body = subhero(
    "",
    'How Your Property Gets <span class="gradient-text">Marketed</span>',
    "Manan holds a BBA in Marketing from SFU's Beedie School of Business — that background shapes a real, structured marketing plan behind every listing, not just an MLS® upload and a lawn sign.",
    TEXT_CTA + EVAL_CTA
)
marketing_body += info_cards(
    "The Marketing Plan Behind Every Listing",
    "Five pieces that work together, scaled to fit the property and the market it's competing in.",
    [
        dict(icon="\U0001F4F8", title="Property Visuals", desc="Professional photography on every listing, with drone/aerial photography and walkthrough video added for larger or higher-value properties where the lot, layout, or setting benefits from it."),
        dict(icon="\U0001F6CB", title="Staging &amp; Design", desc="A walkthrough before photography to flag what to declutter, depersonalize, or rearrange — and a referral to a professional stager when a vacant or awkwardly-furnished property needs it."),
        dict(icon="\U0001F4F1", title="Social Media Marketing", desc="Every listing is promoted across social channels with property-specific content, not a single generic post — built to put the listing in front of active local buyers, not just past clients."),
        dict(icon="\U0001F30D", title="Global Reach", desc="Beyond local promotion, listings are positioned to reach international buyer interest from India, China, and Europe — markets with an established history of investment in Fraser Valley and Lower Mainland real estate."),
        dict(icon="\U0001F4CA", title="Strategic Pricing", desc="Pricing built from actual comparable sales and current absorption rates in the immediate area, not a round number — priced to attract genuine offers instead of sitting and going stale."),
    ],
    cols=3, dark=True
)
marketing_body += point_list_section(
    True, "Global Reach", "Marketing Beyond the Local Market",
    "Surrey and the Lower Mainland have long drawn real estate interest from international buyers, particularly from India, China, and across Europe. Manan's marketing approach accounts for that reality from the start — positioning a listing for the buyers actually active in this market, wherever they're searching from, rather than assuming every buyer is local.",
    [
        dict(icon="\U0001F91D", title="International Buyer Network", desc="Manan works with buyers and investors from a wide range of backgrounds across India, China, Europe, and beyond — his own network and connections are a genuine asset when a listing is a strong fit for international interest."),
        dict(icon="\U0001F30F", title="Broader International Exposure", desc="Listings are syndicated to the international real estate portals and channels that reach active Chinese and European buyer audiences, alongside standard MLS® and Realtor-network distribution."),
        dict(icon="\U0001F91D", title="Matched to the Right Listings", desc="Not every property benefits equally from international marketing — Manan will tell you plainly whether a listing is a strong fit for that exposure or whether local marketing is the better use of the budget."),
    ],
    img_first=False, img_seed='marketing-global-reach', img_alt="International real estate marketing"
)
marketing_body += faq_section("Marketing Questions, Answered", [
    ("Does professional photography actually make a difference?", "Yes — buyers browse listing photos before they decide whether to even click in for details, let alone book a showing. Professional photography, and drone or video for properties where it adds real value, is standard on every listing Manan takes on, not an upsell."),
    ("Do I need to stage my home to sell it?", "Not always. An occupied, well-kept, and reasonably decluttered home often doesn't need formal staging — a walkthrough with styling suggestions is usually enough. Vacant homes and awkward layouts benefit the most from professional staging, and Manan will say plainly when it's worth the cost versus when it isn't."),
    ("How does international marketing actually reach buyers overseas?", "Through a combination of international listing syndication, Manan's own network of international buyers and investors, and targeted digital promotion. It's a supplement to strong local marketing, not a replacement for it — most buyers for most properties are still local or regional."),
    ("How is my home's asking price actually determined?", "From a comparative market analysis of recently sold and currently active comparable properties in your immediate area — adjusted for condition, lot, and finishes — not a formula or an automated online estimate. Manan will walk through the actual comparables with you before you set a number."),
    ("What social media platforms are listings promoted on?", "Promotion is tailored to the property and the audience most likely to be searching for it, rather than a single fixed platform list for every listing — Manan will walk you through the specific plan for your property before it goes live."),
    ("Does more marketing spend always mean a better sale price?", "No — pricing and condition drive the outcome far more than marketing spend alone. Strong marketing matters because it makes sure the right buyers actually see a well-priced, well-presented property; it can't fix a property that's priced above what the comparables support."),
], dark=True)
marketing_body += cta_band(
    'See the Plan for <span class="accent-warm">Your Property</span>',
    "Every marketing plan is built around the specific property — book a free home evaluation to see what Manan would propose for yours.",
    TEXT_CTA + EVAL_CTA
)
write_page(
    '/marketing/',
    "Marketing Strategy | Manan Bhullar Real Estate",
    "Professional photography, staging, social media, international buyer reach, and strategic pricing — the marketing plan behind every Manan Bhullar listing.",
    crumbs(("Marketing", None)),
    marketing_body
)

# ============================================================
# /why-manan/ (formerly split across /about/ + /why-manan/ -- merged into one
# page; the standalone /about/ page was removed), /contact/, /property-search/, /listings/
# ============================================================
why_body = subhero(
    "",
    'Why Work With <span class="gradient-text">Manan</span>?',
    "A marketing-trained, dual-market REALTOR\u00AE who treats residential and commercial clients with the same level of care.",
    CONTACT_CTA,
    flat_dark=True
)
why_body += f"""<section class="content-section why-dark-section">
  <div class="wrap two-col">
    <img class="bio-photo" style="width:100%;" src="/assets/photos/manan-headshot.jpg"{responsive_img_attrs('/assets/photos/manan-headshot.jpg', 1170)} alt="Manan Bhullar headshot" loading="lazy" width="1170" height="1529">
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
why_body += f"""<section class="content-section dark">
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
    "",
    '<span class="gradient-text">Get In Touch</span>',
    "Whether you're buying, selling, or leasing \u2014 reach out any time.",
    '',
    flat_dark=True
)
contact_interested_options = "<option>I'm interested in...</option><option>Buying a Home</option><option>Selling My Property</option><option>Commercial Real Estate</option><option>Free Home Evaluation</option><option>Investment Properties</option><option>Other</option>"
contact_lead_form = lead_form(
    "Send a Message",
    "New Contact Form Message — mananbhullar.com",
    extra_fields=f'<select name="interested_in">{contact_interested_options}</select>',
    message_placeholder="Your Message (optional)"
)
contact_body += f"""<section class="content-section dark">
  <div class="wrap two-col contact-two-col">
    <div>
      <h2>Contact Details</h2>
      <div class="point-list">
        <div class="point"><div class="dot">\U0001F4DE</div><div><strong>Phone</strong><span><a href="tel:+16047279542">(604) 727-9542</a></span></div></div>
        <div class="point"><div class="dot">\U0001F4CD</div><div><strong>Office</strong><span>201-2010 E 48th Ave, Vancouver, BC V5P 1R8</span></div></div>
        <div class="point"><div class="dot">\u2709\uFE0F</div><div><strong>Email</strong><span><a href="mailto:mb_realestate@outlook.com">mb_realestate@outlook.com</a></span></div></div>
        <div class="point"><div class="dot">\U0001F3E2</div><div><strong>Service Area</strong><span>Lower Mainland, BC</span></div></div>
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
    "",
    'Search Properties Across <span class="gradient-text">Surrey &amp; the Lower Mainland</span>',
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
          <option value="49.3200,-123.0724">North Vancouver</option>
          <option value="49.3280,-123.1598">West Vancouver</option>
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
    "",
    '<span class="gradient-text">Current Listings</span>',
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
BLOG_CATEGORIES = ['All Posts', 'Market Updates', 'Neighbourhood Guides', 'Commercial Real Estate', 'Buying Guide', 'Selling Guide']

ARTICLES = [
    dict(slug='fraser-valley-market-update-august-2026', tag='Market Updates',
         title="Fraser Valley Real Estate Market Update \u2014 August 2026",
         desc="Benchmark prices, interest rates, and how the US-Canada tariff dispute is showing up in the Fraser Valley housing market right now.",
         tags=['Market Update', 'Interest Rates', 'Tariffs'],
         img='blog-market-update-2026', img_real='/assets/photos/blog-market-update.jpg', featured=True),
    dict(slug='first-time-buyer-programs-bc', tag='Buying Guide',
         title="BC First-Time Buyer Programs, Explained",
         desc="A plain-language walkthrough of the PTT exemption, FHSA, and RRSP Home Buyers' Plan.",
         tags=['First-Time Buyers', 'BC Programs'],
         img='blog-first-time-buyers', img_real='/assets/photos/blog-photo-206.jpg'),
    dict(slug='preparing-your-home-to-sell', tag='Selling Guide',
         title="Preparing Your Home to Sell: A Practical Checklist",
         desc="The prep work that actually helps a listing perform, without an unnecessary renovation budget.",
         tags=['Selling', 'Home Prep'],
         img='blog-selling-checklist', img_real='/assets/photos/blog-photo-764.jpg'),
    dict(slug='top-5-surrey-neighbourhoods-families-2026', tag='Neighbourhood Guides',
         title="Top 5 Neighbourhoods in Surrey for Families in 2026",
         desc="Where families are actually buying in Surrey right now, and what makes each of these five neighbourhoods work for raising kids.",
         tags=['Surrey', 'Family Homes'],
         img='blog-surrey-family-neighbourhoods', img_real='/assets/photos/blog-surrey-neighbourhoods.jpg'),
    dict(slug='commercial-real-estate-trends-fraser-valley-2026', tag='Commercial Real Estate',
         title="Commercial Real Estate Trends in the Fraser Valley for 2026",
         desc="How tariffs, interest rates, and industrial demand are shaping commercial and industrial real estate across the Fraser Valley.",
         tags=['Commercial', 'Tariffs', 'Industrial'],
         img='blog-commercial-trends-2026', img_real='/assets/photos/blog-photo-948.jpg'),
    dict(slug='first-time-home-buyer-guide-fraser-valley-2026', tag='Buying Guide',
         title="First-Time Home Buyer Guide: Navigating the Fraser Valley Market in 2026",
         desc="A start-to-finish guide for first-time buyers navigating today's buyer-favouring Fraser Valley market.",
         tags=['First-Time Buyers', 'Fraser Valley'],
         img='blog-first-time-buyer-guide', img_real='/assets/photos/blog-photo-424.jpg'),
    dict(slug='affordable-homes-surrey-bc-2026', tag='Buying Guide',
         title="Affordable Homes in Surrey BC: Where to Find the Best Value in 2026",
         desc="Where relative affordability actually exists in Surrey's housing market right now, property type by property type.",
         tags=['Surrey', 'Affordability'],
         img='blog-affordable-surrey', img_real='/assets/photos/blog-photo-76.jpg'),
    dict(slug='south-surrey-vs-white-rock', tag='Neighbourhood Guides',
         title="South Surrey vs White Rock: Which Neighbourhood Is Right for You?",
         desc="Two of the region's most desirable areas, compared honestly \u2014 pricing, lifestyle, and who each one actually suits.",
         tags=['South Surrey', 'White Rock'],
         img='blog-south-surrey-white-rock', img_real='/assets/photos/blog-photo-47.jpg'),
    dict(slug='townhouses-surrey-under-600k-2026', tag='Buying Guide',
         title="Townhouses for Sale in Surrey Under $600,000: Your 2026 Guide",
         desc="Where a sub-$600K townhome budget still goes in Surrey right now, and the trade-offs to expect at that price point.",
         tags=['Townhomes', 'Surrey', 'Budget Buying'],
         img='blog-surrey-townhomes-budget', img_real='/assets/photos/blog-photo-308.jpg'),
    dict(slug='surrey-bc-house-prices-2026', tag='Market Updates',
         title="Surrey BC House Prices: What to Expect in 2026",
         desc="Current benchmark prices across Surrey's property types, and the market forces likely to move them through the rest of the year.",
         tags=['Surrey', 'Market Update'],
         img='blog-surrey-house-prices', img_real='/assets/photos/blog-photo-448.jpg'),
    dict(slug='fleetwood-vs-cloverdale', tag='Neighbourhood Guides',
         title="Fleetwood vs Cloverdale: Comparing Surrey's Best Family Neighbourhoods",
         desc="Two established Surrey neighbourhoods, compared on schools, character, commute, and price.",
         tags=['Fleetwood', 'Cloverdale'],
         img='blog-fleetwood-cloverdale', img_real='/assets/photos/blog-photo-164.jpg'),
    dict(slug='newton-surrey-real-estate-guide', tag='Neighbourhood Guides',
         title="Newton Surrey Real Estate: Your Guide to Affordable Family Living",
         desc="What makes Newton one of Surrey's most accessible entry points for buyers, and what to know before you search there.",
         tags=['Newton', 'Affordability'],
         img='blog-newton-surrey', img_real='/assets/photos/blog-photo-448.jpg'),
    dict(slug='panorama-ridge-surrey-hidden-gem', tag='Neighbourhood Guides',
         title="Panorama Ridge Surrey: A Hidden Gem for Homebuyers",
         desc="An established, quieter Surrey neighbourhood that doesn't get the attention its elevated lots and central access deserve.",
         tags=['Panorama Ridge'],
         img='blog-panorama-ridge', img_real='/assets/photos/blog-photo-973.jpg'),
    dict(slug='surrey-condo-market-2026', tag='Buying Guide',
         title="Surrey Condo Market 2026: Best Areas for First-Time Buyers",
         desc="Where the condo inventory, incentives, and value currently sit across Surrey for a first-time buyer.",
         tags=['Condos', 'Surrey', 'First-Time Buyers'],
         img='blog-surrey-condo-market', img_real='/assets/photos/blog-photo-887.jpg'),
    dict(slug='how-to-get-first-access-new-listings-surrey', tag='Buying Guide',
         title="How to Get First Access to New Listings in Surrey BC",
         desc="What actually gets a buyer in front of a new listing before it's gone, beyond refreshing a public search site.",
         tags=['Buying Strategy', 'Surrey'],
         img='blog-first-access-listings', img_real='/assets/photos/blog-photo-6.jpg'),
    dict(slug='commercial-real-estate-surrey-investment-2026', tag='Commercial Real Estate',
         title="Commercial Real Estate in Surrey: Investment Opportunities for 2026",
         desc="Where Surrey's commercial and industrial investment opportunities currently sit, from industrial corridors to retail corners.",
         tags=['Commercial', 'Investment', 'Surrey'],
         img='blog-surrey-commercial-investment', img_real='/assets/photos/blog-photo-743.jpg'),
    dict(slug='how-to-buy-a-gas-station-bc-2026', tag='Commercial Real Estate',
         title="How to Buy a Gas Station in BC: A Practical Guide for 2026",
         desc="What actually goes into underwriting and closing on a BC gas station, from fuel supply agreements to environmental due diligence.",
         tags=['Gas Stations', 'Commercial'],
         img='blog-buy-gas-station', img_real='/assets/photos/blog-gas-station.jpg'),
    dict(slug='buying-a-motel-bc-due-diligence', tag='Commercial Real Estate',
         title="Buying a Motel in BC: Due Diligence Checklist",
         desc="The specific due-diligence items that matter most when underwriting a BC motel or small hotel purchase.",
         tags=['Hotels & Motels', 'Due Diligence'],
         img='blog-buying-motel-bc', img_real='/assets/photos/blog-photo-743.jpg'),
    dict(slug='convenience-store-acquisition-bc-guide', tag='Commercial Real Estate',
         title="Convenience Store Acquisition in BC: A Buyer's Guide",
         desc="What a buyer needs to underwrite before acquiring a BC convenience store, from lottery/tobacco licensing to lease terms.",
         tags=['Convenience Stores', 'Commercial'],
         img='blog-convenience-store-bc', img_real='/assets/photos/blog-photo-948.jpg'),
    dict(slug='buying-a-restaurant-bc-liquor-licence', tag='Commercial Real Estate',
         title="Buying a Restaurant in BC: From Underwriting to Liquor Licence Transfer",
         desc="How to underwrite a BC restaurant purchase and what the liquor licence transfer process actually involves.",
         tags=['Restaurants', 'Liquor Licence'],
         img='blog-buying-restaurant-bc', img_real='/assets/photos/blog-photo-437.jpg'),
]

def _photo_url(art, w, h):
    if art.get('img_real'):
        return art['img_real']
    if art.get('img_id'):
        return f"https://picsum.photos/id/{art['img_id']}/{w}/{h}"
    return f"https://picsum.photos/seed/{art['img']}/{w}/{h}"

def _photo_alt(art):
    return art['title'] if art.get('img_real') else f"{art['title']} (sample photo)"

def _blog_card_html(art):
    tags_attr = ' '.join(art.get('tags', []))
    search_attr = f"{art['title']} {art['desc']} {tags_attr}".replace('"', '&quot;')
    thumb_src = _photo_url(art, 500, 310)
    return f"""<a class="blog-card" href="/updates/{art['slug']}/" data-blog-card data-category="{art['tag']}" data-search="{search_attr}">
      <img class="thumb" src="{thumb_src}"{responsive_img_attrs(thumb_src, 500, sizes="400px")} alt="{_photo_alt(art)}" loading="lazy" width="500" height="310" style="width:100%;object-fit:cover;">
      <div class="body">
        <span class="tag">{art['tag']}</span>
        <strong>{art['title']}</strong>
        <span>{art['desc']}</span>
        <span class="go">Read More \u2192</span>
      </div>
    </a>"""

_featured_art = next((a for a in ARTICLES if a.get('featured')), ARTICLES[0])
_rest_arts = [a for a in ARTICLES if a is not _featured_art]

_featured_search_attr = f"{_featured_art['title']} {_featured_art['desc']} {' '.join(_featured_art.get('tags', []))}".replace('"', '&quot;')
_featured_thumb_src = _photo_url(_featured_art, 700, 500)
featured_html = f"""<a class="featured-post" href="/updates/{_featured_art['slug']}/" data-blog-card data-category="{_featured_art['tag']}" data-search="{_featured_search_attr}">
  <img class="thumb" src="{_featured_thumb_src}"{responsive_img_attrs(_featured_thumb_src, sizes="(max-width:860px) 100vw, 700px")} alt="{_photo_alt(_featured_art)}" loading="lazy" width="700" height="500">
  <div class="body">
    <div class="pin-label">Featured</div>
    <span class="tag">{_featured_art['tag']}</span>
    <strong>{_featured_art['title']}</strong>
    <span class="desc">{_featured_art['desc']}</span>
    <span class="go">Read More \u2192</span>
  </div>
</a>"""

blog_cards = ''.join(_blog_card_html(a) for a in _rest_arts)
_pills_html = ''.join(
    f'<button class="filter-pill{" active" if c == "All Posts" else ""}" data-pill="{c}">{c}</button>'
    for c in BLOG_CATEGORIES
)

blog_idx_body = f"""<header class="subhero">
  <div class="wrap">
    <h1>Real Estate Insight for <span class="gradient-text">Surrey &amp; the Lower Mainland</span></h1>
    <p class="lead">In-depth guides and current market analysis from your trusted Fraser Valley expert.</p>
    {google_follow_card()}
  </div>
</header>"""
blog_idx_body += f"""<section class="content-section dark">
  <div class="wrap">
    <div class="blog-toolbar">
      <input type="text" id="blogSearch" class="blog-search-input" placeholder="Search articles\u2026">
      <div class="filter-pills">{_pills_html}</div>
    </div>
    {featured_html}
    <div class="blog-grid">{blog_cards}</div>
    <div id="blogEmptyState">No articles match your search. Try a different keyword or category.</div>
  </div>
</section>"""
write_page(
    '/updates/',
    "Updates | Manan Bhullar Real Estate",
    "Real estate guides and market analysis for buyers, sellers, and investors in Surrey and the Lower Mainland, from Manan Bhullar.",
    crumbs(("Updates", None)),
    blog_idx_body
)

def article_page(art, body_html):
    sidebar_form = lead_form(
        "Have Questions? Ask Manan",
        f"New Article Question \u2014 {art['title']} \u2014 mananbhullar.com",
        message_placeholder="Your Question"
    )
    tags_html = ''.join(f'<span class="article-tag">{t}</span>' for t in art.get('tags', []))
    _hero_src = _photo_url(art, 1200, 480)
    full = f"""<header class="subhero" style="padding:48px 0;">
  <div class="wrap" style="text-align:center;">
    <h1 style="max-width:32ch;margin:0 auto;"><span class="gradient-text">{art['title']}</span></h1>
    <div class="article-tags">{tags_html}</div>
  </div>
</header>
<img class="article-hero-img" src="{_hero_src}"{responsive_img_attrs(_hero_src, sizes="(min-width:1180px) 1116px, 100vw")} alt="{_photo_alt(art)}" loading="lazy" width="1200" height="480">
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

_art_by_slug = {a['slug']: a for a in ARTICLES}

article_page(_art_by_slug['first-time-buyer-programs-bc'], """
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

article_page(_art_by_slug['preparing-your-home-to-sell'], """
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

article_page(_art_by_slug['fraser-valley-market-update-august-2026'], """
<p>Two things are shaping the Fraser Valley market right now: interest rates that have come down meaningfully from their peak, and a US-Canada tariff dispute that escalated sharply in the past week. Here's where things actually stand, as of late August 2026.</p>
<h2>Where Prices Stand Right Now</h2>
<p>The Fraser Valley Real Estate Board's composite benchmark price sits at $877,600, with single-family detached homes at $1,350,200, townhomes at $764,100, and apartments/condos at $469,500. Sales-to-active-listings ratios in the region are running well below the 12&ndash;20% range that typically defines a balanced market, which puts the Fraser Valley firmly in buyer's-market territory &mdash; inventory is elevated and prices have softened on a year-over-year basis across every property type. FVREB's own July release headline put it plainly: improving affordability is currently outpacing buyer demand.</p>
<h2>Interest Rates Have Room, But Buyers Are Still Cautious</h2>
<p>The Bank of Canada has held its overnight rate at 2.25% for six consecutive decisions, with the prime lending rate at most banks sitting around 4.45%. Advertised five-year fixed rates start near 4.04% and five-year variable rates near 3.35% through brokerages, though most major banks post somewhat higher headline rates. Lower borrowing costs than a couple of years ago haven't been enough on their own to pull buyers off the sidelines &mdash; affordability has improved, but confidence is the bigger constraint right now.</p>
<h2>How the US-Canada Tariff Dispute Is Showing Up Here</h2>
<p>This is the story to watch. Trade talks between the US and Canada broke down on August 21&ndash;22, 2026, and the US responded with 50% tariffs on roughly $20 billion of Canadian goods, including building materials. Canada is preparing retaliatory tariffs of 15&ndash;50% on a comparable value of US goods effective September 8, doubling its own steel and aluminum counter-tariffs to match. Separately, softwood lumber duties into the US were recently cut from a combined 35.16% to 24.83% &mdash; but a 10% Section 232 tariff layered on top still pushes the effective rate on Canadian lumber producers above 45%.</p>
<p>For homebuilders and renovators, the practical effect is upward pressure on framing lumber, steel, and imported fixtures &mdash; several industry sources are reporting material cost increases on new construction, though exact figures vary and should be confirmed with your builder or contractor rather than taken as a fixed number. The Bank of Canada's own July Monetary Policy Report noted the Canadian economy "continues to adjust to US tariffs" with trade uncertainty remaining a key headwind &mdash; and that was written before this month's escalation.</p>
<h2>What This Means If You're Buying</h2>
<p>This is a genuine buyer's market: more selection, more negotiating room on price and conditions, and less pressure to waive subjects to compete. If tariff-driven construction costs are pushing up the price of new builds, resale inventory may look relatively more attractive by comparison &mdash; worth factoring into a build-versus-buy decision.</p>
<h2>What This Means If You're Selling</h2>
<p>Pricing realistically against actual recent comparables &mdash; not last year's numbers &mdash; matters more than ever in a market where buyers have options. Strong marketing and presentation help a listing stand out, but they can't substitute for a price that reflects where the market actually is today.</p>
<p>Every situation is different depending on property type, area, and timeline. Manan can walk through what these numbers mean specifically for your street, not just the regional averages.</p>
""")

article_page(_art_by_slug['top-5-surrey-neighbourhoods-families-2026'], """
<p>Surrey is BC's second-largest city, and its neighbourhoods vary enormously in character, price, and what they offer a family day-to-day. Here are five that consistently come up for buyers prioritizing schools, space, and community.</p>
<h2>1. Fleetwood</h2>
<p>One of Surrey's long-established residential neighbourhoods, Fleetwood offers tree-lined streets, a mix of single-family homes and newer townhome developments, and easy access to Fraser Highway and Highway 1. Families are drawn to Surrey Christian School (private, K-12) and the Surrey Sport &amp; Leisure Complex, with Fleetwood Park Village and Guildford Town Centre both a short drive away.</p>
<h2>2. Cloverdale</h2>
<p>Cloverdale blends small-town heritage character &mdash; it's home to the Cloverdale Rodeo and Country Fair &mdash; with rapid new-home development. Lord Tweedsmuir and Salish Secondary anchor the school catchments, and the historic downtown core is home to over 200 independent businesses, giving Cloverdale a genuine town-centre feel that's rare in Surrey.</p>
<h2>3. South Surrey / White Rock</h2>
<p>South Surrey, including Grandview Heights, offers oceanfront living along Semiahmoo Bay and is generally regarded as Surrey's premium residential tier. Families here have access to Earl Marriott, Semiahmoo, Elgin Park, and the newer Grandview Heights Secondary (opened 2021), plus private options like SouthRidge. It's a higher price point, but the school and lifestyle draw is real.</p>
<h2>4. Panorama Ridge</h2>
<p>An established, family-oriented neighbourhood known for elevated lots with valley views and a quieter, residential feel. It sits close to Bear Creek Park and Newton's recreation facilities without the density of Surrey's busiest corridors.</p>
<h2>5. Sullivan Heights</h2>
<p>Bordering Cloverdale, Sullivan Heights offers a mix of single-family homes in an established, quiet setting with easy access to Cloverdale's amenities and schools without paying a Cloverdale-core premium.</p>
<p>Every family's priorities are different &mdash; school catchment, commute, lot size, and budget all pull in different directions. Manan can walk through which of these (or Surrey's other neighbourhoods) actually fits yours.</p>
""")

article_page(_art_by_slug['commercial-real-estate-trends-fraser-valley-2026'], """
<p>Commercial real estate in the Fraser Valley is being shaped by the same forces hitting the broader Canadian economy right now &mdash; tariffs, interest rates, and cross-border trade uncertainty &mdash; layered on top of the region's own industrial and retail fundamentals.</p>
<h2>The Tariff Situation Is Live and Fluid</h2>
<p>US-Canada trade talks collapsed on August 21&ndash;22, 2026, triggering 50% US tariffs on roughly $20 billion of Canadian goods and a Canadian retaliatory package of 15&ndash;50% tariffs on a comparable value of US goods, effective September 8. The CUSMA/USMCA agreement is also up for its mandatory review this year, adding another layer of uncertainty to cross-border logistics and manufacturing decisions. For businesses considering industrial space in the Fraser Valley &mdash; particularly anything tied to cross-border trade, warehousing, or manufacturing &mdash; this is a genuinely fluid situation worth watching closely rather than a settled backdrop to plan around.</p>
<h2>A Weaker Canadian Dollar Cuts Both Ways</h2>
<p>The Canadian dollar has been trading in the 1.38&ndash;1.39 USD/CAD range, with some forecasts suggesting further softening. A weaker loonie tends to make Canadian commercial real estate comparatively cheaper for US-based investors and businesses leasing space here, even as it raises the cost of imported building materials and equipment for Canadian owners and tenants. Which effect dominates for a given deal depends heavily on the specific property and business.</p>
<h2>Retail and Restaurant Operators Are Watching Labour Costs</h2>
<p>BC's minimum wage rose from $17.85 to $18.25 per hour on June 1, 2026. For retail, restaurant, and hospitality tenants &mdash; a meaningful share of Fraser Valley commercial leasing activity &mdash; that's a real, ongoing pressure on operating margins that factors into how much rent a space can realistically support.</p>
<h2>What This Means for Investors</h2>
<p>None of this points to one clear direction &mdash; it points to the importance of underwriting each opportunity on its own fundamentals rather than assuming last year's playbook still applies. Industrial space tied to trade and logistics carries more near-term uncertainty than it did a year ago; well-located retail and service-based commercial real estate, less exposed to tariff swings, may look comparatively more stable right now.</p>
<p>Manan works across the full range of commercial categories in the Fraser Valley and can talk through how current conditions apply to the specific type of property you're evaluating.</p>
""")

article_page(_art_by_slug['first-time-home-buyer-guide-fraser-valley-2026'], """
<p>Buying your first home in the Fraser Valley in 2026 means navigating a market that's actually more favourable to buyers than it's been in years &mdash; but the financial programs and steps still take some untangling. Here's a start-to-finish guide.</p>
<h2>Step 1: Understand the Programs You Qualify For</h2>
<p>Eligible first-time buyers can get a full BC Property Transfer Tax exemption on homes up to $835,000 (partial exemption up to $860,000), contribute up to $8,000/year (to a $40,000 lifetime max) into a tax-advantaged First Home Savings Account, and withdraw from an RRSP tax-free through the Home Buyers' Plan, repayable over 15 years. The FHSA and HBP can generally be combined on the same purchase.</p>
<h2>Step 2: Know the Financing Rules</h2>
<p>Buyers putting down less than 20% need CMHC (or similar) mortgage default insurance, and lenders must qualify you at the stress-tested rate &mdash; the greater of your contract rate plus 2%, or 5.25%. First-time buyers and buyers of newly-built homes can access 30-year amortizations on insured mortgages, which lowers the monthly payment compared to the standard 25-year maximum, though you'll pay more interest over the life of the loan.</p>
<h2>Step 3: Get Pre-Approved Before You Search</h2>
<p>A mortgage pre-approval tells you your real budget and locks in a rate for a window of time &mdash; essential before you start seriously viewing properties, and non-negotiable if you want to move quickly on a home you like.</p>
<h2>Step 4: Take Advantage of Today's Buyer's Market</h2>
<p>Fraser Valley benchmark prices are down year-over-year across every property type, and sales-to-active-listings ratios point to a genuine buyer's market. That means more selection, more room to negotiate on price and conditions, and less pressure to waive your inspection or financing subjects just to compete.</p>
<h2>Step 5: Budget for Closing Costs Beyond the Down Payment</h2>
<p>Legal fees, property transfer tax (if not exempt), home inspection, appraisal, and moving costs all add up &mdash; a rough rule of thumb is 1.5&ndash;4% of the purchase price on top of your down payment.</p>
<p>Every first-time buyer's situation is different. Manan offers a free, no-pressure consultation to walk through exactly what you qualify for and what a realistic search looks like on your budget.</p>
""")

article_page(_art_by_slug['affordable-homes-surrey-bc-2026'], """
<p>"Affordable" is relative in the Fraser Valley, but real value still exists in Surrey if you know where to look. Here's an honest breakdown by property type and area.</p>
<h2>Start With the Benchmark Numbers</h2>
<p>As of the Fraser Valley Real Estate Board's most recent report, the composite benchmark across all residential types sits at $877,600, with apartments/condos at $469,500 &mdash; the single most accessible entry point &mdash; and townhomes at $764,100. Detached homes, at a $1,350,200 benchmark, are out of reach for most first-time buyers without a suite or a significant down payment.</p>
<h2>Where Condos Offer the Best Relative Value</h2>
<p>Surrey City Centre, near King George and Gateway SkyTrain stations, has some of the deepest condo inventory in the city, drawing steady demand from SFU Surrey students and young professionals &mdash; and correspondingly more competitive pricing than comparable stock in Vancouver or Burnaby. Newton and Whalley more broadly also offer accessible condo and townhome entry points.</p>
<h2>Where Townhomes and Suited Homes Stretch Further</h2>
<p>Newton is one of Surrey's most diverse and densely populated neighbourhoods, with a mix of older single-family homes, townhomes, and newer condo development at a relatively accessible price point given its central location. A detached home with a legal or conforming secondary suite &mdash; common in Newton and Whalley &mdash; is often the most realistic path to a detached home while offsetting the mortgage with rental income.</p>
<h2>Don't Overlook the Buyer's Market Itself</h2>
<p>Beyond specific neighbourhoods, the current market condition matters: with sales-to-active-listings ratios well below balanced-market territory, sellers across Surrey are generally more open to negotiating on price and conditions than they were a couple of years ago.</p>
<p>"Affordable" always depends on what you're comparing it to and what trade-offs you're willing to make. Manan can walk through real, current comparables for your specific budget rather than general averages.</p>
""")

article_page(_art_by_slug['south-surrey-vs-white-rock'], """
<p>South Surrey and White Rock are often mentioned in the same breath &mdash; and on FVREB's own reporting, they're grouped together &mdash; but they're genuinely different in feel, footprint, and price. Here's how to think about the choice.</p>
<h2>White Rock: Small, Walkable, and Oceanfront</h2>
<p>White Rock is compact &mdash; centred on its iconic pier and beach promenade, with a walkable downtown of cafes and shops. It draws downsizers, retirees, and buyers prioritizing a genuine small-town, seaside lifestyle within commuting distance of the rest of the Lower Mainland. Waterfront and hillside ocean-view properties here command a real premium, with direct ocean-view homes typically running $2.5M&ndash;$6M and the handful of true waterfront lots reaching considerably higher.</p>
<h2>South Surrey: Larger, More Varied, More Family-Oriented</h2>
<p>South Surrey is a much broader area, encompassing Morgan Creek, Grandview Heights, Elgin Chantrell, Ocean Park, and Crescent Beach &mdash; each with its own character. Morgan Creek offers estate homes from $2.5M&ndash;$5M+, often with golf-course frontage. Grandview Heights is one of the most active newer-build luxury markets in the region, with custom homes typically $2.2M&ndash;$4.5M. Elgin Chantrell offers acreage estates starting around $3M. This is a family-oriented, larger-lot alternative to White Rock's compact core, with strong school catchments including Earl Marriott, Semiahmoo, and the newer Grandview Heights Secondary.</p>
<h2>Which One Fits You?</h2>
<p>If a walkable, oceanfront small-town feel is the priority and you don't need a large lot, White Rock is hard to beat. If you want more space, a newer custom build, or a specific sub-area like a golf-course community, South Surrey's broader footprint likely has more of what you're looking for &mdash; often at a comparable or better price per square foot than White Rock's premium core.</p>
<p>Both areas share excellent schools and a premium market position within Surrey. Manan can walk through specific sub-areas and current listings to help you compare directly.</p>
""")

article_page(_art_by_slug['townhouses-surrey-under-600k-2026'], """
<p>Surrey's city-wide townhome benchmark price currently sits at $764,100 &mdash; well above a $600,000 budget. That doesn't mean a sub-$600K townhome search is hopeless, but it does mean being realistic about where and what you'll find.</p>
<h2>Where a $600K Budget Actually Goes</h2>
<p>Older townhome stock in Newton, Whalley/City Centre, and parts of North Surrey is where a sub-$600K budget is most likely to find real options &mdash; typically smaller units, older buildings, or complexes further from SkyTrain access. Newer, larger townhomes in Cloverdale, Fleetwood, or South Surrey are generally priced well above this range.</p>
<h2>What You're Trading Off</h2>
<p>At this budget, expect to weigh: older building age (meaning more attention to the depreciation report and reserve fund), smaller square footage, two bedrooms rather than three, and possibly a longer commute to SkyTrain or major employment centres. None of these are dealbreakers &mdash; they're just the realistic trade-offs at this price point in today's market.</p>
<h2>Don't Skip the Strata Documents</h2>
<p>Older, lower-priced buildings are exactly where strata due diligence matters most. Request at least two years of council meeting minutes, the current depreciation report, and the reserve fund balance before removing subjects &mdash; a building with deferred maintenance or an underfunded reserve can mean an inherited special levy down the road.</p>
<h2>The Current Market Helps</h2>
<p>With Surrey's overall market favouring buyers right now, sellers of older townhome stock are often more open to negotiating on price than list price alone suggests &mdash; worth factoring into how you approach an offer.</p>
<p>A $600K townhome budget is tight but not unrealistic in the right pockets. Manan can point you toward current listings that actually fit, rather than searches that waste your time.</p>
""")

article_page(_art_by_slug['surrey-bc-house-prices-2026'], """
<p>Surrey house prices have softened over the past year, in line with the broader Fraser Valley market. Here's where things stand across property types, and what's likely to move prices from here.</p>
<h2>Current Benchmark Prices</h2>
<p>The Fraser Valley Real Estate Board's composite benchmark &mdash; covering all residential property types across the board's territory, which includes Surrey &mdash; sits at $877,600. Broken down by type: single-family detached at $1,350,200, townhomes at $764,100, and apartments/condos at $469,500. Prices are down on a year-over-year basis across every category.</p>
<h2>It's a Buyer's Market Right Now</h2>
<p>Sales-to-active-listings ratios are running below the 12&ndash;20% range that typically signals a balanced market &mdash; inventory is elevated relative to buyer demand, which is the core reason prices have softened even as interest rates have come down from their peak.</p>
<h2>What Could Move Prices From Here</h2>
<p>A few forces are worth watching: the Bank of Canada's rate decisions (currently held at 2.25% for six straight decisions, with room to cut further if the economy weakens); the resolution &mdash; or further escalation &mdash; of the US-Canada tariff dispute, which affects both construction costs and broader economic confidence; and whether buyer demand responds to the affordability improvement that's already happened, or continues to wait on the sidelines.</p>
<h2>Price Varies Enormously by Sub-Area</h2>
<p>City-wide averages hide real variation &mdash; South Surrey and White Rock command a significant premium over Newton or Whalley, and even within a single neighbourhood, lot size, view, and condition can shift value substantially. Whole-city benchmark numbers are a useful starting point, not a substitute for an actual comparative market analysis on a specific property.</p>
<p>Manan tracks these numbers monthly and can walk through what they mean for your specific street or property type, not just the city-wide average.</p>
""")

article_page(_art_by_slug['fleetwood-vs-cloverdale'], """
<p>Fleetwood and Cloverdale are both established, family-oriented Surrey neighbourhoods that come up together in a lot of buyer searches. Here's how they actually compare.</p>
<h2>Character and Feel</h2>
<p>Fleetwood is known for tree-lined streets and a mix of single-family homes with newer townhome development woven in &mdash; a classic, quieter residential feel. Cloverdale blends small-town heritage charm &mdash; it's home to the Cloverdale Rodeo and Country Fair &mdash; with some of Surrey's fastest new-home development around its historic downtown core, which hosts over 200 independent businesses.</p>
<h2>Schools</h2>
<p>Fleetwood draws on multiple SD36 Surrey elementary and secondary schools plus Surrey Christian School (private, K-12). Cloverdale's secondary catchments are anchored by Lord Tweedsmuir and Salish Secondary, fed by several SD36 elementary schools. Both offer solid public school access &mdash; confirm your specific catchment address with the district, since boundaries can shift block to block.</p>
<h2>Shopping and Amenities</h2>
<p>Fleetwood residents lean on Fleetwood Park Village, Evergreen Mall, and Fresh St Market locally, with Guildford Town Centre a short drive away. Cloverdale offers Willowbrook Shopping Centre, Central City Shopping Centre (SkyTrain-accessible), and its own historic downtown retail core &mdash; giving Cloverdale a more distinct "town centre" feel than Fleetwood's more suburban layout.</p>
<h2>Access and Commute</h2>
<p>Fleetwood has easy access to Fraser Highway and Highway 1, making it a solid commuter location. Cloverdale similarly benefits from Highway 15 and Fraser Highway access, with the added draw of nearby SkyTrain access via Central City.</p>
<h2>Which Fits You?</h2>
<p>If you want a quieter, established residential feel, Fleetwood likely fits better. If you want small-town character with a genuine downtown core and faster-growing new-home inventory, Cloverdale is the stronger match.</p>
<p>Both are strong, real options for families. Manan can walk through current listings and pricing in each to help you compare directly.</p>
""")

article_page(_art_by_slug['newton-surrey-real-estate-guide'], """
<p>Newton is one of Surrey's most diverse, densely populated, and accessible neighbourhoods &mdash; a common starting point for buyers who want central Surrey access without South Surrey or Fleetwood pricing.</p>
<h2>What Makes Newton Different</h2>
<p>Newton offers a genuine mix of older single-family homes, townhomes, and newer condo development, reflecting decades of organic growth rather than a single master-planned identity. Its central location and relative affordability, compared to Surrey's premium neighbourhoods, make it a popular entry point for first-time buyers and growing families alike.</p>
<h2>East Newton vs. West Newton</h2>
<p>Newton splits into distinct East and West sub-areas with different school zones &mdash; East Newton offers family homes close to shopping and recreation with more established streets, while West Newton is a diverse, densely built pocket close to Scott Road and King George Boulevard, known for its South Asian grocers, sweet shops, and jewellers along the Scott Road corridor.</p>
<h2>Shopping and Daily Life</h2>
<p>King's Cross Shopping Centre, Newton Town Centre (anchored by Chalo FreshCo), and Strawberry Hill Shopping Centre cover most day-to-day needs, alongside the Scott Road corridor's concentration of South Asian grocers and restaurants &mdash; a genuine cultural and culinary draw, not just a practical amenity.</p>
<h2>Recreation</h2>
<p>Bear Creek Park and the Newton Recreation Centre give Newton residents solid access to green space and recreation facilities without leaving the neighbourhood.</p>
<h2>Is Newton Right for You?</h2>
<p>If central Surrey access, relative affordability, and a genuinely diverse community matter more to you than a premium address, Newton is worth serious consideration &mdash; particularly for a suited detached home that can help offset your mortgage.</p>
<p>Manan can walk through current East and West Newton listings and school catchments specific to your search.</p>
""")

article_page(_art_by_slug['panorama-ridge-surrey-hidden-gem'], """
<p>Panorama Ridge doesn't get the attention that Fleetwood or Cloverdale do in most Surrey buyer searches &mdash; but for the right buyer, that's part of the appeal.</p>
<h2>What Panorama Ridge Offers</h2>
<p>An established, family-oriented Surrey neighbourhood known for elevated lots with valley views and a quiet, residential feel. It's the kind of area where homes were largely built out a generation ago, giving it a settled, mature character that newer master-planned communities don't have yet.</p>
<h2>Location and Access</h2>
<p>Panorama Ridge sits close to Bear Creek Park and Newton's recreation facilities, with Newton Town Centre nearby for shopping and everyday needs. It's genuinely central within Surrey without carrying the density or traffic of Whalley or Newton's busiest corridors.</p>
<h2>Why It Flies Under the Radar</h2>
<p>Panorama Ridge doesn't have a single defining landmark or town centre the way Cloverdale has its rodeo grounds or White Rock has its pier &mdash; it's simply a solid, quiet residential neighbourhood, which means it doesn't generate the same search volume as more "branded" Surrey areas. For buyers who care more about the home and lot than the neighbourhood's profile, that's an opportunity rather than a drawback.</p>
<h2>Who It Suits</h2>
<p>Buyers who want an established, quiet, family-friendly setting with valley views and don't need to be walking distance to a bustling town centre tend to do well here &mdash; particularly those upgrading from a starter home who want more lot and more quiet without leaving Surrey.</p>
<p>Because it's less searched, Panorama Ridge sometimes offers relative value compared to more heavily marketed neighbourhoods nearby. Manan can walk through current listings to see what's actually available.</p>
""")

article_page(_art_by_slug['surrey-condo-market-2026'], """
<p>Surrey's condo market looks different than it did a couple of years ago &mdash; more inventory, more developer incentives, and genuinely better conditions for a first-time buyer than the peak-market years.</p>
<h2>Current Benchmark Pricing</h2>
<p>The Fraser Valley Real Estate Board's apartment/condo benchmark sits at $469,500 &mdash; the most accessible property type in the region, and down on a year-over-year basis along with every other category.</p>
<h2>The Presale Market Has Softened Meaningfully</h2>
<p>Greater Vancouver has a near-record number of completed, unsold condo units, and developers across the region &mdash; Surrey included, where well over 100 active presale developments are currently marketing &mdash; are responding with real incentives: price reductions, cash-back credits at closing, reduced deposit requirements, and in some cases furniture allowances or rental guarantees. Specific incentive terms vary by project and change frequently, so confirm current offers directly rather than assuming last month's promotion still applies.</p>
<h2>Best Areas for a First-Time Buyer</h2>
<p>Surrey City Centre, anchored by Central City Mall, SFU Surrey, and direct SkyTrain access via the Expo Line, remains the deepest and most liquid condo market in the city &mdash; strong for both resale value and rental demand from students and young professionals. Newton and Whalley more broadly also offer accessible entry points at a relative discount to City Centre's SkyTrain premium.</p>
<h2>What to Watch For With Presale Purchases</h2>
<p>Presale contracts carry real risk if your financing or life circumstances change before completion &mdash; some buyers in the current market have needed to assign their contracts, in some cases at a loss. Resale condos offer more certainty (you know exactly what you're buying, today) even if presale incentives look attractive on paper.</p>
<p>Manan can walk through current resale and presale options in Surrey City Centre and beyond, and help you weigh the real trade-offs between them.</p>
""")

article_page(_art_by_slug['how-to-get-first-access-new-listings-surrey'], """
<p>By the time a new listing shows up on a public search site, other buyers are often already looking at it. Here's what actually gets you ahead of that curve.</p>
<h2>Get Pre-Approved Before You Start Looking</h2>
<p>A current mortgage pre-approval isn't just a formality &mdash; it's what lets you move immediately when a strong listing appears, rather than losing days to financing logistics while another buyer gets there first.</p>
<h2>Work With an Agent Who's Actively Networked</h2>
<p>A meaningful share of listings get discussed among agents &mdash; at office meetings, through direct outreach, or informally &mdash; before or right as they hit the public market. An agent actively working the area you're searching in often hears about a listing earlier than a public portal search will surface it.</p>
<h2>Set Up Real-Time Saved Searches, Not Manual Refreshing</h2>
<p>Automated saved searches that notify you the moment a matching listing hits MLS® are far more reliable than manually checking a site once a day &mdash; the gap between "just listed" and "under offer" can be a matter of days in a competitive segment.</p>
<h2>Be Ready to Move on Subjects</h2>
<p>Even in today's more buyer-favouring market, well-priced listings in sought-after areas can still attract multiple offers. Knowing in advance what inspection, financing, and other conditions you're comfortable shortening &mdash; without cutting corners on genuinely important ones &mdash; puts you in a stronger position when it matters.</p>
<h2>Ask About Coming-Soon and Off-Market Conversations</h2>
<p>Not every property is publicly marketed from day one. Staying in regular contact with an agent means you sometimes hear about a seller's plans before a listing is formally live.</p>
<p>None of this replaces a solid offer on a fairly priced home &mdash; but it does mean you're seeing the listing, and ready to act on it, before most other buyers are. Manan can walk through what this looks like in practice for your specific search.</p>
""")

article_page(_art_by_slug['commercial-real-estate-surrey-investment-2026'], """
<p>Surrey's commercial and industrial market has real depth &mdash; from its industrial corridor to its rapidly densifying City Centre &mdash; and current conditions create some genuine opportunities for investors who underwrite carefully.</p>
<h2>Industrial Corridor</h2>
<p>Surrey's industrial corridor, spanning into Delta and Langley, continues to see steady demand for leasing and distribution space, driven by the region's role in Lower Mainland logistics. The live US-Canada tariff dispute adds real uncertainty here &mdash; particularly for tenants and buyers whose business is tied to cross-border trade &mdash; so underwriting on realistic, conservative assumptions matters more than usual right now.</p>
<h2>Retail and Mixed-Use</h2>
<p>Surrey City Centre's continued densification &mdash; anchored by Central City Mall, SFU Surrey, and direct SkyTrain access &mdash; keeps generating retail and mixed-use opportunity as residential density grows around it. Retail elsewhere in Surrey ranges from storefronts to strip-mall units suited to owner-operators and smaller investors.</p>
<h2>Development Land</h2>
<p>Subdivision and development potential across Surrey depends on current zoning, Official Community Plan designations, minimum lot sizes, and servicing availability &mdash; all requiring direct due diligence with the municipality before you can rely on a site's future potential. Properties within the Agricultural Land Reserve add a further layer of Agricultural Land Commission approval on top of standard municipal review.</p>
<h2>What to Watch Right Now</h2>
<p>Between tariff-driven uncertainty on the industrial side and BC's minimum wage increase to $18.25/hour affecting retail and service tenants' margins, this isn't a market to underwrite on last year's assumptions. Conservative, deal-specific analysis matters more than broad category trends.</p>
<p>Manan works across Surrey's full commercial spectrum &mdash; industrial, retail, and land &mdash; and can talk through where current conditions create real opportunity for your specific investment goals.</p>
""")

article_page(_art_by_slug['how-to-buy-a-gas-station-bc-2026'], """
<p>Buying a gas station in BC means underwriting three distinct things at once: the real estate, the operating business, and environmental risk from decades of underground fuel storage. Here's how to approach it.</p>
<h2>Understand Branded vs. Independent</h2>
<p>Branded stations (Esso, Shell, Petro-Canada, Chevron) come with supply agreements and marketing support but restrict your fuel supplier flexibility. Independents offer more pricing freedom on fuel but rely entirely on their own reputation and location to drive traffic. Neither is inherently better &mdash; it depends on your operating model and risk tolerance.</p>
<h2>Environmental Due Diligence Is Non-Negotiable</h2>
<p>A Phase I Environmental Site Assessment is the baseline requirement on any gas station purchase, checking for soil and groundwater contamination risk from underground storage tanks. If Phase I flags concerns, a Phase II assessment with further soil and groundwater testing follows before closing. Lenders typically won't finance a fuel retail site without a clean Phase I in hand.</p>
<h2>Verify the Full Revenue Picture</h2>
<p>Fuel volume and margin are only part of the picture &mdash; convenience store, car wash, and any liquor add-on revenue all factor into valuation. Cross-check convenience store financials against POS reports and supplier invoices rather than relying on owner-provided summaries alone.</p>
<h2>Review the Supply Agreement and Tank Condition</h2>
<p>For branded sites, understand the exclusivity terms and remaining length on the fuel supply agreement before you commit. Separately, review underground storage tank age, materials, and whether any upgrades are required under current regulations &mdash; this directly affects both environmental risk and your future capital budget.</p>
<h2>Confirm Permits Are Transferable</h2>
<p>Municipal and provincial fuel retail permits need to be current and properly transferable to you as the new owner &mdash; confirm this early rather than assuming it's automatic.</p>
<p>Gas station transactions carry more moving parts than most commercial real estate purchases. Manan can walk through the specific due diligence for a property you're considering.</p>
""")

article_page(_art_by_slug['buying-a-motel-bc-due-diligence'], """
<p>Buying a motel in BC means buying a business as much as a building &mdash; the due diligence checklist reflects that from the start.</p>
<h2>Financial Performance, Not Just the List Price</h2>
<p>Review at least three years of financial statements, occupancy rates by season, average daily rate (ADR), and revenue per available room (RevPAR) to assess true profitability &mdash; a motel's seasonal swings can make a single year's numbers misleading on their own.</p>
<h2>Licensing and Permits</h2>
<p>Confirm exactly which business licences, health authority permits, liquor licences (if applicable), and tourism accommodation compliance requirements transfer with the sale versus need fresh applications under your ownership &mdash; this can materially affect your closing timeline.</p>
<h2>Zoning and Land Use</h2>
<p>Confirm the property is properly zoned for hospitality use, and understand any restrictions on future expansion or rezoning potential if that factors into your investment plan.</p>
<h2>Physical Condition and PIP Requirements</h2>
<p>For branded properties, understand any Property Improvement Plan (PIP) requirements tied to the brand affiliation, along with deferred maintenance and whether the capital reserve is adequate for near-term repairs.</p>
<h2>Staffing and Operational Continuity</h2>
<p>Review staffing levels and management structure, and think through how operations continue through the ownership transition &mdash; a motel with strong repeat business can lose momentum fast if service quality dips during a changeover.</p>
<h2>Financing Looks Different Here</h2>
<p>Hospitality financing evaluates the operating business's income and management track record alongside the real estate itself &mdash; a different conversation than a standard commercial mortgage, so start that conversation with a lender who understands the category early.</p>
<p>Fraser Valley hospitality demand is real &mdash; from Harrison Hot Springs and Cultus Lake tourism to steady Highway 1 corridor motel traffic. Manan can walk through what solid due diligence looks like for a specific property.</p>
""")

article_page(_art_by_slug['convenience-store-acquisition-bc-guide'], """
<p>Most convenience stores in BC are leasehold businesses rather than real estate purchases, which shifts where the real due diligence work needs to happen.</p>
<h2>The Lease Is Often the Most Important Document</h2>
<p>Since most c-stores are leasehold businesses, review the remaining lease term, renewal options, and rent escalation clauses closely &mdash; a short remaining term or an unfavourable escalation clause can undermine an otherwise solid business.</p>
<h2>Understand the Licensing Requirements</h2>
<p>A tobacco retail licence, a lottery terminal agreement with BCLC if applicable, and a standard municipal business licence are all typically required &mdash; confirm what transfers automatically and what needs a fresh application.</p>
<h2>Verify Sales the Right Way</h2>
<p>Tobacco and lottery revenue carry structurally different, more predictable margins than general merchandise &mdash; and they're also easier to verify. Cross-check reported sales against supplier invoices and BCLC lottery commission statements, which are much harder for a seller to misstate than general retail figures.</p>
<h2>Confirm Lease Assignment Is Actually Possible</h2>
<p>Most commercial leases require landlord consent to assign the lease to a new tenant. Confirm this early in your process &mdash; a landlord can decline or attach conditions, and finding out late can derail an otherwise-agreed deal.</p>
<h2>Check the Competitive Landscape</h2>
<p>Nearby convenience and grocery competition, and any upcoming developments in the immediate area, can materially affect future sales &mdash; worth a genuine look at the surrounding block, not just the store's own numbers.</p>
<h2>Timeline Expectations</h2>
<p>Once financials are verified and lease assignment is confirmed, convenience store transactions typically move faster than real estate deals &mdash; often four to eight weeks to close.</p>
<p>Manan works regularly with c-store buyers across the Fraser Valley and can walk through what to prioritize for a specific listing.</p>
""")

article_page(_art_by_slug['buying-a-restaurant-bc-liquor-licence'], """
<p>Restaurant transactions weigh goodwill and location more heavily than most commercial categories &mdash; and if liquor is involved, the licence transfer process adds its own timeline to plan around.</p>
<h2>Underwriting: Adjusted EBITDA, Not Owner Estimates</h2>
<p>Restaurant valuation is generally based on a multiple of adjusted EBITDA (seller's discretionary earnings) from verified financials &mdash; not owner-provided summaries. Watch for cash-heavy sales that are hard to verify, declining year-over-year trends, and rent that represents a disproportionately high share of revenue.</p>
<h2>Goodwill and Location Carry Real Weight</h2>
<p>A strong location with an established customer base can represent a meaningful share of a restaurant's total value beyond the equipment and lease alone &mdash; which is also why a change of concept after purchase carries real risk if you're counting on that existing customer base.</p>
<h2>Kitchen and Lease Condition</h2>
<p>Confirm the remaining lease term, whether existing kitchen and hood infrastructure suits your concept without major buildout, and whether the landlord's use clause allows a change of concept if you're planning one.</p>
<h2>The Liquor Licence Transfer Process</h2>
<p>A liquor licence does not transfer automatically with a restaurant sale &mdash; it goes through a formal approval process with BC's Liquor and Cannabis Regulation Branch. The application fee is $330, the buyer doesn't need to be a Canadian citizen or resident but does need a CRA Business Number and Business BCeID, and the establishment can generally stay open during the transfer process. BC modernized its rules in 2026 to also permit licensee-to-licensee alcohol sales, worth asking about if that's relevant to your deal structure.</p>
<h2>Franchise vs. Independent</h2>
<p>Franchise purchases require franchisor approval of the buyer and come with ongoing royalty and marketing fees and brand-standard requirements, in exchange for established brand recognition and operational support. Independent restaurants offer full operational freedom but rely entirely on their own reputation.</p>
<h2>Labour Costs Are a Real, Current Factor</h2>
<p>BC's minimum wage rose to $18.25/hour on June 1, 2026 &mdash; a genuine, ongoing pressure on restaurant margins worth building into your underwriting rather than assuming last year's numbers still hold.</p>
<p>Manan works across the Fraser Valley's restaurant and food-service market and can walk through underwriting and licence-transfer timelines for a specific opportunity.</p>
""")

# ============================================================
# Legal / footer pages
# ============================================================
def legal_page(path, title, heading, body_text):
    body = subhero("", f'<span class="gradient-text">{heading}</span>', "", '', flat_dark=True)
    body += f"""<section class="content-section dark">
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
