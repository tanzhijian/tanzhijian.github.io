from pathlib import Path
import os.path
import time

import markdown
from jinja2 import Template


path_list = Path(Path.cwd(), "posts").glob("**/*")
template = Path(Path.cwd(), "template.xml")
feed = Path(Path.cwd(), "atom.xml")


def get_summary(text_list):
    for text in text_list:
        if text != '\n' and text[0] != '#':
            return text
    return ''


def read(path):
    with open(path) as f:
        text_list = f.readlines()
    timestamp = os.path.getmtime(path)
    return text_list, timestamp, path.name


def convert(md_list, timestamp, name):
    html = markdown.markdown(''.join(md_list))
    return {
        "id": timestamp,
        "title": md_list[0].lstrip('# ').rstrip('\n'),
        "url": f'https://tanzhijian.org/posts/{name}'.rstrip('.md'),
        'summary': get_summary(md_list),
        "html": html,
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)),
    }


def export(data, template, feed):
    with open(template) as f:
        template = f.read()
    atom = Template(template).render(entries=data)
    with open(feed, "w") as f:
        f.write(atom)


def main():
    data = []
    for path in path_list:
        md_list, timestamp, name = read(path)
        data.append(convert(md_list, timestamp, name))

    # 这里排序，且只生成十篇文章
    data = sorted(data, key=lambda x: x["id"], reverse=True)[:10]

    export(data, template, feed)


if __name__ == "__main__":
    main()
