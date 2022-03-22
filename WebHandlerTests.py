import unittest
from WebHandler import WebHandler


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = WebHandler()
    def tearDown(self) -> None:
        z = 3

    def test_whitePromotionQueen(self):
        self.whitePromotionTest()
        self.handler.makeMove("g7f8q")

    def test_whitePromotionRook(self):
        self.whitePromotionTest()
        self.handler.makeMove("g7f8r")

    def test_whitePromotionKnight(self):
        self.whitePromotionTest()
        self.handler.makeMove("g7f8n")

    def test_whitePromotionBishop(self):
        self.whitePromotionTest()
        self.handler.makeMove("g7f8b")

    def whitePromotionTest(self):
        """
        Plays a game and gets to the point where white can make a promotion
        """
        promotionTestMoves = [x.lower() for x in ['F2F4', 'E7E5', 'F4F5', 'D7D5', 'F5F6', 'H7H5', 'F6G7', 'H8H6']]
        self.handler.playTestGame(promotionTestMoves)
        z = 3






if __name__ == '__main__':
    unittest.main()
