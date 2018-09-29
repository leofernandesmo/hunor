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
