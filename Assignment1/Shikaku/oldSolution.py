import glob
import time
import numpy as np
from math import sqrt
from copy import deepcopy


global rows
global cols
global puzzle
global locationData
global locationDataFactor
global stack
global checkedNodes
global state
global lastCells


def readPuzzle(inputFilename):
    global rows, cols, puzzle, locationData, stack, checkedNodes
    locationData = []
    with open(inputFilename, "r") as inputFile:
        rows = int(inputFile.readline())
        cols = int(inputFile.readline())
        puzzle = [cols * [""] for i in range(rows)]
        for row, line in enumerate(inputFile):
            for col, symbol in enumerate(line.split()):
                if symbol == "-":
                    puzzle[row][col] = -1
                else:
                    locationData.append((row, col, int(symbol)))
                    puzzle[row][col] = len(locationData)-1
        stack = [{"value": deepcopy(puzzle), "index": 0}]
        checkedNodes = []


def factors():
    global locationData, locationDataFactor
    locationDataFactor = []
    for data in locationData:
        value = data[2]
        current = []
        bound = round(sqrt(value))+1
        for i in range(1, int(bound)):
            if value % i == 0:
                if i == value//i:
                    # current.append(i)
                    current.insert(0, i)
                else:
                    # current.append(i)
                    # current.append(value//i)
                    current.insert(0, i)
                    current.insert(0, value//i)
        locationDataFactor.append(current)


def printGrid(grid):
    for row in grid:
        for symbol in row:
            print(str(symbol).rjust(4), end='')
        print("")


def checkEmptyStack():
    global stack
    if len(stack) == 0:
        return True
    return False


def removeFormStack():
    global stack, checkedNodes
    firstNode = stack.pop(0)
    checkedNodes.append(firstNode)
    return firstNode


def insertToStack(node):
    global stack
    stack.insert(0, node)


def verifySolution(selectedNode):
    global rows, cols, puzzle, locationData
    for i, (row, col, val) in enumerate(locationData):
        if selectedNode[row][col] != i:
            return False

        eWhere = [(r, c) for r in range(rows)
                  for c in range(cols) if selectedNode[r][c] == i]
        eNum = len(eWhere)

        if eNum != val:
            return False

        left = min(eWhere, key=lambda x: x[0])[0]
        right = max(eWhere, key=lambda x: x[0])[0]
        top = min(eWhere, key=lambda x: x[1])[1]
        bottom = max(eWhere, key=lambda x: x[1])[1]
        area = (right-left+1) * (bottom-top+1)
        if area != eNum:
            return False
    return True


def checkValid(L, r1, r2, c1, c2):
    numRows = len(L)
    numCols = len(L[0])
    if (r1 > r2 or c1 > c2):
        return False
    if (r1 < 0 or c1 < 0):
        return False
    if (r2 >= numRows or c2 >= numCols):
        return False
    return True


def checkValidWithValue(L, r1, r2, c1, c2, value, value2):
    assert(r1 <= r2)
    assert(c1 <= c2)
    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            if L[r][c] != value and L[r][c] != value2:
                return False
    return True


def setValue(L, r1, r2, c1, c2, value):
    assert(r1 <= r2)
    assert(c1 <= c2)
    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            L[r][c] = value


def extendNode(selectedNode, index):
    global locationData, locationDataFactor, lastCells
    listNewPuzzles = []
    if (index >= len(locationData)):
        return listNewPuzzles
    eRow = locationData[index][0]
    eCol = locationData[index][1]
    eValue = locationData[index][2]
    facList = locationDataFactor[index]
    for fac in facList:
        for i in range(eValue//fac):
            for j in range(fac):
                newPuzzle = deepcopy(selectedNode)
                if checkValid(newPuzzle, eRow-j, eRow+fac-1-j, eCol+i-eValue//fac+1, eCol+i):
                    if checkValidWithValue(newPuzzle, eRow-j, eRow+fac-1-j, eCol+i-eValue//fac+1, eCol+i, -1, index):
                        setValue(newPuzzle, eRow-j, eRow+fac -
                                 1-j, eCol+i-eValue//fac+1, eCol+i, index)
                        notCover = False
                        for z in range(len(lastCells[index])):
                            r = lastCells[index][z][0]
                            c = lastCells[index][z][1]
                            if newPuzzle[r][c] == -1:
                                notCover = True
                                break
                        if notCover == False:
                            listNewPuzzles.append(
                                {"value": newPuzzle, "index": index+1})
    return listNewPuzzles


def notInArray(value, list):
    for element in list:
        if np.array_equal(value, element["value"]):
            return False
    return True


def initialization():
    global locationData, locationDataFactor, count, rows, cols, lastCells

    factors()

    state = [[-1 for c in range(cols)] for r in range(rows)]
    for i in range(len(locationData)):
        state[locationData[i][0]][locationData[i][1]] = i

    for z in range(len(locationData)):
        eRow = locationData[z][0]
        eCol = locationData[z][1]
        eValue = locationData[z][2]
        faclist = locationDataFactor[z]
        for fac in faclist:
            for i in range(eValue//fac):
                for j in range(fac):
                    if checkValid(state, eRow-j, eRow+fac-1-j, eCol+i-eValue//fac+1, eCol+i):
                        setValue(state, eRow-j, eRow+fac-1-j,
                                 eCol+i-eValue//fac+1, eCol+i, z)

    lastCells = [[]for i in range(len(locationData))]
    for row in range(rows):
        for col in range(cols):
            value = state[row][col]
            lastCells[value].append([row, col])


if __name__ == "__main__":
    fileNames = sorted(glob.glob("inputTest/*.txt"))
    for fileName in fileNames:
        readPuzzle(fileName)
        print(fileName)
        startTime = time.time()
        initialization()
        while True:
            if checkEmptyStack():
                endTime = time.time()
                print(
                    f"No Solution Found after {endTime - startTime} seconds!!!")
                break
            selectedNode = removeFormStack()
            if verifySolution(selectedNode["value"]):
                endTime = time.time()
                print(f"Solution Found in {endTime - startTime} seconds")
                printGrid(selectedNode["value"])
                break
            newNodes = extendNode(selectedNode["value"], selectedNode["index"])

            if len(newNodes) > 0:
                for newNode in newNodes:
                    if notInArray(newNode["value"], stack) and notInArray(newNode["value"], checkedNodes):
                        insertToStack(newNode)
