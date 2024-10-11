# tests/test_map.py
import unittest
import pygame
from core.map import Map
from core.player import Player
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class TestMap(unittest.TestCase):
    def setUp(self):
        # Inicializa o Pygame e cria instâncias para teste
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.map = Map()
        self.player = Player()

    def test_generate_elements(self):
        # Testa se os elementos foram gerados corretamente
        initial_elements_count = len(self.map.elements)
        self.assertGreater(initial_elements_count, 0, "Os elementos do mapa não foram gerados corretamente.")

    def test_update_scroll(self):
        # Salva a posição inicial do scroll
        initial_scroll = self.map.scroll[:]
        # Atualiza o mapa com um jogador em movimento para a direita
        self.player.x += 10
        self.map.update(self.player)
        # Testa se o scroll do mapa foi atualizado corretamente
        self.assertNotEqual(initial_scroll, self.map.scroll, "O scroll do mapa não foi atualizado corretamente ao mover o jogador.")

    def test_check_collision(self):
        # Posiciona o jogador em um ponto com um obstáculo
        for element in self.map.elements:
            if element['type'] == 'rock':
                self.player.x = element['x']
                self.player.y = element['y']
                break
        # Verifica colisão
        self.map.check_collision(self.player)
        # Testa se o jogador foi reposicionado ao colidir com uma pedra
        self.assertLess(self.player.x, element['x'], "O jogador não foi reposicionado corretamente após colidir com uma pedra.")

    def test_draw_map(self):
        # Testa se o método draw é executado sem erros
        try:
            self.map.draw(self.screen)
        except Exception as e:
            self.fail(f"O método draw do mapa falhou ao ser executado: {e}")

    def tearDown(self):
        # Finaliza o Pygame
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
