import os
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

        command = [
            self.jdk.java,
            '-classpath', classpath,
            '-Dcoverage-classes=' + self.sut_class,
            '-Dcoverage-output=html',
            '-Dcoverage-metrics=line',
            '-Dcoverage-srcDirs=' + self.source_dir,
            'org.junit.runner.JUnitCore', test_class
        ]

        try:
            subprocess.check_output(command, shell=False, cwd=test_suite,
                                    stderr=subprocess.DEVNULL,
                                    timeout=(60 * 10))
            return True
        except subprocess.CalledProcessError:
            return False
        except subprocess.TimeoutExpired:
            print("# ERROR: Run JUnit tests timed out.")

    def _run_test_suite(self, test_suite, mutant_classpath):
        success = True
        for test_class in test_suite.classes:
            if not self._run_test(test_suite.source_dir,
                                  test_suite.classes_dir,
                                  test_class, mutant_classpath):
                success = False
        return success

    def run_test_suites(self, test_suites, mutant_classpath, mutation_line):
        test_suites = test_suites.copy()
        for t in test_suites:
            test_suite = test_suites[t]
            test_suite.fail = not self._run_test_suite(
                test_suite, mutant_classpath)
            test_suite.coverage = self._count_line_coverage(
                test_suite.source_dir, mutation_line)

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
