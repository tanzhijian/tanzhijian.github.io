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
        self.name = name
        self.timestamp = timestamp
        self.text_lines = text_lines

    @property
    def id(self) -> float:
        return self.timestamp

    @property
    def title(self) -> str:
        return self.text_lines[0].lstrip("# ").rstrip("\n")

    @property
    def url(self) -> str:
        return f"https://tanzhijian.org/posts/{self.name.split('.')[0]}"

    @property
    def summary(self) -> str:
        for line in self.text_lines:
            if line != "\n" and line[0] != "#":
                return line
        return ""

    @property
    def html(self) -> str:
        return marko.convert("".join(self.text_lines))

    @property
    def time(self) -> str:
        return time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.localtime(self.timestamp)
        )


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
    atom_path = Path(Path.cwd(), "atom.xml")
    index_template = Path(Path.cwd(), "index_template.txt")
    index_path = Path(Path.cwd(), "index.md")
    archive_template = Path(Path.cwd(), "archive_template.txt")
    archive_path = Path(Path.cwd(), "archive.md")

    posts = [read(path) for path in post_paths]
    posts.sort(key=lambda post: post.id, reverse=True)
    posts_10 = posts[:10]

    export(posts, archive_template, archive_path)
    export(posts_10, index_template, index_path)
    export(posts_10, atom_template, atom_path)


if __name__ == "__main__":
    main()
