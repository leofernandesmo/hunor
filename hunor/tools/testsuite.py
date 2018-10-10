import os
import copy

from hunor.tools.randoop import Randoop
from hunor.tools.evosuite import Evosuite


class TestSuiteResult:

    def __init__(self, tid, source_dir, classes_dir, classes):
        self.id = tid
        self.source_dir = source_dir
        self.classes_dir = classes_dir
        self.classes = classes
        self.coverage = 0
        self.fail = False
        self.tests_total = 0
        self.fail_tests_total = 0
        self.fail_tests = set()

    def to_dict(self):
        return {
            'coverage': self.coverage,
            'tests_total': self.tests_total,
            'fail_tests_total': self.fail_tests_total,
            'fail_tests': list(self.fail_tests)
        }

    def copy_without_excluded(self, excluded):
        result = copy.deepcopy(self)
        result.fail_tests = result.fail_tests.difference(excluded)
        return result


def generate_test_suites(jdk, classpath, config_file, sut_class, output,
                         is_randoop_disabled, is_evosuite_disabled,
                         project_dir):

    tests_dir = os.path.join(output, 'tests')
    test_suites = {}

    if not is_randoop_disabled:
        randoop = Randoop(jdk, classpath, config_file, tests_dir, sut_class,
                          project_dir)
        source_dir, classes_dir, classes = randoop.generate()

        test_suites['randoop'] = TestSuiteResult(
            tid='RAN',
            source_dir=source_dir,
            classes_dir=classes_dir,
            classes=classes
        )

    if not is_evosuite_disabled:
        evosuite = Evosuite(jdk, classpath, config_file, tests_dir, sut_class)
        source_dir, classes_dir, classes = evosuite.generate()

        test_suites['evosuite'] = TestSuiteResult(
            tid='EVO',
            source_dir=source_dir,
            classes_dir=classes_dir,
            classes=classes
        )

    return test_suites
