import os
import pygame
import time


class SoundManager:
    def __init__(self):
        # Инициализируем pygame mixer с обработкой ошибок
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.initialized = True
            print("Звуковая система инициализирована")
        except Exception as e:
            print(f"Ошибка инициализации звука: {e}")
            self.initialized = False
            return

        # Путь к папке со звуками
        self.sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')

        # Создаем папку если не существует
        os.makedirs(self.sounds_dir, exist_ok=True)

        # Загрузка звуков
        self.sounds = {}
        self.load_sounds()

        self.volume = 0.7
        self.last_play_time = 0
        self.set_volume(self.volume)

    def load_sounds(self):
        """Загружает звуковые файлы с заглушками"""
        sound_files = {
            'correct': 'correct.mp3',
            'wrong': 'wrong.mp3',
            'hint': 'hint.mp3',
            'final_answer': 'final_answer.mp3',
            'win': 'win.mp3'
        }

        for sound_name, filename in sound_files.items():
            try:
                sound_path = os.path.join(self.sounds_dir, filename)
                if os.path.exists(sound_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                    print(f"Загружен: {filename}")
                else:
                    print(f"Файл не найден: {filename}")
                    self.sounds[sound_name] = None
            except Exception as e:
                print(f"Ошибка загрузки {filename}: {e}")
                self.sounds[sound_name] = None

    def play_sound(self, sound_name):
        """Воспроизводит звук с защитой от наложения"""
        if not self.initialized:
            return

        current_time = time.time()
        # Защита от наложения звуков - минимум 0.5 сек между звуками
        if current_time - self.last_play_time < 0.5:
            return

        self.last_play_time = current_time

        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                # Останавливаем предыдущие звуки
                pygame.mixer.stop()
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Ошибка воспроизведения {sound_name}: {e}")

    def set_volume(self, volume):
        """Устанавливает громкость"""
        if not self.initialized:
            return

        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound:
                try:
                    sound.set_volume(self.volume)
                except:
                    pass

    def stop_all(self):
        """Останавливает все звуки"""
        if self.initialized:
            pygame.mixer.stop()

    # Методы для конкретных звуков
    def play_correct(self):
        self.play_sound('correct')

    def play_wrong(self):
        self.play_sound('wrong')

    def play_final_answer(self):
        self.play_sound('final_answer')

    def play_hint(self):
        self.play_sound('hint')

    def play_win(self):
        self.play_sound('win')


# Глобальный экземпляр
sound_manager = SoundManager()