import random
import time

first_player = random.randrange(0, 2)  # Случайно выбираем игрока делающего первый ход
current_player = first_player  # Запоминаем номер текущего игрока
player_markers = ('X', 'O')  # Маркеры игроков
player_wins = [0, 0]  # Победы игроков
game_field = [['-', '-', '-'],  # Игровое поле
              ['-', '-', '-'],
              ['-', '-', '-']]
game_rounds = 1  # Число раундов
players = [input('Введите имя первого игрока: '), input('Введите имя второго игрока: ')]  # Вводим имена игроков

print(f'Крестики нолики - {players[0]} ({player_markers[0]}) против {players[1]} ({player_markers[1]})')
print(f'Первым ходит игрок - {players[first_player]}')


# Функция генератор для перебора клеток игрового поля
def cycle_game_field():
    for id_row, row in enumerate(game_field):
        for id_col, col in enumerate(row):
            yield id_row, id_col, col


# Отображение "рамки" поля
def show_game_field_borders(n_row, n_col):
    if n_col == 0 and n_row == 0:
        print(' ', '1', ' 2', ' 3')
        print('1', end='')
        return ' '
    elif n_col == 0:
        return str(n_row + 1) + ' '
    else:
        return ''


# Отображение игрового поля
def show_game_field():
    # print(show_game_field_borders(id_row, id_col), end='')
    for id_row, id_col, marker in cycle_game_field():
        print(show_game_field_borders(id_row, id_col), end='')
        print(marker, ' ', end='')

        if id_col == 2:
            print('\r')


# Очистка игрового поля
def clear_game_field():
    for id_row, id_col, marker in cycle_game_field():
        game_field[id_row][id_col] = '-'


# Проверка на наличие победителя в текущем раунде
def check_round_winner():
    marker = player_markers[current_player]
    win = False
    draw = False

    # Проверяем выигрышные комбинации
    if all([game_field[0][0] == marker, game_field[0][1] == marker, game_field[0][2] == marker]):
        win = True
    elif all([game_field[0][0] == marker, game_field[1][1] == marker, game_field[2][2] == marker]):
        win = True
    elif all([game_field[0][2] == marker, game_field[1][1] == marker, game_field[2][0] == marker]):
        win = True
    elif all([game_field[2][0] == marker, game_field[2][1] == marker, game_field[2][2] == marker]):
        win = True
    elif all([game_field[0][0] == marker, game_field[1][0] == marker, game_field[2][0] == marker]):
        win = True
    elif all([game_field[0][2] == marker, game_field[1][2] == marker, game_field[2][2] == marker]):
        win = True

    # Проверяем ничью
    if all([game_field[0][0] != '-', game_field[0][1] != '-', game_field[0][2] != '-',
            game_field[0][0] != '-', game_field[1][1] != '-', game_field[2][2] != '-',
            game_field[0][2] != '-', game_field[1][1] != '-', game_field[2][0] != '-',
            game_field[2][0] != '-', game_field[2][1] != '-', game_field[2][2] != '-',
            game_field[0][0] != '-', game_field[1][0] != '-', game_field[2][0] != '-',
            game_field[0][2] != '-', game_field[1][2] != '-', game_field[2][2] != '-']):
        draw = True

    # Если у одного из игроков собрана победная комбинация, показываем уведомление и увеличиваем число побед игрока
    if win:
        show_game_field()
        player_wins[current_player] += 1
        print(f'<<<<<<<<<<<<<<<<  Раунд {game_rounds}! Победил игрок - {players[current_player]}!  >>>>>>>>>>>>>>>>')

    # Если появление выигрышных комбинаций невозможно, заканчиваем раунд
    if draw:
        show_game_field()
        print(f'<<<<<<<<<<<<<<<<  Раунд {game_rounds}! Ничья!  >>>>>>>>>>>>>>>>')

    return win or draw


# Определение победителя в игре
def check_game_winner():
    max_score = max(player_wins[0], player_wins[1])
    id_player = player_wins.index(max_score)
    print(f'===========  Игрок - {players[id_player]}, победил в игре крестики-нолики! Спасибо за игру!  ===========')


# Ввод маркера на игровое поле по координатам
def cell_input():
    show_game_field()

    # Ждем корректного ввода координат клетки
    while True:
        print(f'Ход игрока - {players[current_player]}')

        cell = list(map(str, input('Введите номер строки и колонки (через пробел): ').split()))

        # Проверяем корректность ввода координат клетки
        if len(cell) == 2:
            # Если введенные значения координат являются целочисленными, конвертируем из в int
            if all([cell[0].isdigit(), cell[1].isdigit()]):
                cell = [int(item) for item in cell]

                if all([cell[0] > 0, cell[0] < 4, cell[1] > 0, cell[1] < 4]):
                    if game_field[cell[0] - 1][cell[1] - 1] == '-':
                        game_field[cell[0] - 1][cell[1] - 1] = player_markers[current_player]
                        break
                    else:
                        print('!!!!!!!!!!! Ячейка с данными координатами уже занята !!!!!!!!!!!')
                        print('!!!!!!!!!!!             Введите повторно             !!!!!!!!!!!')

        print(f'Игрок {players[current_player]}, ввел некорректные координаты клетки поля! Введите повторно!')


# Декоратор для подсчета времени игры
def decorator_game_time(func):
    def wrapper():
        game_time = time.time()
        func()
        delta_time = time.time() - game_time
        print(f'Общее время иры: {delta_time:.10f}')
        return delta_time

    return wrapper


# Цикл игры
@decorator_game_time
def main_game_cycle():
    global game_rounds, current_player

    while True:
        cell_input()

        # После каждого хода проверяем наличие победителя
        if check_round_winner():
            while True:
                game_continue = str(
                    input('Для начала следующего раунда введите Y, для завершения игры, введите N: ')).upper()

                # Если есть победитель в раунде, в зависимости от выбора игрока:
                if game_continue == 'N':  # Считаем итоги игры и выбираем победителя
                    check_game_winner()
                    return
                elif game_continue == 'Y':  # Переходим в следующий раунд
                    clear_game_field()
                    game_rounds += 1
                    break
                else:
                    print('Команда не распознана, введите повторно')

        current_player = 1 - current_player  # Переключаем текущего игрока


main_game_cycle()
