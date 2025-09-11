from ..utils.constants import PIECE_COLORS
from ..utils.constants import TETROMINOES

class Piece:
    def __init__(self, shape):
        self.shape_name = shape               # ex: "I", "O", "T"
        self.shape = TETROMINOES[shape]           # matriz 2D da peça
        self.color = PIECE_COLORS[shape]     # cor definida em constants.py
        self.original_shape = TETROMINOES[shape]
        self.x = 0                            # posição no tabuleiro
        self.y = 0

        self.set_pivot()

    def set_pivot(self):
        if self.shape_name in ["T","S","Z","J","L","I"]:
            self.pivot = (1,1)
        else:
            self.pivot = (0,0)
        
      

    def rotate (self,clockwise = True):
        if self.shape_name == "O":
            return
        
        transposed_shape = [list(row) for row in zip(*self.shape)]
        if clockwise:
            self.shape = [row[::-1] for row in transposed_shape]
        else:
            self.shape = transposed_shape[::-1]

    def rotate_clockwise(self):
        self.rotate(clockwise=True)

    def rotate_counterclockwise(self):
        self.rotate(clockwise = False)
