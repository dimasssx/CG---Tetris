from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ..graphics.renderer import BoardRenderer, PieceRenderer
from ..logic.board import Board
from ..logic.piece_manager import PieceManager

# --- Variáveis globais ---
running = True
board_renderer = None
piece_renderer = None
board = None
piece_manager = None
keys = {"left": False, "right": False, "down": False, "rotate": False}
DROP_INTERVAL = 500  
last_drop_time = 0

def keyboard(key, x, y):
    global keys
    key = key.decode("utf-8").lower()
    if key == "a":
        keys["left"] = True
    elif key == "d":
        keys["right"] = True
    elif key == "s":
        keys["down"] = True
    elif key == "w":
        keys["rotate"] = True
    elif key == "\x1b":  
        sys.exit()

def keyboard_up(key, x, y):
    global keys
    key = key.decode("utf-8").lower()
    if key == "a":
        keys["left"] = False
    elif key == "d":
        keys["right"] = False
    elif key == "s":
        keys["down"] = False
    elif key == "w":
        keys["rotate"] = False

def update(value=0):
    global last_drop_time
    from time import time
    current_piece = piece_manager.get_current_piece()
    now = int(time() * 1000)

    if keys["left"] and board.is_valid_position(current_piece, adj_x=-1):
        current_piece.x -= 1
    if keys["right"] and board.is_valid_position(current_piece, adj_x=1):
        current_piece.x += 1
    if keys["down"] and board.is_valid_position(current_piece, adj_y=1):
        current_piece.y += 1
    ##todo
    
    if keys["rotate"]:
        current_piece.rotate_clockwise()
        if not board.is_valid_position(current_piece):
            current_piece.rotate_counterclockwise()
        keys["rotate"] = False

    if now - last_drop_time > DROP_INTERVAL:
        if board.is_valid_position(current_piece, adj_y=1):
            current_piece.y += 1
        else:
            board.lock_piece(current_piece)
            piece_manager.spawn_piece()
        last_drop_time = now

    # Render
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    piece_renderer.render(current_piece, offset_x=current_piece.x, offset_y=current_piece.y)

    board_renderer.render()
    glutSwapBuffers()
    glutTimerFunc(16, update, 0)  # ~60 FPS

# --- Redimensionamento ---
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, board.width, board.height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)

# --- Main ---
def main():
    global board_renderer, piece_renderer, board, piece_manager
    import sys
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(300, 600)
    glutCreateWindow(b"Tetris 2D GLUT")
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    board = Board(width=10, height=20)
    piece_manager = PieceManager()
    piece_manager.spawn_piece()
    board_renderer = BoardRenderer(board)
    piece_renderer = PieceRenderer()

    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutReshapeFunc(reshape)
    glutDisplayFunc(update)
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
