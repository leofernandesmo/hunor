import os


class Major:

    def __init__(self, mutants_dir):
        self.mutants_dir = mutants_dir

    def read_log(self):
        mutants_data = {}

        log_file = os.sep.join([self.mutants_dir, 'mutants.log'])

        with open(log_file) as log:
            for line in log.readlines():
                data = line.split(':')
                mutants_data[int(data[0])] = {
                    'id': int(data[0]),
                    'operator': data[1],
                    'original_symbol': data[2],
                    'replacement_symbol': data[3],
                    'method': data[4],
                    'line_number': int(data[5]),
                    'transformation': data[6]
                 }
            log.close()

        return mutants_data
