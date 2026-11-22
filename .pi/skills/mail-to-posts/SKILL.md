---
name: mail-to-posts
description: Downloads Cleveland Pen Club emails from an IMAP mailbox using ~/.mail.env, lists candidate messages from Michelle, and writes only the chosen ones as Jekyll-style posts in _posts/. Use when turning mailbox messages into site posts.
---

# Mail to Posts

Use this skill when you need to turn emails from the Cleveland Pen Club mailbox into website posts.

## Goal

Fetch emails via IMAP, identify messages from `clevelandpenclub@gmail.com`, show them for review, and — only after the user picks which ones — convert the chosen messages into Markdown posts that match the site’s existing style and write them into `_posts/`.

## Helper Script

The reusable helper lives at [scripts/mail_to_posts.py](scripts/mail_to_posts.py).

Run it like this:

```bash
python3 .pi/skills/mail-to-posts/scripts/mail_to_posts.py list
python3 .pi/skills/mail-to-posts/scripts/mail_to_posts.py write 3 5
```

- `list` shows every candidate email with an index, the post filename it would use, and any notes (`exists`, `same-date: <file>`) — it never writes anything.
- `write INDEX...` writes only the selected indices, using the same numbering `list` showed.
- Use `--dry-run` with `write` to preview without writing.
- Use `--env-file`, `--output-dir`, and `--folders` to override defaults when needed.

## Source of truth

- IMAP settings live in `~/.mail.env`
- Existing post style lives in `_posts/`
- Use the email’s sent date as the post date
- Keep the hand-written posts unless the user explicitly asks to remove or replace them

## Workflow

1. Read `~/.mail.env` and load:
   - `IMAP_HOST`
   - `IMAP_PORT`
   - `IMAP_USER`
   - `IMAP_PASSWORD`
2. Use `python3` and `imaplib` to connect securely.
   - Prefer `IMAP4_SSL` when the port is 993.
   - Otherwise connect and upgrade with `STARTTLS`.
3. Search the mailbox for messages from:
   - `clevelandpenclub@gmail.com`
4. Check only the `INBOX` folder. The `Archive` folder is intentionally NOT scanned: it holds mail that has already been handled, and pulling it in just surfaces duplicates.
5. Deduplicate messages by `Message-ID`.
6. For each message:
   - Decode the subject
   - Parse the `Date` header and use that date in the filename
   - Extract the `text/plain` body if available
   - Fall back to `text/html` only if necessary
7. Run `list` and review the candidates:
   - `[exists]` means the exact filename already exists — the post is already written
   - `[same-date: <file>]` means another post already exists for that date (often a hand-edited title) — usually means the email is already covered
   - Only pick the indices that genuinely need a post
8. Run `write INDEX...` for exactly the posts the user wants. The script will:
   - refuse to overwrite existing files
   - warn when a selected email shares a date with an existing post
   - write each new post to `_posts/` using a Jekyll-style filename such as `YYYY-MM-DD-subject-slug.md`
9. Add front matter in the same style as the existing posts:
   - `---`
   - `title: "..."`
   - `---`
10. End posts with the same comment include used elsewhere on the site:
    - `{% include cle-comments.md %}`
11. If the user asks for it, update `schedule.md` with the newest dated entry while preserving older entries. `schedule.md` should only include a minimum of details needed to know when the next meeting is, but don't strip pleasantries -- maintain the club's casual tone.

## Style guidance

- Match the site’s existing plain, friendly club-email tone
- Avoid over-formatting
- Do not invent content that was not present in the email
- Do not include personal details that the user asked to omit
- When in doubt, inspect a nearby existing post and mirror its structure

## Suggested implementation approach

A simple one-off Python script is usually enough.

Typical pattern:

```bash
python3 - <<'PY'
# read ~/.mail.env
# connect with imaplib
# fetch messages
# sanitize body text
# write files into _posts/
PY
```

## Cautions

- Treat mailbox credentials as secrets
- Do not print the password
- Do not scan the Archive folder; it only contains mail that has already been turned into posts
- Writing is opt-in: never write a post the user did not select
- Avoid overwriting hand-written posts unless the user explicitly requests it
- If a candidate post overlaps with an existing hand-written post, keep the hand-written version
