from Allocation import *
from Instance import *


def update_allocations_graph(key):
    """
    Add a new node that represent an allocation to the allocation_dict, if it does not exist yet. 
    """
    global NODE_COUNT
    if key not in allocation_dict:
        color_map.append('gray')
        allocation_dict[key] = NODE_COUNT  # the value is also unique
        allocations_graph.add_node(NODE_COUNT, name=NODE_COUNT)  # add a new node to the graph
        value = NODE_COUNT
        NODE_COUNT += 1
        flag = True  # the key is new in the dictionary (a new allocation)
    else:
        value = allocation_dict[key]  # already exists in the allocations dictionary
        flag = False
    return value, flag


def get_edge_color(EF1_graph):
    """
    :param EF1_graph: the EF1 graph of some allocation. 
                        Has to be a DAG graph, since all allocations are w-maximal.
    :return: an edge color determines by a topological ordering on the EF1 graph, and color_dict.
    """
    topological = list(nx.all_topological_sorts(EF1_graph))
    colors = []
    for order in topological:
        reversed_order = list(reversed(order))
        color = color_dict[str(reversed_order)]
        colors.append(color)
    return colors


def get_common(a, b):
    """
    Given two lists, returns an element which is common to both.
    If there is no such element, returns 'k' (black color)
    """
    a_set = set(a)
    b_set = set(b)
     
    # check length
    intersection = list(a_set.intersection(b_set))
    if len(intersection) > 0:
        return(intersection[0])  # return the first common element
    else:  # no common element
        return 'k'


def algorithm1(I, stopOnEF1=True):
    """
    Implemantation of our algorithm from the paper: https://arxiv.org/pdf/2205.07779.pdf
    with an intuitive extension to n agents
    :param I: a problem instance
    :param stopOnEF1: a boolean determining if we want to stop when an EF1 allocation is found
                        (as in the original algorithm),
                        or if we want to explore all the search-space (for debugging).
    """
    # Step 1: Find a w-maximal feasible allocation that is EF for some agent.
    w = tuple([1/n]*n)  # a tuple of initial agents' weights (all equal)
    A = W_maximal_allocation(I, w)  # (A1, A2, ..., An), ∀i, Ai is of type list
    print("A = ", A.A)
    global PREV_NODE
    key = ' '.join(map(str, A.A))  # Note that this key is unique for each allocation, since we arranged it.
    value, flag = update_allocations_graph(key)  # flag must to be true in the first allocation
    PREV_NODE = value
    if A.is_EF1():
        color_map[-1] = 'pink'  # update the color of the node of the EF1 allocation to pink (instead of gray)
        print('\n', A.A, " is EF1!\n")
        if stopOnEF1:
            return A
        
    # Step 2: Build a set of item-pairs whose replacement increases the envy-agents' utilities:
    if A.is_EF():  # no exchangeable pairs
        print('\n', A.A, " is EF!\n")
        return A
    A.update_exchangeable_items()
    i, j, exchangeable_pair = A.get_max_r_pair()

    # Step 3: Switch items in order until an EF1 allocation is found
    flag = True
    while flag:  # while we discover new allocations
        if not A.is_EF1() or not stopOnEF1:
            colors_before = get_edge_color(A.EF1_graph)  # the possible colors for the node of the current allocation (before the exchange)
            A.exchange_pair(i, j, exchangeable_pair)
            print("exchange ", exchangeable_pair, " between ", i, " and ", j)
            print("\nupdated A = ", A.A)
            key = ' '.join(map(str, A.A))
            value, flag = update_allocations_graph(key)
            A.update_exchangeable_items()
            colors_after = get_edge_color(A.EF1_graph)  # possible colors after the exchange
            edge_color = get_common(colors_before, colors_after)  # the common edge color before and after the exchange!
            print("colors_before: ", colors_before)
            print("colors_after: ", colors_after)
            print("color: ", edge_color)
            allocations_graph.add_edge(PREV_NODE, value, color=edge_color)  # edge that spesifies we moved from the previous allocation to the current one
            PREV_NODE = value  # update previous node for the next iteration
            if A.is_EF():  # no exchangeable pairs
                print('\n', A.A, " is EF!\n")
                return A
            i, j, exchangeable_pair = A.get_max_r_pair()
        if A.is_EF1(): 
            color_map[-1] = 'pink'
            print('\n', A.A, " is EF1!\n")
            if stopOnEF1:
                return A
    return A
                

# 3 agents
utilities = [[(-1,0,-1),(-4,-1,-1),(-5,-2,-3)],
            [(-4,-1,0),(-5,-3,-2),(-6,-4,-6)],
            [(-2,-6,-7),(-4,-6,-7)]]
capacities = (1, 2, 1)  # capacity constraints
n = 3

I = Instance(utilities, capacities, n, type='same-sign')

# this color dictionary is specific for 3 agents case
color_dict = {
    '[0, 1, 2]' : 'r',   # 0>1>2 --> red
    '[0, 2, 1]' : 'b',   # 0>2>1 --> blue
    '[1, 0, 2]' : 'y',   # 1>0>2 --> yellow
    '[1, 2, 0]' : 'g',   # 1>2>0 --> green
    '[2, 0, 1]' : 'm',   # 2>0>1 --> magenta 
    '[2, 1, 0]' : 'c'    # 2>1>0 --> cyan
}

allocations_graph = nx.Graph()
allocation_dict = {} 
NODE_COUNT = 0
PREV_NODE = None
color_map = []

stopOnEF1 = True
algorithm1(I, stopOnEF1)

edges = allocations_graph.edges()
colors = [allocations_graph[u][v]['color'] for u,v in edges]
nx.draw(allocations_graph, edgelist=edges, edge_color=colors, node_size=1000, font_size=8, font_weight='bold', node_color=color_map, with_labels=True)
plt.savefig("plots/AllocationsGraph.png", format="PNG")
plt.close()

print("_________________________allocation dictionary_________________________")
print(allocation_dict)
print("_______________________________________________________________________")
