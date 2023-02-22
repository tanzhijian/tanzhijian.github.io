from pathlib import Path

import markdown
from jinja2 import Template


path_list = Path(Path.cwd(), "posts").glob("**/*")
template = Path(Path.cwd(), "template.xml")
feed = Path(Path.cwd(), "atom.xml")


def read(path):
    with open(path) as f:
        text = f.read()
    return text


def convert(md):
    html = markdown.markdown(md)
    return {
        "html": html,
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
        md = read(path)
        data.append(convert(md))
    export(data, template, feed)


if __name__ == "__main__":
    main()
