import os
import re
#import copy
import subprocess
#import shutil
import time


#from bs4 import BeautifulSoup

from hunor.utils import generate_classpath


PATH = os.path.dirname(os.path.abspath(__file__))
SAFIRA = os.sep.join([PATH, 'bin', 'safira.jar'])

#JUNIT = os.sep.join([PATH, 'bin', 'junit-4.12.jar'])
#HAMCREST = os.sep.join([PATH, 'bin', 'hamcrest-core-1.3.jar'])
#EVOSUITE = os.sep.join([PATH, 'bin', 'evosuite-standalone-runtime-1.0.6.jar'])
#JMOCKIT = os.sep.join([PATH, 'bin', 'jmockit-1.40-marcio.1.jar'])


#java -cp .\target\safira-0.0.1-SNAPSHOT.jar saferefactor.safira.SafiraStart C:\\workspace\\safira\\example\\original C:\\workspace\\safira\\example\\mutant04

class SafiraImpactAnalysis:

    def __init__(self, jdk, original, mutant, classpath):
        self.jdk = jdk
        self.original = original
        self.mutant = mutant
        self.classpath = classpath

    def run_impactanalysis(self):

        classpath = generate_classpath([
            #self.original,
            #self.mutant,
            SAFIRA,
            self.classpath,
        ])

        

        #if os.path.exists(
        #        os.path.join(mutant_classpath,
        #                     self.sut_class.replace('.', os.sep) + '.java')):
        #        coverage_source_dirs = mutant_classpath
        # path_to_targets = self.original + " " + self.mutant
        command = [
            self.jdk.java,
            '-classpath', classpath,
            'saferefactor.safira.SafiraStart', self.original, self.mutant 
        ]

        start = time.time()
        try:
            output = subprocess.check_output(command, shell=False,
                                             #cwd=test_suite,
                                             stderr=subprocess.STDOUT,
                                             timeout=60*3)
            
            list_methods, list_constructors = _extract_results_ok(output.decode('unicode_escape'))
            return list_methods, list_constructors, time.time() - start

        except subprocess.CalledProcessError as e:
            print("# ERROR: Run Safira Impact Analysis Call Process: {0} ".format(
                e.cmd
            ))
            print(e.output)
            return (_extract_results(e.output.decode('unicode_escape')),
                    time.time() - start)
        except subprocess.TimeoutExpired:
            elapsed_time = time.time() - start
            print("# ERROR: Run Safira Impact Analysis timed out. {0} seconds".format(
                elapsed_time
            ))
            return (0, 0, set()), elapsed_time


def _extract_results_ok(output):
    list_of_methods = []
    list_of_constructors = []

    # result = re.findall(r'OK \([0-9]* tests?\)', output)
    result = output.split("|")
    for res in result:
        if("method :" in res):
            list_of_methods.append(res)
        if("cons :" in res):
            list_of_constructors.append(res)    
    return list_of_methods, list_of_constructors


def _extract_results(output):
    if len(re.findall(r'initializationError', output)) == 0:
        result = re.findall(r'Tests run: [0-9]*,[ ]{2}Failures: [0-9]*', output)
        if len(result) > 0:
            result = result[0]
            result = result.replace(',', ' ')
            r = [int(s) for s in result.split() if s.isdigit()]
            tests_fail = _extract_test_id(output)
            return r[0], r[1], tests_fail
    return 0, 0, set()


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


# def _extract_li_id(li):
#     try:
#         file = re.findall(r'[A-Za-z0-9_]+#', li)[0][:-1]
#         test_case = re.findall(r'#test[0-9]+:', li)[0][1:-1]
#         return '{0}#{1}'.format(file, test_case)
#     except IndexError:
#         return None
