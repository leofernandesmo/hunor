import os
import re
import copy
import subprocess
import shutil

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
                                             timeout=(60 * 5))
            return _extract_results_ok(output.decode('unicode_escape'))
        except subprocess.CalledProcessError as e:
            return _extract_results(e.output.decode('unicode_escape'))
        except subprocess.TimeoutExpired:
            print("# ERROR: Run JUnit tests timed out.")
            return 0, 0, set()

    def _run_test_suite(self, test_suite, mutant_classpath, mutation_line=0,
                        original_path=None):
        total = 0
        fail = 0
        fail_tests = set()
        coverage = 0
        coverage_tests = set()

        for test_class in test_suite.classes:
            t, f, f_s = self._run_test(test_suite.source_dir,
                                       test_suite.classes_dir,
                                       test_class, mutant_classpath)

            total += t
            fail += f
            fail_tests = fail_tests.union(f_s)
            coverage_src = test_suite.source_dir

            if original_path is not None:
                coverage_src = os.path.join(original_path, test_suite.id)

            c, c_t = self._count_line_coverage(coverage_src, mutation_line)
            coverage += c
            coverage_tests = coverage_tests.union(c_t)
            coverage_report_dir = os.path.join(test_suite.source_dir,
                                               'coverage-report')
            coverage_report_dst_dir = os.path.join(
                    mutant_classpath, test_suite.id, 'coverage-report')

            if os.path.exists(coverage_report_dst_dir):
                shutil.rmtree(coverage_report_dst_dir)

            if os.path.exists(coverage_report_dir):
                shutil.copytree(coverage_report_dir, coverage_report_dst_dir)

        return total, fail, fail_tests, coverage, coverage_tests

    def run_test_suites(self, test_suites, mutant_classpath, mutation_line,
                        original_path=None):
        test_suites = copy.deepcopy(test_suites)
        for t in test_suites:
            test_suite = test_suites[t]
            (total, fail, fail_tests,
             coverage, coverage_tests) = self._run_test_suite(
                test_suite, mutant_classpath, mutation_line, original_path)

            test_suite.fail = (fail != 0)
            test_suite.coverage = coverage
            test_suite.tests_total = total
            test_suite.fail_tests_total = fail
            test_suite.fail_tests = fail_tests
            test_suite.coverage_tests = coverage_tests

        return test_suites

    def _count_line_coverage(self, output_dir, mutation_line):

        report_html_path = os.path.join(
            output_dir, 'coverage-report',
            self.sut_class.replace('.', os.sep) + '.html')

        total = 0
        tests = set()

        if os.path.exists(report_html_path):
            with open(report_html_path) as html:
                soup = BeautifulSoup(html, 'html.parser')
                for tr in soup.find_all('tr'):
                    td_line = tr.find_all('td', class_='line')
                    td_count = tr.find_all('td', class_='callpoints-count')
                    if td_line and td_count:
                        if mutation_line == int(td_line[0].string):
                            total = len(tr.find_all('li'))
                            for li in tr.find_all('li'):
                                method_name = _extract_li_id(li.string)
                                if method_name is not None:
                                    tests.add(method_name)
                html.close()

        return total, tests


def _extract_results_ok(output):
    result = re.findall(r'OK \([0-9]* tests?\)', output)[0]
    result = result.replace('(', '')
    r = [int(s) for s in result.split() if s.isdigit()]

    return r[0], 0, set()


def _extract_results(output):
    if len(re.findall(r'initializationError', output)) > 0:
        return 0, 0, set()

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


def _extract_li_id(li):
    try:
        file = re.findall(r'[A-Za-z0-9_]+#', li)[0][:-1]
        test_case = re.findall(r'#test[0-9]+:', li)[0][1:-1]
        return '{0}#{1}'.format(file, test_case)
    except IndexError:
        return None
