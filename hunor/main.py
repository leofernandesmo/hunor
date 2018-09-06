#!/usr/bin/env python3

import os
import shutil

from hunor.utils import config
from hunor.tools.java import JDK
from hunor.tools.maven import Maven
from hunor.tools.junit import JUnit
from hunor.args import arg_parser
from hunor.tools.testsuite import generate_test_suites
from hunor.mutation.nimrod import equivalence_analysis


def _set_source_dir(options):
    if options.source:
        return os.path.abspath(options.source)

    return os.path.join(
        os.path.dirname(options.config_file),
        os.sep.join(config(options.config_file)['source'])
    )


def _set_output_dir(options):
    if os.path.exists(options.output):
        shutil.rmtree(options.output)
    os.mkdir(options.output)

    return options.output


def main():
    parser = arg_parser()

    options = parser.parse_args()

    options.output = os.path.abspath(options.output)
    options.config_file = os.path.abspath(options.config_file)
    options.source = _set_source_dir(options)
    options.output = _set_output_dir(options)

    jdk = JDK(options.java_home)

    classpath = Maven(options.maven_home, jdk).compile_project(options.source)
    test_suites = generate_test_suites(options, jdk, classpath)
    junit = JUnit(jdk, options.sut_class, classpath, options.source)

    equivalence_analysis(options, jdk, junit, classpath, test_suites)


if __name__ == '__main__':
    main()


