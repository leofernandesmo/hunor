from peewee import *
from playhouse.sqlite_ext import JSONField

from hunor.models.database import BaseModel


class TestSuite(BaseModel):
    name = CharField
    coverage = IntegerField()
    tests_total = IntegerField()
    fail_tests_total = IntegerField()
    fail_tests = JSONField()
    coverage_tests = JSONField()
    fail_coverage_tests = JSONField()
    fail_coverage_tests_total = IntegerField()


def dict_to_test_suite(name, d):

    test_suite = TestSuite()

    test_suite.name = name
    test_suite.coverage = d['coverage']
    test_suite.tests_total = d['tests_total']
    test_suite.fail_tests_total = d['fail_tests_total']
    test_suite.fail_tests = d['fail_tests']
    test_suite.coverage_tests = d['coverage_tests']
    test_suite.fail_coverage_tests = d['fail_coverage_tests']
    test_suite.fail_coverage_tests_total = d['fail_coverage_tests_total']

    return test_suite
