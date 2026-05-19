#!/usr/bin/env python3
"""
Fix RU articles missing :page/body marker.
For each broken RU file:
  1. Find the matching EN file
  2. Extract structural frontmatter from EN (tags, category, type, hero-image)
  3. Find the actual body start in the RU file (first line starting with #)
  4. Extract Russian title from that heading
  5. Reconstruct proper EDN frontmatter + body
"""

import os
import re
import sys
import glob

CONTENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RU_DIR = os.path.join(CONTENT_DIR, "articles", "ru")
EN_DIR = os.path.join(CONTENT_DIR, "articles", "en")

def slug_from_filename(fname):
    name = os.path.basename(fname)
    name = re.sub(r'^\d{8}--', '', name)
    name = re.sub(r'__[^.]+\.md$', '', name)
    name = re.sub(r'\.md$', '', name)
    return name

def find_en_file(slug):
    pattern = os.path.join(EN_DIR, f"*--{slug}__*.md")
    matches = glob.glob(pattern)
    if matches:
        return matches[0]
    # fallback: exact match
    pattern2 = os.path.join(EN_DIR, f"{slug}.md")
    matches2 = glob.glob(pattern2)
    return matches2[0] if matches2 else None

def parse_en_frontmatter(path):
    """Extract raw frontmatter fields from EN file (everything before :page/body)."""
    with open(path) as f:
        content = f.read()
    if ':page/body' not in content:
        return {}
    header = content.split(':page/body')[0]
    fields = {}
    # Extract individual fields via regex
    for m in re.finditer(r':article/tags\s+(\[.*?\])', header, re.DOTALL):
        fields['tags'] = m.group(1)
    for m in re.finditer(r':article/category\s+(\S+)', header):
        fields['category'] = m.group(1)
    for m in re.finditer(r':article/type\s+(\S+)', header):
        fields['type'] = m.group(1)
    for m in re.finditer(r':article/product-filter\s+(\{[^}]+\})', header):
        fields['product_filter'] = m.group(1)
    for m in re.finditer(r':article/hero-image\s+"([^"]+)"', header):
        fields['hero_image'] = m.group(1)
    for m in re.finditer(r':article/product-ids\s+(\[.*?\])', header, re.DOTALL):
        fields['product_ids'] = m.group(1)
    return fields

def find_body_start(lines):
    """Return index of first line starting with # (actual article body)."""
    for i, line in enumerate(lines):
        if line.startswith('# '):
            return i
    # fallback: first non-empty line
    for i, line in enumerate(lines):
        if line.strip():
            return i
    return 0

def extract_ru_title(lines, body_start):
    """Extract title text from first # heading."""
    for line in lines[body_start:]:
        if line.startswith('# '):
            return line[2:].strip()
    return None

def build_frontmatter(ru_title, en_fields):
    lines = [':page/lang :ru']
    if ru_title:
        # Escape quotes in title
        escaped = ru_title.replace('"', '\\"')
        lines.append(f':article/title "{escaped}"')
    if 'tags' in en_fields:
        lines.append(f':article/tags {en_fields["tags"]}')
    if 'category' in en_fields:
        lines.append(f':article/category {en_fields["category"]}')
    if 'type' in en_fields:
        lines.append(f':article/type {en_fields["type"]}')
    if 'product_filter' in en_fields:
        lines.append(f':article/product-filter {en_fields["product_filter"]}')
    if 'product_ids' in en_fields:
        lines.append(f':article/product-ids {en_fields["product_ids"]}')
    if 'hero_image' in en_fields:
        lines.append(f':article/hero-image "{en_fields["hero_image"]}"')
    lines.append(':page/body')
    return '\n'.join(lines) + '\n'

def header_is_clean(content):
    """Return True if file already has a clean :page/lang :ru frontmatter."""
    return content.startswith(':page/lang :ru')

def fix_ru_file(ru_path, dry_run=False):
    slug = slug_from_filename(ru_path)
    with open(ru_path) as f:
        content = f.read()

    if ':page/body' in content and header_is_clean(content):
        return 'SKIP', 'already clean'

    en_path = find_en_file(slug)
    if not en_path:
        return 'WARN', f'no EN file found for slug: {slug}'

    en_fields = parse_en_frontmatter(en_path)

    # Find actual body: everything from the first # heading onwards
    if ':page/body' in content:
        body_raw = content.split(':page/body', 1)[1]
    else:
        body_raw = content
    body_lines = body_raw.splitlines()
    body_start = find_body_start(body_lines)
    ru_title = extract_ru_title(body_lines, body_start)
    body_lines = body_lines[body_start:]

    frontmatter = build_frontmatter(ru_title, en_fields)
    new_content = frontmatter + '\n' + '\n'.join(body_lines)

    if not dry_run:
        with open(ru_path, 'w') as f:
            f.write(new_content)

    action = 'FIXED' if ':page/body' not in content else 'FIXED-HEADER'
    return action, f'title: {ru_title}'

def main():
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        print("DRY RUN — no files will be written\n")

    ru_files = sorted(glob.glob(os.path.join(RU_DIR, "*.md")))
    fixed = skipped = warned = 0

    for ru_path in ru_files:
        slug = slug_from_filename(ru_path)
        status, msg = fix_ru_file(ru_path, dry_run=dry_run)
        if status in ('FIXED', 'FIXED-HEADER'):
            fixed += 1
            label = status
            print(f"[{label}] {slug}: {msg}")
        elif status == 'WARN':
            warned += 1
            print(f"[WARN]  {slug}: {msg}")
        # skip SKIP ones silently

    print(f"\nDone: {fixed} fixed, {warned} warnings, skipped already-ok files.")

if __name__ == '__main__':
    main()
