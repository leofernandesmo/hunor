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
            print("\tmutant: {0}#{1}...".format(mutants[i]['operator'],
                                                mutants[i]['id']))

            mutant_dir = os.path.join(os.path.abspath(options.mutants),
                                      str(mutants[i]['id']))

            for java_file in get_class_files(mutant_dir, ext='.java'):
                jdk.run_javac(
                    java_file, 60, mutant_dir, "-classpath", classpath)

            mutants[i]['result'] = junit.run_test_suites(
                test_suites, mutant_dir, mutants[i]['line_number'])

            coverage = (mutants[i]['result'][0]['coverage']
                        + mutants[i]['result'][1]['coverage'])

            fail = (mutants[i]['result'][0]['fail']
                    or mutants[i]['result'][1]['fail'])

            if coverage >= int(options.coverage_threshold) and not fail:
                print('{0}#{1} is EQUIVALENT! [line coverage = {2}]'.format(
                    mutants[i]['operator'], mutants[i]['id'], coverage))
                f.write('{0},{1},{2}\n'.format(mutants[i]['id'], 'x', coverage))
            else:
                f.write('{0},{1},{2}\n'.format(mutants[i]['id'], '', coverage))
        f.close()