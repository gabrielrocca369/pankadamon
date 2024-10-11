# config/settings.py

# Configurações da tela
SCREEN_WIDTH = 800  # Largura da tela atualizada para acomodar melhor os elementos
SCREEN_HEIGHT = 600  # Altura da tela atualizada
GROUND_HEIGHT = 550  # Coordenada Y do chão

# Configurações do jogador
PLAYER_CONFIG = {
    'width': 30,    # Largura do jogador ajustada
    'height': 50,   # Altura do jogador ajustada
    'speed': 5,     # Velocidade de movimento atualizada
    'color': (0, 0, 0)  # Cor do jogador (preto), se usar desenho ao invés de sprite
}

# Cores usadas no jogo
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'GRAY': (128, 128, 128),
    'RED': (255, 0, 0),
    'GREEN': (0, 128, 0),
    'DARK_GREEN': (0, 100, 0),
    'LIGHT_BLUE': (135, 206, 250),
    'DARK_BLUE': (25, 25, 112)
}

# Configurações de FPS (Frames por Segundo)
FPS = 60  # FPS aumentado para uma animação mais suave

# Duração do ciclo dia/noite em segundos
DAY_DURATION_SECONDS = 60  # Mantido o mesmo

# Configurações da tela de introdução
INTRO_CONFIG = {
    'font_size': 24,  # Tamanho da fonte ajustado para melhor visibilidade
    'text': "Pressione qualquer tecla para iniciar",
    'text_color': COLORS['BLACK'],
    'background_color': COLORS['WHITE']
}

# Caminho para a fonte estilo retrô
FONT_PATH = 'assets/fonts/PressStart2P-Regular.ttf'
