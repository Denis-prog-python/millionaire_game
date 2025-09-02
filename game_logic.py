import random
import json
import os


class Question:
    def __init__(self, text, options, correct_index, difficulty):
        self.text = text
        self.options = options
        self.correct_index = correct_index
        self.difficulty = difficulty


class GameState:
    def __init__(self, questions_file='questions.json'):
        self.questions = self.load_questions(questions_file)
        self.current_question_index = 0
        self.score = 0
        self.used_hints = {'50_50': False, 'call_friend': False, 'audience_help': False}
        self.game_over = False
        # Увеличенная шкала выигрышей до 1 млн
        self.prize_levels = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000,
                             64000, 125000, 250000, 500000, 1000000]
        self.safe_havens = [5, 10]  # Несгораемые суммы на 5 и 10 вопросах

    def load_questions(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл с вопросами '{filename}' не найден.")

        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Сортируем вопросы по сложности
        sorted_data = sorted(data, key=lambda x: x['difficulty'])
        questions = []

        for item in sorted_data:
            questions.append(Question(
                text=item['question'],
                options=item['options'],
                correct_index=item['correct_index'],
                difficulty=item['difficulty']
            ))

        return questions[:15]  # Берем 15 вопросов для игры

    def get_current_question(self):
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def check_answer(self, answer_index):
        current_question = self.get_current_question()
        if current_question and answer_index == current_question.correct_index:
            self.score = self.prize_levels[self.current_question_index]
            self.current_question_index += 1

            # Проверяем, достигли ли мы конца игры
            if self.current_question_index >= len(self.questions):
                self.game_over = True
                return True, "ПОБЕДА! Вы выиграли 1.000.000 рублей!"
            return True, "Правильно!"
        else:
            self.game_over = True
            # Определяем несгораемую сумму
            safe_haven = 0
            for safe in self.safe_havens:
                if self.current_question_index >= safe:
                    safe_haven = self.prize_levels[safe - 1]
            return False, f"Неправильно! Ваш выигрыш: {safe_haven} рублей."

    def use_hint_50_50(self):
        if self.used_hints['50_50']:
            return None

        self.used_hints['50_50'] = True
        current_question = self.get_current_question()
        wrong_options = [i for i in range(4) if i != current_question.correct_index]
        remove_options = random.sample(wrong_options, 2)
        return remove_options

    def use_hint_call_friend(self):
        if self.used_hints['call_friend']:
            return None

        self.used_hints['call_friend'] = True
        current_question = self.get_current_question()
        # Друг с 80% вероятностью подсказывает правильный ответ
        if random.random() < 0.8:
            return current_question.correct_index
        else:
            return random.randint(0, 3)

    def use_hint_audience_help(self):
        if self.used_hints['audience_help']:
            return None

        self.used_hints['audience_help'] = True
        current_question = self.get_current_question()

        # Генерируем псевдо-проценты для каждого варианта
        percentages = [0] * 4
        correct_percentage = random.randint(50, 90)
        percentages[current_question.correct_index] = correct_percentage

        # Распределяем оставшиеся проценты между неправильными ответами
        remaining_percentage = 100 - correct_percentage
        wrong_options = [i for i in range(4) if i != current_question.correct_index]

        for i in range(len(wrong_options)):
            if i == len(wrong_options) - 1:
                percentages[wrong_options[i]] = remaining_percentage
            else:
                percent = random.randint(5, remaining_percentage // 2)
                percentages[wrong_options[i]] = percent
                remaining_percentage -= percent

        return percentages