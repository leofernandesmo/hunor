import os
import re

from hunor.mutation.mutant import Mutant


class Pit:

    def __init__(self, mutants_dir, sut_class):
        self.mutants_dir = mutants_dir
        self.sut_class = sut_class

    def read_log(self):
        mutants_data = {}

        log_file = os.sep.join([self.mutants_dir, 'emp_PITEST_MUTANTS.log'])

        with open(log_file) as log:
            for line in log.readlines():
                data = line.split(':')
                if data[0] == self.sut_class:
                    operator = re.findall(r'[A-Za-z]*', data[1])[0]
                    mutants_data[data[1]] = Mutant(
                        mid=data[1],
                        operator=operator,
                        original_symbol=None,
                        replacement_symbol=None,
                        method=None,
                        line_number=int(data[2]),
                        transformation=''.join(data[3:]),
                        path=self._mutant_dir(data[1])
                    )
            log.close()

        return mutants_data

    def _mutant_dir(self, mid):
        return os.path.join(os.path.abspath(self.mutants_dir), str(mid))
