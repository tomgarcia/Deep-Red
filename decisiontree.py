import sys
import numpy as np
from scipy import stats

class DecisionTree:

    def __init__(self, data, schema):
        self.root = DecisionTree.make_node(data, schema, list(range(1, len(schema))))

    @staticmethod
    def make_node(data, schema, indices):
        cls = data[0][0]
        if np.all(data[:,0] == cls):
            return cls
        if len(indices) == 0:
            return stats.mode(data[:,0])[0][0]
        branches = []
        index = 0
        min_entropy = sys.maxsize
        for i in indices:
            avg_entropy = 0
            for value in range(schema[i]):
                subset = data[data[:, i] == value]
                if len(subset) == 0:
                    continue
                subset = subset[:,0]
                entropy = 0
                for cls in range(schema[0]):
                    p = np.sum(subset == cls) / len(subset)
                    if p == 0:
                        continue
                    info = -1 * np.log(p)
                    entropy += p * info
                # Don't divide by len(data) because it's the same for all indices
                avg_entropy += entropy * len(subset)
            if avg_entropy < min_entropy:
                index = i
                min_entropy = avg_entropy
        indices.remove(index)
        for value in range(schema[index]):
            subset = data[data[:,index] == value]
            if subset.size == 0:
                branches.append(stats.mode(data[:,0])[0][0])
            else:
                branches.append(DecisionTree.make_node(subset, schema, indices))
        indices.append(index) # indices is pass by reference, so we need to restore it
        return DecisionTree.Node(branches, index-1)

    def __call__(self, sample):
        ptr = self.root
        while isinstance(ptr, DecisionTree.Node):
            ptr = ptr.branches[sample[ptr.index]]
        return ptr

    class Node:

        def __init__(self, branches, index):
            self.branches = branches
            self.index = index
