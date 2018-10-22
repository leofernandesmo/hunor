import os
import copy

from random import shuffle

from itertools import combinations
from graphviz import Digraph, ExecutableNotFound


def subsuming(mutants, ignored_tests=None, clean=True, coverage_threshold=0):
    mutants = copy.deepcopy(mutants)
    mutants = _remove_invalid_and_equivalent(mutants, coverage_threshold)

    for a, b in combinations(mutants, 2):
        if mutants[a].is_brother(mutants[b], ignored_tests):
            mutants[b].set_as_brother(mutants[a])
            mutants[a].set_as_brother(mutants[b])

    for a, b in combinations(mutants, 2):
        if mutants[a].subsume(mutants[b], ignored_tests):
            mutants[a].subsumes.append(mutants[b])
            mutants[b].subsumed_by.append(mutants[a])

        if mutants[a].is_subsumed_by(mutants[b], ignored_tests):
            mutants[a].subsumed_by.append(mutants[b])
            mutants[b].subsumes.append(mutants[a])

    if clean:
        d_mutants = {}
        for key in mutants:
            if mutants[key].label not in d_mutants:
                d_mutants[mutants[key].label] = mutants[key].to_dict()

        return _clean_dmsg(d_mutants)
    return mutants


def _clean_dmsg(mutants):
    r = sorted(mutants.items(), key=lambda v: len(v[1]['subsumes']),
               reverse=True)
    mutants = {}
    for m in r:
        mutants[m[0]] = dict(m[1])
    for m in mutants:
        all_subsumed = set()
        for s in mutants[m]['subsumes']:
            all_subsumed = _all_subsumed(mutants, mutants[s], all_subsumed)
        for r in all_subsumed:
            if r in mutants[m]['subsumes']:
                mutants[m]['subsumes'].remove(r)

    return mutants


def _all_subsumed(mutants, mutant, subsumed):
    subsumed = set(subsumed)
    for m in mutant['subsumes']:
        subsumed.add(m)
        subsumed = _all_subsumed(mutants, mutants[m], subsumed)
    return subsumed


def _remove_invalid_and_equivalent(mutants, coverage_threshold):
    r = dict(mutants)
    for key in mutants:
        if (mutants[key].maybe_equivalent
                or mutants[key].is_invalid
                or not mutants[key].get_fail_tests()
                or mutants[key].get_coverage_count() < coverage_threshold):
            del r[key]
    return r


def create_dmsg(mutants, export_dir='.', filename='DMSG', format='png',
                render=True):
    dot = Digraph('G')

    elements = dmsg_dot_elements(mutants)

    for n in elements[0]:
        dot.node(n['id'], label=n['label'], peripheries=n['peripheries'])
    for e in elements[1]:
        dot.edge(e[0], e[1])

    if render:
        render_dot(dot, export_dir, filename, format)

    return dot


def dmsg_dot_elements(mutants):
    nodes = []
    edges = []

    for label, mutant in sorted(mutants.items(), key=lambda i: i[0]):
        peripheries = '1'
        if len(mutant['subsumed_by']) == 0:
            peripheries = '2'
        nodes.append({
            'id': str(label),
            'label': str(mutant['mutation_label']),
            'peripheries': peripheries
        })

    for label, mutant in sorted(mutants.items(), key=lambda i: i[0]):
        for s in mutant['subsumes']:
            edges.append((str(label), str(s)))

    return nodes, edges


def multiple_dmsgs(elements, export_dir='.', filename='DMSG', format='svg',
                   render=True):
    dot = Digraph('G')
    dot.attr(ration='0.7')

    def _n(x, y):
        return '{0}_{1}'.format(x, y)

    for i, l in enumerate(elements):
        name, e = l
        with dot.subgraph(name='cluster_' + str(name)) as c:
            for n in e[0]:
                c.node(_n(name, n['id']), label=n['label'],
                       peripheries=n['peripheries'])
            for g in e[1]:
                c.edge(_n(name, g[0]), _n(name, g[1]))
            c.attr(label=str(name))
            c.attr(color='lightgrey')
            c.attr(style='dashed')

    if render:
        render_dot(dot, export_dir, filename, format)

    return dot


def render_dot(dot, export_dir='.', filename='DMSG', format='png'):
    try:
        dot.encoding = 'utf-8'
        dot.format = format
        dot.render(os.path.join(export_dir, str(filename)))
    except ExecutableNotFound:
        print("[WARNING]: Graphviz not found. "
              "Install graphviz package for generate DMSG.")


def minimize(mutants, coverage_threshold=0, shuffle_tests=False):
    mutants = copy.deepcopy(mutants)
    all_tests = set()

    for m in mutants:
        for t in mutants[m].get_fail_tests():
            all_tests.add(t)

    original = subsuming(mutants, clean=False,
                         coverage_threshold=coverage_threshold)
    excluded_tests = set()

    to_check = list(all_tests)
    if shuffle_tests:
        shuffle(to_check)

    for t in to_check:
        excluded_tests.add(t)
        if not _subsuming_equals(
                original,
                subsuming(mutants, clean=False, ignored_tests=excluded_tests,
                          coverage_threshold=coverage_threshold)):
            excluded_tests.remove(t)

    for key in mutants:
        for test_suite in mutants[key].result.test_suites:
            mutants[key].result.test_suites[test_suite] = (
                mutants[key].result.test_suites[test_suite]
                .copy_without_excluded(excluded_tests))

    return (subsuming(mutants, coverage_threshold=coverage_threshold,
                      ignored_tests=excluded_tests),
            all_tests.difference(excluded_tests))


def _subsuming_equals(mutants_a, mutants_b):
    if len(mutants_a.keys()) != len(mutants_b.keys()):
        return False

    for key in mutants_a:
        if not mutants_a[key].subsuming_equal(mutants_b[key]):
            return False

    return True
