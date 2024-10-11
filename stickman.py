# stickman.py > Pankadamón!
import pygame
import sys
import os
import random
import datetime

# Constants and settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 550  # Coordenada Y do chão
FPS = 60

# Colors
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'GRAY': (128, 128, 128),
    'DARK_GREEN': (0, 100, 0),
    'LIGHT_BLUE': (135, 206, 250),
    'DARK_BLUE': (25, 25, 112),
}

# Intro configuration
INTRO_CONFIG = {
    'text': "Pressione qualquer tecla para iniciar",
    'text_color': COLORS['WHITE'],
    'background_color': COLORS['BLACK'],
}

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pankadamón")

# Load font
font_path = os.path.join('assets', 'fonts', 'PressStart2P-Regular.ttf')
if not os.path.exists(font_path):
    print(f"Erro: Fonte não encontrada em {font_path}. Usando fonte padrão.")
    font_path = pygame.font.get_default_font()
font = pygame.font.Font(font_path, 16)

clock = pygame.time.Clock()

# AudioManager placeholder (Atualizado)
class AudioManager:
    def __init__(self):
        # Inicializa o mixer do Pygame
        pygame.mixer.init()
        
        # Caminhos para os arquivos de áudio
        self.intro_music_path = os.path.join('assets', 'sounds', 'intro_music.wav')
        self.day_music_path = os.path.join('assets', 'sounds', 'day_music.wav')
        self.night_music_path = os.path.join('assets', 'sounds', 'night_music.wav')
        
        # Estado atual da música
        self.current_music = None
    
    def load_sound(self, path):
        """
        Carrega um efeito sonoro a partir do caminho especificado.
        
        Args:
            path (str): Caminho para o arquivo de som.
        
        Returns:
            pygame.mixer.Sound: Objeto de som carregado ou None se falhar.
        """
        if os.path.exists(path):
            try:
                sound = pygame.mixer.Sound(path)
                return sound
            except pygame.error as e:
                print(f"Erro ao carregar o som {path}: {e}")
                return None
        else:
            print(f"Erro: Arquivo de som {path} não encontrado.")
            return None
    
    def play_intro_music(self):
        """
        Toca a música de introdução.
        """
        if os.path.exists(self.intro_music_path):
            pygame.mixer.music.load(self.intro_music_path)
            pygame.mixer.music.play(-1)  # -1 para repetir indefinidamente
            self.current_music = 'intro'
        else:
            print(f"Erro: Arquivo de música de introdução {self.intro_music_path} não encontrado.")
    
    def stop_music(self):
        """
        Para a música que está tocando.
        """
        pygame.mixer.music.stop()
        self.current_music = None
    
    def play_music(self, is_day):
        """
        Toca a música de fundo adequada com base no ciclo dia/noite.
        
        Args:
            is_day (bool): True se for dia, False se for noite.
        """
        if is_day:
            music_path = self.day_music_path
            music_state = 'day'
        else:
            music_path = self.night_music_path
            music_state = 'night'
        
        # Evita recarregar a mesma música
        if self.current_music == music_state:
            return
        
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # -1 para repetir indefinidamente
            self.current_music = music_state
        else:
            print(f"Erro: Arquivo de música {music_path} não encontrado.")


audio_manager = AudioManager()

# Utility functions
def draw_text(surface, text, font, color, position, max_width=None):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def check_collision(player, obstacles):
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    objects_destroyed = 0  # Contador de objetos destruídos nesta chamada

    for obstacle in obstacles[:]:
        obstacle_rect = obstacle['rect']
        if player_rect.colliderect(obstacle_rect):
            if obstacle['type'] == 'hole':
                player.is_alive = False
                return objects_destroyed  # Retorna o contador atual
            elif player.is_punching:
                obstacles.remove(obstacle)
                player.objects_destroyed += 1
                objects_destroyed += 1  # Incrementa o contador
            else:
                # Impedir o jogador de atravessar os obstáculos
                if player.direction == 'left':
                    player.x = obstacle_rect.right
                elif player.direction == 'right':
                    player.x = obstacle_rect.left - player.width
                elif player.direction == 'up':
                    player.y = obstacle_rect.bottom
                elif player.direction == 'down':
                    player.y = obstacle_rect.top - player.height

    return objects_destroyed  # Retorna o número de objetos destruídos nesta chamada

def save_score(player_name, total_objects_destroyed):
    """
    Salva a pontuação do jogador em um arquivo de log na pasta Scores.

    Args:
        player_name (str): Nome do jogador.
        total_objects_destroyed (int): Pontuação do jogador.
    """
    # Certifique-se de que o diretório Scores existe
    scores_dir = 'Scores'
    if not os.path.exists(scores_dir):
        os.makedirs(scores_dir)

    # Caminho para o arquivo de log
    log_file_path = os.path.join(scores_dir, 'scores.log')

    # Obtém a data e hora atuais
    now = datetime.datetime.now()
    date_time_str = now.strftime('%Y-%m-%d %H:%M:%S')

    # Prepara a entrada de log
    if player_name.strip() == '':
        player_name = 'Jogador Anônimo'

    log_entry = f"{date_time_str} - {player_name} - Pontuação: {total_objects_destroyed}\n"

    # Anexa a entrada de log ao arquivo
    with open(log_file_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)

# Player class
class Player:
    def __init__(self):
        self.width = 30
        self.height = 50
        self.x = (SCREEN_WIDTH - self.width) // 2  # Centraliza o jogador
        self.y = 50  # Garante que o jogador comece no chão
        self.speed = 5
        self.direction = 'right'
        self.is_punching = False
        self.is_alive = True
        self.objects_destroyed = 0
        self.animation_speed = 0.15
        self.animation_index = 0

        # Carrega as animações do jogador
        self.load_animations()
        self.current_animation = 'idle_right'
        self.image = self.animations[self.current_animation][int(self.animation_index)]

    def load_animations(self):
        # Método para carregar todas as animações
        self.animations = {}
        animation_states = ['run_left', 'run_right', 'run_up', 'run_down',
                            'punch_left', 'punch_right', 'punch_up', 'punch_down',
                            'idle_left', 'idle_right', 'idle_up', 'idle_down']

        for state in animation_states:
            path = os.path.join('assets', 'images', 'player', state)
            images = self.load_images(path)
            if images:
                self.animations[state] = images
            else:
                print(f"Aviso: Nenhuma imagem encontrada para o estado '{state}' em '{path}'. Usando espaço reservado.")
                # Cria uma imagem de espaço reservado
                placeholder = pygame.Surface((self.width, self.height))
                placeholder.fill(COLORS.get('BLACK', (0, 0, 0)))
                self.animations[state] = [placeholder]

    def load_images(self, folder_path):
        images = []
        if os.path.exists(folder_path):
            files = sorted(os.listdir(folder_path))
            for filename in files:
                if filename.endswith('.png'):
                    img_path = os.path.join(folder_path, filename)
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (self.width, self.height))
                    images.append(img)
        return images

    def update(self, keys, screen_width, screen_height, ground_height):
        dx = 0
        dy = 0

        # Movimentação do jogador
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = 'left'
            self.current_animation = 'run_left' if not self.is_punching else 'punch_left'
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = 'right'
            self.current_animation = 'run_right' if not self.is_punching else 'punch_right'
        elif keys[pygame.K_UP]:
            dy = -self.speed
            self.direction = 'up'
            self.current_animation = 'run_up' if not self.is_punching else 'punch_up'
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            self.direction = 'down'
            self.current_animation = 'run_down' if not self.is_punching else 'punch_down'
        else:
            # Animação de idle
            self.current_animation = f"idle_{self.direction}"
            if self.is_punching:
                self.current_animation = f"punch_{self.direction}"

        # Atualiza a posição do jogador
        self.x += dx
        self.y += dy

        # Mantém o jogador dentro dos limites verticais da tela
        if self.y < 0:
            self.y = 0
        if self.y + self.height > ground_height:
            self.y = ground_height - self.height

        # Atualiza a animação
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animations[self.current_animation]):
            self.animation_index = 0
        self.image = self.animations[self.current_animation][int(self.animation_index)]

    def draw(self, surface):
        # Desenha o jogador na tela com a animação atual
        surface.blit(self.image, (self.x, self.y))

# Map class
class Map:
    def __init__(self, difficulty_level=1):
        self.elements = []
        self.is_day = True  # Placeholder para o ciclo dia/noite
        self.current_background_color = COLORS.get('LIGHT_BLUE', (135, 206, 250))
        self.day_duration_seconds = 180  # Duração de um ciclo dia/noite em segundos
        self.start_time = pygame.time.get_ticks()
        self.difficulty_level = difficulty_level

        # Carrega as imagens dos obstáculos
        self.load_assets()
        self.create_elements()

    def load_assets(self):
        # Carrega as imagens de obstáculos com dimensionamento adequado
        self.rock_images = self.load_images('assets/images/obstacles/rocks', (50, 50))
        self.tree_images = self.load_images('assets/images/obstacles/trees', (50, 70))
        self.hole_images = self.load_images('assets/images/obstacles/holes', (60, 30))

        # Caso as imagens não existam, cria superfícies padrão
        if not self.rock_images:
            print("Aviso: Nenhuma imagem de rocha encontrada. Usando espaço reservado.")
            rock_image = pygame.Surface((50, 50))
            rock_image.fill(COLORS.get('GRAY', (128, 128, 128)))
            self.rock_images = [rock_image]

        if not self.tree_images:
            print("Aviso: Nenhuma imagem de árvore encontrada. Usando espaço reservado.")
            tree_image = pygame.Surface((50, 70))
            tree_image.fill(COLORS.get('DARK_GREEN', (0, 100, 0)))
            self.tree_images = [tree_image]

        if not self.hole_images:
            print("Aviso: Nenhuma imagem de buraco encontrada. Usando espaço reservado.")
            hole_image = pygame.Surface((60, 30))
            hole_image.fill(COLORS.get('BLACK', (0, 0, 0)))
            self.hole_images = [hole_image]

    def load_images(self, folder_path, size):
        images = []
        if os.path.exists(folder_path):
            files = sorted(os.listdir(folder_path))
            if not files:
                print(f"Aviso: Nenhuma imagem encontrada na pasta '{folder_path}'.")
            for filename in files:
                if filename.endswith('.png'):
                    img_path = os.path.join(folder_path, filename)
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, size)
                    images.append(img)
        else:
            print(f"Aviso: Pasta '{folder_path}' não encontrada. Usando imagens de espaço reservado.")
        return images

    def create_elements(self):
        # Gera obstáculos e buracos em posições aleatórias
        num_elements = 10 + self.difficulty_level * 5
        self.elements = []
        for i in range(num_elements):
            # Ajusta a probabilidade de cada tipo de obstáculo
            obstacle_type = random.choices(
                ['rock', 'tree', 'hole'],
                weights=[50, 30, 20 + self.difficulty_level * 5],  # Ajusta pesos conforme a dificuldade
                k=1
            )[0]
            x = random.randint(100, SCREEN_WIDTH - 100)

            # Define a posição Y para evitar a área inicial do jogador
            # Supondo que a área inicial do jogador esteja entre y=0 e y=100
            y = random.randint(200, GROUND_HEIGHT - 50)  # Ajuste conforme necessário

            if obstacle_type == 'rock':
                image = random.choice(self.rock_images)
                rect = image.get_rect(topleft=(x, y))
                self.elements.append({'type': 'rock', 'rect': rect, 'image': image})
            elif obstacle_type == 'tree':
                image = random.choice(self.tree_images)
                rect = image.get_rect(topleft=(x, y - 20))  # Ajuste para posicionar a árvore corretamente
                self.elements.append({'type': 'tree', 'rect': rect, 'image': image})
            elif obstacle_type == 'hole':
                image = random.choice(self.hole_images)
                rect = image.get_rect(topleft=(x, y + 20))  # Ajuste para posicionar o buraco corretamente
                self.elements.append({'type': 'hole', 'rect': rect, 'image': image})

    def update(self, player):
        # Atualiza o ciclo dia/noite
        self.update_day_night_cycle()
        # Aqui você pode adicionar lógica para atualizar elementos do mapa, se necessário

    def update_day_night_cycle(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Tempo em segundos
        cycle_progress = (elapsed_time % self.day_duration_seconds) / self.day_duration_seconds
        if cycle_progress < 0.5:
            # Dia
            self.is_day = True
            target_color = COLORS.get('LIGHT_BLUE', (135, 206, 250))
        else:
            # Noite
            self.is_day = False
            target_color = COLORS.get('DARK_BLUE', (25, 25, 112))

        # Transição suave entre as cores
        self.current_background_color = [
            self.current_background_color[i] + (target_color[i] - self.current_background_color[i]) * 0.01
            for i in range(3)
        ]

    def draw(self, surface):
        # Desenha o fundo com a cor atual do ciclo dia/noite
        background_color = tuple(map(int, self.current_background_color))
        surface.fill(background_color)

        # Desenha o chão
        ground_color = COLORS.get('GREEN', (0, 128, 0))
        pygame.draw.rect(surface, ground_color, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))

        # Desenha os elementos (obstáculos e buracos)
        for element in self.elements:
            surface.blit(element['image'], (element['rect'].x, element['rect'].y))

def game_intro():
    """
    Mostra a tela de introdução do jogo e espera uma tecla para iniciar.
    """
    intro = True
    font = pygame.font.Font(font_path, 16)
    text = font.render(INTRO_CONFIG['text'], True, INTRO_CONFIG['text_color'])
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    
    # Carrega a imagem de introdução
    intro_image_path = os.path.join('assets', 'images', 'intro_image.png')
    if os.path.exists(intro_image_path):
        intro_image = pygame.image.load(intro_image_path).convert_alpha()
        # Redimensiona a imagem se necessário
        max_width = 600
        if intro_image.get_width() > max_width:
            scale_factor = max_width / intro_image.get_width()
            new_size = (int(intro_image.get_width() * scale_factor), int(intro_image.get_height() * scale_factor))
            intro_image = pygame.transform.scale(intro_image, new_size)
    else:
        print(f"Erro: Arquivo de imagem de introdução '{intro_image_path}' não encontrado.")
        # Cria uma superfície de espaço reservado caso a imagem não seja encontrada
        intro_image = pygame.Surface((300, 200))
        intro_image.fill(COLORS['GRAY'])
        # Opcional: adicionar texto de aviso na imagem de espaço reservado
        placeholder_font = pygame.font.Font(font_path, 20)
        placeholder_text = placeholder_font.render("Imagem não encontrada", True, COLORS['WHITE'])
        placeholder_rect = placeholder_text.get_rect(center=(150, 100))
        intro_image.blit(placeholder_text, placeholder_rect)

    # Obtém o retângulo da imagem e centraliza horizontalmente
    intro_image_rect = intro_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))  # 50 pixels acima do centro

    # Define a posição do texto abaixo da imagem
    text_rect.centerx = SCREEN_WIDTH / 2
    text_rect.top = intro_image_rect.bottom + 20  # 20 pixels abaixo da imagem

    # Cria uma superfície para o efeito de fade
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(INTRO_CONFIG['background_color'])
    fade_surface.set_alpha(255)  # Opacidade total

    # Toca a música de introdução
    audio_manager.play_intro_music()
    
    # Parâmetros para o efeito de fade-in
    fade_in = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                intro = False
                audio_manager.stop_music()  # Para a música de introdução

        # Preenche o fundo com a cor de fundo configurada
        screen.fill(INTRO_CONFIG['background_color'])

        # Desenha a imagem de introdução
        screen.blit(intro_image, intro_image_rect)

        # Desenha o texto abaixo da imagem
        screen.blit(text, text_rect)

        # Efeito de fade-in
        if fade_in:
            if fade_surface.get_alpha() > 0:
                fade_surface.set_alpha(fade_surface.get_alpha() - 5)  # Reduz a opacidade gradualmente
                screen.blit(fade_surface, (0, 0))
            else:
                fade_in = False  # Finaliza o efeito de fade-in

        # Atualiza a tela
        pygame.display.flip()

        # Controla o frame rate
        clock.tick(FPS)

def game_over(player, total_objects_destroyed):
    """
    Mostra a tela de Game Over, permite que o jogador insira seu nome e salva a pontuação.

    Args:
        player (Player): Objeto do jogador.
        total_objects_destroyed (int): Pontuação total do jogador.
    """
    over = True
    font = pygame.font.Font(font_path, 16)
    game_over_text = f"Sua pontuação: {total_objects_destroyed}"
    name_prompt_text = "Digite seu nome (ou deixe em branco):"
    player_name = ''
    enter_name = True

    # Renderiza os textos iniciais
    text1 = font.render(game_over_text, True, COLORS['GREEN'])
    text1_rect = text1.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))

    name_prompt = font.render(name_prompt_text, True, COLORS['BLACK'])
    name_prompt_rect = name_prompt.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30))

    # Caixa de entrada para o nome
    name_input_rect = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2, 200, 30)
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('dodgerblue2')
    color = color_inactive

    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if enter_name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        enter_name = False  # Termina a entrada do nome
                        # Salva a pontuação no arquivo de log
                        save_score(player_name, total_objects_destroyed)
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 20:
                            player_name += event.unicode
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        over = False  # Reinicia o jogo
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        screen.fill(COLORS['BLACK'])
        screen.blit(text1, text1_rect)

        if enter_name:
            # Desenha o prompt para inserir o nome
            screen.blit(name_prompt, name_prompt_rect)
            # Renderiza o nome atual
            name_surface = font.render(player_name, True, COLORS['WHITE'])
            # Desenha a caixa de entrada
            pygame.draw.rect(screen, color, name_input_rect, 2)
            # Blita o nome na tela
            screen.blit(name_surface, (name_input_rect.x + 5, name_input_rect.y + 5))
            pygame.display.flip()
        else:
            # Após o nome ser inserido, mostra as opções para reiniciar ou sair
            restart_text = "ENTER para tentar novamente ou ESC para sair"
            text2 = font.render(restart_text, True, COLORS['WHITE'])
            text2_rect = text2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))
            screen.blit(text2, text2_rect)
            pygame.display.flip()

def game_loop():
    """
    Executa o loop principal do jogo, atualizando e desenhando elementos.
    """
    player = Player()
    difficulty_level = 1  # Nível de dificuldade inicial
    game_map = Map(difficulty_level)
    audio_manager.stop_music()
    total_objects_destroyed = 0  # Pontuação total acumulada

    # Toca a música de fundo inicial
    audio_manager.play_music(game_map.is_day)
    
    while True:
        # Trata os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Teclas pressionadas
        keys = pygame.key.get_pressed()

        # Atualiza o jogador
        player.is_punching = False
        if keys[pygame.K_SPACE]:
            player.is_punching = True

        player.update(keys, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT)

        # Verifica se o jogador tocou nas extremidades esquerda ou direita
        if player.x + player.width < 0:
            # Saiu pela esquerda
            player.x = SCREEN_WIDTH  # Aparece na direita
            difficulty_level += 1  # Incrementa a dificuldade
            game_map = Map(difficulty_level)  # Gera um novo mapa com dificuldade aumentada
            audio_manager.play_music(game_map.is_day)  # Atualiza a música de fundo
        elif player.x > SCREEN_WIDTH:
            # Saiu pela direita
            player.x = -player.width  # Aparece na esquerda
            difficulty_level += 1  # Incrementa a dificuldade
            game_map = Map(difficulty_level)  # Gera um novo mapa com dificuldade aumentada
            audio_manager.play_music(game_map.is_day)  # Atualiza a música de fundo
    
        obstacles = game_map.elements  # Atualiza a referência dos obstáculos
    
        # Atualiza o mapa
        game_map.update(player)
    
        # Verifica se o ciclo dia/noite mudou e atualiza a música se necessário
        audio_manager.play_music(game_map.is_day)
    
        # Verifica colisões e atualiza obstáculos
        objects_destroyed = check_collision(player, obstacles)
        total_objects_destroyed += objects_destroyed
    
        # Verifica se o jogador caiu em um buraco
        if not player.is_alive:
            game_over(player, total_objects_destroyed)
            return  # Reinicia o jogo
    
        # Desenha tudo
        game_map.draw(screen)
        player.draw(screen)
        draw_text(screen, f"Poder de destruição: {total_objects_destroyed}", font, COLORS['BLACK'], (10, 10))
        draw_text(screen, f"Nível: {difficulty_level}", font, COLORS['BLACK'], (10, 40))
    
        # Atualiza a tela
        pygame.display.flip()
    
        # Controla o frame rate
        clock.tick(FPS)

# Execução principal
game_intro()
while True:
    game_loop()
