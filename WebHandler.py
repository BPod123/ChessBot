from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import chess

class WebHandler(object):
    def __init__(self):
        self.driver = Firefox()
        self.__foundFirstGame = False
        self.postMoveBoard = {}
        self.preMoveBoard = {}
        self.lastMoveMade = None



    def __del__(self):
        self.driver.quit()

    def findGame(self):
        self.driver.get("https://www.chess.com/play/computer")
        if not self.__foundFirstGame:
            sleep(2)
            elements = [x for x in self.driver.find_elements(By.CLASS_NAME, 'x') if
                        x.get_attribute("class") == 'icon-font-chess x modal-seo-close-icon']
            if len(elements) > 0:
                elements[0].click()

    @property
    def color(self):
        boardElements = self.driver.find_elements(By.TAG_NAME, 'chess-board')
        boardElement = boardElements[0]
        return 'flipped' not in boardElement.get_attribute('class')
    @property
    def moves(self):
        moves = self.driver.find_elements(By.CLASS_NAME, 'move')
        moves.sort(key = lambda x: int(x.get_attribute("data-whole-move-number")))
        whiteMoves = []
        blackMoves = []
        for turn in moves:
            turnMoves = turn.find_elements_by_xpath(".//div")
            for turnMove in turnMoves:
                moveString = turnMove.get_attribute("innerHTML")
                # '<span class="icon-font-chess queen-black" data-figurine="Q"></span>h4'
                if 'data-figurine=' in moveString:
                    moveString = moveString[moveString.index('data-figurine=') + len('data-figurine=') + 1
                                            : moveString.index('data-figurine=') + len(
                        'data-figurine=') + 2] + moveString[moveString.rfind('span>') + len('span>'):]

                if "white" in turnMove.get_attribute("class"):
                    whiteMoves.append(moveString)
                else:
                    blackMoves.append(moveString)
        return whiteMoves, blackMoves
    @property
    def turn(self):
        """
        :return: True if it is whites turn, False if it is black's turn
         """
        return len(self.driver.find_elements(By.CLASS_NAME, 'node')) % 2 == 0
    @property
    def moveHasBeenMade(self):
        return self.board != self.postMoveBoard or self.lastMove != self.lastMoveMade

    @property
    def lastMove(self):
        """
        :return: The last move that was made by a player
        """
        moveElements = self.driver.find_elements(By.CLASS_NAME, 'move')


        if len(moveElements) == 0:
            # No move has been made yet
            return None
        lastMoveElement = moveElements[max(range(len(moveElements)), key = lambda i: int(moveElements[i].get_attribute('data-whole-move-number')))]
        roundMoves = lastMoveElement.find_elements_by_xpath(".//div")
        lastRoundMove = roundMoves[max(range(len(roundMoves)), key = lambda i: int(roundMoves[i].get_attribute('data-ply')))]
        moveData = lastRoundMove.get_attribute('innerHTML')
        while not str.isdigit(moveData[-1]):
            moveData = moveData[:-1]
        if 'data-figurine' in moveData:
            index = moveData.find('data-figurine="') + len('data-figurine="')
            moveData = moveData[index: index + 1] + moveData[-2:]
        if 'O-O' in moveData:
            # Castle
            lastMoveColor = 'white' in lastRoundMove.get_attribute('class')
            if moveData == 'O-O':
                # King side castle
                if lastMoveColor:
                    startSquare, endSquare = chess.E1, chess.G1
                else:
                    startSquare, endSquare = chess.E8, chess.G8
            else:
                # Queen side castle
                if lastMoveColor:
                    startSquare, endSquare = chess.E1, chess.C1
                else:
                    startSquare, endSquare = chess.E8, chess.C8
        else:
            endSquare = getattr(chess, moveData[-2:].upper())
            # Highlight the start and end square
            highlightedSquares = self.driver.find_element(By.TAG_NAME, 'chess-board').find_elements(By.CLASS_NAME, 'highlight')
            endSquareClass = letterNumToClassName(moveData[-2:])
            startingSquareClass = [x.get_attribute('class') for x in highlightedSquares if endSquareClass not in x.get_attribute('class')][0]
            startSquare = getattr(chess, classNameToLetterNum(startingSquareClass))
        # if self.__postMoveBoard is not None:
        board = self.board
        endSquareLetterNum = squareIntToLetterNum(endSquare)
        endPieceType = chess.PAWN if board[endSquareLetterNum] in ['wp', 'bp'] else chess.KNIGHT if board[
                                                                                                        endSquareLetterNum] in [
                                                                                                        'wn',
                                                                                                        'bn'] else chess.BISHOP if \
            board[endSquareLetterNum] in ['wb', 'bb'] else chess.ROOK if board[endSquareLetterNum] in ['wr',
                                                                                                       'br'] else chess.QUEEN if \
            board[endSquareLetterNum] in ['wq', 'bq'] else chess.KING
        if endPieceType == chess.PAWN or endPieceType == chess.KING:
            return chess.Move(startSquare, endSquare) # Moved piece is a pawn or king
        elif squareIntToLetterNum(startSquare) in self.postMoveBoard: # The piece was moved after the last move was made
            startPiece = self.postMoveBoard[squareIntToLetterNum(startSquare)]
            startPieceType = chess.PAWN if startPiece in ('wp', 'bp') else chess.KNIGHT if startPiece in (
            'wn', 'bn') else chess.BISHOP if startPiece in ('wb', 'bb') else chess.ROOK if startPiece in (
            'wr', 'br') else chess.QUEEN if startPiece in ('wq', 'bq') else chess.KING
            if startPieceType != endPieceType:
                return chess.Move(startSquare, endSquare, endPieceType) # moved piece was a pawn and was promoted
            else:
                return chess.Move(startSquare, endSquare) # moved piece was not a pawn
        elif squareIntToLetterNum(startSquare) in self.preMoveBoard: # The piece was moved after the last move was made
            startPiece = self.preMoveBoard[squareIntToLetterNum(startSquare)]
            startPieceType = chess.PAWN if startPiece in ('wp', 'bp') else chess.KNIGHT if startPiece in (
            'wn', 'bn') else chess.BISHOP if startPiece in ('wb', 'bb') else chess.ROOK if startPiece in (
            'wr', 'br') else chess.QUEEN if startPiece in ('wq', 'bq') else chess.KING
            if startPieceType != endPieceType:
                return chess.Move(startSquare, endSquare, endPieceType) # moved piece was a pawn and was promoted
            else:
                return chess.Move(startSquare, endSquare) # moved piece was not a pawn
        else:
            return chess.Move(startSquare, endSquare)
            z = 3
            # return self.lastMoveMade



    @property
    def pieces(self):
        letters = 'a b c d e f g h'.split(' ')
        numbers = '1 2 3 4 5 6 7 8'.split(' ')
        pieces = {}
        # movementSquares = set()
        for i in range(1, 9):
            for j in range(1, 9):
                elements = self.driver.find_elements(By.CLASS_NAME, "square-{0}{1}".format(i, j))
                if len(elements) > 0:
                    for e in elements:
                        className = e.get_attribute("class")
                        if 'highlight' in className:
                            # movementSquares.add("{0}{1}".format(letters[i - 1], numbers[j - 1]))
                            continue
                        pieces["{0}{1}".format(letters[i - 1], numbers[j - 1])] = e
        return pieces
    @property
    def board(self):
        """
        :return: A dictionary mapping x-y coordinates to what is on that square. 11 is the bottom left,
         88 is the top right

        """
        letters = 'a b c d e f g h'.split(' ')
        numbers = '1 2 3 4 5 6 7 8'.split(' ')
        board = {}
        # movementSquares = set()
        for i in range(1, 9):
            for j in range(1, 9):
                elements = self.driver.find_elements(By.CLASS_NAME, "square-{0}{1}".format(i, j))
                if len(elements) > 0:
                    for e in elements:
                        className = e.get_attribute("class")
                        if 'highlight' in className:
                            # movementSquares.add("{0}{1}".format(letters[i - 1], numbers[j - 1]))
                            continue
                        piece = className[6:8]
                        board["{0}{1}".format(letters[i - 1], numbers[j - 1])] = piece
        return board




    def getPiece(self, letterNum):
        elements = self.driver.find_elements_by_class_name(letterNumToClassName(letterNum))
        return elements[0]

    # def tileXY(self, letterNum):
    #     if self.A1 is None or self.H8 is None or self.__pieceWidth is None or self.__pieceHeight is None:
    #         board = self.board
    #     x = 'a b c d e f g h'.split(' ').index(letterNum[0].lower()) * self.__pieceWidth + self.A1['x']
    #     y = (int(letterNum[1]) - 1) * self.__pieceWidth + self.A1['y']
    #     return x, y

    def getSquareXY(self, letterNum: str):
        """
        :param letterNum: string of the form a1, a2, ... a8, b1, b2, ..., b8,...,..., h1, ..., h8
        :return: The x,y coordinates of the center of that square
        """
        boardElement = self.driver.find_element(By.TAG_NAME, 'chess-board')
        pieceHeight = boardElement.size['height'] // 8
        pieceWidth = boardElement.size['width'] // 8
        if self.color: # If white
            cols = 'abcdefgh'
            rows = '012345678'
        else:
            cols = 'hgfedcba'
            rows = '087654321'
        x = boardElement.location['x'] + pieceWidth * cols.index(letterNum.lower()[0]) + pieceWidth // 2
        y = boardElement.location['y'] + boardElement.size['height'] - (pieceHeight * (rows.index(letterNum[1]))) - pieceHeight // 2
        return x, y


    def moveOffset(self, move: chess.Move):
        startX, startY = self.getSquareXY(squareIntToLetterNum(move.from_square))
        endX, endY = self.getSquareXY(squareIntToLetterNum(move.to_square))
        return endX - startX, endY - startY

    def makeMove(self, move:chess.Move):
        self.preMoveBoard = self.board
        self.lastMoveMade = move
        # piece = self.getPiece(move[:2])
        from_square = move.from_square
        # to_square = move.to_square

        piece = self.getPiece(squareIntToLetterNum(from_square))
        xOffset, yOffset = self.moveOffset(move)
        # sleep(0.5)
        actions = ActionChains(self.driver)
        actions.move_to_element(piece)
        actions.click_and_hold()
        actions.move_by_offset(xOffset, yOffset)
        actions.release()
        if move.promotion is not None:
            # There is a promotion
            if move.promotion == chess.QUEEN:
                actions.click()
            else:
                if self.color:
                    x, y = self.getSquareXY(str(move)[-3] + str(int(move[-2]) - 1))
                else:
                    x, y = self.getSquareXY(str(move)[-3] + str(int(str(move)[-2]) + 1))
                try:
                    squareHeight = self.driver.find_element(By.TAG_NAME, 'chess-board').size['height'] // 8
                except:
                    squareHeight = self.driver.find_element(By.TAG_NAME, 'chess-board').size['height'] // 8
                yOffset = squareHeight * 'q n r b'.split(" ").index(str(move)[-1].lower())
                actions.move_by_offset(0, yOffset)
                actions.click()
        try:
            actions.perform()
        except:
            sleep(1)
            actions.perform()
        self.postMoveBoard = self.board

    def practiceGame(self):

        self.driver.get("https://www.chess.com/practice")

    def switchSides(self):
        self.driver.find_elements(By.CLASS_NAME, 'shuffle')[0].click()
    def undoMove(self):
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        backButtons = [x for x in buttons if x.get_attribute('data-game-control-button') == "PreviousMove" or x.get_attribute('aria-label') == "Move Back"]
        backButton = backButtons[0]
        backButton.click()

    def playTestGame(self, moves):
        self.driver.get("https://www.chess.com/practice")
        for move in moves:
            self.makeMove(move)
            while self.turn != self.color:
                sleep(0.1)
            self.undoMove()
            self.switchSides()

def squareIntToLetterNum(square:int):
    col = 'a b c d e f g h'.split(" ")[square % 8]
    row = square // 8 + 1
    return col + str(row)
def letterNumToClassName(letterNum):
    """

    :param letterNum: A string of the form ax where a is a letter (a-h) and x is a number (1-8)
    :return: The class name of the tile at the position on the board. a1 -> 'square-11'
    """
    return "square-{0}{1}".format('0abcdefgh'.find(letterNum.lower()[0]), letterNum[1])

def classNameToLetterNum(className):
    """
    :param className: element class name with  "square-**" where ** represent any number in {1, 2, ..., 8}
    :return: letter-number representation of the square in upper case
    """
    squareNum = [x[-2:] for x in className.split(" ") if 'square-' in x][0]
    col = '0ABCDEFGH'[int(squareNum[0])]
    row = squareNum[1]
    return col + row





def classNameToXY(className):
    return int(className[-2]), int(className[-1])
