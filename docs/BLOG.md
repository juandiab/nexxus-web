# Blog management guide

Articles are stored in **`backend/data/blog_posts.json`**. The site reads them through the API; you do **not** need to rebuild the frontend when you add or edit posts. Restart is only needed if you change backend code.

## Quick start: new article

### Option A — Script (recommended)

```bash
python3 scripts/new-blog-post.py \
  --title "Your Article Title" \
  --category "WAF & Security" \
  --content-file path/to/draft.md
```

Then edit the generated entry in `backend/data/blog_posts.json` if needed (excerpt, tags, `featured`). On the server, pull or copy the updated JSON and restart the backend:

```bash
docker compose restart backend
```

### Option B — Copy the template

1. Copy `backend/data/blog_post.template.json`.
2. Paste a new object into the **array** in `blog_posts.json` (comma after the previous post).
3. Fill in all fields (see below).
4. Restart backend on the server: `docker compose restart backend`.

---

## Post fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique string, e.g. `"5"`. Use next number after existing posts. |
| `slug` | Yes | URL path: `/blog/your-slug-here`. Lowercase, hyphens only. Must be unique. |
| `title` | Yes | Headline on the card and article page. |
| `excerpt` | Yes | 1–2 sentences for the blog listing card (plain text). |
| `content` | Yes | Full article in **Markdown** (see style guide below). |
| `category` | Yes | One of: `WAF & Security`, `Zero-Trust`, `AI & Automation`, `Cloud Security` (or add a new one — it will appear in filters). |
| `tags` | Yes | Array of strings, e.g. `["NetScaler", "WAF"]`. |
| `author` | Yes | Display name. |
| `author_role` | Yes | Subtitle under author name. |
| `date` | Yes | ISO date `YYYY-MM-DD` (controls sort order). |
| `read_time` | Yes | Minutes to read (script estimates ~200 words/min). |
| `featured` | Yes | `true` shows on home page; max 2–3 featured recommended. |
| `cover_color` | Yes | Card/hero background. Use brand colors below. |

### Brand cover colors

| Color | Hex | Use for |
|-------|-----|---------|
| Cerulean | `#007BA7` | Default / security |
| Light cerulean | `#00A8E0` | Cloud, identity |
| Dark cerulean | `#005F7F` | Deep technical |
| Dark grey | `#38383D` | Architecture, multicloud |
| Accent blue | `#4DB8E0` | AI, automation |

---

## Markdown style guide

Write in standard Markdown. The site renders it with the same typography as existing posts (headings, lists, code, links).

### Structure (match existing articles)

```markdown
# Article Title (same as JSON title)

Opening paragraph — context and why it matters.

## First major section

Body text...

### Subsection

- Bullet point
- Another point

## Code example

\`\`\`
add appfw profile PROD_WAF -type HTML
\`\`\`

## Conclusion

Short wrap-up.

*Optional CTA: [Contact us](/contact) for a consultation.*
```

### Supported formatting

- `#` `##` `###` — headings (use one `#` title at top; avoid multiple `#` h1s in body)
- `**bold**` and `*italic*`
- `- item` — bullet lists
- `` `inline code` ``
- ` ``` ` fenced code blocks (optional language label)
- `[link text](/contact)` or `[text](https://...)`
- Blank line between paragraphs

### Tips for consistent look

1. **Excerpt** is not Markdown — write plain text for cards.
2. **Slug** must match the topic and stay stable (changing slug breaks old links).
3. Use **2–4 tags** aligned with categories.
4. End with a soft CTA linking to `/contact` like other posts.
5. Keep code blocks under ~20 lines when possible; use fenced blocks for CLI/config.

---

## Workflow on production server

```bash
cd /path/to/nexxus-web
git pull origin main          # if you committed posts in git
# OR edit backend/data/blog_posts.json directly on the server

docker compose restart backend
```

Verify:

- Listing: https://nexxus-tech.com/blog  
- Article: https://nexxus-tech.com/blog/your-slug  

---

## Optional: write in a `.md` file first

1. Draft in `backend/data/drafts/my-article.md` (drafts are not served; folder is for your convenience).
2. Run `new-blog-post.py --content-file backend/data/drafts/my-article.md`.
3. Review the JSON entry, commit, deploy.

---

## Future options

If you outgrow JSON editing, common upgrades are:

- **Headless CMS** (Sanity, Contentful) — visual editor, API to frontend  
- **Admin UI** — protected `/admin` to create posts  
- **One file per post** — `backend/data/posts/*.json` for easier Git diffs  

For now, JSON + template + script keeps styling identical to current posts with minimal infrastructure.
