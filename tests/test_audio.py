# tests/test_audio.py
import unittest
import pygame
from core.audio import AudioManager

class TestAudioManager(unittest.TestCase):
    def setUp(self):
        # Inicializa o Pygame mixer e cria uma instância do AudioManager para os testes
        pygame.mixer.init()
        self.audio_manager = AudioManager()

    def test_jump_sound(self):
        # Testa se o som de pulo pode ser reproduzido sem erros
        try:
            self.audio_manager.play_jump_sound()
        except Exception as e:
            self.fail(f"play_jump_sound() levantou uma exceção inesperada: {e}")

    def test_play_music_day(self):
        # Testa se a música do dia pode ser reproduzida sem erros
        try:
            self.audio_manager.play_music(is_day=True)
        except Exception as e:
            self.fail(f"play_music(is_day=True) levantou uma exceção inesperada: {e}")

    def test_play_music_night(self):
        # Testa se a música da noite pode ser reproduzida sem erros
        try:
            self.audio_manager.play_music(is_day=False)
        except Exception as e:
            self.fail(f"play_music(is_day=False) levantou uma exceção inesperada: {e}")

    def tearDown(self):
        # Finaliza o Pygame mixer
        pygame.mixer.quit()

if __name__ == "__main__":
    unittest.main()