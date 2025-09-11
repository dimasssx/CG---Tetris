import random
from game.logic.piece import Piece
from ..utils.constants import TETROMINOES

class PieceManager:
    def __init__(self):
        #cria uma "sacola" com as 7 peças e a embaralha.
        self.initial_bag = list(TETROMINOES.keys())
        random.shuffle(self.initial_bag)

        #pega a primeira peça da sacola embaralhada
        self.next_piece_name = self.initial_bag.pop()
        self.current_piece = None  
        self.held_piece = None
        self.has_swapped = False
   
    def spawn_piece(self):
        piece_name = self.next_piece_name
        piece = Piece(piece_name)
        piece.x = 3

        #decide qual será a próxima peça.
        if self.initial_bag:
            #se a sacola inicial ainda tem pecas, pega a próxima de la
            self.next_piece_name = self.initial_bag.pop()
        else:
            #mas se a sacola inicial ja esvaziou, volta para o sorteio normal
            self.next_piece_name = random.choice(list(TETROMINOES.keys()))      
        self.current_piece = piece 
        return piece
    def get_current_piece(self):
        return self.current_piece
    def get_next_piece_name(self):
        return self.next_piece_name
    

    def hold_piece(self):
    
        if not self.has_swapped:
            if self.held_piece is None:
                self.held_piece = self.current_piece
                self.spawn_piece()
            else:         
                self.current_piece, self.held_piece = self.held_piece, self.current_piece      
                self.current_piece.x = 3
                self.current_piece.y = 0 
        
                self.has_swapped = True

    def get_current_piece(self):
        return self.current_piece
    
    def get_next_piece_name(self):
        return self.next_piece_name
    def get_held_piece(self):
        return self.held_piece
