# core/player.py
import pygame
import os

# Importe as constantes necessárias
from config.settings import SCREEN_HEIGHT, GROUND_HEIGHT, PLAYER_CONFIG, SCREEN_WIDTH, COLORS

class Player:
    def __init__(self):
        self.width = PLAYER_CONFIG['width']
        self.height = PLAYER_CONFIG['height']
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = GROUND_HEIGHT - self.height  # Inicia no nível do chão
        self.speed = PLAYER_CONFIG['speed']
        self.direction = 'right'
        self.is_punching = False
        self.is_alive = True
        self.objects_destroyed = 0
        self.animation_speed = 0.15
        self.animation_index = 0

        # Carrega as animações
        self.load_animations()
        self.current_animation = 'idle_right'
        self.image = self.animations[self.current_animation][int(self.animation_index)]

    def load_animations(self):
        # Método para carregar todas as animações
        self.animations = {}
        animation_states = ['run_left', 'run_right', 'run_up', 'run_down',
                            'punch_left', 'punch_right', 'punch_up', 'punch_down'
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
            if not files:
                return images
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
            if self.is_punching:
                self.current_animation = 'punch_left'
            else:
                self.current_animation = 'run_left'
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = 'right'
            if self.is_punching:
                self.current_animation = 'punch_right'
            else:
                self.current_animation = 'run_right'
        elif keys[pygame.K_UP]:
            dy = -self.speed
            self.direction = 'up'
            if self.is_punching:
                self.current_animation = 'punch_up'
            else:
                self.current_animation = 'run_up'
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            self.direction = 'down'
            if self.is_punching:
                self.current_animation = 'punch_down'
            else:
                self.current_animation = 'run_down'
        else:
            # Animação de idle
            if self.direction == 'left':
                self.current_animation = 'idle_left'
            elif self.direction == 'right':
                self.current_animation = 'idle_right'
            elif self.direction == 'up':
                self.current_animation = 'idle_up'
            elif self.direction == 'down':
                self.current_animation = 'idle_down'

            # Se estiver socando parado
            if self.is_punching:
                if self.direction == 'left':
                    self.current_animation = 'punch_left'
                elif self.direction == 'right':
                    self.current_animation = 'punch_right'
                elif self.direction == 'up':
                    self.current_animation = 'punch_up'
                elif self.direction == 'down':
                    self.current_animation = 'punch_down'

        # Atualiza a posição do jogador
        self.x += dx
        self.y += dy

        # Mantém o jogador dentro dos limites da tela
        if self.x < 0:
            self.x = 0
        if self.x + self.width > screen_width:
            self.x = screen_width - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > ground_height:
            self.y = ground_height - self.height

        # Atualiza a animação
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animations[self.current_animation]):
            self.animation_index = 0
        self.image = self.animations[self.current_animation][int(self.animation_index)]

    def draw(self, screen):
        # Desenha o jogador na tela com a animação atual
        screen.blit(self.image, (self.x, self.y))
