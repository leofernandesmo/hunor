import os

from itertools import combinations
from graphviz import Digraph, ExecutableNotFound


def subsuming(mutants):
    mutants = _remove_invalid_and_equivalent(mutants)

    for a, b in combinations(mutants, 2):
        if mutants[a].is_brother(mutants[b]):
            mutants[b].set_as_brother(mutants[a])
            mutants[a].set_as_brother(mutants[b])

    for a, b in combinations(mutants, 2):
        if mutants[a].subsume(mutants[b]):
            mutants[a].subsumes.append(mutants[b])
            mutants[b].subsumed_by.append(mutants[a])

        if mutants[a].is_subsumed_by(mutants[b]):
            mutants[a].subsumed_by.append(mutants[b])
            mutants[b].subsumes.append(mutants[a])

    d_mutants = {}
    for key in mutants:
        if mutants[key].label not in d_mutants:
            d_mutants[mutants[key].label] = mutants[key].to_dict()

    return _clean_dmsg(d_mutants)


def _clean_dmsg(mutants):
    r = sorted(mutants.items(), key=lambda v: len(v[1]['subsumes']), reverse=True)
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


def _remove_invalid_and_equivalent(mutants):
    r = dict(mutants)
    for key in mutants:
        if (mutants[key].maybe_equivalent
                or mutants[key].is_invalid):
            del r[key]
    return r


def create_dmsg(mutants, export_dir=''):
    dot = Digraph()

    for label, mutant in sorted(mutants.items(), key=lambda i: i[0]):
        dot.node(str(label), str(label))

    for label, mutant in sorted(mutants.items(), key=lambda i: i[0]):
        for s in mutant['subsumes']:
            dot.edge(str(s), str(label))

    dot.encoding = 'utf-8'

    try:
        dot.format = 'svg'
        dot.render(os.path.join(export_dir, 'DMSG'))
    except ExecutableNotFound:
        print("[WARNING]: Graphviz not found. "
              "Install graphviz package for generate DMSG.")

    try:
        dot.format = 'png'
        dot.render(os.path.join(export_dir, 'DMSG'))
    except ExecutableNotFound:
        print("[WARNING]: Graphviz not found. "
              "Install graphviz package for generate DMSG.")

    return dot
