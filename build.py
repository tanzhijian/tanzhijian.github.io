from pathlib import Path
import os
import time

import marko
from jinja2 import Template


posts = Path(Path.cwd(), "posts").glob("**/*")
atom_template = Path(Path.cwd(), "atom_template.xml")
index_template = Path(Path.cwd(), "index_template.txt")
archive_template = Path(Path.cwd(), "archive_template.txt")
atom = Path(Path.cwd(), "atom.xml")
index = Path(Path.cwd(), "index.md")
archive = Path(Path.cwd(), "archive.md")


def get_summary(text: list[str]) -> str:
    for line in text:
        if line != "\n" and line[0] != "#":
            return line
    return ""


def read(post: Path) -> tuple:
    with open(post) as f:
        text = f.readlines()
    timestamp = os.path.getmtime(post)
    return text, timestamp, post.name


def convert(text: list[str], timestamp: float, name: str) -> dict:
    html = marko.convert("".join(text))
    return {
        "id": timestamp,
        "title": text[0].lstrip("# ").rstrip("\n"),
        "url": f"https://tanzhijian.org/posts/{name.rstrip('.md')}",
        "summary": get_summary(text),
        "html": html,
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(timestamp)),
    }


def export(data: list[dict], template: Path, file: Path) -> None:
    with open(template) as f:
        content = f.read()
    render = Template(content).render(entries=data)
    with open(file, "w") as f:
        f.write(render)


def main() -> None:
    data = []
    for post in posts:
        text, timestamp, name = read(post)
        data.append(convert(text, timestamp, name))

    data.sort(key=lambda x: x["id"], reverse=True)

    export(data, archive_template, archive)
    export(data[:10], index_template, index)
    export(data[:10], atom_template, atom)


if __name__ == "__main__":
    main()
