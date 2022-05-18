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
        self.item_pairs = None


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
            uiAi_lst = utility(i, self.A[i], self.I.utilities)
            uiAj_lst = utility(i, self.A[j], self.I.utilities)
            if not isEF1_two(sum(uiAi_lst), sum(uiAj_lst), min(uiAi_lst), max(uiAj_lst)):
                return False
        return True    


    def replace_names(self, agent0, agent1):
        """
        replace the names of the given agents
        """
        # replace them in allocation A
        A_temp = list(self.A)
        temp = A_temp[agent0]
        A_temp[agent0] = A_temp[agent1]
        A_temp[agent1] = temp
        self.A = tuple(A_temp)

        # replace them in utilities list
        for c in range(self.I.k):  # for each category
            category = self.I.utilities[c]
            for j in range(len(category)):  # for each item in this category
                item_utilities = list(self.I.utilities[c][j])
                # replace
                temp = item_utilities[agent0]
                item_utilities[agent0] = item_utilities[agent1]
                item_utilities[agent1] = temp
                self.I.utilities[c][j] = tuple(item_utilities)


    def order_names_two(self):
        """
        A function for the special case of n=2 only.
        If 0 is the envious agent 1 (in the initial allocation), replace the names of agent 0 and agent 1
        """
        u0A0_lst = utility(0, self.A[0], self.I.utilities)
        u0A1_lst = utility(0, self.A[1], self.I.utilities)
        if not isEF_two(sum(u0A0_lst), sum(u0A1_lst)):  # 0 envious 1
            print("0 envious 1!")
            self.replace_names(0, 1)  
                

    def order_names(self):
        # TODO: fix it!
        """
        order agents' names such that in the (initial) allocation,
        agent 1 is not envy, and the envy-order is 1 > 2 > ... > n, 
        i.e. each agent i can be jealous only in agents j < i
        """
        print("Skip order_names method.")
        return
        pairs = list(combinations(np.arange(self.I.n), 2))  # all the pairs of agents (i, j) s.t. i < j
        hash = {}  # saving agents' names
        for i in range(3): 
            hash[i] = i
        for pair in pairs: 
            agent0 = pair[0]
            agent1 = pair[1]
            u0A0_lst = utility(agent0, A[agent0], self.I.utilities)
            u0A1_lst = utility(agent0, A[agent1], self.I.utilities)
            if not isEF_two(sum(u0A0_lst), sum(u0A1_lst)):  # agent0 envious agent1
                self.replace_names(agent0, agent1)  # replace the names of the agents
                hash[agent0] = agent1
                hash[agent1] = agent0


    def add_exchangeable_pairs_two(self, i, j):
        for oi in self.A[i]:
            for oj in self.A[j]:
                print(oi, oj)


    def update_exchangeable_items(self):
        """
        Create a set of exchangeable pairs whose replacement will benefit the envy agents' utilities.
        It is actually a dictionary in form {
                                                (i,j): [(),(),...]
                                                ...
                                            }
        i.e., the keys are the pairs of agents that the exchangeable pairs belong to them,
        and the values are lists of exchangeable pairs that benefit agent j (the jealous one).
        """
        pairs = list(combinations(np.arange(self.I.n), 2))  # all the pairs of agents (i, j) s.t. i < j
        for pair in pairs: 
            i = pair[0]
            j = pair[1]
            ujAj_lst = utility(j, self.A[j], self.I.utilities)
            ujAi_lst = utility(j, self.A[i], self.I.utilities)
            if not isEF_two(sum(ujAj_lst), sum(ujAi_lst)):  # j envious i
                # find all the exchangeable pairs that can benefit him
                self.add_exchangeable_pairs_two(i, j)


    def get_max_r_pair(self):
        """
        :param item_pairs: a list of exchangeable pairs
        :return: the pair with the maximal r value
        """
        pass


    def exchange_pair(self, exchangeable_pair):
        """
        exchange the given pair between the agents
        """
        pass