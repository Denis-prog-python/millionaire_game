import tkinter as tk
from tkinter import messagebox, Frame, Label, Button, Canvas
from game_logic import GameState
import random


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
            'current_prize': '#f39c12'
        }

        self.game_state = None
        self.main_menu()

    def create_button(self, parent, text, command, **kwargs):
        btn = Button(parent, text=text, command=command,
                     font=("Arial", 12), bg=self.colors['button'],
                     fg=self.colors['text'], relief=tk.RAISED, bd=3,
                     activebackground=self.colors['button_hover'],
                     activeforeground=self.colors['text'],
                     **kwargs)
        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.colors['button_hover']))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.colors['button']))
        return btn

    def main_menu(self):
        self.clear_window()

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
        self.create_button(button_frame, "❌ Выход", self.root.quit,
                           width=20, height=2).pack(pady=10)

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
            btn = self.create_button(left_frame, option, lambda i=i: self.check_answer(i),
                                     width=50, height=2, wraplength=450)
            btn.pack(pady=8)
            self.answer_buttons.append(btn)

        # Подсказки
        hints_frame = Frame(left_frame, bg=self.colors['bg'])
        hints_frame.pack(pady=20)

        self.create_button(hints_frame, "50/50", self.use_50_50,
                           width=12, state=tk.NORMAL if not self.game_state.used_hints['50_50'] else tk.DISABLED).pack(
            side=tk.LEFT, padx=5)
        self.create_button(hints_frame, "📞 Друг", self.use_call_friend,
                           width=12,
                           state=tk.NORMAL if not self.game_state.used_hints['call_friend'] else tk.DISABLED).pack(
            side=tk.LEFT, padx=5)
        self.create_button(hints_frame, "👥 Зал", self.use_audience_help,
                           width=12,
                           state=tk.NORMAL if not self.game_state.used_hints['audience_help'] else tk.DISABLED).pack(
            side=tk.LEFT, padx=5)

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
        is_correct, message = self.game_state.check_answer(answer_index)

        if is_correct:
            # Подсветка правильного ответа зеленым
            self.answer_buttons[answer_index].config(bg=self.colors['secondary'])
            self.root.update()
            self.root.after(1500)  # Пауза для показа правильного ответа

            if self.game_state.game_over:
                self.show_victory(message)
            else:
                messagebox.showinfo("✅ Правильно!", message)
                self.show_question()
        else:
            # Подсветка неправильного ответа красным
            self.answer_buttons[answer_index].config(bg=self.colors['accent'])
            # Подсветка правильного ответа зеленым
            correct_index = self.game_state.get_current_question().correct_index
            self.answer_buttons[correct_index].config(bg=self.colors['secondary'])

            self.root.update()
            self.root.after(2000)  # Пауза для показа ответов
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

        for index in remove_options:
            self.answer_buttons[index].config(state=tk.DISABLED, bg='gray')

    def use_call_friend(self):
        suggested_answer = self.game_state.use_hint_call_friend()
        if suggested_answer is None:
            messagebox.showwarning("⚠️", "Подсказка 'Звонок другу' уже использована!")
            return

        question = self.game_state.get_current_question()
        friend_answers = [
            "Друг уверен, что это вариант {}!".format(chr(65 + suggested_answer)),
            "Друг говорит: 'Определенно {}!'".format(chr(65 + suggested_answer)),
            "Друг сомневается, но склоняется к варианту {}.".format(chr(65 + suggested_answer)),
            "Друг думает, что правильный ответ - {}.".format(chr(65 + suggested_answer))
        ]

        messagebox.showinfo("📞 Звонок другу", random.choice(friend_answers))

    def use_audience_help(self):
        percentages = self.game_state.use_hint_audience_help()
        if percentages is None:
            messagebox.showwarning("⚠️", "Подсказка 'Помощь зала' уже использована!")
            return

        help_window = tk.Toplevel(self.root)
        help_window.title("👥 Помощь зала")
        help_window.geometry("500x400")
        help_window.configure(bg=self.colors['bg'])
        help_window.resizable(False, False)

        Label(help_window, text="Результаты опроса зала:",
              font=("Arial", 16, "bold"), bg=self.colors['bg'],
              fg=self.colors['text']).pack(pady=20)

        question = self.game_state.get_current_question()
        for i, (option, percentage) in enumerate(zip(question.options, percentages)):
            frame = Frame(help_window, bg=self.colors['bg'])
            frame.pack(fill=tk.X, padx=30, pady=8)

            Label(frame, text=f"{chr(65 + i)}. {option}",
                  bg=self.colors['bg'], fg=self.colors['text'],
                  font=("Arial", 11), width=40, anchor="w").pack(side=tk.LEFT)

            # Гистограмма
            bar_canvas = Canvas(frame, width=200, height=25, bg=self.colors['prize_bg'], highlightthickness=0)
            bar_canvas.pack(side=tk.RIGHT, padx=10)

            bar_width = percentage * 2
            bar_canvas.create_rectangle(0, 0, bar_width, 25, fill=self.colors['primary'], outline="")
            bar_canvas.create_text(bar_width + 20, 12, text=f"{percentage}%",
                                   fill=self.colors['text'], font=("Arial", 10, "bold"))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()