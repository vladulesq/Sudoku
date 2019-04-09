from queue import Queue
import copy
import time
from operator import itemgetter
class State:

    def __init__(self, state, newConfig = None):
        self.state = state
        self.newConfig = newConfig

    def getNextState(self, problem, newConfig):
        return State(problem.nextConfig(self.state, newConfig), newConfig)

    def BFSExpand(self, problem):
        myList = []
        for newConfig in problem.BFSStep(self.state):
            myList.append(self.getNextState(problem, newConfig))
        return myList

    def GBFSExpand(self, problem):
        myList = []
        for newConfig in problem.GBFSStep(self.state):
            myList.append(self.getNextState(problem, newConfig))
        return myList


class Problem:

    def __init__(self):

        self.initialState = self.readFromFile()

        self.size = len(self.initialState)
        self.blockSize = int(self.size/3)

    def getAllPossibleValues(self, numbers, unavailable):
        return [number for number in numbers if number not in unavailable]

    def firstPositionBfs(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column

    def heuristic(self, state):
        list = []
        for row in range(0, len(state)):
            for column in range(len(state)):
                if state[row][column] == 0:
                    numberPool = range(1, self.size + 1)
                    colList = []
                    rowList = []
                    blockList = []

                    for indexR in range(self.size):
                        if state[row][indexR] != 0:
                            rowList.append(state[row][indexR])
                    options = self.getAllPossibleValues(numberPool, rowList)

                    for indexC in range(self.size):
                        if state[indexC][column] != 0:
                            colList.append(state[indexC][column])
                    options = self.getAllPossibleValues(options, colList)

                    rStart = int(row / self.blockSize) * self.blockSize
                    cStart = int(column / 3) * 3

                    for blockR in range(0, self.blockSize):
                        for blockC in range(0, 3):
                            blockList.append(state[rStart + blockR][cStart + blockC])
                    options = self.getAllPossibleValues(options, blockList)
                    count = len(options)
                    x = [count, row, column, options]
                    list.append(x)
        sortedList = sorted(list, key = itemgetter(0))
        #print(sortedList)
        return sortedList[0]

    def BFSStep(self, state):
        numberPool = range(1, self.size + 1)
        colList = []
        rowList = []
        blockList = []

        row, column = self.firstPositionBfs(self.size, state)

        for indexR in range(self.size):
            if state[row][indexR] != 0:
                rowList.append(state[row][indexR])
        options = self.getAllPossibleValues(numberPool, rowList)


        for indexC in range(self.size):
            if state[indexC][column] != 0:
                colList.append(state[indexC][column])
        options = self.getAllPossibleValues(options, colList)

        rStart = int(row / self.blockSize) * self.blockSize
        cStart = int(column / 3) * 3

        for blockR in range(0, self.blockSize):
            for blockC in range(0, 3):
                blockList.append(state[rStart + blockR][cStart + blockC])
        options = self.getAllPossibleValues(options, blockList)

        for number in options:
            yield number, row, column

    def GBFSStep(self, state):
        something = self.heuristic(state)
        for value in something[3]:
            yield value, something[1], something[2]

    def nextConfig(self, state, newConfig):
        number, row, column = newConfig[0], newConfig[1], newConfig[2]
        newConfig = copy.deepcopy(state)
        newConfig[row][column] = number
        return newConfig

    def checkIfDone(self, state):
        checkSum = sum(range(1, self.size + 1))
        for row in range(self.size):
            if sum(state[row]) != checkSum:
                return False
            colSum = 0
            for column in range(self.size):
                colSum += state[column][row]
            if colSum != checkSum:
                return False
        for column in range(0, self.size, 3):
            for row in range(0, self.size, self.blockSize):
                squareSum = 0
                for squareRow in range(0, self.blockSize):
                    for squareCol in range(0, 3):
                        squareSum += state[row + squareRow][column + squareCol]
                if squareSum != checkSum:
                    return False
        return True

    def readFromFile(self):
        initialState = []
        with open('hard', 'r') as f:
            for line in f:
                initialState.append([int(x) for x in line.split(" ")])
        f.close()
        return initialState

class Controller:

    def BFS(self, problem):
        root = State(problem.initialState)
        if problem.checkIfDone(root.state):
            return root
        q = Queue()
        q.put(root)
        while q.qsize() != 0:
            node = q.get()
            for neighbour in node.BFSExpand(problem):
                    if problem.checkIfDone(neighbour.state):
                        return neighbour
                    q.put(neighbour)
        return None

    def GBFS(self, problem):
        root = State(problem.initialState)
        if problem.checkIfDone(root.state):
            return root
        q = Queue()
        q.put(root)
        while q.qsize() != 0:
            node = q.get()
            for neighbour in node.GBFSExpand(problem):
                if problem.checkIfDone(neighbour.state):
                    return neighbour
                q.put(neighbour)
        return None

class UI:

    def mainMenu(self):
        print("            Welcome to my Sudoku Program")
        print("1. Solve it using BFS")
        print("2. Solve it using GBFS")
        print("                       If you want to change the difficulty, alter the function readFromFile, and select the desired difficulty ")

    def run(self):

        self.mainMenu()
        while True:
            cmd = input ("Select the desired method of solving!\n>>")
            if cmd == "1":
                self.solveBFS()
            if cmd == "2":
                self.solveGBFS()

    def solveBFS(self):
        start = time.time()
        problem = Problem()
        controller = Controller()
        result = controller.BFS(problem)
        totalTime = time.time() - start

        if result:
            for row in result.state:
                print(row)
        else:
            print("No solution")

        print("Total time: " + str(totalTime))

    def solveGBFS(self):
        start = time.time()
        problem = Problem()
        controller = Controller()
        result = controller.GBFS(problem)
        totalTime = time.time() - start

        if result:
            for row in result.state:
                print(row)
        else:
            print("No solution")

        print("Total time: " + str(totalTime))

def tests():
    pass

def main():
    ui = UI()
    ui.run()
main()