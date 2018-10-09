#!/usr/bin/env python3
from hunor.tools.java import JDK
from hunor.tools.maven import Maven
from hunor.tools.junit import JUnit
from hunor.args import arg_parser, to_options
from hunor.tools.testsuite import generate_test_suites
from hunor.mutation.nimrod import equivalence_analysis
from hunor.mutation.subsuming import subsuming, create_dmsg


class Hunor:

    def __init__(self, options):
        self.options = options

    def run(self):
        jdk = JDK(self.options.java_home)

        classpath = Maven(
            jdk=jdk,
            maven_home=self.options.maven_home,
            no_compile=self.options.no_compile
        ).compile_project(self.options.source)

        test_suites = generate_test_suites(
            jdk=jdk,
            classpath=classpath,
            config_file=self.options.config_file,
            sut_class=self.options.sut_class,
            output=self.options.output,
            is_randoop_disabled=self.options.is_randoop_disabled,
            is_evosuite_disabled=self.options.is_evosuite_disabled,
            project_dir=self.options.source
        )

        junit = JUnit(
            jdk=jdk,
            sut_class=self.options.sut_class,
            classpath=classpath,
            source_dir=self.options.source
        )

        mutants = equivalence_analysis(
            jdk=jdk,
            junit=junit,
            classpath=classpath,
            test_suites=test_suites,
            mutants=self.options.mutants,
            mutation_tool=self.options.mutation_tool,
            sut_class=self.options.sut_class,
            coverage_threshold=self.options.coverage_threshold,
            output=self.options.output
        )

        mutants = subsuming(mutants)
        create_dmsg(mutants=mutants, export_dir=self.options.output)

        return mutants


def main():
    Hunor(to_options(arg_parser())).run()


if __name__ == '__main__':
    main()


