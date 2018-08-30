import os
import shutil

from argparse import ArgumentParser
from hunor.tools.java import JDK
from hunor.tools.maven import Maven
from hunor.tools.randoop import Randoop


def _compile_project(options, jdk):
    maven = Maven(options.maven_home, jdk)
    return maven.compile(options.source)


def _generate_test_suites(options, jdk, classpath):
    tests_dir = os.path.join(options.output, 'tests')

    if not options.is_randoop_disabled:
        randoop = Randoop(jdk, classpath, options.config_file,
                          os.path.join(tests_dir, 'randoop'))
        randoop.generate()

    if not options.is_evosuite_disabled:
        pass


def main():
    parser = ArgumentParser()

    parser.add_argument('-m', '--maven-home', action='store', dest='maven_home')
    parser.add_argument('-j', '--java-home', action='store', dest='java_home')
    parser.add_argument('--maven-timeout', action='store', dest='maven_timeout', default='3600')
    parser.add_argument('--disable-randoop', action='store_true', dest='is_randoop_disabled')
    parser.add_argument('-c', '--config_file', action='store', dest='config_file')
    parser.add_argument('--disable-evosuite', action='store_true', dest='is_evosuite_disabled')
    parser.add_argument('-s', '--source', action='store', dest='source')
    parser.add_argument('-o', '--output', action='store', dest='output', default='output')
    parser.add_argument('--mutants', action='store', dest='mutants')
    parser.add_argument('--coverage-threshold', action='store', dest='coverage_threshold', default='0')

    options = parser.parse_args()

    options.output = os.path.abspath(options.output)

    if os.path.exists(options.output):
        shutil.rmtree(options.output)

    os.mkdir(options.output)

    jdk = JDK(options.java_home)

    classpath = _compile_project(options, jdk)
    _generate_test_suites(options, jdk, classpath)


if __name__ == '__main__':
    main()
