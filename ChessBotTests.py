import unittest
from ChessBot import ChessBot

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.bot = ChessBot(1, 10, False)
        self.bot.webHandler.findGame()
    def test_something(self):
        z = 3
        self.bot.playGame()


if __name__ == '__main__':
    unittest.main()
