def first_with_remainder(l, r):
    try:
        return next(e for e in l if e % 2 == r)
    except:
        return None

def first_even(l):
    return first_with_remainder(l, 0)

def first_odd(l):
    return first_with_remainder(l, 1)

def solution(A, K):
    sortedA = sorted(A, reverse=True)
    selected = sortedA[:K]
    unselected = sortedA[K:]

    if len(A) < K:
        return -1

    candidate = sum(selected)
    if candidate % 2 == 0:
        return candidate

    last_selected_even = first_even(reversed(selected))
    last_selected_odd = first_odd(reversed(selected))
    first_unselected_even = first_even(unselected)
    first_unselected_odd = first_odd(unselected)

    #print("last_selected_even: %s" % last_selected_even)
    #print("last_selected_odd: %s" % last_selected_odd)
    #print("first_unselected_even: %s" % first_unselected_even)
    #print("first_unselected_odd: %s" % first_unselected_odd)
    candidates = [-1]
    if last_selected_even and first_unselected_odd:
        candidates.append(candidate - last_selected_even + first_unselected_odd)
    if last_selected_odd and first_unselected_even:
        candidates.append(candidate - last_selected_odd + first_unselected_even)

    return max(candidates)

def test(A, K):
    print("%s (%s) -> %s" % (A, K, solution(A, K)))

test([5, 4, 3, 2, 1], 3)
test([5, 5, 5, 5, 5], 3)
test([5, 5, 4, 5, 5], 3)
test([5, 5, 5, 5, 4], 3)
test([4, 9, 8, 2, 6], 3)
test([5, 6, 3, 4, 2], 3)
test([7, 7, 7, 7, 7], 1)
test([10000], 2)
