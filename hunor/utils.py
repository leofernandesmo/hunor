import os
import json


def get_class_files(path, package='', ext='.class'):
    files = []

    for node in os.listdir(path):
        node_path = os.path.join(path, node)
        if os.path.isdir(node_path):
            files += get_class_files(node_path, os.path.join(package, node),
                                     ext)
        elif os.path.splitext(node_path)[1] == ext:
            files.append(os.path.join(package, node))

    return files


def generate_classpath(paths):
    return os.pathsep.join(paths)


def qualified_class_to_file(qualified_class, ext='.java'):
    return qualified_class.replace('.', os.sep) + ext


def config(path):
    with open(path, 'r') as c:
        return json.loads(c.read())


def write_json(obj, name, output_dir=''):
    with open(os.path.join(output_dir, name + '.json'), 'w') as f:
        f.write(json.dumps(obj, indent=2))
        f.close()


def list_to_set(l):
    s = set()
    for e in l:
        s.add(e)
    return s


def list_equal(a, b):
    return set_equal(list_to_set(a), list_to_set(b))


def set_equal(a, b):
    return a.issubset(b) and b.issubset(a)
