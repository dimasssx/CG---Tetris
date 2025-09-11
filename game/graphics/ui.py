# game/graphics/ui.py
from OpenGL.GL import *
from OpenGL.GLUT import *

def draw_text(text, x, y, font=GLUT_BITMAP_9_BY_15, color=(255, 255, 255)): # <-- Adicionado 'color' com valor padrão
    """Desenha texto na tela em coordenadas de pixel."""
    #converte RGB para OpenGL
    glColor3f(color[0]/255.0, color[1]/255.0, color[2]/255.0)
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(font, ord(character))

class Button:
    def __init__(self, x, y, width, height, text):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.text = text
        self.is_hovered = False
        self.color_normal = (0.2, 0.2, 0.8)  
        self.color_hover = (0.4, 0.4, 1.0)   

    def draw(self):
        """Desenha o botão."""
        color = self.color_hover if self.is_hovered else self.color_normal
        glColor3f(*color)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()
        draw_text(self.text, self.x + 45, self.y + 18) 

    def is_mouse_over(self, mouse_x, mouse_y):
        """Verifica se o mouse está sobre a área do botão."""
        return (self.x <= mouse_x <= self.x + self.width and
                self.y <= mouse_y <= self.y + self.height)