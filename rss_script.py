from pathlib import Path
import os.path
import time

import markdown
from jinja2 import Template


path_list = Path(Path.cwd(), "posts").glob("**/*")
atom_template = Path(Path.cwd(), "atom_template.xml")
index_template = Path(Path.cwd(), 'index_templete.txt')
atom = Path(Path.cwd(), "atom.xml")
index = Path(Path.cwd(), "index.md")


def get_summary(text_list):
    for text in text_list:
        if text != "\n" and text[0] != "#":
            return text
    return ""


def read(path):
    with open(path) as f:
        text_list = f.readlines()
    timestamp = os.path.getmtime(path)
    return text_list, timestamp, path.name


def convert(md_list, timestamp, name):
    html = markdown.markdown("".join(md_list))
    return {
        "id": timestamp,
        "title": md_list[0].lstrip("# ").rstrip("\n"),
        "url": f"https://tanzhijian.org/posts/{name}".rstrip(".md"),
        "summary": get_summary(md_list),
        "html": html,
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(timestamp)),
    }


def export(data, template, file):
    with open(template) as f:
        template = f.read()
    render = Template(template).render(entries=data)
    with open(file, "w") as f:
        f.write(render)


def main():
    data = []
    for path in path_list:
        md_list, timestamp, name = read(path)
        data.append(convert(md_list, timestamp, name))
    # 排序
    data = sorted(data, key=lambda x: x["id"], reverse=True)

    export(data, index_template, index)
    export(data, atom_template, atom)


if __name__ == "__main__":
    main()
