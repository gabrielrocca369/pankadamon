# core/audio.py
import pygame
import os

class AudioManager:
    def __init__(self):
        # Inicializa o mixer do pygame para áudio
        pygame.mixer.init()
        
        # Carrega músicas para o ciclo dia/noite e a introdução
        self.day_music_path = os.path.join('assets', 'sounds', 'day_music.wav')
        self.night_music_path = os.path.join('assets', 'sounds', 'night_music.wav')
        self.intro_music_path = os.path.join('assets', 'sounds', 'intro_music.wav')
        
        # Variável para armazenar o estado atual da música
        self.current_music = None
   
    def play_music(self, is_day):
        """
        Reproduz a música correspondente ao ciclo dia/noite.
        
        :param is_day: Booleano indicando se é dia ou noite.
        """
        if is_day and self.current_music != 'day':
            self._load_and_play_music(self.day_music_path)
            self.current_music = 'day'
        elif not is_day and self.current_music != 'night':
            self._load_and_play_music(self.night_music_path)
            self.current_music = 'night'
    
    def play_intro_music(self):
        """Reproduz a música da tela de introdução."""
        if self.current_music != 'intro':
            self._load_and_play_music(self.intro_music_path)
            self.current_music = 'intro'
    
    def stop_music(self):
        """Para a música atual."""
        pygame.mixer.music.stop()
        self.current_music = None

    def _load_and_play_music(self, music_path):
        """Carrega e reproduz a música especificada."""
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Reproduz em loop
        except pygame.error as e:
            print(f"Erro ao carregar a música: {e}")
