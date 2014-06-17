import os


def get_date(markdown):
    with open(markdown, "r") as reader:
        reader.readline()
        date_line = reader.readline()
        middle = date_line.split(" ")[1]
        year, month, _ = middle.split("-")
    return year, month


if __name__ == '__main__':
    markdowns = filter(lambda x: x.endswith(".md"), os.listdir("."))
    for markdown in markdowns:
        year, month = get_date(markdown)
        path = "./%s/%s" % (year, month)
        try:
            os.makedirs(path)
        except OSError:
            pass

        src = markdown
        dst = "%s/%s" % (path, markdown)
        os.rename(src, dst)
