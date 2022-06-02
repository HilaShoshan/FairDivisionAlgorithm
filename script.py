"""
This script is checking a lot of arbitrary utilities for an instance with 3 agents,
in order to (maybe) find a counterexample for Lemma 4.11, or for the algorithm. 
I.e., finding an allocation that is EF1 but not w-maximal, or do not find an EF1 allocation!
"""

import random
import math

from base_algorithm import *


def get_category(m):
    """
    :param m: the number of items in the category
    :return: a category with m items and random utilities for the 3 agents.
    """
    return list(
        (
            (
                random.randint(-100, 100),
                random.randint(-100, 100),
                random.randint(-100, 100),
            )
            for k in range(m)
        )
    )


n = 3
num_categories = random.randint(1, 10)
utilities = []
capacities = []
for c in range(num_categories):
    m = random.randint(2, 10)
    utilities.append(get_category(m))
    s_c = random.randint(int(math.ceil(m/n)), m)
    capacities.append(s_c)

capacities = tuple(capacities)

print(num_categories)
print(utilities)
print(capacities, "\n_______________________________________________\n")

I = Instance(utilities, capacities, n, type='mixed')
algorithm1(I)
