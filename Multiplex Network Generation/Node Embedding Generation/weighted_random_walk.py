import networkx as nx
import numpy as np
import random

def getTransitionMatrix(network, nodes):
	nodes = list(nodes)
	matrix = np.empty([len(nodes), len(nodes)])
    
	for i in range(0, len(nodes)):

		#print("Nodes: ", nodes[0])
		#neighs = network.neighbors(nodes[i])
		neighs = network[nodes[i]] # Replaced the above line with this line
		sums = 0
		#print("network[]: ", network[nodes[i]])
		for neigh in neighs:
			
			#print("weight: ", network[nodes[i]][neigh]['weight'])
			sums += network[nodes[i]][neigh]['weight']

		for j in range(0, len(nodes)):
			if i == j :
				matrix[i,j] = 0
			else:
				if nodes[j] not in neighs:
					matrix[i, j] = 0
				else:
					matrix[i, j] = network[nodes[i]][nodes[j]]['weight'] / sums

	return matrix

def generateSequence(startIndex, transitionMatrix, path_length, alpha):
	result = [startIndex]
	current = startIndex

	for i in range(0, path_length):
		if random.random() < alpha:
			nextIndex = startIndex
		else:
			# print("transitionMAtrix")
			# for row in transitionMatrix:
			# 	print(row)
			probs = transitionMatrix[current]
			nextIndex = np.random.choice(len(probs), 1, p=probs)[0]

		result.append(nextIndex)
		current = nextIndex

	return result

def random_walk(G, num_paths, path_length, alpha):
	nodes = G.nodes()
	nodes = list(nodes)
	transitionMatrix = getTransitionMatrix(G, nodes)

	sentenceList = []

	for i in range(0, len(nodes)):
		for j in range(0, num_paths):
			indexList = generateSequence(i, transitionMatrix, path_length, alpha)
			sentence = [int(nodes[tmp]) for tmp in indexList]
			sentenceList.append(sentence)

	return sentenceList