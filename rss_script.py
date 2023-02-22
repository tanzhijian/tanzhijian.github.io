from pathlib import Path

import markdown


path_list = Path(Path.cwd(), 'posts').glob('**/*')


def read(path):
    with open(path) as f:
        md = f.read()
    return md

def convert(md):
    html = markdown.markdown(md)
    return {
        'html': html,
    }


def export(data):
    pass


def main():
    for path in path_list:
        md = read(path)
        # print(text[:100])
        data = convert(md)
    return data['html'][:100]


if __name__ == '__main__':
    print(main())
