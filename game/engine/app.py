import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ..graphics.renderer import BoardRenderer, PieceRenderer
from ..logic.board import Board
from ..logic.piece_manager import PieceManager
from ..graphics.ui import Button, draw_text
import copy

game_over = False
running = True
board_renderer = None
piece_renderer = None
board = None
piece_manager = None
last_move_times = {"left": 0, "right": 0, "down": 0}
keys = {"left": False, "right": False, "down": False, "rotate": False, "hold": False}
DROP_INTERVAL = 500  
MOVE_INTERVAL = 150  
last_drop_time = 0

play_button = None
quit_button = None
window_size = (300, 600)

def keyboard(key, x, y):
    global keys
    key = key.decode("utf-8").lower()
    if key == "a": keys["left"] = True
    elif key == "d": keys["right"] = True
    elif key == "s": keys["down"] = True
    elif key == "w": keys["rotate"] = True
    elif key == "c": keys["hold"] = True
    elif key == "r": restart_game()
    elif key == "\x1b": sys.exit()

def keyboard_up(key, x, y):
    global keys
    key = key.decode("utf-8").lower()
    if key == "a": keys["left"] = False
    elif key == "d": keys["right"] = False
    elif key == "s": keys["down"] = False
    elif key == "w": keys["rotate"] = False


def update(value=0):
    global last_drop_time,last_move_times
    if game_over:
        return
    from time import time
    current_piece = piece_manager.get_current_piece()
    now = int(time() * 1000)
    if keys["hold"]:
        piece_manager.hold_piece()
        keys["hold"] = False
    for direction in ["left", "right", "down"]:
        if keys[direction] and now - last_move_times[direction] > MOVE_INTERVAL:
            if direction == "left" and board.is_valid_position(current_piece, adj_x=-1):
                current_piece.x -= 1
            elif direction == "right" and board.is_valid_position(current_piece, adj_x=1):
                current_piece.x += 1
            elif direction == "down" and board.is_valid_position(current_piece, adj_y=1):
                current_piece.y += 1
            last_move_times[direction] = now
    
    if keys["rotate"]:
        pivot_row, pivot_col = current_piece.pivot
        old_pivot_world_x = current_piece.x + pivot_col
        old_pivot_world_y = current_piece.y + pivot_row

        temp_piece = copy.deepcopy(current_piece)
        temp_piece.rotate_clockwise()
        
        new_pivot_row, new_pivot_col = temp_piece.pivot
        temp_piece.x = old_pivot_world_x - new_pivot_col
        temp_piece.y = old_pivot_world_y - new_pivot_row
        
        kick_tests = [(0, 0), (-1, 0), (1, 0)]

        for adj_x, adj_y in kick_tests:
            if board.is_valid_position(temp_piece, adj_x=adj_x, adj_y=adj_y):
                current_piece.shape = temp_piece.shape
                current_piece.x = temp_piece.x + adj_x
                current_piece.y = temp_piece.y + adj_y
                break

        keys["rotate"] = False

    if now - last_drop_time > DROP_INTERVAL:
        if board.is_valid_position(current_piece, adj_y=1):
            current_piece.y += 1
        else:
            board.lock_piece(current_piece)
            piece_manager.spawn_piece()
            piece_manager.has_swapped = False

            new_piece = piece_manager.get_current_piece()
            if not board.is_valid_position(new_piece):
                game_over_func()  # ativa game over
                return

        last_drop_time = now

    #render
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    piece_renderer.render(current_piece, offset_x=current_piece.x, offset_y=current_piece.y)
    board_renderer.render()
    glutSwapBuffers()
    glutTimerFunc(16, update, 0)

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, board.width, board.height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)


#funcoes do menu

def setup_2d_projection():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_size[0], 0, window_size[1])
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

def restore_projection():
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)

def display_menu():
    """Desenha a tela de menu."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup_2d_projection()
    draw_text("UFAPE TETRIS", 100, 450)
    play_button.draw()
    quit_button.draw()
    restore_projection()
    glutSwapBuffers()

def mouse_click_menu(button, state, x, y):
    """Callback de clique APENAS para o menu."""
    mouse_y = window_size[1] - y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if play_button.is_mouse_over(x, mouse_y):
            start_game()
        elif quit_button.is_mouse_over(x, mouse_y):
            glutLeaveMainLoop()

def mouse_hover_menu(x, y):
    """Callback de hover APENAS para o menu."""
    mouse_y = window_size[1] - y
    play_button.is_hovered = play_button.is_mouse_over(x, mouse_y)
    quit_button.is_hovered = quit_button.is_mouse_over(x, mouse_y)
    glutPostRedisplay()

def start_game():
    """Esta função faz a transição do menu para o jogo."""
    print("Iniciando o jogo...")
    # Registra as suas funções originais do jogo
    glutDisplayFunc(update)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)

    # Desativa as funções do menu para não interferirem
    glutMouseFunc(None)
    glutPassiveMotionFunc(None)

    reshape(window_size[0], window_size[1])
    
    # Inicia o seu game loop pela primeira vez
    glutTimerFunc(0, update, 0)



#main modificada para começar no menu
def main():
    global board_renderer, piece_renderer, board, piece_manager, play_button, quit_button
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(300, 600)
    glutCreateWindow(b"UFAPE Tetris")
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    play_button = Button(x=75, y=300, width=150, height=50, text="Play Game")
    quit_button = Button(x=75, y=220, width=150, height=50, text="Quit")

    # Prepara os objetos do jogo, mas não inicia o loop ainda
    board = Board(width=10, height=20)
    piece_manager = PieceManager()
    piece_manager.spawn_piece()
    board_renderer = BoardRenderer(board)
    piece_renderer = PieceRenderer()

    # Inicia o programa registrando APENAS as funções do menu
    glutDisplayFunc(display_menu)
    glutMouseFunc(mouse_click_menu)
    glutPassiveMotionFunc(mouse_hover_menu)
    
    glutMainLoop()

def game_over_func():
    global game_over
    game_over = True
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display_gameover)
    glutPostRedisplay()

def display_gameover():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup_2d_projection()
    draw_text("GAME OVER", 100, 350)
    draw_text("R para reiniciar", 80, 280)
    draw_text("ESC para sair", 90, 240)
    restore_projection()
    glutSwapBuffers()

def restart_game():
    global board, piece_manager, game_over, last_drop_time
    if not game_over:
        return
    board = Board(width=10, height=20)
    piece_manager = PieceManager()
    piece_manager.spawn_piece()
    board_renderer.board = board  # reaproveita renderer
    game_over = False
    last_drop_time = 0
    glutTimerFunc(0, update, 0)

if __name__ == "__main__":
    main()