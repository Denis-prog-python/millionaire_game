import tkinter as tk
from tkinter import messagebox, Frame, Label, Button, Canvas, Scale
from game_logic import GameState
import random
from sound_manager import sound_manager


class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Кто хочет стать миллионером?")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")

        # Цветовая схема
        self.colors = {
            'bg': '#2c3e50',
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'accent': '#e74c3c',
            'text': '#ecf0f1',
            'button': '#2980b9',
            'button_hover': '#1f618d',
            'prize_bg': '#34495e',
            'current_prize': '#f39c12',
            'disabled': '#7f8c8d'
        }

        self.game_state = None
        self.main_menu()

    def create_button(self, parent, text, command, **kwargs):
        # Создаем копию kwargs и удаляем font, если он есть
        button_kwargs = kwargs.copy()
        if 'font' in button_kwargs:
            del button_kwargs['font']

        btn = Button(parent, text=text, command=command,
                     font=("Arial", 12), bg=self.colors['button'],
                     fg=self.colors['text'], relief=tk.RAISED, bd=3,
                     activebackground=self.colors['button_hover'],
                     activeforeground=self.colors['text'],
                     **button_kwargs)
        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.colors['button_hover']))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.colors['button']))
        return btn

    def create_custom_font_button(self, parent, text, command, font=("Arial", 12), **kwargs):
        """Создание кнопки с кастомным шрифтом"""
        btn = Button(parent, text=text, command=command,
                     font=font, bg=self.colors['button'],
                     fg=self.colors['text'], relief=tk.RAISED, bd=3,
                     activebackground=self.colors['button_hover'],
                     activeforeground=self.colors['text'],
                     **kwargs)
        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.colors['button_hover']))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.colors['button']))
        return btn

    def main_menu(self):
        self.clear_window()

        # Останавливаем все звуки при возврате в главное меню
        sound_manager.stop_all()

        # Фон главного меню
        canvas = Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = Label(canvas, text="Кто хочет стать миллионером?",
                            font=("Arial", 28, "bold"), bg=self.colors['bg'],
                            fg=self.colors['text'])
        title_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # Кнопки
        button_frame = Frame(canvas, bg=self.colors['bg'])
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_button(button_frame, "🎮 Начать игру", self.start_game,
                           width=20, height=2).pack(pady=10)
        self.create_button(button_frame, "⚙️ Настройки звука", self.settings_menu,
                           width=20, height=2).pack(pady=10)
        self.create_button(button_frame, "❌ Выход", self.root.quit,
                           width=20, height=2).pack(pady=10)

    def settings_menu(self):
        self.clear_window()

        canvas = Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        Label(canvas, text="⚙️ Настройки звука",
              font=("Arial", 24, "bold"), bg=self.colors['bg'],
              fg=self.colors['text']).place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Фрейм для настроек громкости
        settings_frame = Frame(canvas, bg=self.colors['bg'])
        settings_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Слайдер громкости
        Label(settings_frame, text="Громкость:",
              font=("Arial", 14), bg=self.colors['bg'],
              fg=self.colors['text']).pack(pady=10)

        volume_scale = Scale(settings_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                             length=300, bg=self.colors['bg'], fg=self.colors['text'],
                             troughcolor=self.colors['primary'],
                             command=self.change_volume)
        volume_scale.set(int(sound_manager.volume * 100))
        volume_scale.pack(pady=10)

        # Кнопки тестирования звуков
        test_frame = Frame(settings_frame, bg=self.colors['bg'])
        test_frame.pack(pady=20)

        Label(test_frame, text="Тест звуков:",
              font=("Arial", 12), bg=self.colors['bg'],
              fg=self.colors['text']).pack(pady=5)

        test_buttons_frame = Frame(test_frame, bg=self.colors['bg'])
        test_buttons_frame.pack()

        self.create_button(test_buttons_frame, "🔊 Правильный",
                           lambda: sound_manager.play_correct(), width=15).pack(side=tk.LEFT, padx=5)
        self.create_button(test_buttons_frame, "🔊 Неправильный",
                           lambda: sound_manager.play_wrong(), width=15).pack(side=tk.LEFT, padx=5)
        self.create_button(test_buttons_frame, "🔊 Подсказка",
                           lambda: sound_manager.play_hint(), width=15).pack(side=tk.LEFT, padx=5)

        # Информация о звуковых файлах
        info_frame = Frame(settings_frame, bg=self.colors['bg'])
        info_frame.pack(pady=20)

        info_text = """Для работы звуков поместите в папку 'sounds':
• correct.mp3 - правильный ответ
• wrong.mp3 - неправильный ответ  
• hint.mp3 - подсказка
• final_answer.mp3 - финальный ответ
• win.mp3 - победа"""

        Label(info_frame, text=info_text,
              font=("Arial", 10), bg=self.colors['bg'], fg=self.colors['text'],
              justify=tk.LEFT).pack()

        # Кнопки навигации
        nav_frame = Frame(canvas, bg=self.colors['bg'])
        nav_frame.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.create_button(nav_frame, "🔙 Главное меню", self.main_menu,
                           width=20, height=2).pack(pady=10)

    def change_volume(self, value):
        """Изменение громкости звука"""
        volume = int(value) / 100.0
        sound_manager.set_volume(volume)

    def start_game(self):
        self.game_state = GameState()
        self.show_question()

    def show_question(self):
        self.clear_window()

        main_frame = Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Левая часть - вопрос и ответы
        left_frame = Frame(main_frame, bg=self.colors['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Номер вопроса
        question_num = Label(left_frame,
                             text=f"Вопрос {self.game_state.current_question_index + 1}",
                             font=("Arial", 16, "bold"),
                             bg=self.colors['bg'], fg=self.colors['text'])
        question_num.pack(pady=(0, 10))

        # Текст вопроса
        question = self.game_state.get_current_question()
        question_text = Label(left_frame, text=question.text,
                              font=("Arial", 18), wraplength=500,
                              bg=self.colors['bg'], fg=self.colors['text'],
                              justify=tk.CENTER)
        question_text.pack(pady=20)

        # Кнопки ответов
        self.answer_buttons = []
        for i, option in enumerate(question.options):
            btn = self.create_custom_font_button(left_frame, f"{chr(65 + i)}. {option}",
                                                 lambda i=i: self.check_answer(i),
                                                 width=50, height=2, wraplength=450,
                                                 font=("Arial", 11))
            btn.pack(pady=8)
            self.answer_buttons.append(btn)

        # Подсказки
        hints_frame = Frame(left_frame, bg=self.colors['bg'])
        hints_frame.pack(pady=20)

        self.hint_50_50_btn = self.create_button(hints_frame, "50/50", self.use_50_50,
                                                 width=12, state=tk.NORMAL if not self.game_state.used_hints[
                '50_50'] else tk.DISABLED)
        self.hint_50_50_btn.pack(side=tk.LEFT, padx=5)

        self.hint_call_btn = self.create_button(hints_frame, "📞 Друг", self.use_call_friend,
                                                width=12, state=tk.NORMAL if not self.game_state.used_hints[
                'call_friend'] else tk.DISABLED)
        self.hint_call_btn.pack(side=tk.LEFT, padx=5)

        self.hint_audience_btn = self.create_button(hints_frame, "👥 Зал", self.use_audience_help,
                                                    width=12, state=tk.NORMAL if not self.game_state.used_hints[
                'audience_help'] else tk.DISABLED)
        self.hint_audience_btn.pack(side=tk.LEFT, padx=5)

        # Правая часть - шкала выигрышей
        prize_frame = Frame(main_frame, bg=self.colors['prize_bg'], width=250)
        prize_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        prize_frame.pack_propagate(False)

        Label(prize_frame, text="🏆 Шкала выигрышей",
              font=("Arial", 16, "bold"), bg=self.colors['prize_bg'],
              fg=self.colors['text']).pack(pady=20)

        self.prize_labels = []
        prizes = self.game_state.prize_levels[::-1]

        for i, prize in enumerate(prizes):
            bg_color = self.colors['prize_bg']
            fg_color = self.colors['text']

            # Текущий вопрос
            if len(prizes) - i - 1 == self.game_state.current_question_index:
                bg_color = self.colors['current_prize']
                fg_color = '#2c3e50'
            # Несгораемые суммы
            elif len(prizes) - i - 1 in self.game_state.safe_havens:
                bg_color = self.colors['secondary']
                fg_color = '#2c3e50'
            # Пройденные вопросы
            elif len(prizes) - i - 1 < self.game_state.current_question_index:
                bg_color = self.colors['primary']

            label = Label(prize_frame, text=f"{prize:,} ₽",
                          bg=bg_color, fg=fg_color,
                          font=("Arial", 12, "bold" if bg_color != self.colors['prize_bg'] else "normal"),
                          width=15, relief=tk.RAISED, bd=2)
            label.pack(pady=2)
            self.prize_labels.append(label)

    def check_answer(self, answer_index):
        # Воспроизводим звук финального ответа
        sound_manager.play_final_answer()

        # Ждем немного перед проверкой ответа
        self.root.update()
        self.root.after(800)  # Уменьшили паузу до 0.8 сек

        is_correct, message = self.game_state.check_answer(answer_index)

        if is_correct:
            # Подсветка правильного ответа зеленым
            self.answer_buttons[answer_index].config(bg=self.colors['secondary'])
            # Воспроизводим звук правильного ответа
            self.root.after(500, sound_manager.play_correct)  # Задержка перед звуком
            self.root.update()

            if self.game_state.game_over:
                # Воспроизводим звук победы с задержкой
                self.root.after(1000, lambda: self.show_victory(message))
            else:
                self.root.after(1500, lambda: self.show_next_question(message))
        else:
            # Подсветка неправильного ответа красным
            self.answer_buttons[answer_index].config(bg=self.colors['accent'])
            # Подсветка правильного ответа зеленым
            correct_index = self.game_state.get_current_question().correct_index
            self.answer_buttons[correct_index].config(bg=self.colors['secondary'])
            # Воспроизводим звук неправильного ответа с задержкой
            self.root.after(500, sound_manager.play_wrong)

            self.root.update()
            self.root.after(2000, lambda: self.show_game_over(message))

    def show_next_question(self, message):
        messagebox.showinfo("✅ Правильно!", message)
        self.show_question()

    def show_game_over(self, message):
        messagebox.showerror("❌ Неправильно!", message)
        self.main_menu()

    def show_victory(self, message):
        self.clear_window()

        canvas = Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        Label(canvas, text="🎉 ПОБЕДА! 🎉",
              font=("Arial", 32, "bold"), bg=self.colors['bg'],
              fg=self.colors['secondary']).place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        Label(canvas, text=message,
              font=("Arial", 18), bg=self.colors['bg'],
              fg=self.colors['text']).place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        button_frame = Frame(canvas, bg=self.colors['bg'])
        button_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.create_button(button_frame, "🔄 Играть снова", self.start_game,
                           width=20, height=2).pack(pady=10)
        self.create_button(button_frame, "🏠 Главное меню", self.main_menu,
                           width=20, height=2).pack(pady=10)

    def use_50_50(self):
        remove_options = self.game_state.use_hint_50_50()
        if remove_options is None:
            messagebox.showwarning("⚠️", "Подсказка 50/50 уже использована!")
            return

        # Воспроизводим звук подсказки
        sound_manager.play_hint()

        # Обновляем состояние кнопки подсказки
        self.hint_50_50_btn.config(state=tk.DISABLED, bg=self.colors['disabled'])

        for index in remove_options:
            self.answer_buttons[index].config(state=tk.DISABLED, bg=self.colors['disabled'])

    def use_call_friend(self):
        suggested_answer = self.game_state.use_hint_call_friend()
        if suggested_answer is None:
            messagebox.showwarning("⚠️", "Подсказка 'Звонок другу' уже использована!")
            return

        # Воспроизводим звук подсказки
        sound_manager.play_hint()

        # Обновляем состояние кнопки подсказки
        self.hint_call_btn.config(state=tk.DISABLED, bg=self.colors['disabled'])

        question = self.game_state.get_current_question()
        friend_answers = [
            f"Друг уверен, что это вариант {chr(65 + suggested_answer)}!",
            f"Друг говорит: 'Определенно {chr(65 + suggested_answer)}!'",
            f"Друг сомневается, но склоняется к варианту {chr(65 + suggested_answer)}.",
            f"Друг думает, что правильный ответ - {chr(65 + suggested_answer)}."
        ]

        messagebox.showinfo("📞 Звонок другу", random.choice(friend_answers))

    def use_audience_help(self):
        percentages = self.game_state.use_hint_audience_help()
        if percentages is None:
            messagebox.showwarning("⚠️", "Подсказка 'Помощь зала' уже использована!")
            return

        # Воспроизводим звук подсказки
        sound_manager.play_hint()

        # Обновляем состояние кнопки подсказки
        self.hint_audience_btn.config(state=tk.DISABLED, bg=self.colors['disabled'])

        help_window = tk.Toplevel(self.root)
        help_window.title("👥 Помощь зала")
        help_window.geometry("500x400")
        help_window.configure(bg=self.colors['bg'])
        help_window.resizable(False, False)

        # Центрируем окно помощи
        help_window.transient(self.root)
        help_window.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() - 500) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 400) // 2
        help_window.geometry(f"500x400+{x}+{y}")

        Label(help_window, text="Результаты опроса зала:",
              font=("Arial", 16, "bold"), bg=self.colors['bg'],
              fg=self.colors['text']).pack(pady=20)

        question = self.game_state.get_current_question()
        for i, (option, percentage) in enumerate(zip(question.options, percentages)):
            frame = Frame(help_window, bg=self.colors['bg'])
            frame.pack(fill=tk.X, padx=30, pady=8)

            Label(frame, text=f"{chr(65 + i)}. {option}",
                  bg=self.colors['bg'], fg=self.colors['text'],
                  font=("Arial", 11), width=30, anchor="w").pack(side=tk.LEFT)

            # Гистограмма
            bar_canvas = Canvas(frame, width=200, height=25, bg=self.colors['prize_bg'], highlightthickness=0)
            bar_canvas.pack(side=tk.RIGHT, padx=10)

            bar_width = min(percentage * 2, 200)  # Ограничиваем максимальную ширину
            bar_canvas.create_rectangle(0, 0, bar_width, 25, fill=self.colors['primary'], outline="")
            bar_canvas.create_text(bar_width + 20, 12, text=f"{percentage}%",
                                   fill=self.colors['text'], font=("Arial", 10, "bold"))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()