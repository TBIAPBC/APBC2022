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


class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.sequences = []
        self.path = []
        self.visited = []
        self.frequency = dict()

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

        if len(self.path) == len(self.edges):
            seq = sequence(self.path)
            if seq not in self.sequences:
                self.sequences.append(seq)

        for neighbour in v.edges:
            for currentEdge in self.getEdges(v, neighbour):
                if currentEdge not in self.visited:
                    self.visited.append(currentEdge)
                    self.path.append(currentEdge)
                    self.findEulerianPath(neighbour, n)
                    self.visited.remove(currentEdge)
                    self.path.pop()

    def getEdges(self, v, neighbour):
        edgeList = []
        for edge in self.edges:
            if (edge.v1.name == v.name) & (
                    edge.v2.name == neighbour.name):
                edgeList.append(edge)
        return edgeList

    def createAdjacencyList(self, sequence, k):
        # create distinct kLet set
        kLetList = {sequence[i:i + k - 1] for i in range(len(sequence) - k + 2)}

        # create vertex list
        self.vertices = [Vertex(kLet) for kLet in kLetList]

        # create adjacency list
        for kLet in range(len(sequence) - k + 1):
            subSeq = sequence[kLet:kLet + k - 1]
            subSeq_ = sequence[kLet + k - 1:kLet + (2 * (k - 1))]
            if len(subSeq_) == k - 1:
                vertex = [vertex for vertex in self.vertices if vertex.name == subSeq].pop()
                vertex_ = [vertex for vertex in self.vertices if vertex.name == subSeq_].pop()
                vertex.addEdge(vertex_)
                self.addEdge(Edge(subSeq + subSeq_, vertex, vertex_))
                vertex.outDegree += 1
                vertex_.inDegree += 1
        return self


def sequence(path):
    string = ''
    for i in range(len(path)):
        if len(string) == 0:
            string += f'{path[i].name}'
        else:
            string += f'{path[i].name[-1]}'
    return string.strip()


# util method to print the adjacency list
def printAdjacencyList(verticesList):
    for value in verticesList:
        string = f'{value.name} -> '
        for subject in value.edges:
            string += f'{subject.name} '
        print(string)


# util method to print the vertices
def printEdges(edgeList):
    for value in edgeList:
        string = f'{value.v1.name} '
        string += f'{value.v2.name} '
        print(string)


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
    # printAdjacencyList(graph.vertices)
    # printEdges(graph.edges)
    # print(graph.hasEulerianPath())

    if graph.hasEulerianPath():
        sequenceList = []
        for vertex in graph.vertices:
            graph.sequences, graph.visited, graph.path = [], [], []
            graph.findEulerianPath(vertex, n)
            sequenceList.extend(graph.sequences)
        print(*sequenceList, sep='\n')


if __name__ == '__main__':
    main()
