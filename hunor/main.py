import os
import shutil

from argparse import ArgumentParser

from hunor.utils import get_class_files
from hunor.tools.java import JDK
from hunor.tools.maven import Maven
from hunor.tools.randoop import Randoop
from hunor.tools.evosuite import Evosuite
from hunor.tools.junit import JUnit
from hunor.tools.major import Major


def _compile_project(options, jdk):
    maven = Maven(options.maven_home, jdk)
    return maven.compile(options.source)


def _generate_test_suites(options, jdk, classpath):
    tests_dir = os.path.join(options.output, 'tests')
    test_suites = []

    if not options.is_randoop_disabled:
        randoop = Randoop(jdk, classpath, options.config_file, tests_dir, options.sut_class)
        source_dir, classes_dir, classes = randoop.generate()
        test_suites.append({
            'id': 'RAN',
            'source_dir': source_dir,
            'classes_dir': classes_dir,
            'classes': classes
        })

    if not options.is_evosuite_disabled:
        evosuite = Evosuite(jdk, classpath, options.config_file, tests_dir, options.sut_class)
        source_dir, classes_dir, classes = evosuite.generate()
        test_suites.append({
            'id': 'EVO',
            'source_dir': source_dir,
            'classes_dir': classes_dir,
            'classes': classes
        })

    return test_suites


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
    parser.add_argument('--class', action='store', dest='sut_class')

    options = parser.parse_args()

    options.output = os.path.abspath(options.output)
    source_dir = os.path.abspath(options.source)

    if os.path.exists(options.output):
        shutil.rmtree(options.output)
    os.mkdir(options.output)

    jdk = JDK(options.java_home)

    classpath = _compile_project(options, jdk)
    test_suites = _generate_test_suites(options, jdk, classpath)
    junit = JUnit(jdk, options.sut_class, classpath, source_dir)

    equivalence_analysis(options, jdk, junit, classpath, test_suites)


def equivalence_analysis(options, jdk, junit, classpath, test_suites):
    major = Major(os.path.abspath(options.mutants))
    mutants = major.read_log()

    with open(os.path.join(options.output, 'equivalents.csv'), 'w') as f:
        f.write('id,equivalent,coverage\n')
        print("RUNNING TEST SUITES FOR ALL MUTANTS...")
        for i in mutants:
            print("\tmutant: {0}#{1}...".format(mutants[i]['operator'], mutants[i]['id']))

            mutant_dir = os.path.join(os.path.abspath(options.mutants), str(mutants[i]['id']))

            for java_file in get_class_files(mutant_dir, ext='.java'):
                jdk.run_javac(java_file, 60, mutant_dir, "-classpath", classpath)

            mutants[i]['result'] = junit.run_test_suites(test_suites, mutant_dir, mutants[i]['line_number'])

            coverage = mutants[i]['result'][0]['coverage'] + mutants[i]['result'][1]['coverage']
            fail = mutants[i]['result'][0]['fail'] or mutants[i]['result'][1]['fail']

            if coverage >= int(options.coverage_threshold) and not fail:
                print('{0}#{1} is EQUIVALENT! [line coverage = {2}]'.format(
                    mutants[i]['operator'], mutants[i]['id'], coverage))
                f.write('{0},{1},{2}\n'.format(mutants[i]['id'], 'x', coverage))
            else:
                f.write('{0},{1},{2}\n'.format(mutants[i]['id'], '', coverage))
        f.close()


if __name__ == '__main__':
    main()


