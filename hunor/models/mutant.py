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

    def subsumes(self):
        return [s.subsumes for s in
                Subsumption.select().where(
                    Subsumption.subsumed_by == self)]

    def subsumed_by(self):
        return [s.subsumed_by for s in
                Subsumption.select().where(
                    Subsumption.subsumes == self)]

    def brothers(self):
        return [b.brother for b in
                Brotherhood.select().where(
                    Brotherhood.mutant == self)]

    @staticmethod
    def find_all():
        return Mutant.select()

    @staticmethod
    def find_all_by_target(target):
        return Mutant.select().where((Mutant.target == target))

    @staticmethod
    def is_redundant_in_targets_group_by_mutation(targets):
        return _group_by_dict(Mutant.select(
            Mutant.mutation,
            fn.COUNT(Mutant.id)
        ).where(
            (Mutant.target.in_(targets))
            & (Mutant.is_redundant == True)
        ).group_by(Mutant.mutation))

    @staticmethod
    def is_not_redundant_in_targets_group_by_mutation(targets):
        return _group_by_dict(Mutant.select(
            Mutant.mutation,
            fn.COUNT(Mutant.id)
        ).where(
            (Mutant.target.in_(targets))
            & (Mutant.is_redundant == False)
        ).group_by(Mutant.mutation))

    @staticmethod
    def belongs_to_minimal_in_targets_group_by_mutation(targets):
        return _group_by_dict(Mutant.select(
            Mutant.mutation,
            fn.COUNT(Mutant.id)
        ).where(
            (Mutant.target.in_(targets))
            & (Mutant.belongs_to_minimal == True)
        ).group_by(Mutant.mutation))

    @staticmethod
    def doesnt_belongs_to_minimal_in_targets_group_by_mutation(targets):
        return _group_by_dict(Mutant.select(
            Mutant.mutation,
            fn.COUNT(Mutant.id)
        ).where(
            (Mutant.target.in_(targets))
            & (Mutant.belongs_to_minimal == False)
        ).group_by(Mutant.mutation))

    @staticmethod
    def redundant_abstract(targets):
        red = Mutant.is_redundant_in_targets_group_by_mutation(targets)
        not_red = Mutant.is_not_redundant_in_targets_group_by_mutation(targets)
        min = Mutant.belongs_to_minimal_in_targets_group_by_mutation(targets)
        not_min = Mutant.doesnt_belongs_to_minimal_in_targets_group_by_mutation(
            targets)

        abstract = {}
        total = _group_by_dict(
            Mutant.select(
                Mutant.mutation,
                fn.COUNT(Mutant.id)
            ).where(
                (Mutant.target.in_(targets))
            ).group_by(Mutant.mutation))

        for r in total:
            abstract[r] = {
                'redundant': red[r] if r in red.keys() else 0,
                'not_redundant': not_red[r] if r in not_red.keys() else 0,
                'dominant': min[r] if r in min.keys() else 0,
                'not_dominant': not_min[r] if r in not_min.keys() else 0,
                'total': total[r]
            }

        return abstract


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


def _group_by_dict(query):
    group = {}
    result = query.tuples()

    for r in result:
        if isinstance(r, tuple):
            group[r[0]] = r[1]

    return group
