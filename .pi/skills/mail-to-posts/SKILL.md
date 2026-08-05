---
name: mail-to-posts
description: Downloads Cleveland Pen Club emails from an IMAP mailbox using ~/.mail.env, converts messages from Michelle into Jekyll-style posts in _posts/, and optionally updates schedule.md. Use when turning mailbox messages into site posts.
---

# Mail to Posts

Use this skill when you need to turn emails from the Cleveland Pen Club mailbox into website posts.

## Goal

Fetch emails via IMAP, identify messages from `clevelandpenclub@gmail.com`, convert the content into Markdown posts that match the site’s existing style, and write them into `_posts/`.

## Helper Script

The reusable helper lives at [scripts/mail_to_posts.py](scripts/mail_to_posts.py).

Run it like this:

```bash
python3 .pi/skills/mail-to-posts/scripts/mail_to_posts.py --dry-run
python3 .pi/skills/mail-to-posts/scripts/mail_to_posts.py
```

Use `--env-file`, `--output-dir`, and `--folders` to override defaults when needed.

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
4. Check the folders that usually contain relevant mail:
   - `INBOX`
   - `Archive`
5. Deduplicate messages by `Message-ID`.
6. For each message:
   - Decode the subject
   - Parse the `Date` header and use that date in the filename
   - Extract the `text/plain` body if available
   - Fall back to `text/html` only if necessary
7. Clean the text so the generated post matches the site style:
   - Remove Michelle’s last name
   - Remove Michelle’s phone number
   - Remove Michelle’s email address
   - Strip signature blocks and separator lines
   - Preserve the email’s content and paragraph breaks
   - Keep links readable in Markdown when possible
8. Write each post to `_posts/` using a Jekyll-style filename such as:
   - `YYYY-MM-DD-subject-slug.md`
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
- Avoid overwriting hand-written posts unless the user explicitly requests it
- If a candidate post overlaps with an existing hand-written post, keep the hand-written version
