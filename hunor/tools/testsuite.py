import os

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
        self.fail_tests = 0


def generate_test_suites(options, jdk, classpath):
    tests_dir = os.path.join(options.output, 'tests')
    test_suites = {}

    if not options.is_randoop_disabled:
        randoop = Randoop(jdk, classpath, options.config_file, tests_dir,
                          options.sut_class)
        source_dir, classes_dir, classes = randoop.generate()
        test_suites['randoop'] = TestSuiteResult('RAN', source_dir,
                                                 classes_dir, classes)

    if not options.is_evosuite_disabled:
        evosuite = Evosuite(jdk, classpath, options.config_file, tests_dir,
                            options.sut_class)
        source_dir, classes_dir, classes = evosuite.generate()
        test_suites['evosuite'] = TestSuiteResult('EVO', source_dir,
                                                  classes_dir, classes)

    return test_suites
