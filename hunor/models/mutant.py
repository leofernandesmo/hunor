from peewee import *
from playhouse.sqlite_ext import JSONField

from hunor.models.database import BaseModel
from hunor.models.test_suite import TestSuite
from hunor.models.target import Target


class Mutant(BaseModel):

    mid = CharField(null=False)
    operator = CharField(null=False)
    original_symbol = CharField(null=True)
    replacement_symbol = CharField(null=True)
    method = CharField(null=False)
    line_number = IntegerField(null=False)
    transformation = CharField(null=False)
    maybe_equivalent = BooleanField(null=False)
    has_brother = BooleanField(null=False)
    path = JSONField(null=True)
    is_invalid = BooleanField(null=False)
    label = CharField(null=True)
    mutation = CharField(null=True)
    is_redundant = BooleanField(null=False)
    belongs_to_minimal = BooleanField(null=False)
    is_useless = BooleanField(null=False)
    mutation_label = CharField(null=True)
    statement_operator = CharField(null=True)
    target = ForeignKeyField(Target, null=True, backref='mutants')


class Brotherhood(BaseModel):
    mutant = ForeignKeyField(Mutant)
    brother = ForeignKeyField(Mutant)


class Subsumption(BaseModel):
    subsumes = ForeignKeyField(Mutant)
    subsumed_by = ForeignKeyField(Mutant)


class MutantTestSuite(BaseModel):
    mutant = ForeignKeyField(Mutant)
    test_suite = ForeignKeyField(TestSuite)


def dict_to_mutant(d):
    mutant = Mutant()

    mutant.mid = d['id']
    mutant.operator = d['operator']
    mutant.original_symbol = d['original_symbol']
    mutant.replacement_symbol = d['replacement_symbol']
    mutant.method = d['method']
    mutant.line_number = d['line_number']
    mutant.transformation = d['transformation']
    mutant.maybe_equivalent = d['maybe_equivalent']
    mutant.has_brother = d['has_brother']
    mutant.path = d['path']
    mutant.is_invalid = d['is_invalid']
    mutant.label = d['label']
    mutant.mutation = d['mutation']
    mutant.is_redundant = d['is_redundant']
    mutant.belongs_to_minimal = d['belongs_to_minimal']
    mutant.is_useless = d['is_useless']
    mutant.mutation_label = d['mutation_label']
    mutant.statement_operator = d['statement_operator']

    return mutant
