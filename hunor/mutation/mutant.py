

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
        self.is_equivalent = False
        self.has_brother = False
        self.brothers = set()
        self.subsumes = set()
        self.subsumed_by = set()
        self.path = path
        self.result = {}

    def __str__(self):
        return '{0}#{1}'.format(self.operator, self.id)
