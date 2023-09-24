'''
Project Meta-Details:
This is a data structures and algorithms project I worked on over the summer of 2023
This project utilized knowledge of graphs, stacks, breadth-first search algorithm, and multiprocessing
The run time for this program is approximately 1:45
Note: For this program to run on a computer:
    the word_list.100000.txt file in the same github repository as this program must be downloaded into the same directory as this file
'''

'''
Game Overview: 
Transform one word into another word of the same length
Only change one letter at a time
Given start word and end word, come up with a chain of words that transform startWord to endWord (Enter start and end word at the bottom)
'''


# Input: starting word, ending word
# Output: chain of words

# Make a graph with words as nodes and edges connected words that are different
# Use BFS between two words/nodes to find the quickest past from startWord to endWord

# Get list of words
# Make a word class
    # Attributes - Word, neighbors
    # Methods - get friends, discoveredBy, seen
# make new list of word nodes for each word
# Make an addFriend method
# Algorithm to check if 2 words are one letter apart
# Make 2 words friends if they are one letter apart

from multiprocessing import Process, Queue

class wordNode:
    def __init__(self, word):
        self._word=word
        self._neighbors=[]
        self._unseen=True
        self._discoveredby=0

    def getNeighbors(self):
        return self._neighbors

    def getWord(self):
        return self._word

    def setWord(self, word):
        self._word=word

    def isUnseen(self):
        if self._unseen:
            return True
        else:
            return False

    def setUnseenStatus(self, status):
        self._unseen=status

    def addNeighbor(self, nodeIndex):
        self._neighbors.append(nodeIndex)

    def setDiscoveredby(self, wordNodeIndex):
        self._discoveredby=wordNodeIndex

    def getDiscoveredby(self):
        return self._discoveredby

# Each process will add word pair to the multiprocessor queue, the main program will take them out and form links/neighbors
def addNeighbors(words, q, starti, endi):
    for i in range(starti, endi):
        print(i)
        for j in range(i+1, len(words)):
            # Compare words[i] and words[j]
            if isNeighbor(words[i].getWord(), words[j].getWord()):
                q.put((i,j))

# isNeighbor takes in 2 words and returns true if they are 1 letter apart
def isNeighbor(word1, word2):
    numSimilar=0
    if len(word1)!=len(word2):
        return False
    for i in range(len(word1)):
        if word1[i:i+1]==word2[i:i+1]:
            numSimilar+=1
    if (len(word1)-1)==numSimilar:
        return True
    return False


class queue:
    def __init__(self):
        self._queue=[]

    def enqueue(self, node):
        self._queue.append(node)

    def dequeue(self):
        return self._queue.pop(0)

    def isEmpty(self):
        return len(self._queue)==0

    def getQueue(self):
        return self._queue


def BFS(wordNodes, startWord, endWord):
    startWordIndex=None
    endWordIndex=None
    for i in range(len(wordNodes)):
        if wordNodes[i].getWord()==startWord:
            startWordIndex=i
        if wordNodes[i].getWord()==endWord:
            endWordIndex=i
    checkList = queue()
    wordNodes[startWordIndex].setUnseenStatus(False)
    checkList.enqueue(startWordIndex)
    while not checkList.isEmpty():
        myNode=checkList.dequeue()
        wordNodes[myNode].setUnseenStatus(False)
        if myNode==endWordIndex:
            return findPath(endWordIndex, startWordIndex)
        else:
            for i in wordNodes[myNode].getNeighbors():
                if wordNodes[i].isUnseen() and i not in checkList.getQueue():
                    wordNodes[i].setDiscoveredby(myNode)
                    checkList.enqueue(i)

def findPath(endNode, startNode):
    # Return path from startNode to endNode
    path=[]
    myNode=endNode
    while myNode!=startNode:
        if len(path)<1:
            path.append(myNode)
        else:
            path2=[]
            path2.append(myNode)
            for i in path:
                path2.append(i)
            path=path2
        myNode=wordNodes[myNode].getDiscoveredby()

    path2 = []
    path2.append(word_list[startNode])
    for i in path:
        path2.append(word_list[i])
    path = path2
    return path


if __name__=='__main__':
    word_list = []
    myDict = open("word_list.100000.txt", "r")
    for line in myDict:
        word_list.append(line.strip())
    wordNodes = []
    for i in word_list:
        wordNodes.append(wordNode(i))

    # The multiprocessor queue is used for getting data that is useful from the processes because direct returning is impossible
    q=Queue()
    processList=[]

    for i in range(0, len(wordNodes)-100, 100):
        p=Process(target=addNeighbors, args=(wordNodes, q, i, i+100))
        processList.append(p)
    p=Process(target=addNeighbors, args=(wordNodes, q, len(wordNodes)-len(wordNodes)%100, len(wordNodes)))
    processList.append(p)

    for p in processList:
        p.start()

    while not q.empty():
        i,j=q.get()
        wordNodes[i].addNeighbor(j)
        wordNodes[j].addNeighbor(i)

    for p in processList:
        # Join makes sure that all processes are finished before moving forward
        p.join()

    while not q.empty():
        i,j=q.get()
        wordNodes[i].addNeighbor(j)
        wordNodes[j].addNeighbor(i)

    print("\nPath: ")
    # Enter start_word and end_word
    print(BFS(wordNodes, "begin", "stops"))