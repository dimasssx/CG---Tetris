import random
from game.logic.piece import Piece
from ..utils.constants import TETROMINOES

class PieceManager:
    def __init__(self):
        self.next_piece_name = random.choice(list(TETROMINOES.keys()))
        self.current_piece = None  
   
    def spawn_piece(self):
        piece_name = self.next_piece_name
        piece = Piece(piece_name)
        piece.x = 3  
        self.next_piece_name = random.choice(list(TETROMINOES.keys()))
        self.current_piece = piece 
        return piece
    def get_current_piece(self):
        return self.current_piece
    def get_next_piece_name(self):
        return self.next_piece_name
