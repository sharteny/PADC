#!/usr/bin/python3
import random

def next_question(questions):
    return random.choice(questions)

def fifty_fifty(options, correct):
    wrong = [opt for opt in options if opt != correct]
    result = random.sample(wrong, 1) + [correct]
    random.shuffle(result)
    return result

def ask_audience(current):
    print("Audience poll: The correct answer is likely to be:", current)

def players():
    username = input("Enter your username: ")
    user = {"username": username, "score": 0, "50/50": False, "audience": False, "pass": False}
    return [user]

def parse_question(q):
    question, answers = q.split("?")
    options = answers.split(",")
    correct = options[0]
    random.shuffle(options)
    return question, options, correct

def use_help(input_choice, options, current, user):
    if input_choice == '50' and not user["50/50"]:
        options = fifty_fifty(options, current)
        print("Options after 50/50:", ", ".join(options))
        user["50/50"] = True
        return options

    elif input_choice == 'audience' and not user["audience"]:
        ask_audience(current)
        user["audience"] = True
        return options

    elif input_choice == 'pass' and not user["pass"]:
        print("You chose to pass. Moving to the next question.")
        user["pass"] = True
        return None

    else:
        print("Invalid choice or already used.")
        return options

def ask_question(question, options, current, user):
    print(question + "?")
    while True:
        print("Options:", ", ".join(options))
        print("Type '50', 'audience', or 'pass'.")

        answ = input("Your answer: ").strip().lower()

        # если выбрали помощь
        if answ in ['50', 'audience', 'pass']:
            res = use_help(answ, options, current, user)
            if res is None:
                return False
            options = res
            continue

        # обычный ответ
        if answ == current.lower():
            print("Correct!")
            return True
        else:
            print("Incorrect. The correct answer is:", current)
            return False

def play_round(user, all_questions):
    user["50/50"] = False
    user["audience"] = False
    user["pass"] = False
    user["score"] = 0

    questions = all_questions.copy()
    for quest in random.sample(questions, 10):
        question, options, correct = parse_question(quest)
        if ask_question(question, options, correct, user):
            user["score"] += 1

    print(f"{user['username']} got {user['score']}/10 questions right.\n")

def get_questions():
    with open("questions.txt", "r") as f:
        questions = [line.strip() for line in f if line.strip()]
    return questions

def main():
    users = []
    all_questions = get_questions()
    while True:
        ask = input("Do you want to play or add questions? (play/add): ").strip().lower()
        if ask == "add":
            new_q = input("Enter a new question in the format 'Question?Option1,Option2,Option3,Option4' (correct answer should be first): ")
            with open("questions.txt", "a") as f:
                f.write(new_q + "\n")
            print("Question added.")
            continue
        new_user_input = input("Enter your username: ").strip()
        existing_user = None
        for u in users:
            if u["username"].lower() == new_user_input.lower():
                existing_user = u
                break
        if existing_user:
            print(f"Player '{new_user_input}' exists. Resetting previous score and lifelines.")
            user = existing_user
        else:
            user = {"username": new_user_input, "score": 0, "50/50": False, "audience": False, "pass": False}
            users.append(user)
        play_round(user, all_questions)
        play = input("Do you want to continue with another player? (yes/no): ").strip().lower()
        if play != 'yes':
            print("Final rankings:")
            for u in sorted(users, key=lambda x: x["score"], reverse=True):
                with open("top_players.txt", "a") as f:
                    f.write(f"{u['username']}: {u['score']} points\n")
            break

if __name__ == "__main__":
    main()