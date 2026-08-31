class Question:
    def __init__(self, question_id, question, options, correct_answer):
        self.question_id = question_id
        self.question = question
        self.options = options
        self.correct_answer = correct_answer

    def display_question(self):
        print(f"\nQ{self.question_id}: {self.question}")

        for index, option in enumerate(self.options, start=1):
            print(f"{index}. {option}")

    def check_answer(self, answer):
        return answer.lower() == self.correct_answer.lower()


class Quiz:
    def __init__(self, title):
        self.title = title
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)

    def display_quiz(self):
        print(f"\n{'=' * 50}")
        print(f"QUIZ: {self.title}")
        print('=' * 50)

        for question in self.questions:
            question.display_question()

    def conduct_quiz(self, user):
        score = 0

        for question in self.questions:
            question.display_question()

            try:
                answer = input("Enter your answer: ")

                if question.check_answer(answer):
                    print("Correct!")
                    score += 1
                else:
                    print(
                        f"Wrong! Correct answer: "
                        f"{question.correct_answer}"
                    )

            except Exception as error:
                print("Error:", error)

        user.update_score(score, len(self.questions))


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.score = 0
        self.total_questions = 0

    def update_score(self, score, total_questions):
        self.score = score
        self.total_questions = total_questions

    def percentage(self):
        if self.total_questions == 0:
            return 0

        return (
            self.score / self.total_questions
        ) * 100

    def display_result(self):
        print("\nRESULT")
        print("-" * 40)
        print(f"Name: {self.name}")
        print(f"Score: {self.score}/{self.total_questions}")
        print(f"Percentage: {self.percentage():.2f}%")


class QuizSystem:
    def __init__(self):
        self.users = {}
        self.results = []

    def add_user(self, user):
        if user.user_id in self.users:
            raise ValueError("User already exists")

        self.users[user.user_id] = user

    def save_result(self, user):
        result = {
            "name": user.name,
            "score": user.score,
            "percentage": user.percentage()
        }

        self.results.append(result)

    def show_leaderboard(self):
        sorted_results = sorted(
            self.results,
            key=lambda result: result["score"],
            reverse=True
        )

        print("\nLEADERBOARD")
        print("=" * 40)

        for rank, result in enumerate(
            sorted_results,
            start=1
        ):
            print(
                f"{rank}. {result['name']} - "
                f"{result['score']} marks "
                f"({result['percentage']:.2f}%)"
            )


quiz = Quiz("Python Basics")

question1 = Question(
    1,
    "What keyword is used to define a function?",
    ["func", "define", "def", "function"],
    "def"
)

question2 = Question(
    2,
    "Which data structure is immutable?",
    ["List", "Dictionary", "Set", "Tuple"],
    "Tuple"
)

question3 = Question(
    3,
    "What does len() return?",
    [
        "Memory address",
        "Number of elements",
        "Data type",
        "Boolean value"
    ],
    "Number of elements"
)

quiz.add_question(question1)
quiz.add_question(question2)
quiz.add_question(question3)

system = QuizSystem()

user = User(101, "Rishav")

system.add_user(user)

quiz.conduct_quiz(user)

user.display_result()

system.save_result(user)

system.show_leaderboard()