#!/usr/bin/env python3
"""갤러리 README 생성기

photos/<N>-devs/ 폴더의 사진을 읽어 README.md 의 GALLERY 구간을 다시 씁니다.

  python3 scripts/build_readme.py           README 갱신
  python3 scripts/build_readme.py --check   사진 파일 검사만 (PR용)

사진 설명은 같은 이름의 .txt 파일 첫 줄에 적습니다.
  photos/6-devs/2026-10-15-crew.webp
  photos/6-devs/2026-10-15-crew.txt   ← "첫 단체 사진"
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "photos"
README = ROOT / "README.md"
START, END = "<!-- GALLERY:START -->", "<!-- GALLERY:END -->"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_BYTES = 5 * 1024 * 1024
GROUP_RE = re.compile(r"^(\d+)-devs$")
NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9][a-z0-9-]*)$")


def groups() -> list[tuple[int, Path]]:
    found = []
    for d in PHOTOS.iterdir() if PHOTOS.is_dir() else []:
        m = GROUP_RE.match(d.name)
        if d.is_dir() and m:
            found.append((int(m.group(1)), d))
    return sorted(found)


def photos_in(folder: Path) -> list[Path]:
    return sorted((p for p in folder.iterdir() if p.suffix.lower() in EXTS), key=lambda p: p.name, reverse=True)


def caption(photo: Path) -> tuple[str, str]:
    m = NAME_RE.match(photo.stem)
    date, slug = (m.group(1), m.group(2)) if m else ("", photo.stem)
    txt = photo.with_suffix(".txt")
    if txt.exists():
        first = txt.read_text(encoding="utf-8").strip().splitlines()
        if first and first[0].strip():
            return first[0].strip(), date
    return slug.replace("-", " "), date


def check() -> list[str]:
    errors = []
    if not PHOTOS.is_dir():
        return ["photos/ 폴더가 없습니다."]
    for d in PHOTOS.iterdir():
        if d.name.startswith("."):
            continue
        if not d.is_dir() or not GROUP_RE.match(d.name):
            errors.append(f"photos/{d.name}: photos/ 안에는 4-devs, 6-devs 처럼 '<인원수>-devs' 폴더만 둡니다.")
            continue
        for p in d.iterdir():
            rel = p.relative_to(ROOT)
            if p.name.startswith("."):
                continue
            if p.suffix.lower() == ".txt":
                if not any(p.with_suffix(e).exists() or p.with_suffix(e.upper()).exists() for e in EXTS):
                    errors.append(f"{rel}: 짝이 되는 사진 파일이 없습니다.")
                continue
            if p.suffix.lower() not in EXTS:
                errors.append(f"{rel}: 사진은 {', '.join(sorted(EXTS))} 만 됩니다.")
                continue
            if not NAME_RE.match(p.stem):
                errors.append(f"{rel}: 파일 이름은 'YYYY-MM-DD-영문-설명' 형식으로 지어 주세요 (예: 2026-10-15-crew.webp).")
            if p.stat().st_size > MAX_BYTES:
                errors.append(f"{rel}: {p.stat().st_size / 1048576:.1f}MB — 5MB 이하로 줄여 주세요.")
    return errors


def cell(photo: Path, width: str) -> str:
    cap, date = caption(photo)
    src = photo.relative_to(ROOT).as_posix()
    alt = html.escape(cap, quote=True)
    sub = html.escape(cap) + (f" · {date}" if date else "")
    return (f'<a href="{src}"><img src="{src}" width="{width}" alt="{alt}"></a><br>'
            f"<sub>{sub}</sub>")


def render() -> str:
    out = []
    found = [(n, d, photos_in(d)) for n, d in groups()]
    nav = " · ".join(f'<a href="#-{n}인-사진">{n}인 사진 ({len(ps)})</a>' for n, _, ps in found)
    if nav:
        out += [f"<p align=\"center\">{nav}</p>", ""]
    for n, _, ps in found:
        out += [f"## 👥 {n}인 사진", ""]
        if not ps:
            out += ["_아직 사진이 없습니다. 첫 사진을 올려 주세요!_", ""]
            continue
        latest, older = ps[0], ps[1:]
        out += ['<p align="center">', cell(latest, "100%"), "</p>", ""]
        if older:
            cols = 2 if n <= 4 else 3
            width = f"{100 // cols}%"
            out.append("<table>")
            for i in range(0, len(older), cols):
                row = older[i:i + cols]
                tds = "".join(f'<td align="center" width="{width}">{cell(p, "100%")}</td>' for p in row)
                out.append(f"<tr>{tds}</tr>")
            out += ["</table>", ""]
    return "\n".join(out).rstrip() + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="사진 파일만 검사")
    args = ap.parse_args(argv)

    errors = check()
    for e in errors:
        print(f"오류: {e}")
    if args.check:
        print("사진 검사 통과" if not errors else f"{len(errors)}개 오류")
        return 1 if errors else 0
    if errors:
        return 1

    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print(f"README.md 에 {START} / {END} 표시가 없습니다.")
        return 1
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    new = f"{head}{START}\n{render()}{END}{tail}"
    if new != text:
        README.write_text(new, encoding="utf-8")
        print("README.md 갱신")
    else:
        print("README.md 그대로")
    return 0


if __name__ == "__main__":
    sys.exit(main())
