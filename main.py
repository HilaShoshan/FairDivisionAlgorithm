from Allocation import *
from Instance import *


def algorithm1(I, stopOnEF1=True):
    """
    Implemantation of our algorithm from the paper: https://arxiv.org/pdf/2205.07779.pdf
    with an intuitive extension to n agents
    :param I: a problem instance
    :param stopOnEF1: a boolean determining if we want to stop when an EF1 allocation is found
                        (as in the original algorithm),
                        or if we want to explore all the search-space (for debuging).
    """
    # Step 1: Find a w-maximal feasible allocation that is EF for some agent.
    w = tuple([1/n]*n)  # a tuple of initial agents' weights (all equal)
    A = W_maximal_allocation(I, w)  # (A1, A2, ..., An), ∀i, Ai is of type list
    if A.is_EF1():
        print(A, " is EF1!")
        if stopOnEF1:
            return A
    # replace agent names if needed such that the envy-order will be 1 > 2 > ... > n
    A.order_names()  
    # we can now assume that for each i,j such that i>j, the allocation is EF for i w.r.t j
    # in particular, the allocation is EF for agent 1

    # Step 2: Build a set of item-pairs whose replacement increases the envy-agents' utilities:
    A.update_exchangeable_items()
    exchangeable_pair = A.get_max_r_pair()

    # Step 3: Switch items in order until an EF1 allocation is found
    while True:
        if not A.is_EF1():
            A.exchange_pair(exchangeable_pair)
            A.update_exchangeable_items()
            exchangeable_pair = A.get_max_r_pair()
        else: 
            print(A, " is EF1!")
            if stopOnEF1:
                return A
        # TODO: add here some stoping condition
                

utilities = [[(-1,0,-1),(-4,-1,-1),(-5,-2,-3)],
            [(-4,-1,0),(-5,-3,-2),(-6,-4,-6)],
            [(-2,-6,-7),(-4,-6,-7)]]
capacities = (1, 2, 1)  # capacity constraints
n = 3
I = Instance(utilities, capacities, n)
algorithm1(I)