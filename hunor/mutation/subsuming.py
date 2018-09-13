from itertools import combinations


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

    import json
    print(json.dumps(d_mutants, indent=2))


def _remove_invalid_and_equivalent(mutants):
    r = dict(mutants)
    for key in mutants:
        if (mutants[key].maybe_equivalent
                or mutants[key].is_invalid):
            del r[key]
    return r
