import os
import re
import copy
import subprocess

from bs4 import BeautifulSoup

from hunor.utils import generate_classpath


PATH = os.path.dirname(os.path.abspath(__file__))

JUNIT = os.sep.join([PATH, 'bin', 'junit-4.12.jar'])
HAMCREST = os.sep.join([PATH, 'bin', 'hamcrest-core-1.3.jar'])
EVOSUITE = os.sep.join([PATH, 'bin', 'evosuite-standalone-runtime-1.0.6.jar'])
JMOCKIT = os.sep.join([PATH, 'bin', 'jmockit-1.40-marcio.1.jar'])


class JUnit:

    def __init__(self, jdk, sut_class, classpath, source_dir):
        self.jdk = jdk
        self.sut_class = sut_class
        self.classpath = classpath
        self.source_dir = source_dir

    def _run_test(self, test_suite, test_classes_dir, test_class,
                  mutant_classpath=''):

        classpath = generate_classpath([
            JMOCKIT, JUNIT, HAMCREST, EVOSUITE,
            test_classes_dir,
            mutant_classpath,
            self.classpath,
        ])

        coverage_source_dirs = self.source_dir

        if os.path.exists(
                os.path.join(mutant_classpath,
                             self.sut_class.replace('.', os.sep) + '.java')):
                coverage_source_dirs = mutant_classpath

        command = [
            self.jdk.java,
            '-classpath', classpath,
            '-Dcoverage-classes=' + self.sut_class,
            '-Dcoverage-output=html',
            '-Dcoverage-metrics=line',
            '-Dcoverage-srcDirs=' + coverage_source_dirs,
            'org.junit.runner.JUnitCore', test_class
        ]

        try:
            output = subprocess.check_output(command, shell=False,
                                             cwd=test_suite,
                                             stderr=subprocess.DEVNULL,
                                             timeout=(60 * 10))
            return _extract_results_ok(output.decode('unicode_escape'))
        except subprocess.CalledProcessError as e:
            return _extract_results(e.output.decode('unicode_escape'))
        except subprocess.TimeoutExpired:
            print("# ERROR: Run JUnit tests timed out.")

    def _run_test_suite(self, test_suite, mutant_classpath, mutation_line=0):
        total = 0
        fail = 0
        fail_tests = set()
        coverage = 0

        for test_class in test_suite.classes:
            t, f, f_s = self._run_test(test_suite.source_dir,
                                       test_suite.classes_dir,
                                       test_class, mutant_classpath)

            total += t
            fail += f
            fail_tests = fail_tests.union(f_s)
            coverage += self._count_line_coverage(test_suite.source_dir,
                                                  mutation_line)

        return total, fail, fail_tests, coverage

    def run_test_suites(self, test_suites, mutant_classpath, mutation_line):
        test_suites = copy.deepcopy(test_suites)
        for t in test_suites:
            test_suite = test_suites[t]
            total, fail, fail_tests, coverage = self._run_test_suite(
                test_suite, mutant_classpath, mutation_line)

            test_suite.fail = (fail != 0)
            test_suite.coverage = coverage
            test_suite.tests_total = total
            test_suite.fail_tests_total = fail
            test_suite.fail_tests = fail_tests

        return test_suites

    def _count_line_coverage(self, output_dir, mutation_line):

        report_html_path = os.path.join(
            output_dir, 'coverage-report',
            self.sut_class.replace('.', os.sep) + '.html')

        total = 0

        if os.path.exists(report_html_path):
            with open(report_html_path) as html:
                soup = BeautifulSoup(html, 'html.parser')
                for tr in soup.find_all('tr'):
                    td_line = tr.find_all('td', class_='line')
                    td_count = tr.find_all('td', class_='callpoints-count')
                    if td_line and td_count:
                        if mutation_line == int(td_line[0].string):
                            total = len(tr.find_all('li'))
                html.close()

        return total


def _extract_results_ok(output):
    result = re.findall(r'OK \([0-9]* tests?\)', output)[0]
    result = result.replace('(', '')
    r = [int(s) for s in result.split() if s.isdigit()]

    return r[0], 0, set()


def _extract_results(output):
    result = re.findall(r'Tests run: [0-9]*,[ ]{2}Failures: [0-9]*', output)[0]
    result = result.replace(',', ' ')
    r = [int(s) for s in result.split() if s.isdigit()]
    tests_fail = _extract_test_id(output)

    return r[0], r[1], tests_fail


def _extract_test_id(output):
    tests_fail = set()
    for test in re.findall(r'\.test[0-9]+\([A-Za-z0-9_]+\.java:[0-9]+\)', output):
        i = re.findall('\d+', test)
        file = re.findall(r'\(.+?(?=\.)', test)[0][1:]
        test_case = re.findall(r'\..+?(?=\()', test)[0][1:]

        if len(i) > 0:
            tests_fail.add('{0}#{1}'.format(file, test_case, int(i[-1])))
        else:
            print("*** ERROR: Error in regex of junit output.")

    return tests_fail
