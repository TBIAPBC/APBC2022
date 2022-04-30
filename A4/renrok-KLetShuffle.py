import copy
import random
import sys


class Edge:
    def __init__(self, name, v1, v2):
        self.name = name
        self.v1 = v1
        self.v2 = v2


class Vertex:
    def __init__(self, name):
        self.name = name
        self.edges = []
        self.inDegree = 0
        self.outDegree = 0

    def addEdge(self, v):
        self.edges.append(v)

    def shuffleEdges(self):
        length = len(self.edges)
        for i in range(length - 1):
            j = random.randint(i, length - 1)
            (self.edges[i], self.edges[j]) = (self.edges[j], self.edges[i])
        return self


class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.sequences = []
        self.path = []
        self.visited = []
        self.sumEdges = 0

    def addEdge(self, edge):
        self.edges.append(edge)

    def hasEulerianPath(self):
        count = []
        for vertex in self.vertices:
            if vertex.inDegree is not vertex.outDegree:
                count.append(vertex)
        if len(count) != 2:
            return False

        if not ((count[0].outDegree == count[0].inDegree + 1) | (count[0].inDegree == count[0].outDegree + 1)):
            return False

        if not ((count[0].outDegree == count[0].inDegree + 1) | (count[0].inDegree == count[0].outDegree + 1)):
            return False

        return True

    def findEulerianPath(self, v, n):

        if len(self.sequences) == n:
            return

        if len(self.path) == self.sumEdges:
            self.sequences.append(sequence(self.path))

        for edge in v.edges:
            if edge not in self.visited:
                self.visited.append(edge)
                self.path.append(edge)
                self.findEulerianPath(edge.v2, n)
                self.visited.remove(edge)
                self.path.pop()

    def createAdjacencyList(self, sequence, k):
        # create distinct k-let set
        kLetList = {sequence[i:i + k - 1] for i in range(len(sequence) - 1)}

        # create vertex list
        self.vertices = [Vertex(kLet) for kLet in kLetList]

        # create adjacency list
        for i in range(len(sequence) - k + 1):
            subSeq = sequence[i:i + k - 1]
            subSeq_ = sequence[i + 1:i + k]
            if len(subSeq_) == k - 1:
                vertex = [vertex for vertex in self.vertices if vertex.name == subSeq].pop()
                vertex_ = [vertex for vertex in self.vertices if vertex.name == subSeq_].pop()
                vertex.addEdge(Edge(subSeq + subSeq_[-1], vertex, vertex_))
                self.sumEdges += 1
                vertex.outDegree += 1
                vertex_.inDegree += 1
        return self

    def shuffleEdges(self):
        for vertex in self.vertices:
            vertex.shuffleEdges()


# util method to get the sequence from an edge list
def sequence(path):
    string = ''
    for i in range(len(path)):
        if len(string) == 0:
            string += f'{path[i].name}'
        else:
            string += f'{path[i].name[-1]}'
    return string.strip()


def main():
    n = 0
    k = 0

    if "N" in sys.argv[1]:
        n = int(sys.argv[2])

    if "k" in sys.argv[3]:
        k = int(sys.argv[4])

    with open(sys.argv[5], 'r', encoding="utf-8") as reader:
        inputSequence = reader.read().strip()

    graph = Graph()
    graph.createAdjacencyList(inputSequence, k)

    sequenceCount = 0
    sequenceList = []
    while sequenceCount < n:
        currentGraph = copy.deepcopy(graph)
        # shuffle all edges of all vertices, since the dfs in findEulerianPath always starts with the first edge in
        # the list
        currentGraph.shuffleEdges()
        if currentGraph.hasEulerianPath():
            # start vertex should have odd degree and at least one out going edge
            startVertices = [vertex for vertex in currentGraph.vertices if
                             ((vertex.inDegree + vertex.outDegree) % 2 != 0) & (vertex.outDegree > 0)]
            for vertex in startVertices:
                currentGraph.visited, currentGraph.path = [], []
                currentGraph.findEulerianPath(vertex, n)
                sequenceList.extend(currentGraph.sequences)
            sequenceCount = len(sequenceList)
    print(*sequenceList[:n], sep='\n')


if __name__ == '__main__':
    main()
