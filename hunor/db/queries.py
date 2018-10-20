from hunor.db.models import Mutant, Brotherhood, Subsumption
from hunor.db.models import dict_to_mutant
from hunor.db.models import TestSuite, dict_to_test_suite
from hunor.db.models import Target, dict_to_target


class Queries:

    def __init__(self, database):
        self.db = database.db

    def create_tables(self):
        self.db.create_tables([
            Mutant,
            Brotherhood,
            Subsumption,
            TestSuite,
            Target
        ])

    def close(self):
        self.db.close()

    @staticmethod
    def save_target_and_mutants(target, mutants):
        t = dict_to_target(target)

        coverage = 0
        if len(mutants) > 0:
            for test_suite in mutants[0]['test_suites']:
                coverage += mutants[0]['test_suites'][test_suite]['coverage']

        t.coverage = coverage
        t.save()

        mid_to_id = {}

        for mutant in mutants:
            m = dict_to_mutant(mutant)
            m.target = t
            m.save()

            mid_to_id[mutant['id']] = m.id

            for test_suite in mutant['test_suites']:
                t_s = dict_to_test_suite(test_suite,
                                         mutant['test_suites'][test_suite])
                t_s.mutant = m
                t_s.save()

        for mutant in mutants:
            m = Mutant.get(Mutant.id == mid_to_id[mutant['id']])
            for brother in mutant['brothers']:
                b = Mutant.get(Mutant.id == mid_to_id[brother])
                brotherhood = Brotherhood()
                brotherhood.mutant = m
                brotherhood.brother = b
                brotherhood.save()

            for subsume in mutant['subsumes_id']:
                s = Mutant.get(Mutant.id == mid_to_id[subsume])
                subsumption = Subsumption()
                subsumption.subsumed_by = m
                subsumption.subsumes = s
                subsumption.save()
