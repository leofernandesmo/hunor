#!/usr/bin/env python3
from hunor.tools.java import JDK
from hunor.tools.maven import Maven
from hunor.tools.junit import JUnit
from hunor.args import arg_parser, to_options
from hunor.tools.testsuite import generate_test_suites
from hunor.mutation.nimrod import equivalence_analysis
from hunor.mutation.subsuming import subsuming, create_dmsg, minimize
from hunor.utils import write_json


class Hunor:

    def __init__(self, options, using_target=False):
        self.options = options
        self.using_target = using_target

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
            project_dir=self.options.source,
            suites_number=self.options.suites_number
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
            output=self.options.output,
            mutants_dir=self.options.mutants,
            using_target=self.using_target
        )

        if mutants is not None:
            subsuming_mutants = subsuming(
                mutants,
                coverage_threshold=self.options.coverage_threshold
            )

            minimized, minimal_tests = minimize(
                mutants,
                coverage_threshold=self.options.coverage_threshold
            )

            create_dmsg(mutants=subsuming_mutants,
                        export_dir=self.options.output)
            mutants = subsuming(
                mutants,
                clean=False,
                coverage_threshold=self.options.coverage_threshold
            )

            mutants_dict = [mutants[m].to_dict() for m in mutants]

            write_json(minimized, 'subsuming_minimal_tests',
                       self.options.mutants)
            write_json(list(minimal_tests), 'minimal_tests',
                       self.options.mutants)
            write_json(mutants_dict, 'mutants',
                       self.options.mutants)
            write_json(subsuming_mutants, 'subsuming_mutants',
                       self.options.mutants)

            return mutants_dict, subsuming_mutants

        return {}, {}


def main():
    Hunor(to_options(arg_parser())).run()


if __name__ == '__main__':
    main()


