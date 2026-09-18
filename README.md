# victoriaweidenbaum.me

A static rebuild of the portfolio site, with no dependency on Squarespace.
Everything is plain HTML, CSS and images, so it can be hosted for free on
Netlify, Cloudflare Pages, GitHub Pages or any static host.

## Structure

```
index.html                  Home (intro + portfolio grid)
about/index.html            About
portfolio/<slug>/index.html Case-study pages
404.html                    Not-found page
css/style.css               All styling
images/                     All images (downloaded from the old site at full size)
videos/                     Screen recordings used in case studies
s/                          Resume PDF (same URL as before)
build.py                    Generates the HTML pages from the content inside it
```

URLs are identical to the old site (`/about`, `/portfolio/checkout`, the
resume link, and so on), so nothing that links to the site breaks.

## Editing content

All text, image references and layout positions live in `build.py`.
Edit it, then regenerate the pages:

```bash
python3 build.py
```

Styling lives in `css/style.css`.

## Previewing locally

Links are root-relative (`/about/`), so the site needs to be served rather
than opened as a file:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Deploying

The site is hosted on GitHub Pages from the public repository
`victoriaweidenbaum/victoriaweidenbaum.github.io`, served at
`victoriaweidenbaum.me` (see the `CNAME` file). To publish a change:

```bash
python3 build.py && git add -A && git commit -m "Describe the change" && git push
```

GitHub rebuilds the site in about a minute. There is no build step on
GitHub's side: it serves the files exactly as committed (`.nojekyll`).

DNS for the domain lives at Squarespace Domains: four `A` records for the
bare domain pointing at GitHub Pages, and a `CNAME` for `www` pointing at
`victoriaweidenbaum.github.io`.
