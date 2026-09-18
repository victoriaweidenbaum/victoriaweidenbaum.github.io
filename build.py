#!/usr/bin/env python3
"""
Generates the static site (index.html, about/, portfolio/*/) from the content below.

Run:  python3 build.py
Then preview with:  python3 -m http.server 8000   (open http://localhost:8000)

Layout notes
- Pages use a 24-column grid on desktop and an 8-column grid on mobile
  (plus one gutter column on each side), the same grid the original site used.
- Each block has a mobile position (m) and a desktop position (d) written as
  "rowStart/colStart/rowEnd/colEnd".
"""
from pathlib import Path
import html as htmlmod

ROOT = Path(__file__).parent
SITE_NAME = "Victoria Weidenbaum"
EMAIL = "vweidenbaum@gmail.com"
RESUME = "/s/VictoriaWeidenbaum-Resume-generic.pdf"

# ----------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------

PROJECTS = [
    # slug, title (shown in grid + pagination), grid image
    ("avail", "Avail 0→1", "grid-avail.jpg"),
    ("iaredesign", "Information Architecture Redesign • Retool", "grid-ia-redesign.png"),
    ("adminconsoleredesign", "Admin Console Redesign • Dropbox", "grid-admin-console.webp"),
    ("securitystrategy", "Security Strategy • Dropbox", "grid-security-strategy.webp"),
    ("checkout", "Checkout • Instacart", "grid-checkout.webp"),
    ("help", "Help Center • Instacart", "grid-help-center.webp"),
    ("shoppingimprovements", "Shopping Improvements • Instacart", "grid-shopping-improvements.webp"),
    ("missingcustomer", "Missing Customer • Instacart", "grid-missing-customer.webp"),
]

HOME_INTRO = (
    "<h1 class=\"hero-title\">Hi, I’m Victoria!</h1>"
    "<p>Product Designer with 11+ years of experience helping Bay Area "
    "tech companies build products people rely on every day. Most recently at Retool, with previous "
    "roles at Dropbox and Instacart. I live in San Francisco with my dog Betty and cat Henry. "
    "I'm the artist behind clay studio <a href=\"https://stonebloom.studio\">Stone Bloom</a>.</p>"
)

ABOUT_TEXT = (
    "<p>I'm a Staff Product Designer with over a decade of experience shaping products at Bay Area tech "
    "companies. Most recently, I was at Retool, working on information architecture that helped developers "
    "explore all the available tools. Before that, I spent over three years at Dropbox shaping core product "
    "experiences for teams of all sizes, and three years at Instacart designing the Shopper app to make "
    "grocery delivery smoother for tens of thousands of shoppers.</p>"
    "<p>I thrive on transforming complex problems into simple solutions and get energized by strategic design "
    "work. The rise of AI excites me, I believe it's reshaping how designers, product managers, and developers "
    "work together, and I'm always exploring new tools to amplify my impact.</p>"
    "<p>When I'm not designing, you'll find me making clay art at "
    "<a href=\"https://stonebloom.studio\" target=\"_blank\" rel=\"noopener\">Stone Bloom</a>, strolling the "
    "beach with my partner Dylan and our dog Betty, experimenting in the kitchen with healthy recipes, "
    "snowboarding down slopes, or planning my next Burning Man adventure.</p>"
    "<p>If you'd like to chat about design, collaboration opportunities, or just connect, email me at "
    f"<a href=\"mailto:{EMAIL}?subject=Hi%20Victoria%2C%20I'd%20like%20to%20connect\" target=\"_blank\">{EMAIL}</a>!</p>"
)


def caption(text, italic=True):
    inner = f"<em>{text}</em>" if italic else text
    return f'<p class="fs-small" style="text-align:center">{inner}</p>'


# Each portfolio page: a list of sections. Section kinds:
#   {"kind": "grid", "height": "small|medium", "valign": "middle|top", "rows_m": n, "rows_d": n, "blocks": [...]}
#   {"kind": "classic", "image": file, "ratio": padding-bottom %, "max": natural width px}
# Block kinds inside a grid: text / image / button.
PAGES = {
    "avail": {
        "title": "Avail 0→1",
        "sections": [
            {"kind": "grid", "height": "medium", "rows_m": 22, "rows_d": 10, "blocks": [
                {"kind": "text", "m": "1/2/4/10", "d": "1/2/4/14", "html": "<h2>Avail 0→1</h2>"},
                {"kind": "text", "m": "4/2/23/10", "d": "1/14/11/26", "html":
                    "<p>Avail is a 0 → 1 product I’m designing and building as a team of two: a small social app for "
                    "letting close friends know you’re free to hang out. Instead of coordinating over group chats, you "
                    "start an “avail” with a time window, a place and a short note. Friends see it on a map and in a "
                    "simple list, and can respond with one tap. It’s launching soon on the Apple App Store.</p>"
                    "<p>Avail is a fully AI-native project. I worked on it exclusively with Claude Code, going from "
                    "first sketches to a working iOS and web app without a traditional design-to-engineering handoff. "
                    "The branding, the visual language and every part of the product design were developed by me.</p>"
                    "<p>This first version is deliberately small. There are a lot more features on the roadmap that "
                    "didn’t make it into 0 → 1, because we’re still in the process of proving the concept. The focus so "
                    "far has been the core loop: open the app, see who’s around, and share your own availability in a "
                    "few seconds.</p>"},
            ]},
            {"kind": "video", "src": "avail-flow.mp4", "poster": "avail-poster.jpg", "width": 604, "height": 1312,
             "caption": "Core flow: opening the app, seeing who’s around, and starting a new avail"},
        ],
    },
    "adminconsoleredesign": {
        "title": "Admin Console Redesign • Dropbox",
        "sections": [
            {"kind": "grid", "height": "medium", "rows_m": 30, "rows_d": 36, "blocks": [
                {"kind": "text", "m": "1/2/4/10", "d": "1/2/3/14", "html": "<h2>Admin Console Redesign</h2>"},
                {"kind": "text", "m": "4/2/10/10", "d": "1/14/4/26", "html":
                    "<p>Admin Console was a catch all, never-loved-by-design-team kind of experience. After 3 months "
                    "of tight sprint cycles across multiple teams, we made it easy for admins (main purchase decision "
                    "makers on business plans) to complete important tasks, and increased admin satisfaction by 10%. </p>"},
                {"kind": "image", "m": "10/2/17/10", "d": "4/2/18/26", "src": "admin-console-1.gif", "fit": "contain", "jm": "center"},
                {"kind": "image", "m": "17/2/23/10", "d": "19/14/37/26", "src": "admin-console-2.gif", "fit": "cover"},
                {"kind": "image", "m": "23/2/31/10", "d": "19/2/37/14", "src": "admin-console-3.webp", "fit": "cover"},
            ]},
        ],
    },
    "checkout": {
        "title": "Checkout • Instacart",
        "sections": [
            {"kind": "grid", "height": "small", "rows_m": 13, "rows_d": 9, "blocks": [
                {"kind": "text", "m": "1/2/6/10", "d": "1/2/4/12", "html": "<h2>Checkout</h2>"},
                {"kind": "text", "m": "6/2/8/10", "d": "3/2/4/8", "html": '<p class="fs-small">September, 2021</p>'},
                {"kind": "text", "m": "8/2/13/10", "d": "1/14/10/26", "html":
                    "<p>At Instacart, I spent three years as a Senior Product Designer on the Fulfillment team, designing "
                    "core experiences for Shoppers who handle grocery shopping and delivery. My final project was leading "
                    "the Shopper Checkout redesign – a complex initiative to streamline the critical path for thousands "
                    "active shoppers across hundreds of retail partners. The project involved rebuilding the checkout flow "
                    "with new components while ensuring flexibility to support diverse store requirements and checkout "
                    "scenarios, ultimately reducing errors and improving completion rates.</p>"
                    f"<p>Interested in learning more? <a href=\"mailto:{EMAIL}?subject=Hello%20from%20%5BYour%20name%5D\" target=\"_blank\">Contact me</a> "
                    "for an in-depth case study of the Checkout redesign.</p>"},
            ]},
            {"kind": "classic", "image": "checkout-1.gif", "ratio": 60.98, "max": 2122},
            {"kind": "classic", "image": "checkout-2.webp", "ratio": 45.23, "max": 5565},
            {"kind": "classic", "image": "checkout-3.webp", "ratio": 45.23, "max": 5565},
        ],
    },
    "help": {
        "title": "Help Center • Instacart",
        "sections": [
            {"kind": "grid", "height": "small", "rows_m": 13, "rows_d": 10, "blocks": [
                {"kind": "text", "m": "1/2/6/10", "d": "1/2/5/12", "html": "<h2>Help Center</h2>"},
                {"kind": "text", "m": "6/2/8/10", "d": "3/2/5/8", "html": "<p>Instacart, 2019</p>"},
                {"kind": "text", "m": "8/2/13/10", "d": "1/14/11/26", "html":
                    "<p>Back in 2019, if a shopper contacted Instacart to get help, our team didn’t have a lot of visibility "
                    "into the issue they were contacting us about. When Care agents took shoppers’ calls, they had to ask a "
                    "lot of questions to understand what problems they were experiencing, which led to long call times. </p>"
                    "<p>Shopper only had access to a web-only Help Center. Switching between the Shopper app and the web "
                    "wasn’t an ideal experience — especially when shoppers were in the middle of an order.</p>"
                    "<p>We aimed to create a simple, dynamic experience for shoppers that offers different options for "
                    "getting support. </p>"
                    f"<p>Interested in learning more? <a href=\"mailto:{EMAIL}?subject=Hello%20from%20%5Binsert%20your%20name%5D\" target=\"_blank\">Contact me</a> "
                    "to learn more details about Help Center project. </p>"},
            ]},
            {"kind": "grid", "height": "small", "rows_m": 11, "rows_d": 17, "blocks": [
                {"kind": "image", "m": "1/2/12/10", "d": "1/5/18/23", "src": "help-center-1.webp", "fit": "cover", "fp": "3.07% 51.2%"},
            ]},
            {"kind": "classic", "image": "help-center-2.webp", "ratio": 56.29, "max": 1400},
            {"kind": "classic", "image": "help-center-3.webp", "ratio": 55.07, "max": 1400},
        ],
    },
    "iaredesign": {
        "title": "Information Architecture Redesign • Retool",
        "sections": [
            {"kind": "grid", "height": "medium", "rows_m": 65, "rows_d": 85, "blocks": [
                {"kind": "text", "m": "1/2/4/10", "d": "1/2/4/14", "jm": "center", "jd": "flex-start",
                 "html": "<h2>Information Architecture Redesign</h2>"},
                {"kind": "text", "m": "4/2/13/10", "d": "1/14/6/26", "jm": "flex-start", "jd": "center", "html":
                    "<p>The browsing experience at Retool spans many surface areas where different personas (admins, "
                    "developers, and end users) create, discover and use internal apps. As part of a small design team, "
                    "I led the redesign process: from conducting and moderating research, defining personas and their "
                    "needs, to prioritizing features in close collaboration with engineering and product.</p>"
                    "<p>The focus of this project was twofold: improving app discoverability and designing a new feature "
                    "called Projects.</p>"},
                {"kind": "image", "m": "13/2/20/10", "d": "8/2/23/26", "src": "ia-redesign-1.gif", "fit": "contain", "jm": "center"},
                {"kind": "text", "m": "20/2/22/10", "d": "23/11/24/17", "html": caption("Home page details and navigation")},
                {"kind": "image", "m": "22/2/29/10", "d": "26/2/41/26", "src": "ia-redesign-2.gif", "fit": "contain", "jm": "center"},
                {"kind": "text", "m": "29/2/31/10", "d": "41/10/42/18", "html": caption("Side rail: Builder, End User and Admin pages. Utilities.")},
                {"kind": "image", "m": "31/2/38/10", "d": "45/2/60/26", "src": "ia-redesign-3.gif", "fit": "contain", "jm": "center"},
                {"kind": "text", "m": "38/2/40/10", "d": "60/10/61/18", "html": caption("Projects: 0→ 1 concept")},
                {"kind": "image", "m": "40/2/52/10", "d": "64/2/82/14", "src": "ia-redesign-4.gif", "fit": "cover"},
                {"kind": "text", "m": "52/2/54/10", "d": "82/4/83/12", "html": caption("Part of design process: low-fidelity flow charting")},
                {"kind": "image", "m": "54/2/64/10", "d": "64/14/82/26", "src": "ia-redesign-5.webp", "fit": "cover"},
                {"kind": "text", "m": "64/2/66/10", "d": "82/16/83/24", "html": caption("Project page", italic=False)},
            ]},
        ],
    },
    "missingcustomer": {
        "title": "Missing Customer • Instacart",
        "sections": [
            {"kind": "grid", "height": "small", "rows_m": 11, "rows_d": 7, "blocks": [
                {"kind": "text", "m": "1/2/6/10", "d": "1/2/4/12", "html": "<h2>Missing customer</h2>"},
                {"kind": "text", "m": "6/2/11/10", "d": "1/14/8/26", "html":
                    "<p>A missing customer is one of the highest contact rate issues that happens when shoppers can’t locate "
                    "customers during delivery. The old experience contained multiple steps that shoppers had to take to "
                    "troubleshoot, leading to confusion and dissatisfaction. I collaborated with the Data Science and "
                    "Research teams to redesign and simplify this experience.</p>"
                    f"<p>Would you like to learn more about this project? Please, <a href=\"mailto:{EMAIL}\">contact me </a>for more information.</p>"},
            ]},
            {"kind": "classic", "image": "missing-customer-1.webp", "ratio": 45.23, "max": 5565},
        ],
    },
    "securitystrategy": {
        "title": "Security Strategy • Dropbox",
        "sections": [
            {"kind": "grid", "height": "small", "rows_m": 11, "rows_d": 5, "blocks": [
                {"kind": "text", "m": "1/2/6/10", "d": "1/2/3/12", "html": "<h2>Security Strategy</h2>"},
                {"kind": "text", "m": "6/2/11/10", "d": "1/14/6/26", "html":
                    "<p>As Design Lead at Dropbox, I led a cross-functional Security journey mapping initiative spanning "
                    "three teams, grounded in user research to identify the core jobs-to-be-done. The journey directly "
                    "informed roadmap planning across all three teams for 2024, a particularly high-impact outcome, given "
                    "that security feature adoption was one of our most important retention signals. The vocabulary "
                    "established through this work has since been adopted company-wide, creating a shared language for "
                    "discussing security experiences.</p>"},
            ]},
            {"kind": "classic", "image": "security-strategy-1.webp", "ratio": 95.625, "max": 3840},
        ],
    },
    "shoppingimprovements": {
        "title": "Shopping Improvements • Instacart",
        "sections": [
            {"kind": "grid", "height": "none", "valign": "top", "rows_m": 11, "rows_d": 7, "blocks": [
                {"kind": "text", "m": "1/2/6/10", "d": "1/2/6/12", "html": "<h2>Shopping improvements</h2>"},
                {"kind": "text", "m": "6/2/11/10", "d": "1/14/8/26", "html":
                    "<p>The goal to improve education for shoppers in Mixed Orders experience. The initial assumption was "
                    "that shoppers’ lack of understanding how things work caused order issues to grow. After a few design "
                    "iterations and a round of concept testing, we identified the gaps in the experience itself. We defined "
                    "and designed solutions that covered these gaps. </p>"
                    f"<p>Would you like to learn more about this project? Please, <a href=\"mailto:{EMAIL}\">contact me</a> for more information. </p>"},
            ]},
            {"kind": "classic", "image": "shopping-improvements-1.webp", "ratio": 45.23, "max": 5565},
        ],
    },
}

# ----------------------------------------------------------------------------
# Templates
# ----------------------------------------------------------------------------

# Photo mask: the original four-petal flower.
FLOWER_MASK = (
    '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
    '<clipPath id="photo-flower" clipPathUnits="objectBoundingBox">'
    '<path d="M0.09 0.5 A0.1 0.103 -45 0 1 0.5 0.09 A0.103 0.1 -45 0 1 0.91 0.5 '
    'A0.1 0.103 -45 0 1 0.5 0.91 A0.103 0.1 -45 0 1 0.09 0.5"/></clipPath></defs></svg>'
)

CARET_LEFT = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16 3 L7 12 L16 21" fill="none" '
              'stroke="currentColor" stroke-width="1" stroke-linecap="square"/></svg>')
CARET_RIGHT = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 3 L17 12 L8 21" fill="none" '
               'stroke="currentColor" stroke-width="1" stroke-linecap="square"/></svg>')


def layout(title, body, active, description=""):
    full_title = SITE_NAME if title is None else f"{title} — {SITE_NAME}"
    nav_items = []
    for key, href, label in (("home", "/", "Portfolio"), ("about", "/about/", "About")):
        cls = ' class="active"' if key == active else ""
        nav_items.append(f'<a href="{href}"{cls}>{label}</a>')
    nav = "".join(nav_items)
    desc = f'\n  <meta name="description" content="{htmlmod.escape(description)}">' if description else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{htmlmod.escape(full_title)}</title>{desc}
  <link rel="icon" type="image/png" href="/images/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@700&family=Open+Sans:wght@400;600&family=Work+Sans:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  {FLOWER_MASK}
  <header class="site-header">
    <div class="header-inner">
      <a class="logo" href="/"><img src="/images/logo.webp" alt="{SITE_NAME}" width="438" height="166"></a>
      <nav class="site-nav" aria-label="Main">{nav}</nav>
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
        <span class="burger-box"><span></span><span></span></span>
      </button>
    </div>
  </header>
  <nav class="mobile-menu" id="mobile-menu" aria-label="Mobile">{nav}</nav>

  <main id="page">
{body}
  </main>

  <footer class="site-footer section">
    <div class="content-wrapper">
      <div class="footer-row">
        <div class="footer-col left"><h4>© 2026</h4></div>
        <div class="footer-col right"><h4><a href="mailto:{EMAIL}">{EMAIL}</a></h4></div>
      </div>
    </div>
  </footer>

  <script>
    (function () {{
      var btn = document.querySelector('.burger');
      btn.addEventListener('click', function () {{
        var open = document.body.classList.toggle('menu-open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      }});
    }})();
  </script>
</body>
</html>
"""


def style_attr(block):
    parts = [f"--m:{block['m']}", f"--d:{block['d']}"]
    if block.get("jm"):
        parts.append(f"--jm:{block['jm']}")
    if block.get("jd"):
        parts.append(f"--jd:{block['jd']}")
    if block.get("fp"):
        parts.append(f"--fp:{block['fp']}")
    return ";".join(parts)


def render_block(block):
    st = style_attr(block)
    k = block["kind"]
    if k == "text":
        cls = ("text " + block["cls"]) if block.get("cls") else "text"
        return f'      <div class="blk" style="{st}"><div class="{cls}">{block["html"]}</div></div>'
    if k == "image":
        cls = "img-fill contain" if block.get("fit") == "contain" else "img-fill"
        alt = htmlmod.escape(block.get("alt", ""))
        return (f'      <div class="blk" style="{st}"><div class="{cls}">'
                f'<img src="/images/{block["src"]}" alt="{alt}" loading="lazy"></div></div>')
    if k == "image-square":
        alt = htmlmod.escape(block.get("alt", ""))
        zoom = block.get("zoom")
        zcls = " zoom" if zoom else ""
        zst = f' style="--iw:{zoom["w"]};--ix:{zoom["x"]};--iy:{zoom["y"]}"' if zoom else ""
        return (f'      <div class="blk sq" style="{st}"><div class="img-square {block.get("mask", "")}{zcls}"{zst}>'
                f'<img src="/images/{block["src"]}" alt="{alt}"></div></div>')
    if k == "button":
        return (f'      <div class="blk" style="{st}"><div class="btn-wrap">'
                f'<a class="btn" href="{block["href"]}" target="_blank" rel="noopener">{block["label"]}</a></div></div>')
    raise ValueError(k)


def render_section(sec):
    if sec["kind"] == "grid":
        cls = ["section", "fluid"]
        if sec.get("height") == "medium":
            cls.append("h-medium")
        elif sec.get("height") == "custom":
            cls.append("h-custom")
        elif sec.get("height") == "none":
            cls.append("h-none")
        if sec.get("valign") == "top":
            cls.append("v-top")
        blocks = "\n".join(render_block(b) for b in sec["blocks"])
        return (f'    <section class="{" ".join(cls)}"><div class="content-wrapper"><div class="content">\n'
                f'      <div class="fe" style="--rows-m:{sec["rows_m"]};--rows-d:{sec["rows_d"]}">\n'
                f'{blocks}\n      </div>\n    </div></div></section>')
    if sec["kind"] == "classic":
        return (f'    <section class="section w-medium"><div class="content-wrapper"><div class="content">\n'
                f'      <figure class="classic-img" style="max-width:{sec["max"]}px"><div class="ratio" style="padding-bottom:{sec["ratio"]}%">'
                f'<img src="/images/{sec["image"]}" alt="" loading="lazy"></div></figure>\n'
                f'    </div></div></section>')
    if sec["kind"] == "video":
        cap = f'<figcaption class="fs-small"><em>{sec["caption"]}</em></figcaption>' if sec.get("caption") else ""
        return (f'    <section class="section"><div class="content-wrapper"><div class="content">\n'
                f'      <figure class="video-panel"><div class="video-stage"><div class="phone">'
                f'<video src="/videos/{sec["src"]}" poster="/images/{sec["poster"]}" width="{sec["width"]}" height="{sec["height"]}" '
                f'autoplay muted loop playsinline controls preload="metadata"></video></div></div>{cap}</figure>\n'
                f'    </div></div></section>')
    raise ValueError(sec["kind"])


def render_pagination(slug):
    idx = [p[0] for p in PROJECTS].index(slug)
    prev_p = PROJECTS[idx - 1] if idx > 0 else None
    next_p = PROJECTS[idx + 1] if idx < len(PROJECTS) - 1 else None
    out = ['    <section class="item-pagination">']
    if prev_p:
        out.append(f'      <a class="prev" href="/portfolio/{prev_p[0]}/"><span class="icon">{CARET_LEFT}</span>'
                   f'<span><span class="visually-hidden">Previous</span><h2 class="pagination-title">{prev_p[1]}</h2></span></a>')
    if next_p:
        out.append(f'      <a class="next" href="/portfolio/{next_p[0]}/"><span><span class="visually-hidden">Next</span>'
                   f'<h2 class="pagination-title">{next_p[1]}</h2></span><span class="icon">{CARET_RIGHT}</span></a>')
    out.append('    </section>')
    return "\n".join(out)


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------

def build_home():
    # Photo: fills the flower at its full width (the closest crop the source allows is also the widest),
    # anchored to the bottom of the image. A "zoom" dict (w/x/y in %) on the block reframes it if needed.
    button = f'<a class="btn" href="{RESUME}" target="_blank" rel="noopener">View resume</a>'
    hero = {"kind": "grid", "height": "custom", "rows_m": 15, "rows_d": 13, "blocks": [
        {"kind": "image-square", "m": "1/3/8/9", "d": "2/7/11/13", "jm": "center", "src": "victoria-home.webp",
         "mask": "mask-flower", "fp": "52% 98.4%", "alt": "Victoria Weidenbaum"},
        {"kind": "text", "cls": "hero-intro", "m": "8/2/16/10", "d": "2/14/11/22", "jd": "center", "html": HOME_INTRO + button},
    ]}
    items = "\n".join(
        f'        <a class="grid-item" href="/portfolio/{slug}/">'
        f'<div class="grid-image"><img src="/images/{img}" alt="{htmlmod.escape(title)}"></div>'
        f'<div class="portfolio-text"><h3 class="portfolio-title">{title}</h3></div></a>'
        for slug, title, img in PROJECTS
    )
    grid = (f'    <section class="portfolio-section">\n      <div class="portfolio-grid">\n{items}\n'
            f'      </div>\n    </section>')
    body = render_section(hero) + "\n" + grid
    return layout(None, body, "home",
                  "Victoria Weidenbaum — Staff Product Designer in San Francisco. Portfolio of work at Retool, Dropbox and Instacart.")


def build_about():
    sec = {"kind": "grid", "height": "small", "valign": "top", "rows_m": 63, "rows_d": 16, "blocks": [
        {"kind": "text", "m": "1/6/64/10", "d": "2/15/17/26", "html": ABOUT_TEXT},
        {"kind": "image", "m": "1/2/6/6", "d": "2/4/16/13", "jm": "center", "src": "victoria-about.webp",
         "fit": "cover", "alt": "Victoria Weidenbaum"},
    ]}
    return layout("About", render_section(sec), "about")


def build_project(slug):
    page = PAGES[slug]
    body = "\n".join(render_section(s) for s in page["sections"]) + "\n" + render_pagination(slug)
    return layout(page["title"], body, "home")


def build_404():
    body = ('    <section class="section"><div class="content-wrapper"><div class="content notfound">'
            '<h2>Page not found</h2><p>The page you are looking for doesn’t exist. '
            '<a href="/">Go back to the portfolio</a>.</p></div></div></section>')
    return layout("Page not found", body, None)


def write(path, content):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    write("index.html", build_home())
    write("about/index.html", build_about())
    for slug in PAGES:
        write(f"portfolio/{slug}/index.html", build_project(slug))
    write("404.html", build_404())
