 # Projeto Tetris - Computação Gráfica

Um clássico jogo Tetris desenvolvido em Python utilizando a biblioteca PyOpenGL para renderização. Este projeto foi criado como parte dos requisitos da disciplina de Computação Gráfica.

![Screenshot do Jogo](./screenshot.png)

## Funcionalidades Implementadas

* **Tela de Início Interativa:** Menu principal com botões para iniciar e sair do jogo.
* **Gameplay Clássica:** Movimentação, rotação, soft drop e hard drop.
* **Sistema de Pontuação:** Pontos são ganhos por queda de peças e por linhas completadas.
* **Sistema de Níveis:** A velocidade do jogo aumenta a cada 10 linhas completadas.
* **Peça Fantasma (Ghost Piece):** Mostra onde a peça atual irá aterrissar.
* **Função Hold:** Permite guardar uma peça para uso posterior.
* **Sorteio "7-bag":** As 7 primeiras peças são sorteadas sem repetição, garantindo variedade no início do jogo.
* **Telas de Game Over e Reinício:** Exibe a pontuação final, o tempo de jogo e permite reiniciar a partida.

## Requisitos

* Python 3.8 ou superior
* Bibliotecas listadas no arquivo `requirements.txt`

## Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o jogo no seu computador.

1.  **Clone o Repositório**
    Abra um terminal e clone o projeto usando Git:
    ```bash
    git clone ```

2.  **Navegue até a Pasta**
    ```bash
    cd CG---Tetris
    ```

3.  **Instale as Dependências**
    Com o Python e o pip instalados, execute o comando abaixo para instalar as bibliotecas necessárias (PyOpenGL).
    ```bash
    pip install -r requirements.txt
    ```
    *(Observação: Este projeto não utiliza ambiente virtual, então as dependências serão instaladas globalmente).*

4.  **Execute o Jogo**
    Para iniciar o jogo, execute o script principal:
    ```bash
    python main.py
    ```
    O jogo iniciará na tela de menu.

## Controles do Jogo

| Tecla | Ação |
| :--- | :--- |
| **A** | Mover peça para a Esquerda |
| **D** | Mover peça para a Direita |
| **S** | Acelerar queda (Soft Drop) |
| **W** | Rotacionar a peça |
| **C** | Guardar a peça atual (Hold) |
| **Espaço** | Queda instantânea (Hard Drop) |
| **R** | Reiniciar o jogo (na tela de Game Over) |
| **ESC**| Fechar o jogo |

## Autores

* José Portela
* Pedro Tobias 
* Dimas Celestino
* Joaci Laurindo
* Augusto Jorge
