from Allocation import *
from Instance import *


allocation_dict = {} 
NODE_COUNT = 0
PREV_NODE = None


def update_allocation_dict(key):
    global NODE_COUNT
    if key not in allocation_dict:
        allocation_dict[key] = NODE_COUNT  # the value is also unique
        value = NODE_COUNT
        NODE_COUNT += 1
        flag = True  # the key is new in the dictionary (a new allocation)
    else:
        value = allocation_dict[key]  # already exists in the allocations dictionary
        flag = False
    return value, flag


def algorithm1(I):
    """
    Implemantation of our algorithm from the paper: https://arxiv.org/pdf/2205.07779.pdf
    with an intuitive extension to n agents.
    :param I: a problem instance
    """
    # Step 1: Find a w-maximal feasible allocation that is EF for some agent.
    w = tuple([1/I.n]*I.n)  # a tuple of initial agents' weights (all equal)
    A = W_maximal_allocation(I, w)  # (A1, A2, ..., An), ∀i, Ai is of type list
    # print("A = ", A.A)
    global PREV_NODE
    key = ' '.join(map(str, A.A))  # Note that this key is unique for each allocation, since we arranged it.
    value, flag = update_allocation_dict(key)  # flag must to be true in the first allocation
    PREV_NODE = value
    if A.is_EF1():
        # print('\n', A.A, " is EF1!\n")
        return A
        
    # Step 2: Build a set of item-pairs whose replacement increases the envy-agents' utilities:
    A.update_exchangeable_items(print=False)
    i, j, exchangeable_pair = A.get_max_r_pair()

    # Step 3: Switch items in order until an EF1 allocation is found
    flag = True
    while flag:  # while we discover new allocations
        if not A.is_EF1():
            A.exchange_pair(i, j, exchangeable_pair)
            # print("exchange ", exchangeable_pair, " between ", i, " and ", j)
            # print("\nupdated A = ", A.A)
            key = ' '.join(map(str, A.A))
            value, flag = update_allocation_dict(key)
            # check if the new allocation is w-maximal. if no - Lemma 4.11 is not true for n agents!
            if not A.is_w_maximal():
                print("Got an allocation that is not w-maximal :(")
                return None
            A.update_exchangeable_items(print=False)
            PREV_NODE = value  # update previous node for the next iteration
            i, j, exchangeable_pair = A.get_max_r_pair()
        if A.is_EF1(): 
            # print('\n', A.A, " is EF1!\n")
            return A
    print("No EF1 allocation was found :(")
    return None