from multiprocessing import Process, Queue
from collections import deque

class wordNode:
    def __init__(self, word):
        # Initialize wordNode with a word, an empty list of neighbors, and unseen status
        self._word = word
        self._neighbors = []
        self._unseen = True
        self._discoveredby = 0

    def getNeighbors(self):
        # Return the list of neighbors of the wordNode
        return self._neighbors

    def getWord(self):
        # Return the word of the wordNode
        return self._word

    def setWord(self, word):
        # Set the word of the wordNode
        self._word = word

    def isUnseen(self):
        # Check if the wordNode is unseen
        return self._unseen

    def setUnseenStatus(self, status):
        # Set the unseen status of the wordNode
        self._unseen = status

    def addNeighbor(self, nodeIndex):
        # Add a neighbor to the wordNode
        self._neighbors.append(nodeIndex)

    def setDiscoveredby(self, wordNodeIndex):
        # Set the discovered-by attribute of the wordNode
        self._discoveredby = wordNodeIndex

    def getDiscoveredby(self):
        # Get the discovered-by attribute of the wordNode
        return self._discoveredby

# Each process will add word pair to the multiprocessor queue, the main program will take them out and form links/neighbors
def addNeighbors(words, q, starti, endi):
    for i in range(starti, endi):
        print(i)
        for j in range(i + 1, len(words)):
            # Compare words[i] and words[j], add to queue if neighbors
            if isNeighbor(words[i].getWord(), words[j].getWord()):
                q.put((i, j))

# isNeighbor takes in 2 words and returns true if they are 1 letter apart
def isNeighbor(word1, word2):
    numSimilar = 0
    if len(word1) != len(word2):
        return False
    for i in range(len(word1)):
        if word1[i:i + 1] == word2[i:i + 1]:
            numSimilar += 1
    return (len(word1) - 1) == numSimilar

class queue:
    def __init__(self):
        # Initialize a deque
        self._queue = deque()

    def enqueue(self, node):
        # Add an element to the deque
        self._queue.append(node)

    def dequeue(self):
        # Remove and return the leftmost element from the deque
        return self._queue.popleft()

    def isEmpty(self):
        # Check if the deque is empty
        return len(self._queue) == 0

    def getDeque(self):
        # Return the deque
        return self._queue

def BFS(wordNodes, startWord, endWord):
    startWordIndex = None
    endWordIndex = None
    for i in range(len(wordNodes)):
        # Find indices of startWord and endWord
        if wordNodes[i].getWord() == startWord:
            startWordIndex = i
        if wordNodes[i].getWord() == endWord:
            endWordIndex = i
    checkList = queue()
    wordNodes[startWordIndex].setUnseenStatus(False)
    checkList.enqueue(startWordIndex)
    while not checkList.isEmpty():
        myNode = checkList.dequeue()
        wordNodes[myNode].setUnseenStatus(False)
        if myNode == endWordIndex:
            return findPath(endWordIndex, startWordIndex, wordNodes)
        else:
            for i in wordNodes[myNode].getNeighbors():
                if wordNodes[i].isUnseen() and i not in checkList.getDeque():
                    wordNodes[i].setDiscoveredby(myNode)
                    checkList.enqueue(i)

def findPath(endNode, startNode, wordNodes):
    # Return path from startNode to endNode
    path = []
    myNode = endNode
    while myNode != startNode:
        if len(path) < 1:
            path.append(myNode)
        else:
            path2 = []
            path2.append(myNode)
            for i in path:
                path2.append(i)
            path = path2
        myNode = wordNodes[myNode].getDiscoveredby()

    path2 = []
    path2.append(word_list[startNode])
    for i in path:
        path2.append(word_list[i])
    path = path2
    return path

if __name__ == '__main__':
    word_list = []
    myDict = open("word_list.100000.txt", "r")
    for line in myDict:
        word_list.append(line.strip())
    wordNodes = []
    for i in word_list:
        wordNodes.append(wordNode(i))

    # The multiprocessor queue is used for getting data that is useful from the processes because direct returning is impossible
    q = Queue()
    processList = []

    for i in range(0, len(wordNodes) - 100, 100):
        p = Process(target=addNeighbors, args=(wordNodes, q, i, i + 100))
        processList.append(p)
    p = Process(target=addNeighbors, args=(wordNodes, q, len(wordNodes) - len(wordNodes) % 100, len(wordNodes)))
    processList.append(p)

    for p in processList:
        p.start()

    while not q.empty():
        i, j = q.get()
        wordNodes[i].addNeighbor(j)
        wordNodes[j].addNeighbor(i)

    for p in processList:
        # Join makes sure that all processes are finished before moving forward
        p.join()

    while not q.empty():
        i, j = q.get()
        wordNodes[i].addNeighbor(j)
        wordNodes[j].addNeighbor(i)

    print("\nPath: ")
    # Enter start_word and end_word
    print(BFS(wordNodes, "begin", "stops"))
