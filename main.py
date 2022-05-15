from allocation_functions import *


def algorithm1(n):
    """
    implemantation of our algorithm, with an extension to n agents
    """
    w = tuple([1/n]*n)  # tuple of initial agents' weights (all equal)
    A = get_w_maximal_allocation(w)
    if is_EF1(A):
        return A
    if get_envious(A) == 1:  # the allocation is EF for 2
        A = replace_names(A)
    # we can now assume that for each i,j such that i>j, the allocation is EF for i w.r.t j
    # in particular, the allocation is EF for agent 1
    item_pairs = get_exchangeable_items(A)
    exchangeable_pair = get_max_r_pair(item_pairs)
    while not is_EF1(A):
        A = exchange_pair(exchangeable_pair)
        item_pairs = get_exchangeable_items(A)
        exchangeable_pair = get_max_r_pair(item_pairs)
    return A


algorithm1(3)