#!/usr/bin/python
# -*- coding: utf8 -*-"

import copy
import collections
from datetime import datetime
import os
import random
import sys

NB_COLORS=4
NB_SLOTS=4
ONLY_PLAY_CANDIDATES=False

def combinations(colors, nb):
    result = []
    if nb == 0:
        return [[]]
    for r in combinations(colors, nb-1):
        for c in colors:
            result.append([c] + r)
    return result

# The response can be (misplaced, good):
# (0, 0) => Eliminate all colors from proposal
# (0, 1)
# (0, 2)
# (0, 3)
# (0, 4) => Won
# (1, 0)
# (1, 1)
# (1, 2)
# (2, 0)
# (2, 1)
# (2, 2)
# (3, 0)
# (3, 1)
# (4, 0) => You have all colors, now find the order
def score_proposal(proposal, combination):
    misplaced = 0
    good = 0
    counted = set()
    #[0, 4, 3, 4]
    #[4, 3, 6, 3]
    for (i, p) in enumerate(proposal):
        if proposal[i] not in combination:
            continue
        if proposal[i] == combination[i]:
            good += 1
            if i in counted:
                misplaced -= 1
            counted.add(i)
        else:
            for (j, c) in enumerate(combination):
                if proposal[i] == combination[j] and j not in counted:
                    misplaced += 1
                    counted.add(j)
                    break
    return (misplaced, good)

def score_proposal2(proposal, combination, set_combination):
    misplaced = 0
    good = 0
    counted = set()
    for (i, p) in enumerate(proposal):
        if proposal[i] not in set_combination:
            continue
        if proposal[i] == combination[i]:
            good += 1
            if i in counted:
                misplaced -= 1
            counted.add(i)
        else:
            for (j, c) in enumerate(combination):
                if proposal[i] == combination[j] and j not in counted:
                    misplaced += 1
                    counted.add(j)
    return (misplaced, good)

def score_proposal3(proposal, combination):
    nb_slots = len(proposal)
    misplaced = 0
    good = 0
    for (i, p) in enumerate(proposal):
        if p == combination[i]:
            good += 1
    p = sorted(proposal)
    c = sorted(combination)
    i, j = 0, 0
    while True:
        if p[i] == c[j]:
            misplaced += 1
            i += 1
            j += 1
        elif p[i] > c[j]:
            j += 1
        else:
            i += 1
        if i >= nb_slots or j >= nb_slots:
            break
    return (misplaced - good, good)

# Return a map from proposal to a map of scores to how many combinations from
# candidates give this score.
def proposals_scores_stats_all(candidates, colors, nb):
    result = collections.defaultdict(lambda: collections.defaultdict(int))
    for candidate in candidates:
        for proposal in combinations(colors, nb):
            result[tuple(proposal)][score_proposal(proposal, candidate)] += 1
    return result

def proposals_scores_stats_candidates(candidates):
    result = collections.defaultdict(lambda: collections.defaultdict(int))
    for candidate in candidates:
        for proposal in candidates:
            result[tuple(proposal)][score_proposal(proposal, candidate)] += 1
    return result

def proposals_elimination_expectation(candidates, colors, nb, candidates_only):
    if candidates_only:
        stats = proposals_scores_stats_candidates(candidates)
    else:
        stats = proposals_scores_stats_all(candidates, colors, nb)
    result = {}
    N = len(candidates)
    for (prop, scores) in stats.items():
        esperance = 0
        for (score, nb) in scores.items():
            esperance += (N - nb) * nb / N
        result[prop] = esperance
    return result

def eliminate(candidates, proposition, score):
    return [c for c in candidates if score_proposal(proposition, c) == score]

def find_best_proposal(candidates, colors, nb, deterministic, candidates_only):
    max_k, max_v, max_r = None, None, None
    for (k,v) in proposals_elimination_expectation(candidates, colors, nb, candidates_only).items():
        if max_v is None or (v > max_v and v > 0.0):
            max_k, max_v, max_r = k, v, random.random()
        elif v == max_v and not deterministic:
            r = random.random()
            if r > max_r:
                max_k, max_v, max_r = k, v, r
    # It's always better to take a candidate if it has the same score, has it
    # gives a chance to win immediately.
    if not candidates_only and list(max_k) not in candidates:
        #print("Proposal %s is not in candidates (value=%s)." % (max_k, max_v))
        for (k,v) in proposals_elimination_expectation(candidates, colors, nb, True).items():
            if v == max_v:
                #print("But %s is and has same value: %s." % (k, v))
                max_k = k
                break
    return max_k

def pick_combination(colors, nb):
    if not colors:
        return []
    return [random.choice(colors) for i in range(nb)]

def try_to_guess(to_find, colors, nb_slots, deterministic, only_play_candidates):
    candidates = combinations(colors, nb_slots)
    nb_tries = 0
    while True:
        if nb_tries == 0:
            # TODO: Doesn't work if there are less colors than slots
            if not deterministic:
                random.shuffle(colors)
            chosen = colors[:nb_slots]
        if len(candidates) <= 3:
            # If only a few possibilities remain, it's better to pick from candidates only
            # to have a chance to win right away.
            chosen = find_best_proposal(candidates, colors, nb_slots, deterministic, True)
        elif nb_tries > 0:
            chosen = find_best_proposal(candidates, colors, nb_slots, deterministic, only_play_candidates)
        nb_tries += 1
        score = score_proposal(chosen, to_find)
        #print("Trying %s -> %s" % (chosen, score))
        if score == (0, nb_slots):
            break
        candidates = eliminate(candidates, chosen, score)
    #print("Found %s in %s tries." % (chosen, nb_tries))
    return chosen, nb_tries

# This find the solution in 3 to 5 tries:
# 5 tries: 22.8%
# 4 tries: 67.2%
# 3 tries: 10.0%
def play_alone(nb_slots, nb_colors, deterministic=False, only_play_candidates=False):
    colors = list(range(nb_colors))
    to_find = pick_combination(colors, nb_slots)
    #print("To find: %s" % to_find)
    return try_to_guess(to_find, colors, nb_slots, deterministic, only_play_candidates)[1]

def random_tries(nb_slots, nb_colors, only_play_candidates, n):
    stats = collections.defaultdict(int)
    for i in range(n):
        stats[play_alone(nb_slots, nb_colors, deterministic=False, only_play_candidates=only_play_candidates)] += 1
    print("Number of games per number of tries:")
    total = sum(stats.values())
    tot_tries = 0
    for (k, v) in stats.items():
        tot_tries += k*v
        print("  %s tries: %s (%s%%)" % (k, v, 100*v/total))
    print("Average tries: %s" % (tot_tries/total))
    print("Total games: %s" % total)

def compute_kind(combi):
    counts = collections.defaultdict(int)
    for c in combi:
        counts[c] += 1
    return tuple(sorted(counts.values(), reverse=True))

def exhaustive_stats(nb_slots, nb_colors, only_play_candidates, output):
    colors = list(range(nb_colors))
    nb_slots = nb_slots
    combi_tries = {}
    stats_tries = collections.defaultdict(int)
    stats_tries_per_kind = collections.defaultdict(lambda: collections.defaultdict(int))
    candidates = combinations(colors, nb_slots)
    for c in candidates:
        result, tries = try_to_guess(c, colors, nb_slots, deterministic=True, only_play_candidates=only_play_candidates)
        assert list(result) == c, "%s != %s" % (result, c)
        stats_tries[tries] += 1
        kind = compute_kind(c)
        stats_tries_per_kind[kind][tries] += 1
        combi_tries[tuple(c)] = tries
    output.write("Number of games per number of tries:\n")
    total = sum(stats_tries.values())
    tot_tries = 0
    for (k, v) in stats_tries.items():
        tot_tries += k*v
        output.write("  %s tries: %s (%s%%)\n" % (k, v, 100*v/total))
    output.write("Average tries: %s\n" % (tot_tries/total))
    print("%s, %s, %s: %s" % (nb_slots, nb_colors, only_play_candidates, (tot_tries/total)))
    output.write("Total games: %s\n" % total)
    for (kind, v) in stats_tries_per_kind.items():
        tot_tries = 0
        tot_cnt = 0
        for (tries, cnt) in v.items():
            output.write("  %s: %s tries: %s\n" % (kind, tries, cnt))
            tot_tries += cnt*tries
            tot_cnt += cnt
        output.write("%s: %s tries in average\n" % (kind, tot_tries/tot_cnt))
    return combi_tries

def exhaustive_stats_grid_test(nb_slots_vals, nb_colors_vals, only_play_candidates_vals):
    try:
        os.mkdir("results")
    except FileExistsError:
        pass
    with open("results/summary_%s.txt" % datetime.now().timestamp(), "a") as summary:
        summary.write(" == Run from %s ==\n" % datetime.now())
        for nb_slots in nb_slots_vals:
            for nb_colors in nb_colors_vals:
                for only_play_candidates in only_play_candidates_vals:
                    summary.write(" = slots=%s, colors=%s, only_play_candidates=%s =\n" % (nb_slots, nb_colors, only_play_candidates))
                    result = exhaustive_stats(nb_slots, nb_colors, only_play_candidates, summary)
                    cand_str = "only_candidates" if only_play_candidates else "all_combis"
                    filename = "results/tries_%s_%s_%s.txt" % (nb_slots, nb_colors, cand_str)
                    with open(filename, "w") as f:
                        for k, v in result.items():
                            f.write("%s,%s\n" % (k,v))
                    summary.write("\n")

def try_all_proposals(remaining, nb_slots, colors, n):
    if n == 0:
        return None
    all_combis = combinations(colors, nb_slots)
    result = collections.defaultdict(list)
    for proposal in all_combis:
        score = score_proposal(proposal, to_guess)
        for option in remaining:
            if score_proposal(proposal, option) == score:
                result[(score, proposal)].append(option)
    for (score, proposal), options in result.items:
        if len(options) > 1:
            try_all_proposals(options, nb_slots, colors, n-1)

def optimal(nb_slots, nb_colors, only_play_candidates):
    colors = list(range(nb_colors))
    all_combis = combinations(colors, nb_slots)
    try_all_proposals(all_combis, nb_slots, colors, 6)

def start_profiling():
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    return pr

def stop_profiling(pr):
    import pstats
    from io import StringIO
    pr.disable()
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

if __name__ == '__main__':
    #colors = list(range(NB_COLORS))
    #slots = NB_SLOTS
    #pr = start_profiling()
    #proposals_elimination_expectation(combinations(colors, slots), colors, slots)
    #stop_profiling(pr)
    #random_tries(NB_SLOTS, NB_COLORS, ONLY_PLAY_CANDIDATES, 1000)
    # exhaustive_stats(NB_SLOTS, NB_COLORS, )

    #if len(sys.argv) != 3:
    #    print("Expect 2 arguments: max_nb_slots and max_nb_colors.")
    #    sys.exit(1)
    #max_nb_slots = int(sys.argv[1])
    #max_nb_colors = int(sys.argv[2])
    #exhaustive_stats_grid_test(list(range(1, max_nb_slots+1)), list(range(1, max_nb_colors+1)), [True, False])

    #exhaustive_stats_grid_test([5, 6], list(range(1, 6)), [True, False])
    exhaustive_stats_grid_test([4], [8], [False])
