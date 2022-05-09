# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
from collections import deque
import random


class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        self.row = rowDimension
        self.col = colDimension
        self.totalMines = totalMines
        self.startX = startX
        self.startY = startY
        self.rowLast = startY
        self.columnLast = startX
        self.moveTrack = 1
        self.moveCap = 0
        self.safeQueue = deque([])
        self.prob = dict()
        self.mines = []
        self.minesLeft = totalMines
        self.undefined = [(j, i)
                          for i in range(self.row)
                          for j in range(self.col)]
        self.board = None
        self.buildBoard()
        self.updateFirstMove()

    def getAction(self, number: int) -> "Action Object":

        self.logPrevPercept(number)

        if (number == 0):

            for col in range(self.columnLast-1, self.columnLast+2):
                for row in range(self.rowLast-1, self.rowLast+2):
                    if (self.inBounds(col, row) and not (col == self.columnLast and row == self.rowLast)) and \
                            ((col, row) not in self.safeQueue) and self.board[col][row].covered == True:
                        self.safeQueue.append((col, row))

        for col in range(0, self.col):
            for row in range(0, self.row):

                if (self.board[col][row].covered == False and
                    self.board[col][row].number != 0 and
                    self.board[col][row].number ==
                        self.neighborCovered(col, row)[0]):
                    mines = self.neighborCovered(col, row)[1]
                    for _ in mines:
                        self.markMines(_)

        for col in range(0, self.col):
            for row in range(0, self.row):

                if ((self.board[col][row].number ==
                     self.neighborMines(col, row)[0]) and
                    (self.neighborCovered(col, row)[0] -
                     self.neighborMines(col, row)[0] > 0)):
                    covered = self.neighborCovered(col, row)[1]
                    mines = self.neighborMines(col, row)[1]
                    for _ in covered:

                        if (_ not in mines) and (_ not in self.safeQueue):
                            self.safeQueue.append(_)

        while (self.safeQueue != deque([])):

            colRow = self.safeQueue.popleft()

            self.logMove(AI.Action(1), colRow[0], colRow[1])

            return Action(AI.Action(1), colRow[0], colRow[1])

        if (self.undefined != []):

            minList = self.minList(self.prob)
            self.safeQueue.append(random.choice(minList))
        if (self.minesLeft == 0):
            return Action(AI.Action(0))

		########################################################################
		#							Helper Functions						   #
		########################################################################


    def buildBoard(self) -> None:

        self.board = [[self.__Tile() for i in range(self.row)]
                      for j in range(self.col)]
        self.moveCap = self.col * self.row * 2 - 1

    def inBounds(self, column: int, r: int) -> bool:

        if column < self.col and column >= 0 and \
           r < self.row and r >= 0:
            return True
        return False

    def markMines(self, coord):

        col = coord[0]
        row = coord[1]
        if (col, row) not in self.mines:
            self.minesLeft -= 1
            self.mines.append((col, row))
            self.board[col][row].mine = True
            self.board[col][row].flag = True
            self.undefined.remove((col, row))

    def logPrevPercept(self, number):

        if self.lastAction == AI.Action(1):
            self.lastTile.covered = False
            self.lastTile.number = number

    def logMove(self, action, column, r):

        self.columnLast = column
        self.rowLast = r
        self.lastTile = self.board[column][r]
        self.lastAction = action
        self.moveTrack += 1
        self.undefined.remove((column, r))
        if (column, r) in list(self.prob.keys()):
            self.prob.pop((column, r))

    def updateFirstMove(self) -> None:

        column = self.startX
        r = self.startY
        self.undefined.remove((column, r))

        self.columnLast = column
        self.rowLast = r

        self.board[column][r].covered = False
        self.board[column][r].nubmer = 0

        self.lastTile = self.board[column][r]
        self.lastAction = AI.Action(1)

    def neighborMines(self, col, row):

        count = 0
        neighbourMines = []
        for column in range(col-1, col+2):
            for r in range(row-1, row+2):
                if self.inBounds(column, r):
                    if self.board[column][r].mine == True:
                        self.board[column][r].flag = True
                        count += 1
                        neighbourMines.append((column, r))
        return count, neighbourMines

    def neighborCovered(self, col, row):

        count = 0
        covered = []
        for column in range(col-1, col+2):
            for r in range(row-1, row+2):
                if self.inBounds(column, r):
                    if self.board[column][r].covered == True:
                        count += 1
                        covered.append((column, r))
        return count, covered
        
    
    class __Tile():

        mine = False    # if the tile is a mine
        covered = True  # if the tile is covered
        flag = False    # Tile is flagged
        number = -10    # Percept number
