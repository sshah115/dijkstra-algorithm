'''
Name    : Shail Kiritkumar Shah
UID     : 119340547
Course  : ENPM661 - Planning
Task    : Project-2

'''

# Importing all necessary modules/libraries for computation
import numpy as np
import cv2 as cv
from queue import PriorityQueue
import math as m

# Drawing polyline shapes
def polyShap(img, polyPts, color, type):
    polyPts = polyPts.reshape((-1,1,2))
    if type == "Obstacle":
        cv.fillPoly(img,[polyPts],color)
    else:
        cv.polylines(img,[polyPts],True,color, thickness = 5)

# Function to generate map with obstacles using cv functions
def genMap():

    # Generating a black background arena
    arena = np.zeros((250,600, 3), dtype="uint8")
    
    # Defining colors
    white = (255,255,255)
    blue = (255, 0, 0)
    orange = (0, 165, 255)
    red = (0, 0, 255)

    # Drawing rectangle obstacles and image border
    cv.rectangle(arena, (100,0), (150,100), blue, -1)
    cv.rectangle(arena, (100,0), (150,100), white, 5)
    cv.rectangle(arena, (100,150), (150,250), blue, -1)
    cv.rectangle(arena, (100,150), (150, 250), white, 5)
    cv.rectangle(arena, (-1, -1), (599, 249), white, 10)

    # Drawing all polygon shaped obstacles
    hexPts = np.array([[235, 87.5], [235, 162.5], [300,200], 
                       [365,162.5], [365, 87.5], [300,50]], np.int32)
    polyShap(arena, hexPts, orange, "Obstacle")
    hexBorPts = np.array([[235, 87.5], [235, 162.5], [300,205], 
                          [369,162.5], [369, 87.5], [300,45]], np.int32)
    polyShap(arena, hexBorPts, white, "Border")
    triPts = np.array([[460, 25], [460, 225], [510,125]], np.int32)
    polyShap(arena, triPts, red, "Obstacle")
    triBorPts = np.array([[456, 20], [456, 230], [514,125]], np.int32)
    polyShap(arena, triBorPts, white, "Border")

    return arena

# Defining node class to allot coordinate, cost and parent to-
# node object for ease of computation and efficient backtracking
class Node:
    def __init__(self,position,cost,parent):
        self.position = position
        self.cost = cost
        self.parent = parent

# Functions to compute eight connected neighbours using different functions-
# as specified in project guideline

# Function to move up
def movUp(curPos):
    curPos[1] += 1
    return curPos, 1

# Function to move down
def movDow(curPos):
    curPos[1] -= 1
    return curPos, 1

# Function to move right
def movRig(curPos):
    curPos[0] += 1
    return curPos, 1

# Function to move left
def movLef(curPos):
    curPos[0] -= 1
    return curPos, 1

# Function to move up-right
def movUpRig(curPos):
    curPos[0] += 1
    curPos[1] += 1
    return curPos, 1.4

# Function to move up-left
def movUpLef(curPos):
    curPos[0] -= 1
    curPos[1] += 1
    return curPos, 1.4

# Function to move down-right
def movDowRig(curPos):
    curPos[0] += 1
    curPos[1] -= 1
    return curPos, 1.4

# Function to move down-left
def movDowLef(curPos):
    curPos[0] -= 1
    curPos[1] -= 1
    return curPos, 1.4

# Function to check feasibility of computed neighbors in terms of its location-
# and subsequently appenging it to a list only if the coordinate's value is zero-
# which is possible exploration space
def feasAppd(curPos):
    nxtNeigh = []
    for ele in curPos:
        if ele[0][1]>=0 and ele[0][1]<250 and ele[0][0]>=0 and ele[0][0]<600:
            if canvas[(249 - ele[0][1]), ele[0][0]].all() == np.array([0, 0, 0]).all():
                nxtNeigh.append([ele[0], ele[1]])
    return nxtNeigh

# Function to accept node coordinate and generate next neighbor list for each node
def eigConNeigh(node):
    curPos = [node.position[0], node.position[1]]
    conNeighList = [movUp(curPos.copy()), movDow(curPos.copy()),
                    movRig(curPos.copy()), movLef(curPos.copy()),
                    movUpRig(curPos.copy()), movDowRig(curPos.copy()),
                    movUpLef(curPos.copy()), movDowLef(curPos.copy())]
    
    nxtNeigh = feasAppd(conNeighList)
    return nxtNeigh

global canvas
que = PriorityQueue()
visSet = set([])
nodeObj = {}
canvas = genMap()
strtNode = [6,6]
goalNode = [500,200]

cstCome = {}
for i in range(250):
    for j in range(600):
        cstCome[str([i, j])] = m.inf

cstCome[str(strtNode)] = 0
visSet.add(str(strtNode))
node = Node(strtNode, 0, None)
nodeObj[str(node.position)] = node
que.put([node.cost, node.position])

iter = 0
while not que.empty():
    queNode = que.get()
    node = nodeObj[str(queNode[1])]
    if queNode[1][0] == goalNode[0] and queNode[1][1] == goalNode[1]:
        nodeObj[str(goalNode)] = Node(goalNode, queNode[0], node)
        break
    
    for neighNode, neighCost in eigConNeigh(node):

        if str(neighNode) in visSet:
            neighUpdCost = neighCost + cstCome[str(node.position)]
            if neighUpdCost<cstCome[str(neighNode)]:
                cstCome[str(neighNode)] = neighUpdCost
                nodeObj[str(neighNode)].parent = node
            
        else:
            visSet.add(str(neighNode))
            canvas[(249 - neighNode[1]), neighNode[0], :] = np.array([0, 255, 0])

            if iter%1000 == 0:
                cv.imshow("Dijkstra Algorithm", canvas)
                cv.waitKey(1)

            updCost = neighCost + cstCome[str(node.position)]
            cstCome[str(neighNode)] = updCost
            nxtNode = Node(neighNode, updCost, nodeObj[str(node.position)])
            que.put([updCost, nxtNode.position])
            nodeObj[str(nxtNode.position)] = nxtNode
    iter += 1

bckTrackNode = nodeObj[str(goalNode)]
prntNode = bckTrackNode.parent
bckTrackLst = []

while prntNode:
    bckTrackLst.append([(249 - prntNode.position[1]), prntNode.position[0]])
    prntNode = prntNode.parent

# bckTrackLst = sorted(bckTrackLst, key=lambda x: x[1])
bckTrackLst.reverse()

for val in bckTrackLst:
    canvas[val[0], val[1], :] = np.array([255, 0, 0])
    cv.imshow("Dijkstra Algorithm", canvas)
    cv.waitKey(1)
    