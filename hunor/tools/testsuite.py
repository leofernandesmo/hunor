import os
import copy
import threading

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
        self.elapsed_time = None
        self.maybe_in_loop = False

    def to_dict(self):
        return {
            'coverage': self.coverage,
            'tests_total': self.tests_total,
            'fail_tests_total': self.fail_tests_total,
            'fail_tests': list(self.fail_tests),
            'coverage_tests': list(self.coverage_tests),
            'fail_coverage_tests': list(self.fail_coverage_tests),
            'fail_coverage_tests_total': len(self.fail_coverage_tests),
            'is_valid': self.is_valid,
            'elapsed_time': self.elapsed_time,
            'maybe_in_loop': self.maybe_in_loop
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
                         project_dir, suites_evosuite, suites_randoop, junit):

    # import pdb 
    # pdb.set_trace()

    reuse_tests = os.path.join(output, '')
    saved_suites = {}

    if reuse_tests:
        if not os.path.exists(reuse_tests):
            os.makedirs(reuse_tests)
        saved_suites_file = os.path.join(reuse_tests, 'saved_suites.json')
        if os.path.exists(saved_suites_file):
            saved_suites = read_json(saved_suites_file)

    tests_dir = os.path.join(output, 'tests')
    test_suites = {}

    if sut_class in saved_suites.keys():
        valid_suites = []
        for s in saved_suites[sut_class]:
            if os.path.exists(s['source_dir']):
                valid_suites.append(s)
        if len(valid_suites) > 0:
            saved_suites[sut_class] = valid_suites
        else:
            del saved_suites[sut_class]

    if sut_class not in saved_suites.keys():
        saved_suites[sut_class] = []
        #print('Threading EvoSuite')
        thread_randoop = threading.Thread(target=generate_randoop_tests, args=(is_randoop_disabled, suites_randoop, jdk, classpath, config_file, tests_dir, sut_class, project_dir, junit, test_suites, saved_suites))
        thread_evosuite = threading.Thread(target=generate_evosuite_tests, args=(is_evosuite_disabled, suites_evosuite, jdk, classpath, config_file, tests_dir, sut_class, junit, test_suites, saved_suites))

        thread_randoop.start()
        thread_evosuite.start()

        thread_randoop.join()
        thread_evosuite.join()

        #OLD sequential execution...
        #generate_randoop_tests(is_randoop_disabled, suites_randoop, jdk, classpath, config_file, tests_dir, sut_class, project_dir, junit, test_suites, saved_suites)
        #generate_evosuite_tests(is_evosuite_disabled, suites_evosuite, jdk, classpath, config_file, tests_dir, sut_class, junit, test_suites, saved_suites)
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

def generate_evosuite_tests(is_evosuite_disabled, suites_evosuite, jdk, classpath, config_file, tests_dir, sut_class, junit, test_suites, saved_suites):
    if not is_evosuite_disabled:
        for i in range(suites_evosuite):
            test_suite_name = '{0}_{1}'.format('evosuite', i + 1)
            evosuite = Evosuite(jdk, classpath, config_file, tests_dir,
                                sut_class, test_suite_name=test_suite_name)
            source_dir, classes_dir, classes = evosuite.generate()

            test_suite = TestSuiteResult(
                tid=test_suite_name,
                source_dir=source_dir,
                classes_dir=classes_dir,
                classes=classes,
                prefix='{0}_{1}'.format('EVO', i + 1)
            )

            checked_test_suites = junit.run_test_suites(
                {test_suite_name: test_suite}, classpath)

            if (not checked_test_suites[test_suite_name].maybe_in_loop
                    and not checked_test_suites[test_suite_name].fail
                    and checked_test_suites[test_suite_name].is_valid):
                test_suites[test_suite_name] = test_suite

                saved_suites[sut_class].append({
                    'tid': test_suite_name,
                    'source_dir': source_dir,
                    'classes_dir': classes_dir,
                    'classes': classes,
                    'prefix': '{0}_{1}'.format('EVO', i + 1)
                })
            else:
                print('# ERROR: invalid suite. FAIL: {0}, LOOP: {1}, '
                      'FAILED TESTES: {2}'.format(
                        checked_test_suites[test_suite_name].fail,
                        checked_test_suites[test_suite_name].maybe_in_loop,
                        checked_test_suites[test_suite_name].fail_tests
                      ))

def generate_randoop_tests(is_randoop_disabled, suites_randoop, jdk, classpath, config_file, tests_dir, sut_class, project_dir, junit, test_suites, saved_suites):
    
    if not is_randoop_disabled:
        for i in range(suites_randoop):
            test_suite_name = '{0}_{1}'.format('randoop', i + 1)
            randoop = Randoop(jdk, classpath, config_file, tests_dir,
                              sut_class, project_dir,
                              test_suite_name=test_suite_name)
            source_dir, classes_dir, classes = randoop.generate()

            test_suite = TestSuiteResult(
                tid=test_suite_name,
                source_dir=source_dir,
                classes_dir=classes_dir,
                classes=classes,
                prefix='{0}_{1}'.format('RAN', i + 1)
            )

            checked_test_suites = junit.run_test_suites(
                {test_suite_name: test_suite}, classpath)

            if (not checked_test_suites[test_suite_name].maybe_in_loop
                    and not checked_test_suites[test_suite_name].fail
                    and checked_test_suites[test_suite_name].is_valid):
                test_suites[test_suite_name] = test_suite

                saved_suites[sut_class].append({
                    'tid': test_suite_name,
                    'source_dir': source_dir,
                    'classes_dir': classes_dir,
                    'classes': classes,
                    'prefix': '{0}_{1}'.format('RAN', i + 1)
                })
            else:
                print('# ERROR: invalid suite. FAIL: {0}, LOOP: {1}, '
                      'FAILED TESTES: {2}'.format(
                        checked_test_suites[test_suite_name].fail,
                        checked_test_suites[test_suite_name].maybe_in_loop,
                        checked_test_suites[test_suite_name].fail_tests
                      ))
