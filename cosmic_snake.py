import pygame  # подключение всех необходимых библиотек
import random
import math

pygame.init()  # иннициализация подключенных модулей

pygame.mixer.music.load('Veorra_The City.mp3')  # загрузка аудио
pygame.mixer.music.play(-1)  # зацикленное воспроизведение аудио

grey = (127, 127, 127)  # объявление всех используемых цветов
white = (255, 255, 255)
yellow = (238, 186, 4)
red = (213, 50, 80)
violet = (155, 80, 211)

dis_width = 600  # объявление ширины экрана
dis_height = 400  # высоты экрана
screen_size = (600, 400)  # кортеж с шириной и высотой экрана

dis = pygame.display.set_mode((dis_width, dis_height))  # установка рабочего окна
pygame.display.set_caption('snake!')  # имя окна
background_image = pygame.image.load('background.png').convert()  # загрузка фонового изображения

clock = pygame.time.Clock()  # объявление переменной clock, связанной с реальным временем из модуля pygame

snake_block = 10  # объявление змейки (размер)
snake_speed = 15  # скорость змейки

font_style = pygame.font.Font(None, 30)  # стили шрифтов для надписей
score_font = pygame.font.Font(None, 35)


class Asteroid:  # класс астероида
    def __init__(self, position, velocity, radius, mass):  # при создании экземпляра класса записываем в него
        # первоначальные значения параметров
        self.position = position  # метод для астероида (кортеж с x и y координатами)
        self.velocity = velocity  # метод для астероида (кортеж с x и y компонентами скорости)
        self.radius = radius  # радиус астероида
        self.mass = mass  # масса астероида


def is_collides(_screen_size, obj1, obj2):  # проверяет, сталкиваются ли два астероида
    dist = ((obj1.position[0] - obj2.position[0]) ** 2 + (obj1.position[1] - obj2.position[1]) ** 2) ** 0.5
    # по теореме Пифагора
    return dist < obj1.radius + obj2.radius  # возвращает True, если коллизия происходит


def collide_asteroids(_screen_size, asteroid1, asteroid2):  # сталкивание двух астероидов
    if is_collides(_screen_size, asteroid1, asteroid2):
        max_speed = 30  # максимальная скорость астероида

        asteroid1.position[0] -= asteroid1.velocity[0] * 1 / 15  # возвращаем астероиды в состояние до коллизии(x)
        asteroid1.position[1] -= asteroid1.velocity[1] * 1 / 15  # возвращаем астероиды в состояние до коллизии(y)
        asteroid2.position[0] -= asteroid2.velocity[0] * 1 / 15  # возвращаем астероиды в состояние до коллизии(x)
        asteroid2.position[1] -= asteroid2.velocity[1] * 1 / 15  # возвращаем астероиды в состояние до коллизии(x)

        asteroid1.velocity[0] = random.uniform(-max_speed, max_speed)  # меняем x- и y- компоненты скорости у каждого
        # астероида
        asteroid1.velocity[1] = random.uniform(-max_speed, max_speed)  # они могут быть как положительными, так и отриц
        asteroid2.velocity[0] = random.uniform(-max_speed, max_speed)  # если скорость отрицательная - астероид
        # движется в обратную сторону
        asteroid2.velocity[1] = random.uniform(-max_speed, max_speed)


def my_Snake(snake_block, snake_list):  # отрисовка змеи
    for x in snake_list:  # отрисовывается каждый элемент длины
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])


def your_Score(score):  # вывод на экран текущего счета пользователя
    value = score_font.render("Your Score: " + str(score), True, violet)  # фиолетовым цветом
    dis.blit(value, [0, 0])


def message(msg, color):  # функция, печатающая любое передаваемое сообщение для пользователя при вызове
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():  # цикл игры
    game_over = False  # флаг игра окончена
    game_close = False  # флаг закрытие игрового окна

    x1 = dis_width / 2  # начальные координаты змейки по x
    y1 = dis_height / 2  # и по y

    x1_change = 0  # изменение координат змейки
    y1_change = 0

    snake_List = []  # список всех частей змеи
    Length_of_snake = 1  # изначльная длина змейки = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    # инициализация положения еды для змейки с помощью random
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    # в случайном месте в пределах игрового окна

    asteroids = []  # массив астероидов
    for i in range(10):  # в параметре range я указываю желаемое количество астероидов
        size = random.random()  # присваиваю случайное значение от 0 до 1
        radius = int(5 + size * 20)  # определяю радиус будущего астероида
        pos = [random.randint(radius, dis_width - radius - 1), random.randint(radius, dis_height - radius - 1)]
        # с помощью random выбираю случайные целочисленные числа для x и y коордиаат в диапазоне от радиуса до
        # ширина/высота экрана - радиус - 1
        while True:
            ok = True  # флаг для проверки положения астероидов, чтобы они не рисовались друг в друге и в стенах
            for asteroid in asteroids:
                dist = ((asteroid.position[0] - pos[0]) ** 2 + (asteroid.position[1] - pos[1]) ** 2) ** 0.5
                if dist < asteroid.radius + radius:  # если условие коллизии выполняется, то ок становится ложью
                    ok = False  # следовательно, нужно переиницализировать астероид, пока у него не будет нормальное
                    # положение
                    break
            if not ok:  # переиницаилизация
                pos = [random.randint(radius, dis_width - radius - 1), random.randint(radius, dis_height - radius - 1)]
            else:
                break
        max_speed = 30
        vel = [random.uniform(-max_speed, max_speed), random.uniform(-max_speed, max_speed)]  # задаем скорость
        # астероиду(по x и по y)
        mass = math.pi * radius ** 2  # задаем массу
        asteroids.append(Asteroid(pos, vel, radius, mass))  # добавляем только что созданный астероид в массив
        # астероидов

    prev = ''  # строковая переменная для запоминания предыдущей нажатой клавиши
    while not game_over:  # пока игра запущена

        while game_close:  # переходим сюда, если игрок проиграл
            dis.blit(background_image, [0, 0])  # отрисовываем фон
            message("You Lost! Press P-Play Again or Q-Quit", red)  # выводим сообщение пользователю
            your_Score(Length_of_snake - 1)  # выводим очки
            pygame.display.update()  # обновляем экран

            for event in pygame.event.get():  # если отлавливаем какое-то событие
                if event.type == pygame.KEYDOWN:  # и если оно - нажатая клавиша
                    if event.key == pygame.K_q:  # а именно клавиша q
                        game_over = True  # выходим из игры
                        game_close = False
                    if event.key == pygame.K_p:  # клавиша p
                        gameLoop()  # запускаем игровой цикл заново

        for event in pygame.event.get():  # отслеживаем события
            if event.type == pygame.QUIT:  # если нажат крестик у окна приложения, то выходим
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # клавиша влево
                    if prev == 'right':  # если предыдущей нажатой клавишой была вправо, то ничего не делаем
                        x1_change = snake_block  # т.к. змейка не умеет разворачиваться на 180 градусов
                        y1_change = 0
                    else:
                        x1_change = -snake_block  # иначе - меняем положение и идем влево
                        y1_change = 0
                        prev = 'left'
                elif event.key == pygame.K_RIGHT:  # аналогично с остальными направлениями
                    if prev == 'left':
                        x1_change = -snake_block
                        y1_change = 0
                    else:
                        x1_change = snake_block
                        y1_change = 0
                        prev = 'right'
                elif event.key == pygame.K_UP:
                    if prev == 'down':
                        y1_change = snake_block
                        x1_change = 0
                    else:
                        y1_change = -snake_block
                        x1_change = 0
                        prev = 'up'
                elif event.key == pygame.K_DOWN:
                    if prev == 'up':
                        y1_change = -snake_block
                        x1_change = 0
                    else:
                        y1_change = snake_block
                        x1_change = 0
                        prev = 'down'

        for asteroid in asteroids:  # движение астероидов (меняем x и y координаты при помощи скорости)
            asteroid.position[0] += asteroid.velocity[0] * 1/15
            asteroid.position[1] += asteroid.velocity[1] * 1/15
            # обработка столкновений с краями экрана
            asteroid.velocity[0] = -asteroid.velocity[0] if (asteroid.position[0] + asteroid.radius > dis_width or
                                                             asteroid.position[0] - asteroid.radius < 0) else asteroid.velocity[0]  # отскок
            asteroid.velocity[1] = -asteroid.velocity[1] if (asteroid.position[1] + asteroid.radius > dis_height or
                                                             asteroid.position[1] - asteroid.radius < 0) else asteroid.velocity[1]

        for i, asteroid1 in enumerate(asteroids):  # обработка столкновений астероидов с астероидами
            for asteroid2 in asteroids[i + 1:]:
                collide_asteroids(screen_size, asteroid1, asteroid2)

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:  # змейка врезается в края экрана
            game_close = True  # игра заканчивается

        x1 += x1_change  # меняем положение змейки по x
        y1 += y1_change  # меняем положение змейки по y
        dis.blit(background_image, [0, 0])  # отрисовываем фон

        for asteroid in asteroids:
            ast_pos = asteroid.position
            ast_pos = tuple(ast_pos)  # преобразую список координат в кортеж для передачи в draw
            pygame.draw.circle(dis, grey, ast_pos, asteroid.radius, 0)  # отрисовываю астероид

        pygame.draw.rect(dis, yellow, [foodx, foody, snake_block, snake_block])  # отрисовка еды

        snake_Head = [x1, y1]  # массив для двух координат x и y
        snake_List.append(snake_Head)  # массив массивов, для каждого элемента змейки есть свои x и y координаты
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:  # если врезались в свой хвост
            if x == snake_Head:
                game_close = True  # игра окончена

        for i in snake_List:  # обработка столкновений змейки и астероидов
            for asteroid in asteroids:
                if ((asteroid.position[0] - i[0]) ** 2 + (asteroid.position[1] - i[1]) ** 2) ** 0.5 < asteroid.radius:
                    # проверяем каждый угол каждого составного элемента змейки
                    # по теореме Пифагора находим расстояние между двумя точками (центр астероида и углом элемента змеи)
                    # если расстояние между ними меньше радиуса астероида, значит они столкнулись и игра окончена
                    game_close = True
                elif ((asteroid.position[0] - i[0] + snake_block) ** 2 + (asteroid.position[1] - i[1]) ** 2) ** 0.5 < asteroid.radius:
                    game_close = True
                elif ((asteroid.position[0] - i[0]) ** 2 + (asteroid.position[1] - i[1] + snake_block) ** 2) ** 0.5 < asteroid.radius:
                    game_close = True
                elif ((asteroid.position[0] - i[0] + snake_block) ** 2 + (asteroid.position[1] - i[1] + snake_block) ** 2) ** 0.5 < asteroid.radius:
                    game_close = True

        my_Snake(snake_block, snake_List)  # вызываю функцию отрисовки змейки
        your_Score(Length_of_snake - 1)  # обновляю счетчик очков

        pygame.display.update()  # обновляю окно

        if x1 == foodx and y1 == foody:  # проверка условия поедания еды
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0  # если x змйки = x еды
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0  # если y змейки = y еды
            Length_of_snake += 1  # увеличиваем длину на 1

        clock.tick(snake_speed)  # обновляем экран snake_speed(15) раз в секунду

    pygame.quit()  # выходим из модуля
    quit()  # закрытие программы


gameLoop()  # вызываем функцию игрового цикла
