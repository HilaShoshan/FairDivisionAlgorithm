from Allocation import *
from Instance import *


def update_allocations_graph(key):
    global NODE_COUNT
    if key not in allocations_dict:
        color_map.append('gray')
        allocations_dict[key] = NODE_COUNT  # the value is also unique
        allocations_graph.add_node(NODE_COUNT, name=NODE_COUNT)  # add a new node to the graph
        value = NODE_COUNT
        NODE_COUNT += 1
        flag = True  # the key is new in the dictionary (a new allocation)
    else:
        value = allocations_dict[key]  # already exists in the allocations dictionary
        flag = False
    return value, flag


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
    print("A = ", A.A)
    global PREV_NODE
    if not stopOnEF1:  # debug mode
        key = ' '.join(map(str, A.A))  # TODO: if items indices are different, this should be the same key!
        value, flag = update_allocations_graph(key)  # flag must to be true in the first allocation
        PREV_NODE = value
    if A.is_EF1():
        print(A.A, " is EF1!")
        if stopOnEF1:
            return A
        else:
            color_map[-1] = 'pink'  # update the color of the node of the EF1 allocation to pink (instead of gray)

    # Step 2: Build a set of item-pairs whose replacement increases the envy-agents' utilities:
    A.update_exchangeable_items()
    i, j, exchangeable_pair = A.get_max_r_pair()

    # Step 3: Switch items in order until an EF1 allocation is found
    while True:
        # print("NODE_COUNT: ", NODE_COUNT, "\nPREV_NODE: ", PREV_NODE)
        if not A.is_EF1():
            A.exchange_pair(i, j, exchangeable_pair)
            print("exchange ", exchangeable_pair, " between ", i, " and ", j)
            print("updated A = ", A.A)
            if not stopOnEF1:  # debug
                key = ' '.join(map(str, A.A))
                value, flag = update_allocations_graph(key)
                # TODO: add edge color determines by a topological ordering on the envy graph
                allocations_graph.add_edge(PREV_NODE, value)  # edge that spesifies we moved from the previous allocation to the current one
                PREV_NODE = value  # update previous node for the next iteration
                # a stoping condition to the debug mode
                if not flag:  # we back to an allocation we already found (and the algorithm is deterministic) 
                    return A
            A.update_exchangeable_items()
            i, j, exchangeable_pair = A.get_max_r_pair()
        else: 
            print(A.A, " is EF1!")
            if stopOnEF1:
                return A
            else:  # if flag ?
                color_map[-1] = 'pink'  # update the color of the node of the EF1 allocation to pink (instead of gray)
                

# 2 agents
"""
C1: clean the house
    o_0,0: floor sweep
    o_0,1: floor wash
    o_0,2: do dishes
    o_0,3: clean the oven
    o_0,4: windows
    o_0,5: clean furniture from dust, include mirrors
    o_0,6: clean toilet and sink in bathroom
agent0 = hatif haben: ['o_0,5', 'o_0,6', 'o_0,0', 'd_0,7']
agent1 = hatif habutt: ['o_0,3', 'o_0,4', 'o_0,1', 'o_0,2'] 
"""
# utilities = [[(-100,-50),(0,0),(-900,0),(-30,-1),(-60,-5),(0,-6),(-12,-10)]]
# capacities = tuple([4])
# n = 2

# 3 agents
utilities = [[(-1,0,-1),(-4,-1,-1),(-5,-2,-3)],
            [(-4,-1,0),(-5,-3,-2),(-6,-4,-6)],
            [(-2,-6,-7),(-4,-6,-7)]]
capacities = (1, 2, 1)  # capacity constraints
n = 3

I = Instance(utilities, capacities, n)

# the allocations graph is specific for 3 agents case
allocations_graph = nx.Graph()
colors_dict = {
    '1>2>3' : 'red',
    '1>3>2' : 'blue',
    '2>1>3' : 'yellow',
    '2>3>1' : 'black',
    '3>1>2' : 'purple',
    '3>2>1' : 'green'
}
allocations_dict = {} 
NODE_COUNT = 0
PREV_NODE = None
color_map = []

algorithm1(I, stopOnEF1=False)

nx.draw(allocations_graph, node_size=1000, font_size=8, font_weight='bold', node_color=color_map, with_labels=True)
plt.savefig("AllocationsGraph.png", format="PNG")
plt.close()
