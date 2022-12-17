from _queue import Queue
from ast import literal_eval
import pandas as pd
import pdbr

# df = pd.read_pickle('data/data_small.pkl') 
df = pd.read_csv('data/player_teams_played_for_mmapping.csv') 

class Vertex:
	def __init__(self, key):
		self.id = key
		self.connectedTo = []
		self.discovered = False
		self.parent = None

	def addNeighbor(self, other):
		self.connectedTo.append(other)
		other.connectedTo.append(self)

	def __str__(self):
		return str(self.id) + " connectedTo: " + str([x.id for x in self.connectedTo])


class Graph:
	def __init__(self):
		self.vertList = {}
		self.numVertices = 0

	def addVertex(self, key):
		self.numVertices+=1
		newVertex = Vertex(key)
		self.vertList[key] = newVertex
		return newVertex

	def addEdge(self, f, t):
		if f not in self.vertList:
			self.addVertex(f)
		if t not in self.vertList:
			self.addVertex(t)
		self.vertList[f].addNeighbor(self.vertList[t])

	def getVertex(self, item):
		try:
			return self.vertList[item]
		except KeyError:
			return None

	def __iter__(self):
		return iter(self.vertList.values())

g = Graph()

for idx in range(len(df)):
    for team in  literal_eval(df.iloc[idx]['teams']):
        g.addEdge(df.iloc[idx]['player_name'], team)


def bfs(player_one:str, player_two:str) -> list:
    s = player_one
    e= player_two
    start = g.getVertex(s)
    end = g.getVertex(e)
    if not start:
        print(f"{s} not in graph")
        return []
    if not end:
        print(f"{e} not in graph")
        return []
    Q = Queue()
    start.discovered = True
    Q.push(start)

    while not Q.isEmpty():
        current = Q.pop()
        if current.id == end.id:
            break

        for neighbour in current.connectedTo:
            if not neighbour.discovered:
                neighbour.discovered = True
                neighbour.parent = current
                Q.push(neighbour)

    curr = end
    connection_result_list = []
    if curr.parent == None: return []
    while curr.parent is not None:
        connection_result_list.append(curr.id)
        curr = curr.parent
    connection_result_list.append(start.id)
    return connection_result_list

