from allocation_functions import *


def algorithm1(n, utilities, s, stopOnEF1=True):
    """
    implemantation of our algorithm, with an extension to n agents
    """
    w = tuple([1/n]*n)  # tuple of initial agents' weights (all equal)
    A = get_w_maximal_allocation(w, utilities, s)  # (A1, A2, ..., An), ∀i, Ai is of type list
    if is_EF1(A, utilities):
        print(A, " is EF1!")
        if stopOnEF1:
            return A
    # TODO: fix order_names function and run it below
    # A = order_names(A, utilities)  # replace agent names if needed such that the envy-order will be 1 > 2 > ... > n
    # we can now assume that for each i,j such that i>j, the allocation is EF for i w.r.t j
    # in particular, the allocation is EF for agent 1
    return
    item_pairs = get_exchangeable_items(A)
    exchangeable_pair = get_max_r_pair(item_pairs)
    while True:
        if not is_EF1(A, utilities):
            A = exchange_pair(exchangeable_pair)
            item_pairs = get_exchangeable_items(A)
            exchangeable_pair = get_max_r_pair(item_pairs)
        else: 
            print(A, " is EF1!")
            if stopOnEF1:
                return A
        # TODO: add here some stop condition
                

utilities = [[(-1,0,-1),(-4,-1,-1),(-5,-2,-3)],
            [(-4,-1,0),(-5,-3,-2),(-6,-4,-6)],
            [(-2,-6,-7),(-4,-6,-7)]]
s = (1, 2, 1)  # capacity constraints
algorithm1(3, utilities, s)