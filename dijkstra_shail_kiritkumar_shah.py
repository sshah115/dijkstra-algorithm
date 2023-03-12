'''
Name    : Shail Kiritkumar Shah
UID     : 119340547
Course  : ENPM661 - Planning
Task    : Project-2

'''

# Importing all necessary modules/libraries for computation
import numpy as np
import cv2 as cv

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

    cv.imshow("Preview", arena)
    cv.waitKey(0)

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

canvas = genMap()

node = Node([10, 10], 0, None)
result = eigConNeigh(node)

print(result)
