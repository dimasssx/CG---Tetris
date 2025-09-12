import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ..graphics.renderer import BoardRenderer, PieceRenderer
from ..logic.board import Board
from ..logic.piece_manager import PieceManager
from ..graphics.ui import Button, draw_text
from ..logic.piece import Piece
from time import time
import copy

running = True
game_over = False
board_renderer = None
piece_renderer = None
board = None
piece_manager = None


#variáveis para o sistema de pontuação e nível
score = 0
level = 0
total_lines_cleared = 0
points_map = {
    1: 100,
    2: 300,
    3: 500,
    4: 1000
}

#variaveis de tempo
start_time = 0
elapsed_time = 0

last_move_times = {"left": 0, "right": 0, "down": 0}
keys = {"left": False, "right": False, "down": False, "rotate": False, "hold": False,"hard_drop": False}
DROP_INTERVAL_BASE = 500 # A velocidade inicial é ajustada pelo o nivel 
MOVE_INTERVAL = 150 

last_drop_time = 0

play_button = None
quit_button = None
window_size = (450, 600)

def keyboard(key, x, y):
    global keys
    key = key.decode("utf-8").lower()
    if key == "a": keys["left"] = True
    elif key == "d": keys["right"] = True
    elif key == "s": keys["down"] = True
    elif key == "w": keys["rotate"] = True
    elif key == "c": keys["hold"] = True
    elif key == " ": keys["hard_drop"] = True
    elif key == "r": restart_game()
    elif key == "\x1b": glutLeaveMainLoop()

def keyboard_up(key, x, y):
    global keys
    key = key.decode("utf-8").lower()
    if key == "a": keys["left"] = False
    elif key == "d": keys["right"] = False
    elif key == "s": keys["down"] = False
    elif key == "w": keys["rotate"] = False

def calculate_ghost_piece_y(current_piece):
    ghost_y = current_piece.y
    while board.is_valid_position(current_piece, adj_y=ghost_y - current_piece.y + 1):
        ghost_y += 1
    return ghost_y

def update(value=0):

    global last_drop_time, score, level, total_lines_cleared,last_move_times
    from time import time
    current_piece = piece_manager.get_current_piece()
    now = int(time() * 1000)
    
    if keys["hold"]:
        piece_manager.hold_piece()
        keys["hold"] = False
    
    if keys["hard_drop"]:
        final_y = calculate_ghost_piece_y(current_piece)
        score += 10
        current_piece.y = final_y
        lines_cleared_now = board.lock_piece(current_piece)
        if lines_cleared_now > 0:
            score += points_map.get(lines_cleared_now, 0) * (level + 1)
            total_lines_cleared += lines_cleared_now
            level = total_lines_cleared // 10
        piece_manager.spawn_piece()
        piece_manager.has_swapped = False

        new_piece = piece_manager.get_current_piece()
        if not board.is_valid_position(new_piece):
            game_over_func()
            return 

        last_drop_time = now
        keys["hard_drop"] = False

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

    #calcula o intervalo de queda com base no nivel atual
    #a velocidade aumenta em 50ms a cada nivel, com um minimo de 50ms.
    drop_interval = max(50, DROP_INTERVAL_BASE - (level * 50))

    if now - last_drop_time > drop_interval:
        if board.is_valid_position(current_piece, adj_y=1):
            current_piece.y += 1
            score += 1 #pontos por queda manual
        else:
            #logica de pontuação e nivel
            lines_cleared_now = board.lock_piece(current_piece)
            if lines_cleared_now > 0:
                #calcula a pontuação
                score += lines_cleared_now * 100
                total_lines_cleared += lines_cleared_now
                #verifica se o jogador subiu de nivel (a cada 10 linhas)
                if total_lines_cleared // 10 > level:
                    level = total_lines_cleared // 10
                    print(f"LEVEL UP! Nível: {level}")
            piece_manager.spawn_piece()
            piece_manager.has_swapped = False

            new_piece = piece_manager.get_current_piece()
            if not board.is_valid_position(new_piece):
                game_over_func()  # ativa game over
                return

        last_drop_time = now

    #render
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #define a matriz de projeção para o jogo
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 15, 20, 0, -1, 1) 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    ghost_y = calculate_ghost_piece_y(current_piece)
    piece_renderer.render_ghost(current_piece, offset_x=current_piece.x, offset_y=ghost_y)

    #renderiza o tabuleiro e a peça
    piece_renderer.render(current_piece, offset_x=current_piece.x, offset_y=current_piece.y)
    render_next_piece_preview()
    render_held_piece()
    board_renderer.render()

    #renderiza a UI (Pontuação e Nível)
    setup_2d_projection()
    draw_text("UFAPE TETRIS", 320, 550)
    draw_text(f"Score: {score}", 320, 500)
    draw_text(f"Level: {level}", 320, 470)
    draw_text(f"Lines: {total_lines_cleared}", 320, 440)
    draw_text("HOLD", 320, 405)
    draw_text("NEXT", 320, 275)

    restore_projection()

    glutSwapBuffers()
    glutTimerFunc(16, update, 0)

def render_held_piece():
    held_piece = piece_manager.get_held_piece()
    setup_2d_projection()
    glPushMatrix()
    #posição para a caixa do "Hold"
    glTranslatef(330, 305, 0) 
    glScalef(20, 20, 1)
    glLineWidth(2)
    glColor3ub(255, 255, 255) 
    glBegin(GL_LINE_LOOP)
    glVertex2f(-0.5, -0.5)
    glVertex2f(4.5, -0.5)
    glVertex2f(4.5, 4.5)
    glVertex2f(-0.5, 4.5)
    glEnd()

    #renderiza a peça dentro da caixa
    if held_piece is not None:
        temp = copy.deepcopy(held_piece)
        temp.shape = held_piece.original_shape
        piece_renderer.render(temp, 0.5, 0.5)

    glPopMatrix()
    restore_projection()


def render_next_piece_preview():
    next_piece_name = piece_manager.get_next_piece_name()
    if next_piece_name:
        next_piece = Piece(next_piece_name)
        setup_2d_projection()
        glPushMatrix()
        glTranslatef(330, 180, 0)
        glScalef(20, 20, 1)
        glLineWidth(2)
        glColor3ub(255, 255, 255)  # branco
        glBegin(GL_LINE_LOOP)
        glVertex2f(-0.5, -0.5)
        glVertex2f(4.5, -0.5)
        glVertex2f(4.5, 4.5)
        glVertex2f(-0.5, 4.5)
        glEnd()

        temp = copy.deepcopy(next_piece)
        temp.shape = next_piece.original_shape
        
        piece_renderer.render(temp,0.5,0.5)
        glPopMatrix()

        restore_projection()


def reshape(width, height):
    #essa função ficou simples, a projeção é controlada no loop de update
    glViewport(0, 0, width, height)


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
    draw_text("UFAPE TETRIS", 170, 450)
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
    global start_time
    print("Iniciando o jogo...")
    #registra as suas funções originais do jogo

    start_time = time()

    glutDisplayFunc(update)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)

    #desativa as funções do menu para não interferirem
    glutMouseFunc(None)
    glutPassiveMotionFunc(None)

    reshape(window_size[0], window_size[1])
    
    #inicia o seu game loop pela primeira vez
    glutTimerFunc(0, update, 0)



#main modificada para começar no menu
def main():
    global board_renderer, piece_renderer, board, piece_manager, play_button, quit_button
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_size[0], window_size[1])
    glutCreateWindow(b"UFAPE Tetris")
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    #posição dos botões ajustado para nova largura
    play_button = Button(x=150, y=300, width=150, height=50, text="Iniciar")
    quit_button = Button(x=150, y=220, width=150, height=50, text="Sair")

    #prepara os objetos do jogo, mas não inicia o loop ainda
    board = Board(width=10, height=20)
    piece_manager = PieceManager()
    piece_manager.spawn_piece()
    board_renderer = BoardRenderer(board)
    piece_renderer = PieceRenderer()

    #inicia o programa registrando APENAS as funções do menu
    glutDisplayFunc(display_menu)
    glutMouseFunc(mouse_click_menu)
    glutPassiveMotionFunc(mouse_hover_menu)
    
    glutMainLoop()

def game_over_func():
    global game_over, elapsed_time
    game_over = True

    #para o cronômetro e calcula o tempo total 
    end_time = time()
    elapsed_time = end_time - start_time

    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display_gameover)
    glutPostRedisplay()

def display_gameover():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup_2d_projection()

    window_width = window_size[0] #largura da janela 
    window_height = window_size[1] #altura da janela
    
    draw_text("GAME OVER", (window_width / 2) - 60, window_height - 200, color=(255, 69, 0))

    draw_text(f"Pontuacao Final: {score}", (window_width / 2) - 100, window_height - 250, color=(0, 255, 255))
    draw_text(f"Tempo: {elapsed_time:.2f} segundos", (window_width / 2) - 100, window_height - 280, color=(0, 255, 255))

    draw_text("R para reiniciar", (window_width / 2) - 90, window_height - 350, color=(255, 255, 0))
    draw_text("ESC para sair", (window_width / 2) - 80, window_height - 380, color=(255, 255, 0))

    restore_projection()
    glutSwapBuffers()

def restart_game():
    global board, piece_manager, game_over, last_drop_time, score, level, total_lines_cleared, start_time, elapsed_time
    if not game_over:
        return
    board = Board(width=10, height=20)
    piece_manager = PieceManager()
    piece_manager.spawn_piece()
    board_renderer.board = board  #reaproveita renderer
    game_over = False
    last_drop_time = 0
    score = 0
    level = 0
    total_lines_cleared = 0
    elapsed_time = 0

    #reinicia o cronômetro
    start_time = time()
    
    glutDisplayFunc(update)
    glutTimerFunc(0, update, 0)

if __name__ == "__main__":
    main()