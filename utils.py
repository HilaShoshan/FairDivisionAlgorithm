import networkx as nx


epsilon = 0.0001  # to solve numeric problems


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


def get_allocation(n, matching):
    # print(matching)
    A = tuple(list() for _ in range(n))  # an empty allocation in form A = (A1, A2, ..., An)
    for match in matching:
        agent, item = recognize_agent_and_item(match)
        A[agent].append(item)
        # print("item ", item, " appended to agent ", agent, " allocation.")
    return A


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


def utility(agent, bundle, utilities):
    """
    :param agent: agent index
    :param bundle: some bundle (Ai)
    :return: a list containing the agent's utility values on each item in the bundle
    """
    res = []
    for item in bundle:
        type = item.split("_")[0]  # a real item or a dummy
        if type == "d":
            res.append(0)
        else:  # "o"
            indices = item.split("_")[1].split(",")
            category_indx = int(indices[0])
            item_indx = int(indices[1])
            res.append(utilities[category_indx][item_indx][agent])
    return res