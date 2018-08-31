import os


def get_class_files(path, package='', ext='.class'):
    files = []

    for node in os.listdir(path):
        node_path = os.path.join(path, node)
        if os.path.isdir(node_path):
            package = os.path.join(package, node)
            files += get_class_files(node_path, package, ext)
        elif os.path.splitext(node_path)[1] == ext:
            files.append(os.path.join(package, node))

    return files


def generate_classpath(paths):
    return os.pathsep.join(paths)
