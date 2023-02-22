from pathlib import Path
import os.path
import time

import markdown
from jinja2 import Template


path_list = Path(Path.cwd(), "posts").glob("**/*")
template = Path(Path.cwd(), "template.xml")
feed = Path(Path.cwd(), "atom.xml")


def read(path):
    with open(path) as f:
        text = f.read()
    timestamp = os.path.getmtime(path)
    return text, timestamp


def convert(md, timestamp):
    html = markdown.markdown(md)
    return {
        'id': timestamp,
        "html": html,
        'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
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
        md, timestamp = read(path)
        data.append(convert(md, timestamp))

    # 这里排序，且只生成十篇文章
    data = sorted(data, key=lambda x: x['id'], reverse=True)[:10]

    export(data, template, feed)


if __name__ == "__main__":
    main()
