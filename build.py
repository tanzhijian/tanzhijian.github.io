from pathlib import Path
import time

import marko
from jinja2 import Template


class Post:
    def __init__(
        self,
        name: str,
        timestamp: float,
        text_lines: list[str],
    ) -> None:
        self.id = timestamp
        self.title = text_lines[0].lstrip("# ").rstrip("\n")
        self.url = f"https://tanzhijian.org/posts/{name.split('.')[0]}"
        self.summary = self._get_summary(text_lines)
        self.html = marko.convert("".join(text_lines))
        self.time = time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.localtime(timestamp)
        )

    def _get_summary(self, text_lines: list[str]) -> str:
        for line in text_lines:
            if line != "\n" and line[0] != "#":
                return marko.convert(line)
        return ""


def read(path: Path) -> Post:
    with open(path) as f:
        text_lines = f.readlines()
    timestamp = path.stat().st_mtime
    return Post(path.name, timestamp, text_lines)


def export(posts: list[Post], template_path: Path, export_path: Path) -> None:
    with open(template_path) as f:
        template = f.read()
    render = Template(template).render(posts=posts)
    with open(export_path, "w") as f:
        f.write(render)


def main() -> None:
    post_paths = Path(Path.cwd(), "posts").glob("**/*")
    atom_template = Path(Path.cwd(), "atom_template.xml")
    index_template = Path(Path.cwd(), "index_template.txt")
    archive_template = Path(Path.cwd(), "archive_template.txt")
    atom_path = Path(Path.cwd(), "atom.xml")
    index_path = Path(Path.cwd(), "index.md")
    archive_path = Path(Path.cwd(), "archive.md")

    posts = [read(path) for path in post_paths]
    posts.sort(key=lambda post: post.id, reverse=True)
    posts_10 = posts[:10]

    export(posts, archive_template, archive_path)
    export(posts_10, index_template, index_path)
    export(posts_10, atom_template, atom_path)


if __name__ == "__main__":
    main()
