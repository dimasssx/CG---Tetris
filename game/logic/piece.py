from ..utils.constants import PIECE_COLORS
from ..utils.constants import TETROMINOES

class Piece:
    def __init__(self, shape):
        self.shape_name = shape               # ex: "I", "O", "T"
        self.shape = TETROMINOES[shape]           # matriz 2D da peça
        self.color = PIECE_COLORS[shape]     # cor definida em constants.py
        self.x = 0                            # posição no tabuleiro
        self.y = 0
