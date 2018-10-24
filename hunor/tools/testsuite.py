import os
import copy

from hunor.tools.randoop import Randoop
from hunor.tools.evosuite import Evosuite
from hunor.utils import read_json, write_json


class TestSuiteResult:

    def __init__(self, tid, source_dir, classes_dir, classes, prefix=''):
        self.id = tid
        self.prefix = prefix
        self.source_dir = source_dir
        self.classes_dir = classes_dir
        self.classes = classes
        self.coverage = 0
        self.fail = False
        self.tests_total = 0
        self.fail_tests_total = 0
        self.fail_tests = set()
        self.coverage_tests = set()
        self.is_valid = True

    def to_dict(self):
        return {
            'coverage': self.coverage,
            'tests_total': self.tests_total,
            'fail_tests_total': self.fail_tests_total,
            'fail_tests': list(self.fail_tests),
            'coverage_tests': list(self.coverage_tests),
            'fail_coverage_tests': list(self.fail_coverage_tests),
            'fail_coverage_tests_total': len(self.fail_coverage_tests),
            'is_valid': self.is_valid
        }

    @property
    def fail_coverage_tests(self):
        return self.coverage_tests.intersection(self.fail_tests)

    def copy_without_excluded(self, excluded):
        result = copy.deepcopy(self)
        result.fail_tests = result.fail_tests.difference(excluded)
        return result


def generate_test_suites(jdk, classpath, config_file, sut_class, output,
                         is_randoop_disabled, is_evosuite_disabled,
                         project_dir, suites_number):

    reuse_tests = os.path.join(output, '..')
    saved_suites = {}

    if reuse_tests:
        if not os.path.exists(reuse_tests):
            os.makedirs(reuse_tests)
        saved_suites_file = os.path.join(reuse_tests, 'saved_suites.json')
        if os.path.exists(saved_suites_file):
            saved_suites = read_json(saved_suites_file)

    tests_dir = os.path.join(output, 'tests')
    test_suites = {}

    if sut_class not in saved_suites.keys():
        saved_suites[sut_class] = []

        if not is_randoop_disabled:
            for i in range(suites_number):
                test_suite_name = '{0}_{1}'.format('randoop', i + 1)
                randoop = Randoop(jdk, classpath, config_file, tests_dir,
                                  sut_class, project_dir,
                                  test_suite_name=test_suite_name)
                source_dir, classes_dir, classes = randoop.generate()

                test_suites[test_suite_name] = TestSuiteResult(
                    tid=test_suite_name,
                    source_dir=source_dir,
                    classes_dir=classes_dir,
                    classes=classes,
                    prefix='{0}_{1}'.format('RAN', i + 1)
                )

                saved_suites[sut_class].append({
                    'tid': test_suite_name,
                    'source_dir': source_dir,
                    'classes_dir': classes_dir,
                    'classes': classes,
                    'prefix': '{0}_{1}'.format('RAN', i + 1)
                })

        if not is_evosuite_disabled:
            for i in range(suites_number):
                test_suite_name = '{0}_{1}'.format('evosuite', i + 1)
                evosuite = Evosuite(jdk, classpath, config_file, tests_dir,
                                    sut_class, test_suite_name=test_suite_name)
                source_dir, classes_dir, classes = evosuite.generate()

                test_suites[test_suite_name] = TestSuiteResult(
                    tid=test_suite_name,
                    source_dir=source_dir,
                    classes_dir=classes_dir,
                    classes=classes,
                    prefix='{0}_{1}'.format('EVO', i + 1)
                )

                saved_suites[sut_class].append({
                    'tid': test_suite_name,
                    'source_dir': source_dir,
                    'classes_dir': classes_dir,
                    'classes': classes,
                    'prefix': '{0}_{1}'.format('EVO', i + 1)
                })
    else:
        for t in saved_suites[sut_class]:
            test_suites[t['tid']] = TestSuiteResult(
                tid=t['tid'],
                source_dir=t['source_dir'],
                classes_dir=t['classes_dir'],
                classes=t['classes'],
                prefix=t['prefix']
            )

    if reuse_tests:
        write_json(saved_suites, name='saved_suites', output_dir=reuse_tests)

    return test_suites
