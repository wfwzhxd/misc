import hashlib
import json
from zipfile import ZipFile

class Testcase:

    Template = "\t".join(["ID", "模块", "路径", "测试点"])

    def __init__(self, module, path, name):
        self.id = "-".join(x for x in map(str_hash, [module, path, name]))
        self.module = module
        self.path = path
        self.name = name

    def __str__(self) -> str:
        return "\t".join([self.id, self.module, self.path, self.name])


def str_hash(s, len=3):
    hexstr = hashlib.new("md5", str.encode(s, "utf-8")).hexdigest()
    return hexstr[:len].upper()

def read_xmind_content(xmind_file):
    global content
    with ZipFile(xmind_file) as xf:
        for zf in xf.namelist():
            if "content.json" == zf:
                return json.loads(xf.open(zf).read().decode('utf-8'))[0]
    raise Exception("error input file: content.json not found!")

def travel_topic(topic, module=None, path=None):
    title = topic["title"]
    if "children" not in topic:
        yield [module, path, title]
        return
    if not module:
        module = title
    path = (path + "/" + title) if path else title
    for c in topic["children"]["attached"]:
        for x in travel_topic(c, module, path):
            yield x


def process(xmind_file):
    xmind_content = read_xmind_content(xmind_file)
    topic = xmind_content["rootTopic"]
    # title = topic["title"]
    outfile = xmind_file+".txt"
    with open(outfile, "w", encoding="utf-8") as outf:
        print("write to file:{}...".format(outfile))
        print(Testcase.Template, file=outf)
        for x in travel_topic(topic):
            print(Testcase(*x), file=outf)
        print("OK")

if __name__ == "__main__":
    from sys import argv
    if len(argv) < 2:
        print("usage: {} xmind1 xmind2 ...".format(argv[0]))
        exit(1)
    for v in argv[1:]:
        process(v)