from random import choice
import hashlib as hash


class Password:
    def __init__(self):
        print('Я помогу вам создать пароль!')
        print()
        self.SYMBOLS: list = ['!', '.', ',', '@', '#', '$', '%', '?', '*']
        self.MAIN_LIST: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C',
                                'D', 'I', 'F', 'G', 'H', 'I', 'G', 'K', 'L',
                                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                                'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                                'i', 'f', 'g', 'h', 'i', 'g', 'k', 'l', 'm',
                                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                'w', 'x', 'y', 'z']
        print(self.MAIN_LIST)
        self.create_password()

    def create_val(self):
        while True:
            try:
                count_char: int = int(
                    input('Введите количество символов в пароле: '))
                print('-' * 25)
                break
            except ValueError:
                print('Вы ввели недопустимое значение! Введите число')

        while True:
            try:
                symbol: str = str(input(
                    'Использовать в пароле дополнительные символы? (! ? @ и т.д.) Y/N '))
                if symbol in ['Y', 'y']:
                    self.MAIN_LIST += self.SYMBOLS
                    print('-' * 50)
                    break
                elif symbol in ['N', 'n']:
                    print('-' * 50)
                    break
                else:
                    print(
                        'Вы ввели неверное значение! Введите Y - да, или N - нет')
            except ValueError:
                print('Вы ввели недопустимое значение! Введите Y/N')

        return count_char

    def create_password(self):
        char = self.create_val()
        restart: str = 'Y'

        while restart == 'Y':
            passwords = ''
            for i in range(char):
                passwords += str(choice(self.MAIN_LIST))
            print(passwords)
            print('-' * 50)

            while True:
                try:
                    symbol: str = str(
                        input('Повторить генерацию пароля? Y/N '))
                    if symbol in ['Y', 'y']:
                        print('-' * 50)
                        break
                    elif symbol in ['N', 'n']:
                        restart = 'N'
                        break
                    else:
                        print(
                            'Вы ввели неверное значение! Введите Y - да, или N - нет')
                except ValueError:
                    print('Вы ввели недопустимое значение! Введите Y/N')


class Encrypttion:
    encrypt = hash.sha1(b'password')
    print(encrypt.hexdigest())


if __name__ == '__main__':
    pas = Password()