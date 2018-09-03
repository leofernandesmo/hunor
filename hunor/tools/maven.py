import os
import subprocess


class Maven:

    def __init__(self, maven_home, javac):
        self.maven_home = maven_home
        self.javac = javac
        self._check_maven()

    def _check_maven(self):
        if not self.maven_home:
            if 'M2_HOME' in os.environ and os.environ['M2_HOME']:
                self.maven_home = os.environ['M2_HOME']
            elif 'MAVEN_HOME' in os.environ and os.environ['MAVEN_HOME']:
                self.maven_home = os.environ["MAVEN_HOME"]
            else:
                print('ERROR: MAVEN_HOME not found.')
                raise SystemExit()

        try:
            self._run(None, None, 10, '-version')
        except OSError:
            print('maven not found.')
            raise SystemExit()

    def _run(self, project_dir, target, timeout, *args):

        command = [os.path.join(self.maven_home, os.sep.join(['bin', 'mvn']))]

        if target:
            command.append(target)

        command = command + list(args)

        env = os.environ.copy()
        env['JAVA_HOME'] = self.javac.java_home

        subprocess.call(command, cwd=project_dir, env=env, timeout=timeout,
                        stdout=subprocess.DEVNULL)

    def compile(self, project_dir, timeout=(60 * 60)):
        try:
            project_dir = os.path.abspath(project_dir)
            self._run(project_dir, 'compile', timeout)
            print('SUCCESS: {0} compiled!'.format(project_dir))

            if os.path.exists(os.path.join(project_dir, 'target')):
                return os.path.join(project_dir, 'target', 'classes')
            elif os.path.exists(os.path.join(project_dir, 'build')):
                return os.path.join(project_dir, 'build', 'classes')
            else:
                print("ERROR: Maven classes directory not found.")
                raise SystemExit
        except subprocess.CalledProcessError as e:
            print(e.output.decode('unicode_escape'))
            raise SystemError
        except subprocess.TimeoutExpired:
            print('# ERROR: Maven compile timed out.')
            raise SystemError
