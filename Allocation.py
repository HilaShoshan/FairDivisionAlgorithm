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

    def __init__(self, I, w, save_images=True):
        self.I = I  # problem instance
        self.w = w  # agents' weights
        self.save_images = save_images
        self.A = self.get_w_maximal_allocation(w)  # the allocation
        self.all_item_pairs = {}  # all the exchangeable pairs
        self.item_pairs = {}  # all the exchangeable pairs whose replacement will benefit the jealous agents
        self.init_envy_graphs()


    def init_envy_graphs(self):
        """
        Create an empty envy graph & EF1 graph, which is a graph with nodes that represent the agents,
        and there is a directed edge from i to j iff i envious j in more than one item / in more than
        one good and one chore in the mixed instances.
        """
        self.envy_graph = nx.DiGraph()
        self.EF1_graph = nx.DiGraph()
        # add nodes representing the agents
        for i in range(self.I.n):
            self.envy_graph.add_node(i, name=i)
            self.EF1_graph.add_node(i, name=i)
        # self.envy_graph.add_nodes_from(np.arange(self.I.n))  
        if self.save_images:
            self.save_envy_graph()
            self.save_EF1_graph()


    def save_Gw(self, G, V1, V2):
        """
        Saving Gw graph in a bipartite graph position, as Gw.png in 'plots' directory
        """
        pos = dict()
        pos.update((n, (1, i)) for i, n in enumerate(V1))  # put nodes from V1 at x=1
        pos.update((n, (2, i)) for i, n in enumerate(V2))  # put nodes from V2 at x=2
        nx.draw(G, pos=pos, with_labels=True)
        plt.savefig("plots/Gw.png", format="PNG")
        plt.close()


    def get_w_maximal_allocation(self, w):
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
        if self.save_images:
            self.save_Gw(G, V1, V2)
        matching = nx.max_weight_matching(G, maxcardinality=True)
        return get_allocation(self.I.n, matching, self.I.s)


    def is_EF1(self):
        """
        A boolean method, that checks if the allocation is EF1 -- for same-sign instances,
        or is it's EF[1,1] -- fot general mixed instances.
        """
        pairs = list(permutations(np.arange(self.I.n), 2))  # all the pairs of agents, with an importance to the order
        for pair in pairs: 
            i = pair[0]
            j = pair[1]
            uiAi_lst = utility_bundle(i, self.A[i], self.I.utilities)
            uiAj_lst = utility_bundle(i, self.A[j], self.I.utilities)
            if self.I.type == 'same-sign':
                if not isEF1_two(sum(uiAi_lst), sum(uiAj_lst), min(uiAi_lst), max(uiAj_lst)):
                    return False
            elif self.I.type == 'mixed':
                if not isEF11_two(sum(uiAi_lst), sum(uiAj_lst), min(uiAi_lst), max(uiAj_lst)):
                    return False
        return True  


    def is_EF(self):
        pairs = list(permutations(np.arange(self.I.n), 2))  # all the pairs of agents, with an importance to the order
        for pair in pairs: 
            i = pair[0]
            j = pair[1]
            uiAi_lst = utility_bundle(i, self.A[i], self.I.utilities)
            uiAj_lst = utility_bundle(i, self.A[j], self.I.utilities)
            if not isEF_two(sum(uiAi_lst), sum(uiAj_lst)):
                return False
        return True    


    def add_exchangeable_pairs_two(self, i, j, all=False):
        # print("add_exchangeable_pairs_two\n i,j = ", i, j, '\n Ai = ', self.A[i], '\n Aj = ', self.A[j])
        for oi in self.A[i]:
            for oj in self.A[j]:
                # check if both items are in the same category
                oi_category, oi_idx = get_category_and_index(oi)
                oj_category, oj_idx = get_category_and_index(oj)
                if oi_category != oj_category:
                    continue
                key = str(i) + "," + str(j)
                if all:
                    if key not in self.all_item_pairs.keys():
                        self.all_item_pairs[key] = [(oi, oj)]
                    else:
                        value = self.all_item_pairs[key]
                        value.append(tuple((oi, oj)))  # add this pair to the value list
                        self.all_item_pairs[key] = value  # update it in the dictionary
                else:
                    # check if j preferes oi
                    ujoi = utility_item(j, oi, self.I.utilities)
                    ujoj = utility_item(j, oj, self.I.utilities)
                    if ujoi > ujoj:
                        if key not in self.item_pairs.keys():
                            self.item_pairs[key] = [(oi, oj)]
                        else: 
                            value = self.item_pairs[key]
                            value.append(tuple((oi, oj)))  # add this pair to the value list
                            self.item_pairs[key] = value  # update it in the dictionary

                    
    def save_envy_graph(self):
        pos = nx.spring_layout(self.envy_graph)
        nx.draw(self.envy_graph, pos, node_size=1000, node_color='yellow', font_size=8, font_weight='bold', with_labels=True)
        plt.savefig("plots/EnvyGraph.png", format="PNG")
        plt.close()


    def save_EF1_graph(self):
        pos = nx.spring_layout(self.EF1_graph)
        nx.draw(self.EF1_graph, pos, node_size=1000, node_color='orange', font_size=8, font_weight='bold', with_labels=True)
        plt.savefig("plots/EF1Graph.png", format="PNG")
        plt.close()


    def update_exchangeable_items(self, to_print=True):
        """
        Create two sets of exchangeable pairs, and save them as class's fields.
        1) self.item_pairs: all the exchangeable pairs whose replacement will benefit the envy agents' utilities.
        It is actually a dictionary in form {
                                                'i,j': [(),(),...]  # here j envious i
                                                ...
                                            }
        i.e., the keys are the pairs of agents that the exchangeable pairs belong to them,
        and the values are lists of exchangeable pairs that benefit agent j (the jealous one).
        2) self.all_item_pairs: all the exchangeable pairs in this allocation. 
        Has similar form as self.item_pairs. Used in "is_w_maximal" method.
        """
        pairs = list(permutations(np.arange(self.I.n), 2))  
        for pair in pairs: 
            i = pair[0]
            j = pair[1]
            self.add_exchangeable_pairs_two(i, j, all=True)  # add to self.all_item_pairs
            ujAj_lst = utility_bundle(j, self.A[j], self.I.utilities)
            ujAi_lst = utility_bundle(j, self.A[i], self.I.utilities)
            if not isEF_two(sum(ujAj_lst), sum(ujAi_lst)):  # j envious i
                # find all the exchangeable pairs that can benefit j
                if to_print:
                    print(j, "envious ", i)
                self.add_exchangeable_pairs_two(i, j, all=False)  # add to self.item_pairs
                self.envy_graph.add_edge(j, i)  # a directed edge from j to i, that represents that j envious i
                if to_print:
                    print("updated exchangeable pairs list:\n", self.item_pairs)
                if self.save_images:
                    self.save_envy_graph()

            # update the EF1 graph
            if self.I.type == 'same-sign':
                if not isEF1_two(sum(ujAj_lst), sum(ujAi_lst), min(ujAj_lst), max(ujAi_lst)):
                    self.EF1_graph.add_edge(j, i)  # add a directed edge from j to i
            elif self.I.type == 'mixed':
                if not isEF11_two(sum(ujAj_lst), sum(ujAi_lst), min(ujAj_lst), max(ujAi_lst)):
                    self.EF1_graph.add_edge(j, i)  # add a directed edge from j to i
            if self.save_images:
                self.save_EF1_graph()


    def get_max_r_pair(self):
        """
        Find the pair with the maximal r value among all the exchangeable pairs of some agents in 
        which one envious the other in more than one item (or more than one good and one chore).
        :return: this pair with the maximal r value and the agents that should replace it.
                 Specifically, the function returns i,j,(oi,oj) s.t. oi???Ai, oj???Aj
        """
        max_i = -1
        max_j = -1
        max_oi = None
        max_oj = None
        max_r = -inf
        # print("____________________________________")
        EF1_edges = list(self.EF1_graph.edges)  # all the edges in the current EF1_graph, if the allocation is not EF1, it must has at least one edge
        if len(EF1_edges) == 0:  # empty edge list --> the allocation is EF1 --> we won't exchange this pair anyway!
            return -1, -1, (None, None)
        j, i = EF1_edges[0]  # take the first pair, TODO: think what to do if there are some edges
        key = str(i) + ',' + str(j)
        pairs_list = self.item_pairs[key]
        for pair in pairs_list:
            oi = pair[0]
            oj = pair[1]
            r = compute_r(i, j, oi, oj, self.I.utilities)
            # print("r(", i, ",", j, ",", oi, ",", oj, ") = ", r)
            if r > max_r:
                max_r = r
                max_i = i
                max_j = j
                max_oi = oi
                max_oj = oj
        # print("maximum: ", max_i, max_j, (max_oi, max_oj), max_r)
        # print("____________________________________")
        return max_i, max_j, (max_oi, max_oj)


    def exchange_pair(self, i, j, exchangeable_pair):
        """
        exchange the given pair between agents i and j
        """
        # update the allocation
        oi = exchangeable_pair[0]
        oj = exchangeable_pair[1]
        oi_idx = self.A[i].index(oi)  # the index of oi in A[i]
        oj_idx = self.A[j].index(oj)  # the index of oj in A[j]
        self.A[i][oi_idx] = oj
        self.A[j][oj_idx] = oi

        # arrange the allocation
        self.A = tuple(arrange_A(self.I.n, list(self.A), self.I.s))
    

    def empty_fields(self):
        """
        this function is called before we find the new exchangeable items 
        (in a new allocation after the exchange)
        """
        # empty item-pairs lists
        self.item_pairs = {}
        self.all_item_pairs = {}

        # delete edges from the envy graphs
        edges = list(self.envy_graph.edges)  # all the edges in the current envy_graph
        self.envy_graph.remove_edges_from(edges)
        edges = list(self.EF1_graph.edges)  # all the edges in the current EF1_graph
        self.EF1_graph.remove_edges_from(edges)


    def is_w_maximal(self):
        """
        Check if allocation A is w-maximal, according to Lemma 4.7 in our paper [i <--> iii].
        Specifically, we check the following:
        1. for each exchangable pair (oi, oj) s.t. ui(oi) = ui(oj), uj(oj) >= uj(oi)
        2. there exists some w ??? R such that
            all the r(i,j,oi,oj) of (oi,oj) with ui(oi) < ui(oj), greater or equal to w,
            and
            all the r(i,j,oi,oj) of (oi,oj) with ui(oi) > ui(oj), smaller or equal to w.
            (all the r values of the first group are greater than all the r-values of the second group --> 
            the minimum of the first group is greater than the maximum of the second group).
        """
        min_group1 = inf  # the maximal r-value of a pair from the group of pairs with ui(oi) < ui(oj)
        max_group2 = -inf  # the minimal r-value of a pair from the group of pairs with ui(oi) > ui(oj)
        print("CHECKING W-MAXIMALITY...")
        # print("all_item_pairs is: ", self.all_item_pairs)
        for key in self.all_item_pairs.keys():  # key = agents pair (i,j)
            i = int(key.split(",")[0])
            j = int(key.split(",")[1])
            # print("i, j: ", i, j)
            pairs_list = self.all_item_pairs[key]
            # if i == 0 and j == 2:
                # print(pairs_list)
            for pair in pairs_list:
                oi = pair[0]
                oj = pair[1]
                uioi = utility_item(i, oi, self.I.utilities)
                uioj = utility_item(i, oj, self.I.utilities)
                ujoi = utility_item(j, oi, self.I.utilities)
                ujoj = utility_item(j, oj, self.I.utilities)
                if uioi == uioj and ujoj < ujoi:  # not uj(oj) >= uj(oi)
                    print("FAILED in first condition:\n i, j, oi, oj, uioi, uioj, ujoj, ujoi = ", i, j, oi, oj, uioi, uioj, ujoj, ujoi)
                    return False
                else:
                    r = compute_r(i, j, oi, oj, self.I.utilities)
                    if uioi < uioj:  # group1
                        # print("group1, r = ", r)
                        if r < min_group1:
                            min_group1 = r  # update min
                            # if r == 0.26666666666666666:
                            #     print("i, j, oi, oj, r: ", i, j, oi, oj, r)
                    else:  # uioi > uioj -- group2
                        # print("group2, r = ", r)
                        if r > max_group2:
                            max_group2 = r  # update max
                            # if r == 1.3513513513513513:
                            #     print("i, j, oi, oj, r: ", i, j, oi, oj, r)
            if min_group1 < max_group2:  # not min group1 >= max_group2
                print("FAILED in second condition:\n i, j, max_group2, min_group1 = ", i, j, max_group2, min_group1)
                return False
            else:
                print(max_group2, " <= w", i, "/ w", j, " <= ", min_group1)
                min_group1 = inf 
                max_group2 = -inf
        return True  # all the conditions of Lemma 4.7(iii) are true for all the pairs i!=j