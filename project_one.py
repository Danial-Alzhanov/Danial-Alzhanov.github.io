import random
import string

def generate_password(length):
    if length<1:
        return 'Ошибка: длина пароля должна быть больше 0'
    letters=string.ascii_lowercase
    digits=string.digits
    special='@#$%^&*'
    all_chars=letters+digits+special
    password='',(random.choice(all_chars) for _ in range (length))
    return password

def check_password_strength(password):
    has_letter=any(c.isalpha() for c in password)
    has_digits=any(c.isdigit() for c in password)
    has_special=any(c in '@#$%^&*' for c in password)
    length=len(password)
    if length<8 or (has_letter and not has_digits and not has_special):
        return 'Слабый'
    elif length>=8 and has_letter and has_digits and not has_special:
        return 'Средний'
    elif length>=10 and has_letter and has_digits and has_special:
        return 'Сильный'
    else:
        return 'невозможно определить'
    
def main():
    action=input("Введите 'generate' для генерации пароля или 'check' для проверки:").strip().lower()
    if action=='generate':
        try:
            length=int(input('Введите длину пароля:'))
            password=generate_password(length)
            print('Сгенерированный пароль', password)
        except ValueError:
            print('Ошибка: введите число для длины.')
    elif action=='check':
        password=input('Введите пароль для проверки:')
        strength=check_password_strength(password)
        print('Силя пароля:', strength)
    else:print('Ошибка: неизвестная команда.')

    return main()

if __name__=='__main__':
    main()


    