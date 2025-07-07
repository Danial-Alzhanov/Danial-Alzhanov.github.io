import time
import random
import re

users = {}
session_user = None

cards = {}
notes = {}

def is_valid_password(pw):
    return len(pw) >= 5 and pw.isalnum()

def register():
    global users
    username = input("\nПридумай имя пользователя: ")
    if username in users:
        print("Имя уже занято. Попробуй другое.")
        return
    password = input("Придумай пароль (мин. 5 символов, латиница и цифры): ")
    if not is_valid_password(password):
        print("Пароль не подходит.")
        return
    users[username] = password
    cards[username] = []
    notes[username] = []
    print("Регистрация успешна!")

def login():
    global session_user
    username = input("\nИмя пользователя: ")
    password = input("Пароль: ")
    if users.get(username) == password:
        session_user = username
        print(f"\nДобро пожаловать, {username}!")
    else:
        print("Неверное имя или пароль.")

def add_card():
    question = input("\nВведите вопрос: ")
    answer = input("Введите ответ: ")
    cards[session_user].append({'q': question, 'a': answer})
    print("Карточка добавлена!")

def review_card():
    user_cards = cards.get(session_user, [])
    if not user_cards:
        print("\nКарточек нет.")
        return
    card = random.choice(user_cards)
    print("\nВопрос:", card['q'])
    input("Нажмите Enter, чтобы увидеть ответ...")
    print("Ответ:", card['a'])

def quiz():
    user_cards = cards.get(session_user, [])
    if not user_cards:
        print("\nНет карточек для викторины.")
        return
    score = 0
    for i, card in enumerate(random.sample(user_cards, len(user_cards))):
        print(f"\nВопрос {i+1}: {card['q']}")
        start = time.time()
        try:
            answer = input_with_timeout("Ответ (30 сек): ", 30)
        except TimeoutError:
            print("\nВремя вышло!")
            continue
        if answer.strip().lower() == card['a'].strip().lower():
            print("Верно!")
            score += 1
        else:
            print(f"Неверно. Правильный ответ: {card['a']}")
    print(f"\nВикторина окончена. Результат: {score}/{len(user_cards)}")

def input_with_timeout(prompt, timeout):
    print(prompt, end='', flush=True)
    start = time.time()
    user_input = ''
    while True:
        if time.time() - start > timeout:
            raise TimeoutError
        if m := input_ready():
            user_input = input()
            break
    return user_input

def input_ready():
    import sys, select
    return select.select([sys.stdin], [], [], 0.1)[0]

def add_note():
    text = input("\nВведите текст заметки: ")
    notes[session_user].append(text)
    print("Заметка сохранена.")

def view_notes():
    for i, note in enumerate(notes[session_user], 1):
        print(f"{i}. {note}")

def delete_note():
    view_notes()
    try:
        idx = int(input("Введите номер заметки для удаления: ")) - 1
        if 0 <= idx < len(notes[session_user]):
            notes[session_user].pop(idx)
            print("Заметка удалена.")
        else:
            print("Неверный номер.")
    except:
        print("Ошибка ввода.")

def edit_note():
    view_notes()
    try:
        idx = int(input("Введите номер заметки для редактирования: ")) - 1
        if 0 <= idx < len(notes[session_user]):
            new_text = input("Новый текст: ")
            notes[session_user][idx] = new_text
            print("Заметка обновлена.")
        else:
            print("Неверный номер.")
    except:
        print("Ошибка ввода.")

def main_menu():
    while True:
        print("""
Меню:
1. Добавить карточку
2. Повторить карточку
3. Викторина
4. Добавить заметку
5. Посмотреть заметки
6. Удалить заметку
7. Редактировать заметку
0. Выйти
        """)
        choice = input("Выбор: ")
        if choice == '1': add_card()
        elif choice == '2': review_card()
        elif choice == '3': quiz()
        elif choice == '4': add_note()
        elif choice == '5': view_notes()
        elif choice == '6': delete_note()
        elif choice == '7': edit_note()
        elif choice == '0': break
        else: print("Неверный выбор.")

def start():
    print("Добро пожаловать в StudyApp!")
    while not session_user:
        print("\n1. Регистрация\n2. Вход\n0. Выход")
        choice = input("Выбор: ")
        if choice == '1': register()
        elif choice == '2': login()
        elif choice == '0': return
        else: print("Неверный выбор.")
    main_menu()

start()
