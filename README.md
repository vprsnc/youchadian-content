# youchadian-content

Wiki articles, blog posts and photos for 又一家茶店. Nothing is hosted: the
app in `../youchadian-next` reads this directory at runtime (`CONTENT_DIR`,
default `../youchadian-content`). There is no import step: a saved file shows
on the next page load.

## Layout

```
articles/{locale}/{YYYYMMDD}--{slug}__{category}_{type}.md   ← wiki
blog/{locale}/{YYYYMMDD}--{slug}.md                          ← blog
images/{wiki,blog,products}/<slug>/<file>                    ← photos
```

Locales: `en/` `ru/` `bg/`, one file per locale. RU is written first and EN/BG
are derived from it. The date in the filename is the publication date, and the
slug is the URL slug (untoned pinyin, e.g. `rougui`). A blog post's RU file
uses the EN slug.

## Frontmatter

EDN pairs, then `:page/body` on its own line, then markdown.

```
:page/lang :en
:article/title "Ròuguì (肉桂) — Cinnamon Rock Oolong"
:article/tags ["oolong" "wuyi"]
:article/category :tea
:article/type :oolong-dark
:article/description "SEO one-liner"
:article/hero-image "01-hero.jpg"
:page/body

# Ròuguì (肉桂) — Cinnamon Rock Oolong
```

Blog: `:blogpost/title`, `:blogpost/tags`, optional `:blogpost/hero-image`,
then `:page/body`.

## Images: relative file names, never URLs

Photos are files, one folder per slug:

```
images/wiki/rougui/01-hero.jpg
images/wiki/rougui/02-leaves.jpg
```

Markdown refers to them by file name, relative to that folder, so editor
previews show the real photo:

```
:article/hero-image "01-hero.jpg"

![Dry ròuguì leaves, long dark twisted strips](02-leaves.jpg)
```

- **Same file name in every locale.** Only the alt text is translated, so one
  photo serves RU, EN and BG.
- **Order:** file name order is display order. If `:article/hero-image` /
  `:blogpost/hero-image` is left out, the first file is the hero. Number files
  `01-…`, `02-…` to control that.
- **Alt text** describes what the photo shows, in the file's language.
- **Formats:** jpg, jpeg, png, webp — other files in the folder (heic, tif…)
  are ignored; convert them first. The app converts to
  WebP at 400/800/1600 on request, caches the result, and serves the right size
  per screen.
- **Product photos** go in `images/products/<slug>/`, normally via the upload on
  the admin product page.
- **`images/` is gitignored** — photos are not in this repo's history.

A file name that isn't in the folder logs a warning; in dev the page shows a
dashed "missing image" box, which is fine for drafts.

### Older content

`img:<stem>` refs (from the retired Yandex Disk sync) still resolve, matched by
file stem, and plain `https://…` URLs pass through unchanged — no need to
migrate them. New content uses plain file names.
