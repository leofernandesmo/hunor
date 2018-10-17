import re
import os

from hunor.utils import list_equal
from difflib import ndiff


class Result:

    def __init__(self):
        self.test_suites = {}


class Mutant:

    def __init__(self, mid, operator, original_symbol, replacement_symbol,
                 method, line_number, transformation, path):
        self.id = mid
        self.operator = operator
        self.original_symbol = original_symbol
        self.replacement_symbol = replacement_symbol
        self.method = method
        self.line_number = line_number
        self.transformation = transformation
        self.maybe_equivalent = False
        self.has_brother = False
        self.brothers = list()
        self.subsumes = list()
        self.subsumed_by = list()
        self.path = path
        self.result = Result()
        self.is_invalid = False
        self.label = mid
        self.mutation = self.gen_label()
        self.mutation_label = self.mutation

    def __str__(self):
        return '{0}#{1}'.format(self.operator, self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def get_fail_tests(self):
        fail_tests = set()

        for test_suite in self.result.test_suites:
            fail_tests = fail_tests.union(
                self.result.test_suites[test_suite].fail_tests)

        return fail_tests

    def get_coverage_count(self):
        coverage_count = 0

        for test_suite in self.result.test_suites:
            coverage_count += self.result.test_suites[test_suite].coverage

        return coverage_count

    def is_brother(self, mutant, ignore_tests=None):
        fail_tests_a = self.get_fail_tests()
        fail_tests_b = mutant.get_fail_tests()

        if ignore_tests is not None:
            fail_tests_a = fail_tests_a.difference(ignore_tests)
            fail_tests_b = fail_tests_b.difference(ignore_tests)

        return (not self.is_invalid and not self.maybe_equivalent
                and (fail_tests_a.issubset(fail_tests_b)
                     and fail_tests_b.issubset(fail_tests_a)))

    def subsume(self, mutant, ignore_tests=None):
        fail_tests_a = self.get_fail_tests()
        fail_tests_b = mutant.get_fail_tests()

        if ignore_tests is not None:
            fail_tests_a = fail_tests_a.difference(ignore_tests)
            fail_tests_b = fail_tests_b.difference(ignore_tests)

        return (not self.is_invalid and not self.maybe_equivalent
                and fail_tests_a.issubset(fail_tests_b))

    def is_subsumed_by(self, mutant, ignore_tests=None):
        fail_tests_a = self.get_fail_tests()
        fail_tests_b = mutant.get_fail_tests()

        if ignore_tests is not None:
            fail_tests_a = fail_tests_a.difference(ignore_tests)
            fail_tests_b = fail_tests_b.difference(ignore_tests)

        return (not self.is_invalid and not self.maybe_equivalent
                and fail_tests_b.issubset(fail_tests_a))

    def subsuming_equal(self, mutant):
        return (list_equal(self.brothers, mutant.brothers)
                and list_equal(self.subsumes, mutant.subsumes)
                and list_equal(self.subsumed_by, mutant.subsumed_by))

    def to_dict(self):

        subsumes = []
        subsumed_by = []
        test_suites = {}

        for m in self.subsumes:
            if m.label != self.label and m.label not in subsumes:
                subsumes.append(m.label)

        for m in self.subsumed_by:
            if m.label != self.label and m.label not in subsumed_by:
                subsumed_by.append(m.label)

        for t in self.result.test_suites:
            test_suites[t] = self.result.test_suites[t].to_dict()

        return {
            'id': str(self.id),
            'operator': self.operator,
            'original_symbol': self.original_symbol,
            'replacement_symbol': self.replacement_symbol,
            'method': self.method,
            'line_number': self.line_number,
            'transformation': self.transformation.strip() if self.transformation
            else None,
            'maybe_equivalent': self.maybe_equivalent,
            'has_brother': self.has_brother,
            'brothers': [str(m.id) for m in self.brothers],
            'subsumes': subsumes,
            'subsumed_by': subsumed_by,
            'path': self.path.split(os.sep)[-2:],
            'is_invalid': self.is_invalid,
            'label': self.label,
            'test_suites': test_suites,
            'mutation': self.gen_label(),
            'is_redundant': self.is_redundant(),
            'belongs_to_minimal': self.belongs_to_minimal(),
            'is_useless': self.is_useless(),
            'mutation_label': self.mutation_label
        }

    def set_as_brother(self, brother):
        self.has_brother = True
        if brother not in self.brothers:
            self.brothers.append(brother)

        brother.has_brother = True
        if self not in brother.brothers:
            brother.brothers.append(self)

        all_brothers = set()
        all_brothers_mutation = set()

        for b in self.brothers:
            all_brothers.add(b.id)
            all_brothers_mutation.add(b.mutation)

        for b in brother.brothers:
            all_brothers.add(b.id)
            all_brothers_mutation.add(b.mutation)

        label = _create_label(all_brothers)

        self.label = label
        brother.label = label

        mutation_label = _create_label(all_brothers_mutation)

        self.mutation_label = mutation_label
        brother.mutation_label = mutation_label

    def is_redundant(self):
        return len(self.subsumed_by) > 0 or self.has_brother

    def belongs_to_minimal(self):
        return len(self.subsumed_by) == 0 and not self.maybe_equivalent

    def is_useless(self):
        return len(self.subsumed_by) > 0 or self.maybe_equivalent

    def statement(self):
        return self.transformation.split(' => ')[0].strip()

    def diff(self):
        diff = []
        transformation = self.transformation.split(' => ')
        original = transformation[0].strip().replace(' ', '')
        mutation = transformation[1].strip().replace(' ', '')
        for d in ndiff(original, mutation):
            if d[0] != ' ':
                diff.append([d[0], d[-1]])
        return diff

    def gen_label(self):
        transformation = self.transformation.split(' => ')
        original = transformation[0].strip().replace(' ', '')
        mutation = transformation[1].strip().replace(' ', '')
        if self.operator == 'COI':
            return self.operator + ' ' + '!()'
        else:
            label = re.sub(r'[a-zA-Z0-9._(),]*', '', mutation)
            if len(label) == 0:
                if self.operator == 'ROR' and mutation == 'true':
                    return self.operator + ' ' + 'true'
                elif self.operator == 'ROR' and mutation == 'false':
                    return self.operator + ' ' + 'false'
                elif original.startswith(mutation):
                    return self.operator + ' ' + 'lhs'
                elif original.endswith(mutation):
                    return self.operator + ' ' + 'rhs'
                return self.operator + ' ' + mutation

        return self.operator + ' ' + label


def _create_label(brothers):
    return ', '.join(sorted(list(brothers)))