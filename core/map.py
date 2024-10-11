# core/map.py
import pygame
import random
import os

# Importe as constantes necessárias
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT, COLORS

class Map:
    def __init__(self):
        self.elements = []
        self.is_day = True  # Placeholder para o ciclo dia/noite
        self.current_background_color = COLORS.get('LIGHT_BLUE', (135, 206, 250))
        self.day_duration_seconds = 300  # Duração de um ciclo dia/noite em segundos
        self.start_time = pygame.time.get_ticks()
        
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
        self.elements = []
        for i in range(15):
            obstacle_type = random.choice(['rock', 'tree', 'hole'])
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = GROUND_HEIGHT - 50  # Ajuste a altura conforme necessário
            
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
    
    def draw(self, screen):
        # Desenha o fundo com a cor atual do ciclo dia/noite
        background_color = tuple(map(int, self.current_background_color))
        screen.fill(background_color)
        
        # Desenha o chão
        ground_color = COLORS.get('GREEN', (0, 128, 0))
        pygame.draw.rect(screen, ground_color, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        # Desenha os elementos (obstáculos e buracos)
        for element in self.elements:
            screen.blit(element['image'], (element['rect'].x, element['rect'].y))
