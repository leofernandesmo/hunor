import os

from hunor.tools.mujava import MuJava
from hunor.tools.java import JDK
from hunor.utils import qualified_class_to_file, config


def main():
    project_dir = os.path.abspath('../../example/relational')
    mutants_dir = os.path.join(project_dir, 'mutants', 'gen')
    jdk = JDK('/home/marcio/Tools/java/jdk1.8.0_161')

    classes_dir = os.path.join(project_dir, 'target', 'classes')
    mujava = MuJava(mutants_dir, jdk=jdk, classpath=classes_dir)
    source_dir = os.path.join(project_dir, 'src', 'main', 'java')

    config_file = config('../../example/relational/config.json')

    for target in config_file['targets']:
        java_file = qualified_class_to_file(target['class'])
        mujava.generate(classes_dir, source_dir, java_file)


if __name__ == '__main__':
    main()
