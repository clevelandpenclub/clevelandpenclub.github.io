#!/usr/bin/env python3
"""Download Cleveland Pen Club emails from IMAP and convert them into posts.

This script reads IMAP settings from ~/.mail.env, fetches messages from
clevelandpenclub@gmail.com in INBOX and Archive, and writes Jekyll-style
Markdown posts into _posts/.

It is intentionally conservative:
- it skips messages whose output file already exists
- it strips Michelle's surname, phone number, and email address
- it keeps the hand-written site posts untouched
"""

from __future__ import annotations

import argparse
import email
import imaplib
import os
import re
import ssl
from dataclasses import dataclass
from datetime import datetime
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

EMAIL_FROM = "clevelandpenclub@gmail.com"
DEFAULT_FOLDERS = ["INBOX", "Archive"]
DEFAULT_OUTPUT_DIR = Path("_posts")
DEFAULT_ENV_FILE = Path.home() / ".mail.env"


class _HTMLStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in {"br", "p", "div", "li", "tr"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"p", "div", "li", "tr"}:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)

    def text(self) -> str:
        return unescape("".join(self.parts))


@dataclass
class MailConfig:
    host: str
    port: int
    user: str
    password: str


@dataclass
class PostDraft:
    subject: str
    date: datetime
    body: str
    message_id: str
    filename: str
    content: str


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_config(path: Path = DEFAULT_ENV_FILE) -> MailConfig:
    values = load_env_file(path)
    missing = [k for k in ("IMAP_HOST", "IMAP_PORT", "IMAP_USER", "IMAP_PASSWORD") if k not in values]
    if missing:
        raise SystemExit(f"Missing required settings in {path}: {', '.join(missing)}")
    return MailConfig(
        host=values["IMAP_HOST"],
        port=int(values["IMAP_PORT"]),
        user=values["IMAP_USER"],
        password=values["IMAP_PASSWORD"],
    )


def connect_imap(cfg: MailConfig):
    if cfg.port == 993:
        mail = imaplib.IMAP4_SSL(cfg.host, cfg.port)
    else:
        mail = imaplib.IMAP4(cfg.host, cfg.port)
        mail.starttls(ssl.create_default_context())
    mail.login(cfg.user, cfg.password)
    return mail


def decode_subject(msg: email.message.Message) -> str:
    return str(make_header(decode_header(msg.get("Subject", "")))).strip()


def parse_date(msg: email.message.Message) -> datetime:
    raw = msg.get("Date")
    if not raw:
        raise ValueError("Message has no Date header")
    return parsedate_to_datetime(raw)


def slugify(text: str) -> str:
    text = text.replace("Fwd: ", "Fwd ").replace("FW: ", "FW ")
    text = re.sub(r"[^A-Za-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-") or "post"


def extract_text(msg: email.message.Message) -> str:
    if msg.is_multipart():
        plain = None
        html_part = None
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = (part.get_content_disposition() or "").lower()
            if disp == "attachment":
                continue
            if ctype == "text/plain" and plain is None:
                payload = part.get_payload(decode=True) or b""
                plain = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
            elif ctype == "text/html" and html_part is None:
                payload = part.get_payload(decode=True) or b""
                html_part = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
        if plain is not None:
            return plain
        if html_part is not None:
            stripper = _HTMLStripper()
            stripper.feed(html_part)
            return stripper.text()
        return ""

    payload = msg.get_payload(decode=True) or b""
    return payload.decode(msg.get_content_charset() or "utf-8", errors="replace")


def normalize_body(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"<mailto:([^>]+)>", r"\1", text)
    text = re.sub(r"<(https?://[^>]+)>", r"\1", text)
    text = re.sub(r"\bMichelle\s+[A-Z][A-Za-z'\-]*\b", "Michelle", text)
    text = text.replace("*", "")
    text = re.sub(r"\*~\s*This is no illness - it is medicine\. ~\*", "", text)

    lines = text.splitlines()
    out: list[str] = []
    blank = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not blank:
                out.append("")
                blank = True
            continue

        # End the body when we hit a signature marker.
        if re.match(r"^(Warmly,\s*)?your Cleveland pen friend,?$", stripped, flags=re.I):
            break
        if re.match(r"^Your Cleveland Pen Club friend,?$", stripped, flags=re.I):
            break
        if re.match(r"^Michelle\.?$", stripped, flags=re.I):
            break
        if re.match(r"^--\s*$", stripped):
            break

        # Remove obvious personal details.
        stripped = re.sub(r"\(?\d{3}\)?[\s.-]*\d{3}[\s.-]*\d{4}", "", stripped)
        stripped = re.sub(r"clevelandpenclub@clevelandpen\.club", "", stripped, flags=re.I)
        stripped = re.sub(r"\bMichelle\s+[A-Z][A-Za-z'\-]*\b", "Michelle", stripped, flags=re.I)

        # Collapse whitespace that may have been left after removal.
        stripped = re.sub(r"\s{2,}", " ", stripped).strip()
        if not stripped:
            continue

        # Keep raw URLs readable.
        stripped = re.sub(
            r"(?<!\()\b([A-Za-z0-9][A-Za-z0-9./&_-]*?)\s+(https?://[^\s]+)",
            r"[\1](\2)",
            stripped,
        )

        out.append(stripped)
        blank = False

    body = "\n".join(out).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body


def format_post(subject: str, date: datetime, body: str) -> tuple[str, str]:
    filename = f"{date:%Y-%m-%d}-{slugify(subject)}.md"
    content = (
        "---\n"
        f'title: "{subject.replace("\"", r"\\\"")}"\n'
        "---\n\n"
        f"{body}\n\n"
        "--Michelle\n\n"
        "{% include cle-comments.md %}\n"
    )
    return filename, content


def collect_messages(mail, folders: Iterable[str]) -> list[PostDraft]:
    drafts: list[PostDraft] = []
    seen_ids: set[str] = set()

    for folder in folders:
        typ, _ = mail.select(folder, readonly=True)
        if typ != "OK":
            continue
        typ, data = mail.search(None, "FROM", EMAIL_FROM)
        if typ != "OK" or not data or not data[0]:
            continue

        for msgid in data[0].split():
            typ, raw = mail.fetch(msgid, "(RFC822)")
            if typ != "OK" or not raw or not raw[0]:
                continue

            msg = email.message_from_bytes(raw[0][1])
            message_id = (msg.get("Message-ID") or f"{folder}:{msgid.decode()}").strip()
            if message_id in seen_ids:
                continue
            seen_ids.add(message_id)

            subject = decode_subject(msg)
            date = parse_date(msg)
            body = normalize_body(extract_text(msg))
            filename, content = format_post(subject, date, body)
            drafts.append(
                PostDraft(
                    subject=subject,
                    date=date,
                    body=body,
                    message_id=message_id,
                    filename=filename,
                    content=content,
                )
            )

    drafts.sort(key=lambda draft: draft.date)
    return drafts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE, help="Path to .mail.env")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Where to write posts")
    parser.add_argument("--folders", nargs="*", default=DEFAULT_FOLDERS, help="IMAP folders to scan")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be written without writing files")
    args = parser.parse_args()

    cfg = load_config(args.env_file)
    mail = connect_imap(cfg)
    try:
        drafts = collect_messages(mail, args.folders)
    finally:
        try:
            mail.logout()
        except Exception:
            pass

    args.output_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    for draft in drafts:
        path = args.output_dir / draft.filename
        if path.exists():
            print(f"skip {path} (already exists)")
            skipped += 1
            continue
        if args.dry_run:
            print(f"dry-run {path}")
            continue
        path.write_text(draft.content, encoding="utf-8")
        print(f"write {path}")
        written += 1

    print(f"done: {written} written, {skipped} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
