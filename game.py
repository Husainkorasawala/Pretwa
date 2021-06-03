from enum import Enum


class State(Enum):
    RED = 'red'
    GREEN = 'green'
    EMPTY = 'empty'


class Game():
    def __init__(self):

        self.coordinates = {    # positions on the board numbered from 1 to 19 in spiral form
            1: (275, -25),
            2: (530, 125),
            3: (530, 425),
            4: (275, 575),
            5: (20, 425),
            6: (20, 125),
            7: (275, 75),
            8: (445, 175),
            9: (445, 375),
            10: (275, 475),
            11: (105, 375),
            12: (105, 175),
            13: (275, 175),
            14: (355, 225),
            15: (355, 325),
            16: (275, 375),
            17: (190, 325),
            18: (190, 225),
            19: (275, 275)}

        self.movePositions = [] # two-element board, 1 element - a selected piece on the board, 2 object - an empty field

        self.boardState = {  # state of a field on the board: 3 possibilities (RED, GREEN, EMPTY)
            1: State.RED,
            2: State.RED,
            3: State.RED,
            4: State.GREEN,
            5: State.GREEN,
            6: State.GREEN,
            7: State.RED,
            8: State.RED,
            9: State.RED,
            10: State.GREEN,
            11: State.GREEN,
            12: State.GREEN,
            13: State.RED,
            14: State.RED,
            15: State.RED,
            16: State.GREEN,
            17: State.GREEN,
            18: State.GREEN,
            19: State.EMPTY}

        self.redTurn = True
        self.redWins = False
        self.greenWins = False

        self.canMoveTo = {
            1: [2, 6, 7],
            2: [1, 3, 8],
            3: [2, 4, 9],
            4: [3, 5, 10],
            5: [4, 6, 11],
            6: [1, 5, 12],
            7: [1, 12, 8, 13],
            8: [2, 7, 9, 14],
            9: [3, 8, 10, 15],
            10: [4, 9, 11, 16],
            11: [5, 10, 12, 17],
            12: [6, 11, 7, 18],
            13: [7, 18, 14, 19],
            14: [8, 13, 15, 19],
            15: [9, 14, 16, 19],
            16: [10, 15, 17, 19],
            17: [11, 16, 18, 19],
            18: [12, 17, 13, 19],
            19: [13, 14, 15, 16, 17, 18]}

        self.canHit = {
            1: [5, 3, 13],
            2: [6, 4, 14],
            3: [1, 5, 15],
            4: [2, 6, 16],
            5: [3, 1, 17],
            6: [4, 2, 18],
            7: [11, 9, 19],
            8: [12, 10, 19],
            9: [7, 11, 19],
            10: [8, 12, 19],
            11: [9, 7, 19],
            12: [10, 8, 19],
            13: [17, 15, 1, 16],
            14: [18, 16, 2, 17],
            15: [13, 17, 3, 18],
            16: [14, 18, 4, 13],
            17: [15, 13, 5, 14],
            18: [16, 14, 6, 15],
            19: [7, 8, 9, 10, 11, 12]
        }

    def hasCommon(self, a, b):
        """Checks if two lists have a common element"""
        for x in a:
            for y in b:
                if x == y:
                    return x
        return False

    def isIntersection(self, mousePos):
        """Returns the number/position of the field clicked by the user"""
        for i in range(1, 20):
            xMin = self.coordinates[i][0]
            xMax = self.coordinates[i][0]+50
            yMin = self.coordinates[i][1]
            yMax = self.coordinates[i][1]+50
            if (mousePos[0] >= xMin) \
                    and (mousePos[0] <= xMax) \
                    and (mousePos[1] >= yMin) \
                    and (mousePos[1] <= yMax):
                return i

    def checkBeadHits(self, myState, opponentState, myPosition):
        """Checks whether a specific beat can be captured"""
        for y in self.canHit[myPosition]:
            if self.boardState[y] == State.EMPTY:
                nextStep = y
                position = myPosition
                hit = self.hasCommon(self.canMoveTo[position], self.canMoveTo[nextStep])
                if self.boardState[hit] == opponentState:
                    return True
        return False

    def checkAnyHits(self, myState, opponentState):
        """Checks if the player can make any capture on this move"""
        for x in self.boardState:
            if self.boardState[x] == myState:
                for y in self.canHit[x]:
                    if self.boardState[y] == State.EMPTY:
                        nextStep = y
                        position = x
                        hit = self.hasCommon(self.canMoveTo[position], self.canMoveTo[nextStep])
                        if self.boardState[hit] == opponentState:
                            return True
        return False

    def checkWin(self, checkedState):
        """Checks if there is a victory"""
        counter = sum(self.boardState[x] == checkedState for x in self.boardState)
        return counter <= 3

    def makeHit(self):
        """Player taking a capture"""
        hitBeat = self.hasCommon(self.canMoveTo[self.movePositions[0]], self.canMoveTo[self.movePositions[1]])
        self.boardState[hitBeat] = State.EMPTY
        self.boardState[self.movePositions[1]] = self.boardState[self.movePositions[0]]
        self.boardState[self.movePositions[0]] = State.EMPTY

    def makeMove(self):
        """The player's making a move"""
        self.boardState[self.movePositions[1]] = self.boardState[self.movePositions[0]]
        self.boardState[self.movePositions[0]] = State.EMPTY
        self.redTurn = not self.redTurn
        self.movePositions.clear()

    def addToMovePositions(self, pos):  # sourcery no-metrics
        """Player movements"""
        if self.redTurn:
            if (len(self.movePositions)) == 0 and self.boardState[pos] == State.RED: # the first field clicked by the user cannot be empty
                self.movePositions.append(pos)

            elif (len(self.movePositions)) == 1 and self.boardState[pos] != State.EMPTY:  # attempt to move to the occupied seat
                self.movePositions.clear()

            elif (len(self.movePositions)) == 1:  # correct movement
                self.movePositions.append(pos)
                if self.checkAnyHits(State.RED,State.GREEN):
                    if self.movePositions[1] in self.canMoveTo[self.movePositions[0]]:  # movement without hitting
                        pass

                    elif (self.movePositions[1] not in self.canMoveTo[self.movePositions[0]]) and ((self.movePositions[1] in self.canHit[self.movePositions[0]]) and (self.boardState[self.hasCommon(self.canMoveTo[self.movePositions[0]], self.canMoveTo[self.movePositions[1]])] == State.GREEN)):
                        self.makeHit()
                        if not self.checkBeadHits(State.RED, State.GREEN, self.movePositions[1]):
                            self.redTurn = False
                    self.movePositions.clear()

                else:
                    if self.movePositions[1] in self.canMoveTo[self.movePositions[0]]:  # movement without hitting
                        self.makeMove()

                    elif (self.movePositions[1] not in self.canMoveTo[self.movePositions[0]]) and ((self.movePositions[1] in self.canHit[self.movePositions[0]]) and (self.boardState[self.hasCommon(self.canMoveTo[self.movePositions[0]], self.canMoveTo[self.movePositions[1]])] == State.GREEN)):
                        self.makeHit()
                        if self.checkBeadHits(State.RED, State.GREEN, self.movePositions[1]):
                            self.movePositions.clear()
                        else:
                            self.redTurn = False
                    else:
                        self.movePositions.clear()
                if self.checkWin(State.GREEN):
                    self.redWins = True

        else:
            if (len(self.movePositions)) == 0 and self.boardState[pos] == State.GREEN: #the first field clicked by the user cannot be empty
                self.movePositions.append(pos)

            elif (len(self.movePositions)) == 1 and self.boardState[pos] != State.EMPTY:
                self.movePositions.clear()

            elif (len(self.movePositions)) == 1:
                self.movePositions.append(pos)
                if self.checkAnyHits(State.GREEN, State.RED):
                    if self.movePositions[1] in self.canMoveTo[self.movePositions[0]]:  # movement without hitting
                        pass

                    elif (self.movePositions[1] not in self.canMoveTo[self.movePositions[0]]) and ((self.movePositions[1] in self.canHit[self.movePositions[0]])and (self.boardState[self.hasCommon(self.canMoveTo[self.movePositions[0]],self.canMoveTo[self.movePositions[1]])] == State.RED)):
                        self.makeHit()
                        if not self.checkBeadHits(State.GREEN, State.RED, self.movePositions[1]):
                            self.redTurn = True
                    self.movePositions.clear()

                else:
                    if self.movePositions[1] in self.canMoveTo[self.movePositions[0]]:  # movement without hitting
                        self.makeMove()

                    elif (self.movePositions[1] not in self.canMoveTo[self.movePositions[0]]) and ((self.movePositions[1] in self.canHit[self.movePositions[0]]) and (self.boardState[self.hasCommon(self.canMoveTo[self.movePositions[0]], self.canMoveTo[self.movePositions[1]])] == State.RED)):
                        self.makeHit()
                        if not self.checkBeadHits(State.GREEN, State.RED, self.movePositions[1]):
                            self.redTurn = True
                        self.movePositions.clear()
                    else:
                        self.movePositions.clear()
                if self.checkWin(State.RED):
                    self.greenWins = True