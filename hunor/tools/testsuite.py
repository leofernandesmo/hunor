import os

from hunor.tools.randoop import Randoop
from hunor.tools.evosuite import Evosuite


def generate_test_suites(options, jdk, classpath):
    tests_dir = os.path.join(options.output, 'tests')
    test_suites = []

    if not options.is_randoop_disabled:
        randoop = Randoop(jdk, classpath, options.config_file, tests_dir,
                          options.sut_class)
        source_dir, classes_dir, classes = randoop.generate()
        test_suites.append({
            'id': 'RAN',
            'source_dir': source_dir,
            'classes_dir': classes_dir,
            'classes': classes
        })

    if not options.is_evosuite_disabled:
        evosuite = Evosuite(jdk, classpath, options.config_file, tests_dir,
                            options.sut_class)
        source_dir, classes_dir, classes = evosuite.generate()
        test_suites.append({
            'id': 'EVO',
            'source_dir': source_dir,
            'classes_dir': classes_dir,
            'classes': classes
        })

    return test_suites
