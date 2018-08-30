import os
import subprocess
import json

from hunor.utils import get_class_files

RANDOOP = os.path.abspath(os.sep.join(['..', 'bin', 'randoop-all-4.0.3.jar']))
JUNIT = os.path.abspath(os.sep.join(['..', 'bin', 'junit-4.12.jar']))
HAMCREST = os.path.abspath(os.sep.join(['..', 'bin', 'hamcrest-core-1.3.jar']))


class Randoop:

    def __init__(self, jdk, classpath, config, tests_dir):
        self.jdk = jdk
        self.randoop = os.path.abspath(RANDOOP)
        self.tests_dir = tests_dir
        self.classpath = classpath
        self.tests_src = os.path.join(tests_dir, 'tests')
        self.tests_classes = os.path.join(tests_dir, 'classes')
        self.parameters = []

        with open(config, 'r') as c:
            self.parameters = json.loads(c.read())['randoop']['parameters']

    def _exec_randoop(self):
        command = [
            self.jdk.java,
            '-classpath', self.classpath + ':' + self.randoop,
            'randoop.main.Main',
            'gentests'
        ]

        command += self.parameters

        try:
            return subprocess.call(command, shell=False,
                                   cwd=self.tests_src,
                                   stdout=subprocess.DEVNULL,
                                   timeout=36000)
        except subprocess.TimeoutExpired:
            print("# ERROR: Randoop generate timed out.")

    def _compile(self):
        os.mkdir(self.tests_classes)

        classpath = self.classpath + ':' + self.tests_classes + ':' + JUNIT + ':' + HAMCREST

        for java_test_file in sorted(get_class_files(self.tests_src, ext='.java')):
            self.jdk.run_javac(os.path.join(self.tests_src, java_test_file), 36000,
                               self.tests_src, '-classpath', classpath, '-d',
                               self.tests_classes)

    def generate(self):

        if not os.path.exists(self.tests_dir):
            os.makedirs(self.tests_dir)

        self._exec_randoop()
        self._compile()

