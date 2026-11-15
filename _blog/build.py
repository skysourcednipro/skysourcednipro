"""Emit crawlable, standalone blog pages for the existing static site."""

from html import escape
from json import dumps
from pathlib import Path
from urllib.parse import quote, urlencode
from xml.etree import ElementTree as ET

from posts import POSTS

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://skysource.com.ua'
BLOG = '/blog.html'
ORDER = '/water.html#order-card'
ASSETS = '/assets/blog'
PUBLISHED = '2026-11-15'
VISIBLE_DATE = '15 листопада 2026'
LOGO = 'https://i.ibb.co/Y7jCqPDF/c660937a-9272-4146-82e4-074b94f35d73.png'
BY_SLUG = {post['slug']: post for post in POSTS}
BLOG_TITLE = 'Блог SkySource — питна вода та доставка в Дніпрі'
BLOG_DESCRIPTION = 'Практичні статті SkySource про замовлення й доставку води в Дніпрі, зберігання бутлів, догляд за кулером та запаси для офісу.'


def permalink(slug):
    return f'/blog/{slug}.html'


def head(title, description, path, cover, alt, schema, is_article=False):
    canonical = SITE + path
    social_image = f'{SITE}{ASSETS}/{cover}.jpg'
    metadata = dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    published = f'<meta property="article:published_time" content="{PUBLISHED}">' if is_article else ''
    return f"""<!doctype html>
<html lang="uk">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#f6f9fd">
    <title>{escape(title)}</title>
    <meta name="description" content="{escape(description)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="{'article' if is_article else 'website'}">
    <meta property="og:locale" content="uk_UA">
    <meta property="og:site_name" content="SkySource">
    <meta property="og:title" content="{escape(title)}">
    <meta property="og:description" content="{escape(description)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{social_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="{escape(alt)}">
    {published}
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%230958bf' d='M12 2C10 5 5 10 5 15a7 7 0 0 0 14 0c0-5-5-10-7-13Z'/%3E%3C/svg%3E">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;650;700;750;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{ASSETS}/blog.css">
    <script type="application/ld+json">{metadata}</script>
    <script src="{ASSETS}/blog.js" defer></script>
</head>"""


def site_header(is_article=False):
    nav_link = f'<a class="nav-link" href="{BLOG}">Блог</a>' if is_article else '<a class="nav-link" href="/">Особистий кабінет</a>'
    return f"""
    <header class="site-header">
        <div class="wrap header-inner">
            <a class="brand" href="/" aria-label="SkySource — головна">
                <img src="{LOGO}" alt="SkySource" width="148">
            </a>
            <nav class="nav" aria-label="Основна навігація">
                {nav_link}
                <a class="button" href="{ORDER}">Замовити воду</a>
            </nav>
        </div>
    </header>"""


SITE_FOOTER = """
    <footer class="site-footer">
        <div class="wrap footer-inner">
            <p>© SkySource · Дніпро</p>
            <div class="footer-links">
                <a href="/">Особистий кабінет</a>
                <a href="/privacy.html">Політика конфіденційності</a>
            </div>
        </div>
    </footer>"""


ORDER_PANEL = f"""
        <section class="order-panel" aria-label="Замовити воду в Дніпрі">
            <div>
                <h2>Потрібна вода додому чи в офіс?</h2>
                <p>Безкоштовна доставка по Дніпру. Замовлення онлайн без входу.</p>
            </div>
            <div class="order-actions">
                <a class="button" href="{ORDER}">Замовити воду</a>
                <span class="phone"><a href="tel:+380966974664">+38&nbsp;(096)&nbsp;697‑46‑64</a></span>
                <span class="phone"><a href="tel:+380506974664">+38&nbsp;(050)&nbsp;697‑46‑64</a></span>
            </div>
        </section>"""


def image(cover, alt, css_class='', priority=False, thumbnail=False):
    sizing = 'fetchpriority="high"' if priority else 'loading="lazy" decoding="async"'
    src = f'{ASSETS}/{cover}.jpg'
    if thumbnail:
        return f'<img src="{ASSETS}/{cover}-card.webp" alt="{escape(alt)}" width="640" height="336" {sizing}>'
    return f'<img class="{css_class}" src="{src}" alt="{escape(alt)}" width="1200" height="630" {sizing}>'


def share_panel(title, canonical):
    caption = f'{title}\n{canonical}'
    targets = {
        'Telegram': 'https://t.me/share/url?' + urlencode({'url': canonical, 'text': title}),
        'Facebook': 'https://www.facebook.com/sharer/sharer.php?' + urlencode({'u': canonical}),
        'WhatsApp': 'https://wa.me/?' + urlencode({'text': caption}),
    }
    links = ' '.join(
        f'<a href="{escape(url)}" target="_blank" rel="noopener noreferrer">{platform}</a>'
        for platform, url in targets.items()
    )
    return f"""
        <section class="share" aria-label="Поділитися статтею">
            <h2>Поділитися статтею</h2>
            <div class="share-links">
                {links}
                <a href="viber://forward?text={quote(caption, safe='')}">Viber</a>
                <button type="button" data-copy-link>Копіювати посилання</button>
            </div>
            <input class="copy-input" type="url" value="{canonical}" readonly hidden aria-label="Посилання на статтю">
            <p class="share-status" role="status"></p>
        </section>"""


def wrap_document(metadata, main, is_article=False):
    document = f"""{metadata}
<body>
{site_header(is_article)}
{main}
{SITE_FOOTER}
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def render_article(post):
    slug = post['slug']
    path = permalink(slug)
    canonical = SITE + path
    title = post['title']
    description = post['description']
    source = ''
    if 'source' in post:
        label, href = post['source']
        source = f'<p class="source">Джерело: <a href="{escape(href)}">{escape(label)}</a></p>'
    related = ''.join(
        f'<li><a href="{permalink(item)}">{escape(BY_SLUG[item]["title"])}</a></li>' for item in post['related']
    )
    article = {
        '@type': 'BlogPosting',
        'url': canonical,
        'mainEntityOfPage': {'@type': 'WebPage', '@id': canonical},
        'headline': title,
        'description': description,
        'image': [f'{SITE}{ASSETS}/{post["cover"]}.jpg'],
        'datePublished': PUBLISHED,
        'dateModified': PUBLISHED,
        'author': {'@type': 'Organization', 'name': 'SkySource', 'url': SITE + '/'},
        'publisher': {'@type': 'Organization', 'name': 'SkySource', 'url': SITE + '/'},
        'articleSection': post['category'],
        'inLanguage': 'uk-UA',
    }
    breadcrumbs = {
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i, 'name': name, 'item': SITE + url}
            for i, (name, url) in enumerate([('SkySource', '/'), ('Блог', BLOG), (title, path)], 1)
        ],
    }
    schema = {'@context': 'https://schema.org', '@graph': [article, breadcrumbs]}
    main = f"""
    <main class="wrap article-page">
        <nav class="breadcrumb" aria-label="Навігаційний шлях">
            <a href="/">Головна</a><span aria-hidden="true">/</span>
            <a href="{BLOG}">Блог SkySource</a><span aria-hidden="true">/</span>
            <span aria-current="page">{escape(post['category'])}</span>
        </nav>
        <article id="post-content" class="article-panel">
            <header class="post-header">
                <p class="eyebrow">{escape(post['category'])}</p>
                <h1>{escape(title)}</h1>
                <p class="deck">{escape(description)}</p>
                <p class="post-meta"><time datetime="{PUBLISHED}">{VISIBLE_DATE}</time> · SkySource</p>
            </header>
            {image(post['cover'], post['alt'], 'post-cover', priority=True)}
            <div class="post-copy">
{post['body'].strip()}
                {source}
            </div>
            {share_panel(title, canonical)}
            {ORDER_PANEL}
            <nav class="related" aria-label="Читайте також">
                <h2>Читайте також</h2>
                <ul>{related}</ul>
            </nav>
        </article>
    </main>"""
    metadata = head(f'{title} | SkySource', description, path, post['cover'], post['alt'], schema, is_article=True)
    return wrap_document(metadata, main, is_article=True)


def render_card(post, index):
    slug = post['slug']
    category = escape(post['category'])
    anchor = 'voda-dlia-ofisu' if slug == 'skilky-vody-zamovliaty-v-ofis' else slug
    return f"""
                <article class="card" id="{anchor}" data-slug="{slug}" data-category="{category}">
                    {image(post['cover'], '', priority=index == 0, thumbnail=True)}
                    <div class="card-body">
                        <p class="eyebrow">{category}</p>
                        <h3><a href="{permalink(slug)}" data-read>{escape(post['title'])}</a></h3>
                        <p>{escape(post['description'])}</p>
                        <span class="read-link" aria-hidden="true">Читати статтю <span>→</span></span>
                    </div>
                </article>"""


def render_blog():
    categories = dict.fromkeys(post['category'] for post in POSTS)
    filters = ''.join(
        f'<button type="button" data-category="{escape(category)}" aria-pressed="false">{escape(category)}</button>'
        for category in categories
    )
    hero_alt = 'Блакитний бутель зі склянкою води на світлій стільниці'
    schema = {
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        'name': BLOG_TITLE,
        'description': BLOG_DESCRIPTION,
        'url': SITE + BLOG,
        'inLanguage': 'uk-UA',
        'mainEntity': {
            '@type': 'ItemList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': index, 'name': post['title'], 'url': SITE + permalink(post['slug'])}
                for index, post in enumerate(POSTS, 1)
            ],
        },
    }
    cards = ''.join(render_card(post, index) for index, post in enumerate(POSTS))
    main = f"""
    <main class="wrap">
        <section class="hero" aria-labelledby="blog-title">
            <div class="hero-copy">
                <p class="eyebrow">Блог SkySource</p>
                <h1 id="blog-title">Питна вода вдома й&nbsp;в&nbsp;офісі</h1>
                <p>Як замовити доставку в Дніпрі, зберігати бутлі та доглядати за кулером.</p>
            </div>
            {image('hero', hero_alt, 'hero-visual', priority=True)}
        </section>
        <section class="catalog" aria-labelledby="articles-title">
            <h2 class="section-title" id="articles-title">Статті</h2>
            <div class="filters" role="group" aria-label="Теми статей" hidden>
                <button type="button" data-category="" aria-pressed="true">Усі</button>
                {filters}
            </div>
            <div class="card-grid">{cards}
            </div>
        </section>
        {ORDER_PANEL}
    </main>
    <dialog class="reader" id="article-reader" aria-label="Стаття блогу SkySource">
        <div class="reader-bar">
            <a class="reader-permalink" href="{BLOG}">Відкрити окремою сторінкою ↗</a>
            <form method="dialog">
                <button class="reader-close" aria-label="Закрити статтю" autofocus>×</button>
            </form>
        </div>
        <div class="reader-scroll">
            <div class="reader-note">
                <p class="reader-message" role="status"></p>
                <a href="{BLOG}" hidden>Перейти на сторінку статті</a>
            </div>
            <div class="reader-content"></div>
        </div>
    </dialog>"""
    return wrap_document(head(BLOG_TITLE, BLOG_DESCRIPTION, BLOG, 'hero', hero_alt, schema), main)


def update_sitemap():
    path = ROOT / 'sitemap.xml'
    namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', namespace)
    document = ET.parse(path)
    root = document.getroot()
    ns_tag = '{' + namespace + '}'
    for entry in list(root):
        location = entry.findtext(ns_tag + 'loc') or ''
        if location == SITE + BLOG or location.startswith(SITE + '/blog/'):
            root.remove(entry)
    for location in (BLOG, *(permalink(post['slug']) for post in POSTS)):
        url = ET.SubElement(root, ns_tag + 'url')
        ET.SubElement(url, ns_tag + 'loc').text = SITE + location
        ET.SubElement(url, ns_tag + 'lastmod').text = PUBLISHED
    ET.indent(document, space='  ')
    path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode') + '\n', encoding='utf-8')


def main():
    (ROOT / 'blog').mkdir(exist_ok=True)
    (ROOT / BLOG.lstrip('/')).write_text(render_blog(), encoding='utf-8')
    for post in POSTS:
        (ROOT / permalink(post['slug']).lstrip('/')).write_text(render_article(post), encoding='utf-8')
    update_sitemap()


if __name__ == '__main__':
    main()
