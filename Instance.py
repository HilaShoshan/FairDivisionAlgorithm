
class Instance:
    """
    This class representing an instance of a fair division problem,
    as defined in our paper
    """
    def __init__(self, utilities, capacities, n, type='same-sign'):
        """
        :param n: number of agents
        :param utilities: a list of lists of tuples in form
                    [
                        [(u1(o_1,1),...,un(o_1,1)), ..., (u1(o_1,|C1|),...,un(o_1,|C1|))],   // C1
                        ... , 
                        [(u1(o_k,1),...,un(o_k,1)), ..., (u1(o_1,|Ck|),...,un(o_1,|Ck|))]    // Ck
                    ]
        :param capacities: a list of size k of capacity constraints, s = (s1, s2, ..., sk)
        """
        self.n = n  # number of agents
        self.type = type  # 'same-sign' or 'mixed'
        self.utilities = utilities
        self.s = capacities
        self.k = len(utilities)  # number of categories (equals to len(capacities))
        # total number of items
        self.m = 0  
        for j in range(self.k):
            self.m += len(utilities[j])  # add the category size 