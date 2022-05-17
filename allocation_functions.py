import numpy as np
import matplotlib.pyplot as plt
from utils import *
from itertools import permutations


epsilon = 0.0001  # to solve numeric problems


def get_w_maximal_allocation(w, utilities, s, plotGraph=False):
    """
    returns a w-maximal matching by a maximum weighted matching in Gw graph.
    :param w: a tuple in form w = (w1, w2, ..., wn)
    :param utilities: a list of tuples of tuples in form
                    [
                        ((u1(o_1,1),...,un(o_1,1)), ..., (u1(o_1,|C1|),...,un(o_1,|C1|))),   // C1
                        ... , 
                        ((u1(o_k,1),...,un(o_k,1)), ..., (u1(o_1,|Ck|),...,un(o_1,|Ck|)))    // Ck
                    ]
    :param s: a list of size k of capacity constraints, s = (s1, s2, ..., sk)
    """
    G, V1, V2 = create_G(w, utilities, s)
    if plotGraph:
        pos = dict()
        pos.update((n, (1, i)) for i, n in enumerate(V1))  # put nodes from V1 at x=1
        pos.update((n, (2, i)) for i, n in enumerate(V2))  # put nodes from V2 at x=2
        nx.draw(G, pos=pos, with_labels=True)
        plt.show()
    matching = nx.max_weight_matching(G, maxcardinality=True)
    return get_allocation(len(w), matching)


def is_EF1(A, utilities):
    n = len(A)  # number of agents
    pairs = list(permutations(np.arange(n), 2))  # all the pairs of agents
    for pair in pairs: 
        agent0 = pair[0]
        agent1 = pair[1]
        u0A0_lst = utility(agent0, A[agent0], utilities)
        u0A1_lst = utility(agent0, A[agent1], utilities)
        if not isEF1_two(sum(u0A0_lst), sum(u0A1_lst), min(u0A0_lst), max(u0A1_lst)):
            return False
    return True


def ordered(A):
    """
    :param A: an allocation
    :return: true if the envy-order equals to 1 > 2 > ... > n
             else reurn false
    """
    pass


def replace_names(A):
    """
    replace agents' names such that in the (initial) allocation,
    agent 1 is not envy, and 1 > 2 > ... > n
    """
    pass


def get_exchangeable_items(A):
    """
    returns a set of exchangeable pairs whose replacement will benefit the envy agents' utilities
    """
    pass


def get_max_r_pair(item_pairs):
    """
    gets a list of exchangeable pairs and returns the pair with the maximum r value
    """
    pass


def exchange_pair(exchangeable_pair):
    """
    exchange the given pair between the agents
    """
    pass