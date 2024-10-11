# utils/helpers.py
import pygame

def check_collision(player, obstacles):
    """
    Verifica colisões entre o jogador e os obstáculos e processa de acordo com o tipo de obstáculo.

    :param player: Objeto do jogador.
    :param obstacles: Lista de obstáculos no mapa.
    """
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for obstacle in obstacles[:]:  # Iterar sobre uma cópia da lista para evitar problemas ao remover
        obstacle_rect = obstacle['rect']
        if player_rect.colliderect(obstacle_rect):
            if obstacle['type'] == 'hole':
                # O jogador cai no buraco
                player.is_alive = False
                return  # Não precisa verificar mais colisões
            elif player.is_punching:
                # O jogador destrói o obstáculo
                obstacles.remove(obstacle)
                player.objects_destroyed += 1
            else:
                # Impedir o jogador de atravessar o obstáculo
                if player.direction == 'left':
                    player.x = obstacle_rect.right
                elif player.direction == 'right':
                    player.x = obstacle_rect.left - player.width
                elif player.direction == 'up':
                    player.y = obstacle_rect.bottom
                elif player.direction == 'down':
                    player.y = obstacle_rect.top - player.height

def draw_text(surface, text, font, color, position, max_width=None):
    """
    Função para desenhar texto na tela, quebrando linhas se necessário para caber na largura máxima.

    :param surface: A superfície onde o texto será desenhado (ex.: tela do jogo).
    :param text: O texto a ser desenhado.
    :param font: A fonte a ser usada para o texto.
    :param color: A cor do texto.
    :param position: Uma tupla (x, y) representando a posição onde o texto será desenhado.
    :param max_width: Largura máxima permitida para o texto (opcional).
    """
    if max_width is None:
        # Sem quebra de linha
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=position)
        surface.blit(text_surface, text_rect)
    else:
        # Quebra de linha para caber no max_width
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width, _ = font.size(word + ' ')
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        lines.append(' '.join(current_line))

        y_offset = 0
        for line in lines:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(topleft=(position[0], position[1] + y_offset))
            surface.blit(text_surface, text_rect)
            y_offset += font.get_linesize()
