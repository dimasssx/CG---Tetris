from  OpenGL.GL  import  *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from tetrominos import *
import time

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
GRID_COLS = 10
GRID_ROWS = 20
CELL_SIZE = 30
board = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]



piece_x, piece_y = 3, GRID_ROWS - 1  # posição inicial
last_time = time.time()
current_piece = getPiece()

def draw_piece():
    global current_piece
    for row in range(len(current_piece)):
        for col in range(len(current_piece[row])):
            if current_piece[row][col] == 1:
                draw_square(piece_x + col, piece_y - row)

def draw_square(x, y, color=(0.0, 1.0, 1.0)):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x * CELL_SIZE, y * CELL_SIZE)
    glVertex2f((x + 1) * CELL_SIZE, y * CELL_SIZE)
    glVertex2f((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE)
    glVertex2f(x * CELL_SIZE, (y + 1) * CELL_SIZE)
    glEnd()    
def fix_piece():
    global board
    for row in range(4):
        for col in range(4):
            if current_piece[row][col] == 1:
                board_y = piece_y - row
                board_x = piece_x + col
                if 0 <= board_x < GRID_COLS and 0 <= board_y < GRID_ROWS:
                    board[board_y][board_x] = 1   # ocupa célula no grid
def draw_board():
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            if board[y][x] == 1:
                draw_square(x, y, (1.0, 0.5, 0.0))  # cor diferente das peças caindo

def draw_grid():

    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    for x in range(GRID_COLS + 1):
        glVertex2f(x * CELL_SIZE, 0)
        glVertex2f(x * CELL_SIZE, GRID_ROWS * CELL_SIZE)
    for y in range(GRID_ROWS + 1):
        glVertex2f(0, y * CELL_SIZE)
        glVertex2f(GRID_COLS * CELL_SIZE, y * CELL_SIZE)
    glEnd()

def spawn_piece():
    """Sorteia nova peça no topo."""
    global current_piece, piece_x, piece_y
    current_piece = getPiece()
    piece_x = 3
    piece_y = GRID_ROWS - 1
    # se já nasce colidindo → game over
    if check_collision(piece_x, piece_y, current_piece):
        print("GAME OVER")
        glutLeaveMainLoop()
def check_collision(x, y, piece):
    """Verifica se a peça colide com borda ou blocos fixos."""
    for row in range(4):
        for col in range(4):
            if piece[row][col] == 1:
                board_x = x + col
                board_y = y - row
                # Fora do tabuleiro
                if board_x < 0 or board_x >= GRID_COLS or board_y < 0:
                    return True
                # Colisão com bloco fixo
                if board_y < GRID_ROWS and board[board_y][board_x] == 1:
                    return True
    return False   
def fix_piece():
    """Copia a peça atual para o tabuleiro."""
    global board
    for row in range(4):
        for col in range(4):
            if current_piece[row][col] == 1:
                board_y = piece_y - row
                board_x = piece_x + col
                if 0 <= board_x < GRID_COLS and 0 <= board_y < GRID_ROWS:
                    board[board_y][board_x] = 1
    spawn_piece() 
def update(value):
    
    global piece_y
    if not check_collision(piece_x, piece_y - 1, current_piece):
        piece_y -= 1
    else:
        fix_piece()  # quando encosta, fixa e gera nova peça
    glutPostRedisplay()
    glutTimerFunc(500, update, 0)  # velocidade da queda

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_grid()
    draw_board()
    draw_piece()
    glutSwapBuffers()

def keyboard(key, x, y):
    global piece_x, piece_y
    if key == b'a':  # esquerda
        piece_x -= 1
    elif key == b'd':  # direita
        piece_x += 1
    elif key == b's':  # descer mais rápido
        piece_y -= 1
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Tetris OpenGL")
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glScalef(1, 1, 1)

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(50, update, 0)

    glutMainLoop()


if __name__ == "__main__":
    main()