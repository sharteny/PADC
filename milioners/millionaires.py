#!/usr/bin/python3
import random


class Player:
    def __init__(self, username):
        self.username = username
        self.score = 0
        self.fifty_fifty = False
        self.audience = False
        self.passed = False

    def add_score(self):
        self.score += 1


class Question:
    def __init__(self, text, options, correct):
        self.text = text
        self.options = options
        self.correct = correct


def next_question(questions):
    return random.choice(questions) if questions else None


def fifty_fifty(options, correct):
    wrong = [opt for opt in options if opt != correct]
    if len(wrong) <= 1:
        return options
    result = random.sample(wrong, 1) + [correct]
    random.shuffle(result)
    return result


def ask_audience(current):
    print("Audience poll: The correct answer is likely to be:", current)


def players():
    username = input("Enter your username: ").strip()
    while not username:
        print("Username cannot be empty.")
        username = input("Enter your username: ").strip()

    user = Player(username)
    return [user]


def parse_question(q):
    try:
        if "?" not in q:
            raise ValueError

        question, answers = q.split("?", 1)
        options = [o.strip() for o in answers.split(",") if o.strip()]

        if len(options) < 4:
            raise ValueError

        correct = options[0]
        random.shuffle(options)

        return Question(question, options, correct)

    except Exception:
        print("Invalid question format:", q)
        return None


def use_help(input_choice, options, current, user):
    if input_choice == '50' and not user.fifty_fifty:
        options = fifty_fifty(options, current)
        print("Options after 50/50:", ", ".join(options))
        user.fifty_fifty = True
        return options

    elif input_choice == 'audience' and not user.audience:
        ask_audience(current)
        user.audience = True
        return options

    elif input_choice == 'pass' and not user.passed:
        print("You chose to pass. Moving to the next question.")
        user.passed = True
        return None

    else:
        print("Invalid choice or already used.")
        return options


def ask_question(question, options, current, user):
    print(question + "?")

    while True:
        print("Options:", ", ".join(options))
        print("Type your answer or '50', 'audience', 'pass'.")

        answ = input("Your answer: ").strip().lower()

        if not answ:
            print("Empty input. Try again.")
            continue

        if answ in ['50', 'audience', 'pass']:
            res = use_help(answ, options, current, user)
            if res is None:
                return False
            options = res
            continue

        if answ not in [o.lower() for o in options]:
            print("Invalid answer. Choose one of the available options.")
            continue

        if answ == current.lower():
            print("Correct!")
            return True
        else:
            print("Incorrect. The correct answer is:", current)
            return False


def play_round(user, all_questions):
    user.fifty_fifty = False
    user.audience = False
    user.passed = False
    user.score = 0

    if not all_questions:
        print("No questions available.")
        return

    questions = random.sample(all_questions, min(10, len(all_questions)))

    for quest in questions:
        question = parse_question(quest)
        if question is None:
            continue

        try:
            if ask_question(question.text, question.options, question.correct, user):
                user.add_score()
        except Exception:
            print("Error in question, skipping...")
            continue

    print(f"{user.username} got {user.score}/10 questions right.\n")


def get_questions():
    try:
        with open("questions.txt", "r", encoding="utf-8") as f:
            questions = [line.strip() for line in f if line.strip()]

        if not questions:
            print("questions.txt is empty.")
            return []

        return questions

    except FileNotFoundError:
        print("Error: questions.txt file not found.")
        return []


def add_question():
    try:
        new_q = input("Enter a new question in format Question? ").strip()
        if not new_q:
            print("Empty question.")
            return

        if "?" not in new_q:
            new_q += "?"

        current = input("Enter the correct answer: ").strip()
        if not current:
            print("Empty correct answer.")
            return

        options = input("Enter three wrong options separated by commas: ").strip()

        if not options:
            print("Empty options.")
            return

        new_q += current + "," + options

        with open("questions.txt", "a", encoding="utf-8") as f:
            f.write(new_q + "\n")

        print("Question added.")

    except Exception:
        print("Error adding question.")


def load_players():
    players = []

    try:
        with open("top_players.txt", "r", encoding="utf-8") as f:
            for line in f:
                try:
                    name, score = line.strip().split(":")
                    user = Player(name.strip())
                    user.score = int(score.split()[0])
                    players.append(user)
                except Exception:
                    print("Invalid player data:", line)

    except FileNotFoundError:
        pass

    return players


def main():
    users = []
    old_players = load_players()
    all_questions = get_questions()

    while True:
        ask = input("Do you want to play or add questions? (play/add/exit): ").strip().lower()

        if ask == "add":
            add_question()
            continue

        elif ask == "play":
            new_user_input = input("Enter your username: ").strip()

            if not new_user_input:
                print("Username cannot be empty.")
                continue

            existing_user = None
            for u in users:
                if u.username.lower() == new_user_input.lower():
                    existing_user = u
                    break

            if existing_user:
                user = existing_user
            else:
                user = Player(new_user_input)
                users.append(user)

            play_round(user, all_questions)

            play = input("Continue? (yes/no): ").strip().lower()

            if play != 'yes':
                all_players = users + old_players
                all_players = sorted(all_players, key=lambda x: (x.score, x.username), reverse=True)

                try:
                    with open("top_players.txt", "w", encoding="utf-8") as f:
                        for u in all_players:
                            f.write(f"{u.username}: {u.score} points\n")
                            print(f"{u.username}: {u.score} points")
                except Exception:
                    print("Error saving leaderboard.")

                break

        elif ask == "exit":
            print("Goodbye.")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()