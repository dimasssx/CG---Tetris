from OpenGL.GL import *

class BoardRenderer:
    def __init__(self, board):
        self.board = board

    def render(self):
        for y, row in enumerate(self.board.grid):
            for x, cell in enumerate(row):
                if cell:  
                    self.draw_cube(x, y, cell)
                else:    
                    self.draw_cube(x, y, self.board.color)

    def draw_cube(self, x, y, color):
        glColor3ub(*color)          
        glBegin(GL_QUADS)             
        glVertex2f(x, y)              
        glVertex2f(x + 1, y)          
        glVertex2f(x + 1, y + 1)      
        glVertex2f(x, y + 1)          
        glEnd()
    
class PieceRenderer:
    def render(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_cube(x + offset_x, y + offset_y, piece.color)

    def draw_cube(self, x, y, color):
        glColor3ub(*color)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + 1, y)
        glVertex2f(x + 1, y + 1)
        glVertex2f(x, y + 1)
        glEnd()