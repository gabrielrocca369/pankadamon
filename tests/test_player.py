# tests/test_player.py
import unittest
import pygame
from core.player import Player
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT

class TestPlayer(unittest.TestCase):
    def setUp(self):
        # Inicializa o Pygame e cria uma instância do jogador para teste
        pygame.init()
        self.player = Player()

    def test_initial_position(self):
        # Testa se o jogador está na posição inicial correta
        expected_x = SCREEN_WIDTH // 2
        expected_y = SCREEN_HEIGHT - self.player.height - GROUND_HEIGHT
        self.assertEqual(self.player.x, expected_x, "A posição inicial X do jogador está incorreta.")
        self.assertEqual(self.player.y, expected_y, "A posição inicial Y do jogador está incorreta.")

    def test_movement_left(self):
        # Simula movimento para a esquerda
        initial_x = self.player.x
        keys = {pygame.K_LEFT: True}
        self.player.update(keys, [0, 0], SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT)
        self.assertLess(self.player.x, initial_x, "O jogador não se moveu para a esquerda corretamente.")

    def test_movement_right(self):
        # Simula movimento para a direita
        initial_x = self.player.x
        keys = {pygame.K_RIGHT: True}
        self.player.update(keys, [0, 0], SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT)
        self.assertGreater(self.player.x, initial_x, "O jogador não se moveu para a direita corretamente.")

    def test_jump(self):
        # Testa se o jogador pode pular
        keys = {pygame.K_SPACE: True}
        initial_y = self.player.y
        self.player.update(keys, [0, 0], SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT)
        self.assertNotEqual(self.player.y, initial_y, "O jogador não iniciou o pulo corretamente.")
        self.assertTrue(self.player.is_jumping, "O estado de pulo do jogador não foi atualizado corretamente.")

    def test_gravity_effect(self):
        # Simula o efeito da gravidade
        self.player.is_jumping = True
        initial_y = self.player.y
        self.player.update({}, [0, 0], SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT)
        self.assertGreater(self.player.y, initial_y, "A gravidade não afetou o jogador corretamente.")

    def test_landing(self):
        # Testa se o jogador aterrissa corretamente
        self.player.velocity_y = 5
        self.player.is_jumping = True
        self.player.update({}, [0, 0], SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT)
        self.assertFalse(self.player.is_jumping, "O jogador não aterrissou corretamente.")
        self.assertEqual(self.player.y, SCREEN_HEIGHT - self.player.height - GROUND_HEIGHT, "A posição do jogador após aterrissar está incorreta.")

    def test_animation_change(self):
        # Testa se a animação muda conforme a direção
        keys = {pygame.K_LEFT: True}
        self.player.update(keys, [0, 0], SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT)
        self.assertEqual(self.player.current_animation, 'run_left', "A animação não mudou corretamente para 'run_left'.")

    def tearDown(self):
        # Finaliza o Pygame
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
