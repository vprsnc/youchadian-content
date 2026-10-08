# youchadian-content

Wiki articles and blog posts for 又一家茶店. Pushing to `master` triggers the
main repo's `sync-content.yml`, which copies `articles/` and `blog/` into the app
and runs the importers. Nothing else in this repo reaches the site, except
`infographics/`, which is uploaded separately.

## Layout

```
articles/{locale}/{YYYYMMDD}--{slug}__{category}_{type}.md   ← wiki
blog/{locale}/{YYYYMMDD}--{slug}.md                          ← blog
```

Locales: `en/` `ru/` `bg/`, one file per locale. RU is written first and EN/BG
are derived from it. The date in the filename is the publication date, and the
slug is the URL slug (untoned pinyin, e.g. `rougui`).

## Frontmatter

EDN pairs, then `:page/body` on its own line, then markdown.

```
:page/lang :en
:article/title "Ròuguì (肉桂) — Cinnamon Rock Oolong"
:article/tags ["oolong" "wuyi"]
:article/category :tea
:article/type :oolong-dark
:article/description "SEO one-liner"
:article/hero-image "img:01-hero"
:page/body

# Ròuguì (肉桂) — Cinnamon Rock Oolong
```

Blog: `:blogpost/title`, `:blogpost/tags`, optional `:blogpost/hero-image`,
then `:page/body`.

## Images: `img:` names, never URLs

Photos live on Yandex Disk, one folder per slug:

```
disk:/content-images/<slug>/01-hero.jpg
disk:/content-images/<slug>/02-leaves.heic
```

Markdown refers to them by file name without the extension:

```
:article/hero-image "img:01-hero"

![Dry ròuguì leaves, long dark twisted strips](img:02-leaves)
```

- **Same `img:` name in every locale.** Only the alt text is translated, so one
  photo serves RU, EN and BG.
- **Hero:** if `:article/hero-image` / `:blogpost/hero-image` is left out, the
  first file by name is used. Number files `01-…`, `02-…` to control that.
- **Alt text** describes what the photo shows, in the file's language.
- **Formats:** jpg, png, webp, heic, tif, avif. The server converts to WebP at
  400/800/1600 and serves the right size per screen.

### Publishing photos

1. New slug? On `/admin/content-images`, click **Create missing folders**. The
   slug must already be imported, so push the article first.
2. Drop photos into the folder from the Disk app or web.
3. On `/admin/content-images`, click **Sync now** (all slugs or one).

Photos show up on the next page load, with no content push needed: refs are
resolved when the page renders. Re-shooting a photo under the same file name
updates it in every locale at once. Re-syncing an unchanged photo costs
nothing, and an empty folder never removes photos that were already published.

### What happens when a photo is missing

- The import still succeeds but prints
  `WARN <slug>: not synced — img:02-leaves`. This is fine for drafts.
- On the live site the image is left out. In local dev it shows a dashed
  "missing image" box.

### Older content

Plain `https://…` image URLs still work unchanged, so there is no need to
migrate them. New content should use `img:`. The local `bb push-images` /
`bb sync-images` tasks (which wrote S3 URLs into the markdown) are superseded.
