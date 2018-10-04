import os
import copy

from hunor.tools.mujava import MuJava
from hunor.tools.major import Major
from hunor.tools.java import JDK
from hunor.tools.maven import Maven
from hunor.utils import get_class_files
from hunor.args import arg_parser, to_options
from hunor.targets.main import write_config_json
from hunor.main import Hunor


def main():
    options = to_options(arg_parser())

    jdk = JDK(options.java_home)

    classes_dir = Maven(
        jdk=jdk,
        maven_home=options.maven_home,
    ).compile_project(options.source)

    tool = MuJava(options.mutants, jdk=jdk, classpath=classes_dir)
    tool = Major(options.mutants, jdk=jdk, classpath=classes_dir)
    source_dir = os.path.join(options.source, 'src', 'main', 'java')

    files = get_class_files(source_dir, ext='.java')
    targets = []

    for file in files:
        targets += tool.generate(classes_dir, source_dir, file, len(targets))

    write_config_json(targets, options.mutants)

    for target in targets:
        o = copy.copy(options)
        o.mutants = os.path.join(o.mutants, str(target['id']))
        o.output = o.mutants
        o.sut_class = target['class']
        o.no_compile = True

        Hunor(o).run()


if __name__ == '__main__':
    main()
