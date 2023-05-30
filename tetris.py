import pygame
import random
import pygame_gui

fileiras_completas = 0



# Inicialização do Pygame
pygame.init()


# Definição das cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
CIANO = (0, 255, 255)
AMARELO = (255, 255, 0)
ROXO = (255, 0, 255)
LARANJA = (255, 165, 0)

# Configurações da tela
largura_tela = 900
altura_tela = 900
tamanho_bloco = 30

# Configurações do tabuleiro
largura_tabuleiro = 19
altura_tabuleiro = 30

# Configurações das peças
formas = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 1], [1, 0, 0]]  # L
]

cores = [CIANO, AMARELO, ROXO, VERDE, VERMELHO, LARANJA, AZUL]

# Inicialização da tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Tetris")

# Criação do objeto clock
clock = pygame.time.Clock()

# Função para criar a matriz do tabuleiro vazia
def criar_tabuleiro():
    tabuleiro = [[PRETO for _ in range(largura_tabuleiro)] for _ in range(altura_tabuleiro)]
    return tabuleiro

# Função para desenhar o tabuleiro na tela
def desenhar_tabuleiro(tabuleiro):
    for i in range(altura_tabuleiro):
        for j in range(largura_tabuleiro):
            pygame.draw.rect(tela, tabuleiro[i][j], (j * tamanho_bloco, i * tamanho_bloco, tamanho_bloco, tamanho_bloco))
            pygame.draw.rect(tela, BRANCO, (j * tamanho_bloco, i * tamanho_bloco, tamanho_bloco, tamanho_bloco), 1)

# Função para criar uma nova peça aleatória
def nova_peca():
    forma = random.choice(formas)
    cor = random.choice(cores)
    peca = {
        'forma': forma,
        'cor': cor,
        'x': largura_tabuleiro // 2 - len(forma[0]) // 2,
        'y': 0
    }
    return peca

# Função para verificar se uma posição é válida
def posicao_valida(peca, tabuleiro, dx=0, dy=0):
    for i in range(len(peca['forma'])):
        for j in range(len(peca['forma'][0])):
            if peca['forma'][i][j] != 0:
                novo_x = peca['x'] + j + dx
                novo_y = peca['y'] + i + dy
                if novo_x < 0 or novo_x >= largura_tabuleiro or novo_y >= altura_tabuleiro or tabuleiro[novo_y][novo_x] != PRETO:
                    return False
    return True

# Função para desenhar a peça na tela
def desenhar_peca(peca):
    for i in range(len(peca['forma'])):
        for j in range(len(peca['forma'][0])):
            if peca['forma'][i][j] != 0:
                pygame.draw.rect(tela, peca['cor'], ((peca['x'] + j) * tamanho_bloco, (peca['y'] + i) * tamanho_bloco, tamanho_bloco, tamanho_bloco))
                pygame.draw.rect(tela, BRANCO, ((peca['x'] + j) * tamanho_bloco, (peca['y'] + i) * tamanho_bloco, tamanho_bloco, tamanho_bloco), 1)

# Função para atualizar o tabuleiro com a posição da peça
def atualizar_tabuleiro(tabuleiro, peca):
    for i in range(len(peca['forma'])):
        for j in range(len(peca['forma'][0])):
            if peca['forma'][i][j] != 0:
                tabuleiro[peca['y'] + i][peca['x'] + j] = peca['cor']

# Função para remover as linhas completas do tabuleiro
def remover_linhas(tabuleiro):
    global fileiras_completas

    linhas_completas = []
    for i in range(altura_tabuleiro):
        if PRETO not in tabuleiro[i]:
            linhas_completas.append(i)

    for linha in linhas_completas:
        del tabuleiro[linha]
        tabuleiro.insert(0, [PRETO for _ in range(largura_tabuleiro)])

    # Atualizar a contagem de fileiras completas
    fileiras_completas += len(linhas_completas)

    

    
# Função principal do jogo
def jogar_tetris():
    tabuleiro = criar_tabuleiro()
    peca_atual = nova_peca()
    pontuacao = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and posicao_valida(peca_atual, tabuleiro, dx=-1):
                    peca_atual['x'] -= 1
                elif event.key == pygame.K_RIGHT and posicao_valida(peca_atual, tabuleiro, dx=1):
                    peca_atual['x'] += 1
                elif event.key == pygame.K_DOWN and posicao_valida(peca_atual, tabuleiro, dy=1):
                    peca_atual['y'] += 1
                elif event.key == pygame.K_SPACE:
                    while posicao_valida(peca_atual, tabuleiro, dy=1):
                        peca_atual['y'] += 1
                elif event.key == pygame.K_UP:
                    girar_peca_horario(peca_atual)
                elif event.key == pygame.K_z or event.key == pygame.K_w:
                    girar_peca_anti_horario(peca_atual)

        

        if posicao_valida(peca_atual, tabuleiro, dy=1):
            peca_atual['y'] += 1
        else:
            atualizar_tabuleiro(tabuleiro, peca_atual)
            remover_linhas(tabuleiro)
            pontuacao += 10

            if peca_atual['y'] == 0:
                pygame.quit()
                return

            peca_atual = nova_peca()

        def girar_peca_horario(peca):
            nova_forma = list(zip(*reversed(peca['forma'])))
            peca['forma'] = nova_forma

        def girar_peca_anti_horario(peca):
            nova_forma = list(reversed(list(zip(*peca['forma']))))
            peca['forma'] = nova_forma

        
            

        tela.fill(PRETO)
        desenhar_tabuleiro(tabuleiro)
        
        desenhar_peca(peca_atual)

        def exibir_pontuacao():
                fonte = pygame.font.Font(None, 36)
                texto_fileiras = fonte.render("Fileiras: " + str(fileiras_completas), True, BRANCO)
                tela.blit(texto_fileiras, (largura_tela - 150, 100))
        
        exibir_pontuacao()
        
        pygame.display.update()
        

        # Limitação da taxa de atualização do jogo
        clock.tick(4)  # Ajuste o valor para controlar a velocidade do jogo (10 fps no exemplo)


# Execução do jogo
jogar_tetris()
