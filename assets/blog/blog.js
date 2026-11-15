document.documentElement.classList.add("js");

const reader = document.querySelector('#article-reader');

if (reader?.showModal && window.fetch) {
    const content = reader.querySelector('.reader-content');
    const scrollArea = reader.querySelector('.reader-scroll');
    const note = reader.querySelector('.reader-note');
    const message = reader.querySelector('.reader-message');
    const fullPage = reader.querySelector('.reader-permalink');
    const fallbackLink = note.querySelector('a');
    const posts = new Map([...document.querySelectorAll('.card[data-slug]')].map(card => [
        card.dataset.slug,
        card.querySelector('[data-read]').href
    ]));
    const aliases = { 'voda-dlia-ofisu': 'skilky-vody-zamovliaty-v-ofis' };
    let current = '';
    let pending;

    async function showArticle(slug) {
        const url = posts.get(slug);
        pending?.abort();
        const request = new AbortController();
        pending = request;
        current = slug;

        fullPage.href = url;
        fallbackLink.href = url;
        fallbackLink.hidden = true;
        message.textContent = 'Завантажуємо статтю…';
        note.hidden = false;
        content.replaceChildren();
        if (!reader.open) reader.showModal();
        scrollArea.scrollTop = 0;

        try {
            const response = await fetch(url, { signal: request.signal });
            if (!response.ok) throw new Error('Article unavailable');
            const articlePage = new DOMParser().parseFromString(await response.text(), 'text/html');
            const article = articlePage.querySelector('#post-content');
            if (!article || !article.querySelector('h1')) throw new Error('Article missing');
            if (request.signal.aborted) return;

            content.replaceChildren(document.importNode(article, true));
            note.hidden = true;
        } catch {
            if (request.signal.aborted) return;
            message.textContent = 'Не вдалося завантажити статтю у вікні.';
            fallbackLink.hidden = false;
        }
    }

    function syncArticle() {
        const fragment = window.location.hash.slice(1);
        const slug = aliases[fragment] || fragment;
        if (posts.has(slug)) {
            if (current !== slug || !reader.open) showArticle(slug);
        } else if (reader.open) {
            reader.close();
        }
    }

    document.addEventListener('click', event => {
        const link = event.target.closest('a[data-read]');
        if (!link || event.defaultPrevented || event.button !== 0 ||
            event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

        const slug = link.closest('.card').dataset.slug;
        history.pushState({ blogArticle: true }, '', '#' + slug);
        event.preventDefault();
        syncArticle();
    });

    reader.addEventListener('click', event => {
        if (event.target === reader) {
            const bounds = reader.getBoundingClientRect();
            if (event.clientX < bounds.left || event.clientX > bounds.right ||
                event.clientY < bounds.top || event.clientY > bounds.bottom) reader.close();
        }
    });

    reader.addEventListener('close', () => {
        if (reader.open) return;
        pending?.abort();
        current = '';
        const fragment = window.location.hash.slice(1);
        if (!posts.has(aliases[fragment] || fragment)) return;
        if (history.state?.blogArticle) history.back();
        else history.replaceState(null, '', window.location.pathname + window.location.search);
    });

    window.addEventListener('hashchange', syncArticle);
    syncArticle();
}

const filters = document.querySelector('.filters');
if (filters) {
    const buttons = [...filters.querySelectorAll('button[data-category]')];
    const cards = document.querySelectorAll('.card[data-category]');
    filters.hidden = false;
    filters.addEventListener('click', event => {
        const selected = event.target.closest('button[data-category]');
        if (!selected) return;
        buttons.forEach(button => button.setAttribute('aria-pressed', String(button === selected)));
        cards.forEach(card => {
            card.hidden = Boolean(selected.dataset.category && selected.dataset.category !== card.dataset.category);
        });
    });
}

document.addEventListener('click', async event => {
    const button = event.target.closest('button[data-copy-link]');
    if (!button) return;

    const share = button.closest('.share');
    const status = share.querySelector('.share-status');
    const input = share.querySelector('.copy-input');
    try {
        await navigator.clipboard.writeText(input.value);
        input.hidden = true;
        status.textContent = 'Посилання скопійовано.';
    } catch {
        input.hidden = false;
        input.focus();
        input.select();
        status.textContent = 'Скопіюйте виділене посилання.';
    }
});
