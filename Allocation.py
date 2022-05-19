from cmath import inf
import numpy as np
import matplotlib.pyplot as plt
from Utils import *
from itertools import permutations, combinations


class W_maximal_allocation: 
    """
    This class representing an w-maximal allocation A = (A1, A2, ..., An)
    This allocation is updating in the class's methdods
    """

    def __init__(self, I, w):
        self.I = I  # problem instance
        self.w = w  # agents' weights
        self.A = self.get_w_maximal_allocation(w)  # the allocation
        self.item_pairs = {}  # all the exchangeable pairs whose replacement will benefit the jealous agents
        self.init_envy_graph()


    def init_envy_graph(self):
        self.fig = plt.figure(figsize=(8,6))
        self.envy_graph = nx.DiGraph()
        # add nodes representing the agents
        for i in range(self.I.n):
            self.envy_graph.add_node(i, name=i)
        # self.envy_graph.add_nodes_from(np.arange(self.I.n))  
        self.save_envy_graph()


    def get_w_maximal_allocation(self, w, plotGraph=False):
        """
        returns a w-maximal matching by a maximum weighted matching in Gw graph.
        :param w: a tuple in form w = (w1, w2, ..., wn)
        :param utilities: a list of lists of tuples in form
                        [
                            [(u1(o_1,1),...,un(o_1,1)), ..., (u1(o_1,|C1|),...,un(o_1,|C1|))],   // C1
                            ... , 
                            [(u1(o_k,1),...,un(o_k,1)), ..., (u1(o_1,|Ck|),...,un(o_1,|Ck|))]    // Ck
                        ]
        :param s: a list of size k of capacity constraints, s = (s1, s2, ..., sk)
        """
        G, V1, V2 = create_G(w, self.I.utilities, self.I.s)
        if plotGraph:
            pos = dict()
            pos.update((n, (1, i)) for i, n in enumerate(V1))  # put nodes from V1 at x=1
            pos.update((n, (2, i)) for i, n in enumerate(V2))  # put nodes from V2 at x=2
            nx.draw(G, pos=pos, with_labels=True)
            plt.show()
        matching = nx.max_weight_matching(G, maxcardinality=True)
        return get_allocation(self.I.n, matching)


    def is_EF1(self):
        pairs = list(permutations(np.arange(self.I.n), 2))  # all the pairs of agents, with an importance to the order
        for pair in pairs: 
            i = pair[0]
            j = pair[1]
            uiAi_lst = utility_bundle(i, self.A[i], self.I.utilities)
            uiAj_lst = utility_bundle(i, self.A[j], self.I.utilities)
            if not isEF1_two(sum(uiAi_lst), sum(uiAj_lst), min(uiAi_lst), max(uiAj_lst)):
                return False
        return True    


    def add_exchangeable_pairs_two(self, i, j):
        for oi in self.A[i]:
            for oj in self.A[j]:
                # check if both items are in the same category
                oi_category, oi_idx = get_category_and_index(oi)
                oj_category, oj_idx = get_category_and_index(oj)
                if oi_category != oj_category:
                    continue
                # check if j preferes oi
                ujoi = utility_item(j, oi, self.I.utilities)
                ujoj = utility_item(j, oj, self.I.utilities)
                if ujoi > ujoj:
                    key = str(i) + "," + str(j)
                    if key not in self.item_pairs.keys():
                        self.item_pairs[key] = [(oi, oj)]
                    else: 
                        value = self.item_pairs[key]
                        value.append(tuple((oi, oj)))  # add this pair to the value list
                        self.item_pairs[key] = value  # update it in the dictionary

                    
    def save_envy_graph(self):
        pos = nx.spring_layout(self.envy_graph)
        nx.draw(self.envy_graph, pos, node_size=1000, node_color='yellow', font_size=8, font_weight='bold', with_labels=True)
        plt.savefig("EnvyGraph.png", format="PNG")
        plt.close()


    def update_exchangeable_items(self):
        """
        Create a set of exchangeable pairs whose replacement will benefit the envy agents' utilities.
        It is actually a dictionary in form {
                                                'i,j': [(),(),...]  # here j envious i
                                                ...
                                            }
        i.e., the keys are the pairs of agents that the exchangeable pairs belong to them,
        and the values are lists of exchangeable pairs that benefit agent j (the jealous one).
        """
        pairs = list(permutations(np.arange(self.I.n), 2))  
        for pair in pairs: 
            i = pair[0]
            j = pair[1]
            ujAj_lst = utility_bundle(j, self.A[j], self.I.utilities)
            ujAi_lst = utility_bundle(j, self.A[i], self.I.utilities)
            if not isEF_two(sum(ujAj_lst), sum(ujAi_lst)):  # j envious i
                # find all the exchangeable pairs that can benefit him
                print(j, "envious ", i)
                self.add_exchangeable_pairs_two(i, j)
                self.envy_graph.add_edge(j, i)  # a directed edge from j to i, that represents that j envious i
                print("updated exchangeable pairs list:\n", self.item_pairs)
                self.save_envy_graph()


    def get_max_r_pair(self):
        """
        Find the pair with the maximal r value among all the exchangeable pairs (in self.item_pairs).
        :return: the pair with the maximal r value and the agents that should replace it.
                 Specificaly, the function returns i,j,(oi,oj) s.t. oi∈Ai, oj∈Aj
        """
        max_i = -1
        max_j = -1
        max_oi = None
        max_oj = None
        max_r = -inf
        for key in self.item_pairs.keys():  # key = agents pair
            i = int(key.split(",")[0])
            j = int(key.split(",")[1])
            pairs_list = self.item_pairs[key]
            for pair in pairs_list:
                oi = pair[0]
                oj = pair[1]
                r = compute_r(i, j, oi, oj, self.I.utilities)
                if r > max_r:
                    max_r = r
                    max_i = i
                    max_j = j
                    max_oi = oi
                    max_oj = oj
        return max_i, max_j, (max_oi, max_oj)


    def exchange_pair(self, i, j, exchangeable_pair):
        """
        exchange the given pair between agents i and j
        """
        oi = exchangeable_pair[0]
        oj = exchangeable_pair[1]
        oi_idx = self.A[i].index(oi)  # the index of oi in A[i]
        oj_idx = self.A[j].index(oj)  # the index of oj in A[j]
        self.A[i][oi_idx] = oj
        self.A[j][oj_idx] = oi