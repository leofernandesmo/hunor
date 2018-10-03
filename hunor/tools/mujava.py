import os
import re
import subprocess
import shutil

from hunor.mutation.mutant import Mutant
from hunor.utils import generate_classpath
from hunor.tools import junit
from hunor.targets.main import get_targets


PATH = os.path.dirname(os.path.abspath(__file__))

MUJAVA = os.sep.join([PATH, 'bin', 'mujava.jar'])
OPENJAVA = os.sep.join([PATH, 'bin', 'openjava.jar'])
COMMONSIO = os.sep.join([PATH, 'bin', 'commons-io-2.4.jar'])


class MuJava:

    def __init__(self, mutants_dir, jdk=None, classpath=None):
        self.mutants_dir = mutants_dir
        self.jdk = jdk
        self.classpath = classpath

    def read_log(self, log_dir=None):
        mutants_data = {}

        log_file = os.sep.join([self.mutants_dir if not log_dir else log_dir,
                                'mutation_log'])

        with open(log_file) as log:
            for line in log.readlines():
                data = line.split(':')
                operator = re.findall(r'[A-Z]*', data[0])[0]
                mutants_data[data[0]] = Mutant(
                    mid=data[0],
                    operator=operator,
                    original_symbol=None,
                    replacement_symbol=None,
                    method=data[2],
                    line_number=int(data[1]) if (
                        not operator == 'SDL') else int(data[1]) - 1,
                    transformation=data[3],
                    path=self._mutant_dir(data[0])
                )
            log.close()

        return mutants_data

    def _mutant_dir(self, mid):
        return os.path.join(os.path.abspath(self.mutants_dir), str(mid))

    def _exec(self, com, parameters, cwd=None):
        cwd = self.mutants_dir if cwd is None else cwd

        classpath = generate_classpath(['.', MUJAVA, COMMONSIO, OPENJAVA,
                                       self.jdk.tools, junit.JUNIT,
                                       junit.HAMCREST, self.classpath])

        command = [self.jdk.java, '-classpath', classpath, com]
        command += parameters

        try:
            env = os.environ.copy()
            env['CLASSPATH'] = classpath
            return subprocess.check_output(command, shell=False,
                                           cwd=cwd,
                                           env=env,
                                           timeout=36000)
        except subprocess.TimeoutExpired:
            print('# ERROR: muJava timed out.')
        except subprocess.CalledProcessError as e:
            print('# ERROR: {0} returned non-zero exit status.\n{1}'.format(
                'muJava', e.output.decode('unicode_escape')))

    def _exec_genmutes(self, session, operators, cwd):
        parameters = ['-' + str(o).upper() for o in operators]
        parameters.append(session)

        self._exec('mujava.cli.genmutes', parameters, cwd=cwd)

    def _exec_testnew(self, session, classes_dir, source_dir, java_file):
        generate_dir = os.path.join(self.mutants_dir, '.tmp')
        session_dir = os.path.join(generate_dir, session)

        if os.path.exists(generate_dir):
            shutil.rmtree(generate_dir)

        pkg_dir = os.path.join(session_dir, 'src', os.path.dirname(java_file))
        result_dir = os.path.join(session_dir, 'result')
        os.makedirs(generate_dir)
        os.makedirs(pkg_dir)
        os.makedirs(result_dir)
        os.makedirs(os.path.join(session_dir, 'testset'))
        shutil.copy(os.path.join(source_dir, java_file), pkg_dir)
        os.symlink(classes_dir, os.path.join(session_dir, 'classes'))

        with open(os.path.join(generate_dir, 'mujavaCLI.config'), 'w') as f:
            f.write('MuJava_HOME={0}'.format(generate_dir))

        return session, generate_dir, result_dir

    def generate(self, classes_dir, source_dir, java_file, count=0):
        session, generate_dir, result_dir = self._exec_testnew(
            'session', classes_dir, source_dir, java_file)
        self._exec_genmutes(session, ['all'], cwd=generate_dir)

        targets = []

        if len(os.listdir(result_dir)) > 0:
            class_dir = os.path.join(result_dir, os.listdir(result_dir)[0])
            targets = get_targets(os.path.join(class_dir, 'original'),
                                  java_file.split(os.sep)[-1], count=count)

            self._copy_result(class_dir, targets, java_file)

        return targets

    def _copy_result(self, class_dir, targets, java_file):
        trad_mutants = os.path.join(class_dir, 'traditional_mutants')
        mutants = self.read_log(trad_mutants)

        for target in targets:
            mutant_target = os.path.join(self.mutants_dir,
                                         str(target['id']))
            if os.path.exists(mutant_target):
                shutil.rmtree(mutant_target)
            os.makedirs(mutant_target)
            with open(os.path.join(mutant_target, 'mutation_log'), 'w') as f:
                for mutant in mutants:
                    m = mutants[mutant]
                    pck = os.sep.join(java_file.split(os.sep)[0:-1])
                    src = os.path.join(trad_mutants, m.method, m.id)
                    dst = os.path.join(mutant_target, m.id, pck)
                    if (target['line'] == m.line_number
                            and target['statement'] == m.statement()
                            and os.path.exists(src)):
                        f.write('{0}:{1}:{2}:{3}'.format(
                            m.id, m.line_number, m.method, m.transformation
                        ))
                        shutil.copytree(src, dst)
                f.close()
