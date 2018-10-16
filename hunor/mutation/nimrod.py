import os
import math

from hunor.utils import get_class_files
from hunor.tools.major import Major
from hunor.tools.mujava import MuJava
from hunor.tools.pit import Pit


def equivalence_analysis(jdk, junit, classpath, test_suites, mutants,
                         mutation_tool, sut_class, coverage_threshold,
                         output, mutants_dir):

    if mutation_tool == 'pit':
        mutation_tool = Pit(mutants, sut_class)
    elif mutation_tool == 'major':
        mutation_tool = Major(mutants)
    elif mutation_tool == 'mujava':
        mutation_tool = MuJava(mutants)

    mutants = mutation_tool.read_log()

    with open(os.path.join(output, 'equivalents.csv'), 'w') as f:
        f.write('id,maybe_equivalent,not_equivalent,coverage\n')
        f.close()

    original_dir = os.path.join(mutants_dir, 'ORIGINAL')
    if os.path.exists(original_dir):
        junit.run_test_suites(test_suites, original_dir, 0)

    print("RUNNING TEST SUITES FOR ALL MUTANTS...")
    for i, m in enumerate(mutants):
        mutant = mutants[m]
        print("\tmutant: {0}... {1}/{2}".format(mutant, i + 1, len(mutants)))

        if os.path.exists(mutant.path):
            compile_success = True
            for java_file in get_class_files(mutant.path, ext='.java'):
                compile_success = compile_success and jdk.run_javac(
                    java_file, 60, mutant.path, "-classpath", classpath)

            if compile_success:
                mutant.result.test_suites = junit.run_test_suites(
                    test_suites, mutant.path, mutant.line_number, original_dir)

                coverage = 0
                fail = False
                coverage_log = []
                tests_total = 0
                fail_tests_total = 0
                fail_tests = set()

                for r in mutant.result.test_suites:
                    coverage += mutant.result.test_suites[r].coverage
                    fail = fail or mutant.result.test_suites[r].fail
                    tests_total += mutant.result.test_suites[r].tests_total
                    fail_tests_total += (mutant.result.test_suites[r]
                                         .fail_tests_total)
                    fail_tests = fail_tests.union(
                        mutant.result.test_suites[r].fail_tests)

                    coverage_log.append('{0}: {1}'.format(
                        r, mutant.result.test_suites[r].coverage))

                coverage_threshold = float(coverage_threshold)
                if coverage_threshold < 1:
                    coverage_threshold = math.ceil(
                        coverage_threshold * tests_total)
                else:
                    coverage_threshold = math.ceil(coverage_threshold)

                print('\t\tcoverage: {0}/{4} ({1}) tests fail: {2}/{3}'.format(
                    coverage, ', '.join(coverage_log), fail_tests_total,
                    tests_total, coverage_threshold))
                with open(os.path.join(output, 'equivalents.csv'), 'a') as f:
                    if coverage >= coverage_threshold and not fail:
                        print('\t\t +++ THIS MUTANT MAY BE EQUIVALENT!')
                        mutant.maybe_equivalent = True
                        f.write('{0},{1},{2},{3}\n'.format(mutant.id, 'x', '',
                                                           coverage))
                    elif fail:
                        print('\t\t --- THIS MUTANT IS NOT EQUIVALENT!')
                        f.write('{0},{1},{2},{3}\n'.format(mutant.id, '', 'x',
                                                           coverage))
                    else:
                        f.write('{0},{1},{2},{3}\n'.format(mutant.id, '', '',
                                                           coverage))
                    f.close()
            else:
                print('\t\tWARNING: mutant not compile: {0}'.format(
                    mutant.path))
                mutant.is_invalid = True
        else:
            print('\t\tWARNING: mutant directory not found: {0}'
                  .format(mutant.path))
            mutant.is_invalid = True

    return mutants
