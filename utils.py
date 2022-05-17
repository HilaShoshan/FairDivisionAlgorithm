import networkx as nx


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