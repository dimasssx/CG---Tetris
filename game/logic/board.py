from ..utils.constants import BOARD_COLOR

class Board:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.color = BOARD_COLOR

    def is_valid_position(self, piece, adj_x=0, adj_y=0):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = piece.x + j + adj_x
                    y = piece.y + i + adj_y
                    if x < 0 or x >= self.width or y >= self.height:
                        return False
                    if y >= 0 and self.grid[y][x] is not None:
                        return False
        return True
    def update(self, piece):
        if self.is_valid_position(piece, adj_y=1):
            piece.y += 1
        else:
            self.lock_piece(piece)

    def lock_piece(self, piece):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = piece.x + j
                    y = piece.y + i
                    if y >= 0:
                        self.grid[y][x] = piece.color
        # MODIFICADO: Agora, lock_piece retorna o número de linhas limpas.
        return self.clear_lines()

    def clear_lines(self):
        new_grid = [row for row in self.grid if not all(cell is not None for cell in row)]
        lines_cleared = self.height - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(self.width)])
        self.grid = new_grid
         # ADICIONADO: Retorna o número de linhas que foram limpas para calcular pontos.
        return lines_cleared

