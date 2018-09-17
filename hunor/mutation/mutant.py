class Result:

    def __init__(self):
        self.test_suites = {}


class Mutant:

    def __init__(self, mid, operator, original_symbol, replacement_symbol,
                 method, line_number, transformation, path=list()):
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

    def __str__(self):
        return '{0}#{1}'.format(self.operator, self.id)

    def __eq__(self, other):
        return self.id == other.id

    def get_fail_tests(self):
        fail_tests = set()

        for test_suite in self.result.test_suites:
            fail_tests = fail_tests.union(
                self.result.test_suites[test_suite].fail_tests)

        return fail_tests

    def is_brother(self, mutant):
        fail_tests_a = self.get_fail_tests()
        fail_tests_b = mutant.get_fail_tests()

        return (not self.is_invalid and not self.maybe_equivalent
                and (fail_tests_a.issubset(fail_tests_b)
                     and fail_tests_b.issubset(fail_tests_a)))

    def subsume(self, mutant):
        fail_tests_a = self.get_fail_tests()
        fail_tests_b = mutant.get_fail_tests()

        return (not self.is_invalid and not self.maybe_equivalent
                and fail_tests_b.issubset(fail_tests_a))

    def is_subsumed_by(self, mutant):
        fail_tests_a = self.get_fail_tests()
        fail_tests_b = mutant.get_fail_tests()

        return (not self.is_invalid and not self.maybe_equivalent
                and fail_tests_a.issubset(fail_tests_b))

    def to_dict(self):

        subsumes = []
        subsumed_by = []

        for m in self.subsumes:
            if m.label != self.label and m.label not in subsumes:
                subsumes.append(m.label)

        for m in self.subsumed_by:
            if m.label != self.label and m.label not in subsumed_by:
                subsumed_by.append(m.label)

        return {
            'id': str(self.id),
            'operator': self.operator,
            'original_symbol': self.original_symbol,
            'replacement_symbol': self.replacement_symbol,
            'method': self.method,
            'line_number': self.line_number,
            'transformation': self.transformation,
            'maybe_equivalent': self.maybe_equivalent,
            'has_brother': self.has_brother,
            'brothers': [str(m.id) for m in self.brothers],
            'subsumes': subsumes,
            'subsumed_by': subsumed_by,
            'path': self.path,
            'is_invalid': self.is_invalid,
            'label': self.label
        }

    def set_as_brother(self, brother):
        self.has_brother = True
        if brother not in self.brothers:
            self.brothers.append(brother)

        brother.has_brother = True
        if self not in brother.brothers:
            brother.brothers.append(self)

        all_brothers = set()

        for b in self.brothers:
            all_brothers.add(b.id)

        for b in brother.brothers:
            all_brothers.add(b.id)

        label = _create_label(all_brothers)

        self.label = label
        brother.label = label


def _create_label(brothers):
    return ', '.join(sorted(list(brothers)))
