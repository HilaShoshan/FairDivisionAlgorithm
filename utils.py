from cmath import inf
import networkx as nx
import re


def create_G(w, utilities, s):
    """
    create Gw graph using the weights and the utilities and return it.
    """
    n = len(w)  # number of agents
    G = nx.Graph()
    V1 = []  # agents 
    V2 = []  # items
    for c in range(len(utilities)):  # for each category
        category = utilities[c]
        num_dummies = n*s[c] - len(category)  # preproccesing 
        for j in range(len(category) + num_dummies):  # for each item in this category
            if j < len(category):  # it's a real item
                item = "o_" + str(c) + "," + str(j)  # item name
            else:  # dummy item
                item = "d_" + str(c) + "," + str(j)
            V2.append(item)
            for i in range(n):  # for each agent
                for d in range(s[c]):  # duplicate each agent s_c times
                    if j < len(category):
                        weight = utilities[c][j][i] * w[i]  # edge weight
                    else:
                        weight = 0
                    agent = "Agent_" + str(i) + "_" + str(c) + "_" + str(d)  # a unique name for each copy
                    if agent not in V1:
                        V1.append(agent)
                    G.add_edge(agent, item, weight=weight)
    return G, V1, V2


def recognize_agent_and_item(match):
    first = match[0].split("_")[0]  # the first char in the first element
    if first == "o" or first == "d":  # the first is the item
        item = match[0]
        agent = int(match[1].split("_")[1])
    else:  # the second is the item
        item = match[1]
        agent = int(match[0].split("_")[1])
    return agent, item


def is_dummy(item):
    """
    :param item: a string in form o_c_j or d_c_j, 
                 where o representing a real item and d representing a dummy item.
    :return: true if the item is a dummy item, else return false.
    """
    type = item.split("_")[0]
    if type == "d":
        return True
    return False 
    

def get_category_and_index(item):
    """
    :param item: a string in form o_c_j (or d_c_j), 
                 where c representing the category and j representing the index of the item in category c.
    :return: c and j
    """
    splitted = item.split("_")[1].split(",")
    c = int(splitted[0])
    j = int(splitted[1])
    return c, j


def arrange_categories(allocation, capacities):
    """
    :param allocation: the bundle of some agent in some allocation, sorted by categories indices
    :param capacities: the capacity constraint of each category
    :return: a list of lists of all the items that the agent gets from each category, 
                that is also sorted according to the items' indices.
                The indices representing by the second number in each item name, 
                i.e. o_c,j --> c is the (common) category, and j is the index. 
    """
    start = 0
    categories = [] 
    # separate into categories 
    for s_c in capacities:  # each agent gets exactly s_c items from each category C_c
        categories.append(allocation[start: start + s_c])
        start += s_c
    # sort each category by the items' indices
    for i in range(len(categories)):
        categories[i].sort(key = lambda category : list(map(int, re.findall(r'\d+', category)))[1])
    return categories


def arrange_A(n, A, capacities):
    """
    Arrange the allocation such that the items in each sub-allocation Ai are arranged in a way 
    that the categories are arranged by their indices, and also the items in each category.
    This ensures that equivalent allocations are written in a unique way, according to this order.
    :param n: the number of agents 
    :param A: an allocation as a list
    :param capacities: the capacities for each category
    :return: the arranged allocation as a list
    """
    for agent in range(n):
        allocation = A[agent]
        allocation.sort(key = lambda allocation : list(map(int, re.findall(r'\d+', allocation)))[0])
        categories = arrange_categories(allocation, capacities)
        A[agent] = [item for sublist in categories for item in sublist]
    return A


def get_allocation(n, matching, capacities):
    # print(matching)
    A = list(list() for _ in range(n))  # an empty allocation in form A = (A1, A2, ..., An)
    for match in matching:
        agent, item = recognize_agent_and_item(match)
        A[agent].append(item)
        # print("item ", item, " appended to agent ", agent, " allocation.")
    A = arrange_A(n, A, capacities)
    return tuple(A)


def isEF1_two(first, second, worst, best):
    """
    :param first: some agent's utility on his bundle
    :param second: first's utility on other agent's bundle
    :param worst: the most difficult chore on first's bundle (in his eyes)
    :param best: the most valuable good in second's bundle (in the first's eyes)
    :return: true if the first envious the second up to one item
    (i.e. the allocation is EF1 for first w.r.t second)
    """
    if first-worst >= second or first >= second-best:
        return True
    return False


def isEF11_two(first, second, worst, best):
    """
    :param first: some agent's utility on his bundle
    :param second: first's utility on other agent's bundle
    :param worst: the most difficult chore on first's bundle (in his eyes)
    :param best: the most valuable good in second's bundle (in the first's eyes)
    :return: true if the first envious the second up to one good and one chore
    """
    if first-worst >= second-best:
        return True
    return False


def isEF_two(first, second):
    """
    :param first: some agent's utility on his bundle
    :param second: first's utility on other agent's bundle
    :return: true if the first does not envy the second
    """
    if first >= second:
        return True
    return False


def utility_bundle(agent, bundle, utilities):
    """
    :param agent: agent index
    :param bundle: some bundle (Ai)
    :return: a list containing the agent's utility values on each item in the bundle
    """
    res = []
    for item in bundle:
        if is_dummy(item):
            res.append(0)
        else:  # a real item
            category_indx, item_indx = get_category_and_index(item)
            res.append(utilities[category_indx][item_indx][agent])
    return res


def utility_item(agent, item, utilities):
    """
    :param agent: agent index
    :param item: some item
    :return: the utility of the given agent over the given item
    """
    category, idx = get_category_and_index(item)
    if is_dummy(item):
        return 0
    return utilities[category][idx][agent]


def compute_r(i, j, oi, oj, utilities):
    """
    computes the difference ratio r (by definition 4.6):
    r(i,j,oi,oj) = [uj(oi)-uj(oj)] / [ui(oi)-ui(oj)]
    """
    # numerator elements
    ujoi = utility_item(j, oi, utilities)
    ujoj = utility_item(j, oj, utilities)
    if ujoi == ujoj:  # first edge case
        return 0
    # denominator elements
    uioi = utility_item(i, oi, utilities)
    uioj = utility_item(i, oj, utilities)
    if uioi == uioj:  # second edge case
        if ujoi > ujoj:
            return inf
        else:  # ujoi < ujoj
            return -inf
    # ratio
    return (ujoi-ujoj) / (uioi-uioj)