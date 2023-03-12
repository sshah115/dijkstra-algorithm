'''
Name    : Shail Kiritkumar Shah
UID     : 119340547
Course  : ENPM661 - Planning
Task    : Project-2
github link : https://github.com/sshah115/dijkstra-algorithm.git

'''

# Importing all necessary modules/libraries for computation
import numpy as np
import cv2 as cv
from queue import PriorityQueue
import math as m
import time as tm

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
    hexPts = np.array([[300,50], [365, 87.5], [365,162.5], 
                       [300,200], [235, 162.5], [235, 87.5]], np.int32)
    polyShap(arena, hexPts, orange, "Obstacle")
    hexBorPts = np.array([[300,45], [369, 87.5], [369,162.5], 
                          [300,205], [235, 162.5], [235, 87.5]], np.int32)
    polyShap(arena, hexBorPts, white, "Border")
    triPts = np.array([[460, 25], [460, 225], [510,125]], np.int32)
    polyShap(arena, triPts, red, "Obstacle")
    triBorPts = np.array([[456, 20], [456, 230], [514,125]], np.int32)
    polyShap(arena, triBorPts, white, "Border")

    return arena

# Checking coordinates if it lies in obstacle space
def chckCoor(startPt, endPt):
    # This function will check if the points are okay, on border or
    # inside obstacle
    if canvas[(249 -startPt[1]), startPt[0]].any() == np.array([0, 0, 0]).all():
        if canvas[(249 - endPt[1]), endPt[0]].any() == np.array([0, 0, 0]).all():
            print("Processing!!!")
            status = True
        elif canvas[(249 - endPt[1]), endPt[0]].all() == np.array([255, 255, 255]).all():
            print("The goal coordinate is on border")
            status = False
        else:
            print("The goal coordinate is inside obstacle")
            status = False 
    elif canvas[(249 -startPt[1]), startPt[0]].all() == np.array([255, 255, 255]).all():
        print("The start coordinate is on border")
        status = False
    else:
        print("The start coordinate is inside obstacle")
        status = False 
    return status

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

# main code stub for node object initialization and backtracking
global canvas
que = PriorityQueue()
visSet = set([])
nodeObj = {}
# Generating map
canvas = genMap()
videoStr = []
# Checking user input if it is on border or inside any obstacle
status = False
while not status:
    strtNode = [int(ele) for ele in input("Enter starting coordinates: ").split(" ")]
    goalNode = [int(ele) for ele in input("Enter goal coordinates: ").split(" ")]
    status = chckCoor(strtNode, goalNode)

# Starting time for calculation algorithm time
start_t = tm.time()

# Initializing cost to come as infinite initially for all coordinates
cstCome = {}
for i in range(250):
    for j in range(600):
        cstCome[str([i, j])] = m.inf

# Cost to come for initial node to be zero
cstCome[str(strtNode)] = 0
# Adding first node to visited set
visSet.add(str(strtNode))
node = Node(strtNode, 0, None)
nodeObj[str(node.position)] = node
# Using Queue for putting cost and position as it will help in getting
# node with least cost first by default
que.put([node.cost, node.position])

iter = 0
# Running the loop until the queue is empty
while not que.empty():
    # Fetching node with least cost
    queNode = que.get()
    node = nodeObj[str(queNode[1])]
    if queNode[1][0] == goalNode[0] and queNode[1][1] == goalNode[1]:
        nodeObj[str(goalNode)] = Node(goalNode, queNode[0], node)
        break
    
    # Finding neighbors
    for neighNode, neighCost in eigConNeigh(node):

        # Checking if the neighbor is already in visited set
        if str(neighNode) in visSet:
            # If yes then updating only if less than cost to come
            neighUpdCost = neighCost + cstCome[str(node.position)]
            if neighUpdCost<cstCome[str(neighNode)]:
                cstCome[str(neighNode)] = neighUpdCost
                nodeObj[str(neighNode)].parent = node
            
        else:
            visSet.add(str(neighNode))
            canvas[(249 - neighNode[1]), neighNode[0], :] = np.array([0, 255, 0])

            if iter%1000 == 0:
                videoStr.append(canvas.copy())
                cv.imshow("Dijkstra Algorithm", canvas)
                cv.waitKey(1)

            updCost = neighCost + cstCome[str(node.position)]
            cstCome[str(neighNode)] = updCost
            nxtNode = Node(neighNode, updCost, nodeObj[str(node.position)])
            que.put([updCost, nxtNode.position])
            nodeObj[str(nxtNode.position)] = nxtNode
    iter += 1

# Backtracking algorithm
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
    videoStr.append(canvas.copy())
    cv.imshow("Dijkstra Algorithm", canvas)
    cv.waitKey(1)

end_t = tm.time()

print("Total time taken to find the optimal path: {:.2f}".format(end_t - start_t), " seconds")

# Video writing stub
clip = cv.VideoWriter(
    'dijkstra.mp4', cv.VideoWriter_fourcc(*'MP4V'), 25, (600, 250))

for idx in range(len(videoStr)):
    frame = videoStr[idx]
    clip.write(frame)
clip.release()

print("Clip stored at terminal's directory path")
