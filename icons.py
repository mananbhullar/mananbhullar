# ============================================================
# ICON SYSTEM -- replaces every emoji glyph with an inline line-style SVG
# (24x24 viewBox, 1.75px stroke, round caps/joins, currentColor) so icons pick
# up the site's own accent blue instead of relying on the OS emoji font.
# Used by build.py (via apply_icons() in write_page(), covering every
# generated page plus the shared nav/footer) and by index.html, which is
# hand-maintained and gets its own one-off conversion pass.
# ============================================================
ICON_PATHS = {
    'house': '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-9"/><path d="M9.5 20v-6h5v6"/>',
    'key': '<circle cx="7.5" cy="14.5" r="4"/><path d="M10.5 11.5 19.5 2.5"/><path d="M16.5 5.5l2.5 2.5"/><path d="M14 8l2 2"/>',
    'building': '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 7.5h1.2M13.8 7.5H15M9 11.5h1.2M13.8 11.5H15M9 15.5h1.2M13.8 15.5H15"/><path d="M10.2 21v-3.2h3.6V21"/>',
    'tag': '<path d="M3 6a2 2 0 0 1 2-2h5.5a2 2 0 0 1 1.4.6l8.5 8.5a2 2 0 0 1 0 2.8l-5.6 5.6a2 2 0 0 1-2.8 0l-8.5-8.5A2 2 0 0 1 3 11.5V6Z"/><circle cx="7.5" cy="7.5" r="1.1" fill="currentColor" stroke="none"/>',
    'phone': '<path d="M6.6 10.8c1.5 3 3.9 5.3 6.8 6.8l2.1-2.1a1 1 0 0 1 1.1-.2c1.1.4 2.3.6 3.5.6a1 1 0 0 1 1 1v3.4a1 1 0 0 1-1 1C10.7 21.3 2.7 13.3 2.7 3.9a1 1 0 0 1 1-1H7a1 1 0 0 1 1 1c0 1.2.2 2.4.6 3.5a1 1 0 0 1-.2 1.1L6.6 10.8Z"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M20 20l-4.8-4.8"/>',
    'clipboard': '<rect x="5" y="4" width="14" height="17" rx="1.5"/><rect x="9" y="2.3" width="6" height="3" rx="1"/><path d="M9 11h6M9 15h6M9 19h3.5"/>',
    'wrench': '<path d="M14.5 3.5a4.5 4.5 0 0 0-5.8 5.8L3 15l3 3 5.7-5.7a4.5 4.5 0 0 0 5.8-5.8l-3.2 3.2-2.2-.6-.6-2.2 3-3Z"/>',
    'bar-chart': '<rect x="4" y="12" width="4" height="8" rx="1"/><rect x="10" y="7" width="4" height="13" rx="1"/><rect x="16" y="15" width="4" height="5" rx="1"/>',
    'document': '<path d="M7 3h7l4 4v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Z"/><path d="M14 3v4h4"/><path d="M9 13h6M9 17h6"/>',
    'flask': '<path d="M10 3h4"/><path d="M10.5 3v6.5L5.8 18a2 2 0 0 0 1.8 3h8.8a2 2 0 0 0 1.8-3L13.5 9.5V3"/><path d="M8 15h8"/>',
    'map': '<path d="M9 4 3 6.5v13L9 17l6 2.5 6-2.5v-13L15 6.5 9 4Z"/><path d="M9 4v13M15 6.5v13"/>',
    'check': '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.5 2.5L16 9.5"/>',
    'package': '<path d="M3.5 8 12 3.5 20.5 8 12 12.5 3.5 8Z"/><path d="M3.5 8v9L12 21.5 20.5 17V8"/><path d="M12 12.5V21.5"/>',
    'trend-up': '<path d="M3 17 9.5 10.5 13.5 14.5 21 6"/><path d="M15 6h6v6"/>',
    'ruler': '<path d="M4 16 16 4l4 4L8 20Z"/><path d="M13 7l2 2M10 10l2 2M7 13l2 2"/>',
    'partnership': '<circle cx="9" cy="12" r="6"/><circle cx="15" cy="12" r="6"/>',
    'target': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor" stroke="none"/>',
    'wheat': '<path d="M12 21V9"/><path d="M12 9c0-3.5 2-6 6-6-1 4-3 6-6 6Z"/><path d="M12 13c0-3-2-5-6-5 1 3 2.5 5 6 5Z"/>',
    'receipt': '<path d="M6 3h12v18l-2-1.5L14 21l-2-1.5L10 21l-2-1.5L6 21V3Z"/><path d="M9 8h6M9 12h6M9 16h4"/>',
    'trend-down': '<path d="M3 7 9.5 13.5 13.5 9.5 21 17"/><path d="M15 17h6v-6"/>',
    'road': '<path d="M8 3 4 21M16 3l4 18"/><path d="M12 3v3M12 10.5v3M12 18v3"/>',
    'money': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5v9M14.5 9.8a2.6 2.6 0 0 0-2.5-1.8c-1.4 0-2.5.9-2.5 2s1 1.6 2.5 2 2.5 1 2.5 2-1.1 2-2.5 2a2.6 2.6 0 0 1-2.5-1.8"/>',
    'users': '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20c0-3.3 2.5-6 5.5-6s5.5 2.7 5.5 6"/><circle cx="17.5" cy="9" r="2.6"/><path d="M15 20c.2-2.6 1.7-4.6 3.8-4.6 2.2 0 4 2.2 4.2 4.6"/>',
    'scale': '<path d="M12 4v16"/><path d="M6 20h12"/><path d="M4 8h6M14 8h6"/><path d="M4 8l-2.5 5.5a3 3 0 0 0 5 0L4 8Z"/><path d="M20 8l-2.5 5.5a3 3 0 0 0 5 0L20 8Z"/>',
    'utensils': '<path d="M6 3v6a1.5 1.5 0 0 0 3 0V3M7.5 9V21"/><path d="M17 3c-1.3 1-2 3-2 5.5S16 13 17 13v8"/>',
    'bookmark': '<path d="M7 3h10v18l-5-4-5 4Z"/>',
    'bank': '<path d="M4 10 12 4l8 6"/><path d="M5 10v9M9.5 10v9M14.5 10v9M19 10v9"/><path d="M3.5 21h17"/>',
    'scroll': '<path d="M6 4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2"/><circle cx="6" cy="4" r="2"/><circle cx="6" cy="20" r="2"/><path d="M9 8h7M9 12h7M9 16h5"/>',
    'droplet': '<path d="M12 3c4 5 6.5 8.5 6.5 12a6.5 6.5 0 1 1-13 0C5.5 11.5 8 8 12 3Z"/>',
    'sparkles': '<path d="M11 3 12.6 8 18 9.5 12.6 11 11 16 9.4 11 4 9.5 9.4 8 11 3Z"/><path d="M18 15l.9 2.1L21 18l-2.1.9L18 21l-.9-2.1L15 18l2.1-.9L18 15Z"/>',
    'store': '<path d="M4 9 6 3h12l2 6"/><path d="M4 9v11a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9"/><path d="M4 9h16"/><path d="M9 21v-6h6v6"/>',
    'factory': '<path d="M4 21V11l5 3V11l5 3V11l5 3v7Z"/><path d="M4 21h15"/><path d="M9 21v-4M14 21v-4"/>',
    'shopping-bag': '<path d="M6 8h12l-1 13H7L6 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    'hotel': '<path d="M3 19v-9"/><path d="M3 15h18"/><path d="M21 19v-5a2 2 0 0 0-2-2h-8v7"/><circle cx="7" cy="11.5" r="1.6"/><path d="M21 19v2M3 19v2"/>',
    'drink': '<path d="M6 4h12l-1.3 15.5a1 1 0 0 1-1 .9H8.3a1 1 0 0 1-1-.9L6 4Z"/><path d="M6.6 11h10.8"/>',
    'zap': '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/>',
    'ban': '<circle cx="12" cy="12" r="9"/><path d="M6 6l12 12"/>',
    'parking': '<circle cx="12" cy="12" r="9"/><path d="M9.5 16V8h3.2a2.4 2.4 0 0 1 0 4.8H9.5"/>',
    'lock': '<rect x="5" y="11" width="14" height="9" rx="1.5"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    'hourglass': '<path d="M6 3h12M6 21h12"/><path d="M7 3v4.5a5 5 0 0 0 2.2 4.15L12 13l2.8-1.35A5 5 0 0 0 17 7.5V3"/><path d="M7 21v-4.5a5 5 0 0 1 2.2-4.15L12 11l2.8 1.35A5 5 0 0 1 17 16.5V21"/>',
    'microscope': '<path d="M6 20h11"/><circle cx="10.5" cy="14.5" r="4"/><path d="M13.3 11.7 18 7M9 3l3 3"/><path d="M7.3 7.6 10 4.9"/>',
    'message': '<path d="M5 5h14a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H10l-4 4v-4H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z"/>',
    'laptop': '<rect x="4" y="4" width="16" height="10" rx="1"/><path d="M2 19h20l-2-3H4l-2 3Z"/>',
    'id-card': '<rect x="3" y="5" width="18" height="14" rx="1.5"/><circle cx="9" cy="11" r="2"/><path d="M6 16c0-1.8 1.3-3 3-3s3 1.2 3 3"/><path d="M14 9h4M14 12h4"/>',
    'shield': '<path d="M12 3 19 6v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3Z"/>',
    'calendar': '<rect x="4" y="5" width="16" height="16" rx="1.5"/><path d="M4 10h16"/><path d="M8 3v4M16 3v4"/>',
    'flame': '<path d="M12 21c-4 0-6.5-2.6-6.5-6 0-2.7 1.7-4.3 2.7-6.3.6-1.2.8-2.5.6-3.9 2.2 1 3.7 3 3.9 5.3.9-1 1.3-2.3 1.2-3.6 2.4 1.8 4.6 4.8 4.6 8 0 3.7-2.5 6.5-6.5 6.5Z"/>',
    'edit': '<path d="M4 20h4l11-11-4-4L4 16v4Z"/><path d="M13.5 6.5 17.5 10.5"/>',
    'dollar': '<path d="M12 2v20"/><path d="M17 6.5A4 4 0 0 0 13 4H11a4 4 0 0 0 0 8h2a4 4 0 0 1 0 8h-2a4 4 0 0 1-4-2.5"/>',
    'arrow-up-right': '<path d="M7 17 17 7"/><path d="M9 7h8v8"/>',
    'pin': '<path d="M12 21s7-7.5 7-12a7 7 0 1 0-14 0c0 4.5 7 12 7 12Z"/><circle cx="12" cy="9" r="2.5"/>',
    'plane': '<path d="M3 13.5 21 6l-7.5 18-2-8-8-2.5Z"/>',
    'envelope': '<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3 6.5 12 13 21 6.5"/>',
    'car': '<path d="M4 16 5.5 9.5A2 2 0 0 1 7.4 8h9.2a2 2 0 0 1 1.9 1.5L20 16"/><rect x="3" y="16" width="18" height="4" rx="1"/><circle cx="7.5" cy="20" r="1.5"/><circle cx="16.5" cy="20" r="1.5"/>',
    'fuel-pump': '<rect x="4" y="4" width="10" height="17" rx="1"/><path d="M7 8h4"/><path d="M14 9h2.5a1.5 1.5 0 0 1 1.5 1.5V17a1.5 1.5 0 0 0 3 0v-6l-3-3"/>',
    'truck': '<rect x="2" y="8" width="12" height="9" rx="1"/><path d="M14 11h4l3 3v3h-7"/><circle cx="6.5" cy="19" r="1.6"/><circle cx="17" cy="19" r="1.6"/>',
    'tractor': '<circle cx="7" cy="18" r="3"/><circle cx="18" cy="18" r="2.2"/><path d="M10 18h5.5"/><path d="M8 12h5l3 3.5h2.5"/><path d="M9 8h3v4"/>',
    'school': '<path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="M6 10.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-5.5"/><path d="M21 8v6"/>',
    'cityscape': '<path d="M3 21V9l4-3 4 3v12"/><path d="M11 21V6l4-3 4 3v15"/><path d="M3 21h18"/><path d="M6 12h2M6 16h2M14 9h2M14 13h2M14 17h2"/>',
    'cake': '<path d="M4 21v-7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v7Z"/><path d="M4 17h16"/><path d="M9 12V8M12 12V8M15 12V8"/><path d="M9 8c0-1 .5-1.5.5-2.5S9 4 9 4M12 8c0-1 .5-1.5.5-2.5S12 4 12 4M15 8c0-1 .5-1.5.5-2.5S15 4 15 4"/>',
    'teddy-bear': '<circle cx="9" cy="5" r="1.8"/><circle cx="15" cy="5" r="1.8"/><circle cx="12" cy="12" r="7"/><circle cx="9" cy="11" r="1"/><circle cx="15" cy="11" r="1"/><path d="M10 15c.7.7 3.3.7 4 0"/>',
    'park': '<path d="M8 13 5 20h6L8 13Z"/><path d="M8 9 5.5 14h5L8 9Z"/><path d="M16 15l-3.5 5H19l-3-5Z"/><path d="M8 20v2M16 20v2"/>',
    'briefcase': '<rect x="3" y="8" width="18" height="12" rx="1.5"/><path d="M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M3 13h18"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.5 4 5.8 4 9s-1.5 6.5-4 9c-2.5-2.5-4-5.8-4-9s1.5-6.5 4-9Z"/>',
    'stopwatch': '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2"/><path d="M9 2h6"/><path d="M12 2v3"/>',
    'construction': '<path d="M5 21V9l6-5 6 5v12"/><path d="M5 21h12"/><path d="M9 21v-6h4v6"/><path d="M18 6h3v4"/>',
    'pedestrian': '<circle cx="12" cy="4.5" r="1.8"/><path d="M12 7v5l-3 8M12 12l3 3-1 5M9 11l-3 2"/>',
    'smoking': '<path d="M3 17h13"/><path d="M18 17h3"/><path d="M16 14c1-1 1-2.5 0-3.5M18 12c1.3-1.3 1.3-3.2 0-4.5"/>',
    'thermometer': '<path d="M12 3a2 2 0 0 0-2 2v9.5a4 4 0 1 0 4 0V5a2 2 0 0 0-2-2Z"/><path d="M12 15v-6"/>',
    'graduation-cap': '<path d="M2 9 12 4l10 5-10 5-10-5Z"/><path d="M6 11.5V16c0 1.5 2.7 3 6 3s6-1.5 6-3v-4.5"/><path d="M22 9v6"/>',
    'lightbulb': '<path d="M9 18h6"/><path d="M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3Z"/>',
    'cart': '<circle cx="9" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/><path d="M2.5 3h2.5l2.6 12.4a1.5 1.5 0 0 0 1.5 1.2h8.4a1.5 1.5 0 0 0 1.5-1.2L21 8H6.5"/>',
}

def icon_svg(name):
    return (f'<svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" '
            f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" '
            f'style="vertical-align:-0.15em">{ICON_PATHS[name]}</svg>')

# Ordered so multi-codepoint sequences (e.g. the farmer emoji, adult+ZWJ+wheat)
# are matched before their standalone component characters.
EMOJI_ICON = [
    ('\U0001F9D1‍\U0001F33E', 'wheat'),
    ('\U0001F9D1‍\U0001F3EB', 'school'),
    ('\U0001F9EA', 'flask'), ('\U0001F5FA', 'map'), ('\U0001F6E3', 'road'),
    ('⚡', 'zap'), ('\U0001F4C4', 'document'), ('\U0001F4D0', 'ruler'),
    ('\U0001F4CF', 'ruler'), ('\U0001F6AB', 'ban'), ('\U0001F4B0', 'money'),
    ('\U0001F4B5', 'money'), ('\U0001F527', 'wrench'), ('\U0001F4CA', 'bar-chart'),
    ('\U0001F4CB', 'clipboard'), ('\U0001F465', 'users'), ('\U0001F91D', 'partnership'),
    ('\U0001F92B', 'lock'), ('\U0001F510', 'lock'), ('\U0001F4E6', 'package'),
    ('\U0001F3AF', 'target'), ('⚖', 'scale'), ('\U0001F33E', 'wheat'),
    ('\U0001F52C', 'microscope'), ('\U0001F4C8', 'trend-up'), ('\U0001F9FE', 'receipt'),
    ('\U0001F4AC', 'message'), ('\U0001F37D', 'utensils'), ('✅', 'check'),
    ('\U0001F4D1', 'bookmark'), ('\U0001F4C9', 'trend-down'), ('\U0001F3E6', 'bank'),
    ('\U0001F50D', 'search'), ('\U0001F4BB', 'laptop'), ('\U0001F4C7', 'id-card'),
    ('\U0001F6E1', 'shield'), ('\U0001F4C5', 'calendar'), ('\U0001F9EF', 'flame'),
    ('\U0001F4DC', 'scroll'), ('\U0001F4DD', 'edit'), ('\U0001F4B2', 'dollar'),
    ('\U0001F4A7', 'droplet'), ('\U0001F6B0', 'droplet'), ('\U0001F3E0', 'house'),
    ('\U0001F3E1', 'house'), ('\U0001F511', 'key'), ('\U0001F3E2', 'building'),
    ('✨', 'sparkles'), ('\U0001F3F7', 'tag'), ('\U0001F3EC', 'store'),
    ('\U0001F3EA', 'store'), ('\U0001F3ED', 'factory'), ('\U0001F6CD', 'shopping-bag'),
    ('\U0001F6D2', 'cart'), ('\U0001F3E8', 'hotel'), ('\U0001F943', 'drink'),
    ('\U0001F37A', 'drink'), ('\U0001F17F', 'parking'), ('⏳', 'hourglass'),
    ('⏱', 'stopwatch'), ('\U0001F4CD', 'pin'), ('✈', 'plane'),
    ('\U0001F4DE', 'phone'), ('✉', 'envelope'), ('\U0001F697', 'car'),
    ('⛽', 'fuel-pump'), ('\U0001F69B', 'truck'), ('\U0001F69C', 'tractor'),
    ('\U0001F3EB', 'school'), ('\U0001F3D9', 'cityscape'), ('\U0001F382', 'cake'),
    ('\U0001F9F8', 'teddy-bear'), ('\U0001F3DE', 'park'), ('\U0001F4A1', 'lightbulb'),
    ('\U0001F4BC', 'briefcase'), ('\U0001F310', 'globe'), ('\U0001F3D7', 'construction'),
    ('\U0001F6B6', 'pedestrian'), ('\U0001F6AC', 'smoking'), ('\U0001F321', 'thermometer'),
    ('\U0001F414', 'wheat'), ('\U0001F393', 'graduation-cap'),
]

def apply_icons(html):
    html = html.replace('️', '')
    for ch, name in EMOJI_ICON:
        if ch in html:
            html = html.replace(ch, icon_svg(name))
    return html

