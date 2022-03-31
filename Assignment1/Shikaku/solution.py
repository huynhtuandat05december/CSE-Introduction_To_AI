
import glob
import time
from math import sqrt


global rows
global cols
global puzzle
global locationData
global state
global locationDataFactor
global count
global lastCells


def readPuzzle(inputFilename):
    global rows, cols, puzzle, locationData
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
                    puzzle[row][col] = int(symbol)
                    locationData.append((row, col, int(symbol)))


def verifySolution():
    global rows, cols, puzzle, locationData, state
    for i, (row, col, val) in enumerate(locationData):

        if state[row][col] != i:
            return False

        eWhere = [(r, c) for r in range(rows)
                  for c in range(cols) if state[r][c] == i]
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


def printGrid(grid):
    for row in grid:
        for symbol in row:
            print(str(symbol).rjust(4), end='')
        print("")


def factors():
    global locationData, locationDataFactor
    for anchor in locationData:
        value = anchor[2]
        current = []
        bound = round(sqrt(value))+1
        for i in range(1, int(bound)):
            if value % i == 0:
                if i == value//i:
                    current.append(i)
                else:
                    current.append(i)
                    current.append(value//i)
        locationDataFactor.append(current)
    return


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


def DFS(nextIndex):
    global rows, cols, puzzle, locationData, state, count, locationDataFactor, lastCells

    if nextIndex > len(locationData)-1:
        return True

    eRow = locationData[nextIndex][0]
    eCol = locationData[nextIndex][1]
    eValue = locationData[nextIndex][2]

    while count[nextIndex] < len(locationDataFactor[nextIndex]):
        facList = locationDataFactor[nextIndex]
        fac = facList[count[nextIndex]]
        for i in range(eValue//fac):
            for j in range(fac):
                if checkValid(state, eRow-j, eRow+fac-1-j, eCol+i-eValue//fac+1, eCol+i):
                    if checkValidWithValue(state, eRow-j, eRow+fac-1-j, eCol+i-eValue//fac+1, eCol+i, -1, nextIndex):
                        setValue(state, eRow-j, eRow+fac-1-j,
                                 eCol+i-eValue//fac+1, eCol+i, nextIndex)
                        notCover = False
                        for z in range(len(lastCells[nextIndex])):
                            r = lastCells[nextIndex][z][0]
                            c = lastCells[nextIndex][z][1]
                            if state[r][c] == -1:
                                notCover = True
                                break

                        if notCover == False:
                            if DFS(nextIndex+1) == True:
                                return True

                        setValue(state, eRow-j, eRow+fac-1-j,
                                 eCol+i-eValue//fac+1, eCol+i, -1)

                        state[locationData[nextIndex][0]
                              ][locationData[nextIndex][1]] = nextIndex
        count[nextIndex] += 1

    if nextIndex > 0:
        count[nextIndex] = 0


def initialization():
    global state, locationDataFactor, count, rows, cols, lastCells
    locationDataFactor = []
    factors()

    count = [0]*len(locationData)

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

    state = [[-1 for c in range(cols)] for r in range(rows)]
    for i in range(len(locationData)):
        state[locationData[i][0]][locationData[i][1]] = i


if __name__ == "__main__":
    fileNames = sorted(glob.glob("inputTable/*.txt"))
    for fileName in fileNames:
        readPuzzle(fileName)
        print(fileName)
        startTime = time.time()
        initialization()
        DFS(0)
        printGrid(state)
        endTime = time.time()
        if verifySolution():
            print("solved")
        else:
            print("not solved")
        print(endTime - startTime)
        print("")
