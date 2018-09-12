import os
import re

from hunor.mutation.mutant import Mutant


class MuJava:

    def __init__(self, mutants_dir):
        self.mutants_dir = mutants_dir

    def read_log(self):
        mutants_data = {}

        log_file = os.sep.join([self.mutants_dir, 'mutation_log'])

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
