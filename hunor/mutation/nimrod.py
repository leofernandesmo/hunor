import os

from hunor.utils import get_class_files
from hunor.tools.major import Major


def equivalence_analysis(options, jdk, junit, classpath, test_suites):
    major = Major(os.path.abspath(options.mutants))
    mutants = major.read_log()

    with open(os.path.join(options.output, 'equivalents.csv'), 'w') as f:
        f.write('id,equivalent,coverage\n')
        print("RUNNING TEST SUITES FOR ALL MUTANTS...")
        for i in mutants:
            mutant = mutants[i]
            print("\tmutant: {0}...".format(mutant))

            for java_file in get_class_files(mutant.path, ext='.java'):
                jdk.run_javac(
                    java_file, 60, mutant.path, "-classpath", classpath)

            mutant.result.test_suites = junit.run_test_suites(
                test_suites, mutant.path, mutant.line_number)

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

            print('\t\tcoverage: {0} ({1}) tests fail: {2}/{3}'.format(
                coverage, ', '.join(coverage_log), fail_tests_total,
                tests_total))
            # print('\t\tfail: {0}'.format(fail_tests))

            if coverage >= int(options.coverage_threshold) and not fail:
                print('\t\t >>> THIS MUTANT MAY BE EQUIVALENT!')
                mutant.maybe_equivalent = True
                f.write('{0},{1},{2}\n'.format(mutant.id, 'x', coverage))
            else:
                f.write('{0},{1},{2}\n'.format(mutant.id, '', coverage))
        f.close()

    return mutants
