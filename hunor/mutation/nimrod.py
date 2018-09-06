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

            mutant.result['test_suites'] = junit.run_test_suites(
                test_suites, mutant.path, mutant.line_number)

            coverage = 0
            fail = False
            coverage_log = []

            for r in mutant.result['test_suites']:
                coverage += mutant.result['test_suites'][r].coverage
                fail = fail or mutant.result['test_suites'][r].fail
                coverage_log.append('{0}: {1}'.format(
                    r, mutant.result['test_suites'][r].coverage))

            print('\t\tCoverage: {0} ({1})'.format(coverage, ', '.join(coverage_log)))

            if coverage >= int(options.coverage_threshold) and not fail:
                print('\t\tTHE MUTANT IS EQUIVALENT!')
                f.write('{0},{1},{2}\n'.format(mutant.id, 'x', coverage))
            else:
                f.write('{0},{1},{2}\n'.format(mutant.id, '', coverage))
        f.close()
