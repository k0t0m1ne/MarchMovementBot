import random
from django.shortcuts import HttpResponse
import telebot
from django.views.decorators.csrf import csrf_exempt
from telebot import types
from .models import Player, PlayerTask, Tasks, QrCodes
import datetime

bot = telebot.TeleBot('5862254534:AAEuWEH-4D6V7H4BbQmsFALGwv2pl6U93GE')
# https://api.telegram.org/bot5862254534:AAEuWEH-4D6V7H4BbQmsFALGwv2pl6U93GE/setWebhook?url=https://4b7f-91-228-178-74.eu.ngrok.io/

@csrf_exempt
def index(request):
    if request.method == 'GET':
        print('ГЕт')
    if request.method == "POST":
        print('Привет')
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('<h1>Ты подключился!</h1>')


def is_subscribed(chat_1id, user_1id):
    try:
        bot.get_chat_member(chat_id=chat_1id, user_id=user_1id)
        return True
    except telebot.apihelper.ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False


def task_massive():
    task = []
    for i in range(1,20,1):
        task.append(i)
    randtask = []
    for i in range(19):
        a = random.randint(1,20)
        while a not in task:
            a = random.randint(1,20)
        randtask.append(str(a))
        task.remove(a)
    return ",".join(randtask)



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    mess = f'Привет!\n\nМы рады приветствовать тебя на квесте, приуроченному к ' \
           f'замечательному празднику - 8 марта!\n\nПеред тем, как начать квест, ' \
           f'подпишись на наш канал!\n@hse_movement\nvk.com/movement_hse'
    register = types.KeyboardButton("Зарегистрироваться на квест")
    markup.add(register)
    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler(commands=['send'])
def send(message):
    text = message.text.split()
    idf = Player.objects.get(tg_tag=text[1]).foreign_id
    bot.send_message(idf, ' '.join(text[2:]), parse_mode='html')


@bot.message_handler(commands=['score'])
def score(message):
    text = ["Покровка","МИЭМ","Басманная",
            "Шаболовка","Международные отношения"]
    for j in text:
        a2 = PlayerTask.objects.filter(place=j).values('foreign_id')

        bot.send_message(message.chat.id, j, parse_mode='html')
        massive1 = []
        for i in list(a2):
            b1 = Player.objects.get(foreign_id=i['foreign_id'])
            mess = str(b1.last_name) + '; ' \
                   + str(b1.first_name) + '; ' \
                   + str(b1.tg_tag) + '; ' \
                   + str(b1.time1) + '; ' \
                   + str(b1.score)
            massive1.append(mess)
            print(mess)
        message1 = '/n'.join(massive1)
        bot.send_message(message.chat.id, message1, parse_mode='html')


@bot.message_handler(content_types=['text'])
def register(message):
    if not Player.objects.filter(foreign_id=message.from_user.id).exists():
        text = list(message.text.split())
        if message.text == "Зарегистрироваться на квест":
            mess = f'Напиши по порядку свои данные: Фамилия Имя @Тег'
            bot.send_message(message.chat.id, mess, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
        elif len(text) == 3:

            if text[2][0] != '@':
                bot.send_message(message.chat.id, 'Не могу распознать ваш тэг')
            else:
                bot.send_message(message.chat.id, 'Принято...')
                p, _ = Player.objects.get_or_create(
                    foreign_id=message.from_user.id,
                    first_name=text[0],
                    last_name=text[1],
                    tg_tag=text[2],
                    score=0,
                    time1=datetime.datetime.now()
                )
                if _:
                    bot.send_message(message.chat.id, 'Профиль создан!')
                    markup = types.ReplyKeyboardMarkup()
                    pokr = types.KeyboardButton("Покровский бульвар")
                    miem = types.KeyboardButton("МИЭМ")
                    shabl = types.KeyboardButton("ВШБ")
                    basm = types.KeyboardButton("Старая Басманная, 21/4")
                    mezhd = types.KeyboardButton("Большая Ордынка, 47/7")
                    markup.add(pokr, miem, shabl, basm, mezhd)
                    bot.send_message(message.chat.id, 'Выбери среди всех вариантов ниже корпус, в котором ты учишься и собираешься участвовать', reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, 'Такой профиль уже существует, я не могу обновить данные')

        else:
            bot.send_message(message.chat.id, 'Недостаточно данных для регистрации')
    elif not PlayerTask.objects.filter(foreign_id=message.from_user.id).exists():
        corp1 = '0'
        if message.text == "Покровский бульвар":
            corp1 = "Покровка"
        elif message.text == "МИЭМ":
            corp1 = "МИЭМ"
        elif message.text == "ВШБ":
            corp1 = "Шаболовка"
        elif message.text == "Старая Басманная, 21/4":
            corp1 = "Басманная"
        elif message.text == "Большая Ордынка, 47/7":
            corp1 = "Международные отношения"
        else:
            bot.send_message(message.chat.id, 'Попробуй ещё раз')
        if corp1 != '0':
            tasks1 = task_massive()
            qrcodes1 = task_massive()

            p, _ = PlayerTask.objects.get_or_create(
                foreign_id=message.from_user.id,
                place=corp1,
                stage=0,
                questions=tasks1,
                qr_codes=qrcodes1
                )

            bot.send_message(message.chat.id, 'Регистрация успешна! Теперь мы можем приступить к квесту!',
                             reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
            bot.send_message(message.chat.id,
                             'Перед каждым вопросом мы будем тебе присылать описание местоположения,'
                             ' где находится QR код, после чего ты будешь должна написать здесь слово, '
                             'зашифрованное в QR коде',
                             reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
            bot.send_message(message.chat.id, 'Далее после правильно введенного кода мы будем присылать вопрос,'
                                             ' за правильный ответ на который ты получаешь 1 балл.\n\n'
                                             'Помни, что будет лишь один шанс ответить на вопрос правильно!',
                             reply_markup=types.ReplyKeyboardRemove(),parse_mode='html')
            bot.send_message(message.chat.id, 'Если у тебя будут какие-либо вопросы, обращайся к @kudoff',
                             reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')

            a2 = PlayerTask.objects.get(foreign_id=message.from_user.id).place
            if str(a2) == "Покровка":
                q1 = PlayerTask.objects.get(foreign_id=message.from_user.id)
                q2 = q1.qr_codes
                asking = QrCodes.objects.get(number=int(q2.split(',')[0]))
                asking1 = asking.pokr

            elif str(a2) == "МИЭМ":
                q1 = PlayerTask.objects.get(foreign_id=message.from_user.id)
                q2 = q1.qr_codes
                asking = QrCodes.objects.get(number=int(q2.split(',')[0]))
                asking1 = asking.miem

            elif str(a2) == "Шаболовка":
                q1 = PlayerTask.objects.get(foreign_id=message.from_user.id)
                q2 = q1.qr_codes
                asking = QrCodes.objects.get(number=int(q2.split(',')[0]))
                asking1 = asking.vsb

            elif str(a2) == "Басманная":
                q1 = PlayerTask.objects.get(foreign_id=message.from_user.id)
                q2 = q1.qr_codes
                asking = QrCodes.objects.get(number=int(q2.split(',')[0]))
                asking1 = asking.bas

            elif str(a2) == "Международные отношения":
                q1 = PlayerTask.objects.get(foreign_id=message.from_user.id)
                q2 = q1.qr_codes
                asking = QrCodes.objects.get(number=int(q2.split(',')[0]))
                asking1 = asking.mo

            bot.send_message(message.chat.id, 'Следующий вопрос ты найдешь здесь:', parse_mode='html')
            bot.send_message(message.chat.id, asking1, parse_mode='html')

    elif PlayerTask.objects.filter(foreign_id=message.from_user.id).exists():
        stage2 = PlayerTask.objects.get(foreign_id=message.from_user.id)
        stage1 = stage2.stage
        if stage1 % 2 == 0:
            q1 = PlayerTask.objects.get(foreign_id=message.from_user.id)
            q2 = q1.qr_codes
            if message.text.lower() == QrCodes.objects.get(number=int(q2.split(',')[stage1 // 2])).code.lower():
                bot.send_message(message.chat.id, 'Код верный!', parse_mode='html')
                PlayerTask.objects.filter(foreign_id=message.from_user.id).update(stage=stage1+1)
                a1 = PlayerTask.objects.get(foreign_id=message.from_user.id).questions
                asking = Tasks.objects.get(number=int(a1.split(',')[stage1 // 2])).question
                bot.send_message(message.chat.id, asking, parse_mode='html')
        else:

            if message.text.lower() in Tasks.objects.get(number=int(PlayerTask.objects.get(foreign_id=message.from_user.id).questions.split(',')[(stage1 // 2)])).answer.lower():
                bot.send_message(message.chat.id, 'Верно!', parse_mode='html')
                score1 = Player.objects.get(foreign_id=message.from_user.id).score
                Player.objects.filter(foreign_id=message.from_user.id).update(score = score1 + 1)
            else:
                bot.send_message(message.chat.id, 'Неверно!', parse_mode='html')
            if stage1 != 37:
                a1 = PlayerTask.objects.get(foreign_id=message.from_user.id).place
                a2 = PlayerTask.objects.get(foreign_id=message.from_user.id).qr_codes
                if a1 == 'Покровка':
                    asking = QrCodes.objects.get(number=int(a2.split(',')[(stage1 // 2 + 1)]))
                    asking1 = asking.pokr

                if a1 == 'МИЭМ':
                    asking = QrCodes.objects.get(number=int(a2.split(',')[(stage1 // 2 + 1)]))
                    asking1 = asking.miem

                if a1 == 'Шаболовка':
                    asking = QrCodes.objects.get(number=int(a2.split(',')[(stage1 // 2 + 1)]))
                    asking1 = asking.vsb

                if a1 == 'Басманная':
                    asking = QrCodes.objects.get(number=int(a2.split(',')[(stage1 // 2 + 1)]))
                    asking1 = asking.bas

                if a1 == 'Международные отношения':
                    asking = QrCodes.objects.get(number=int(a2.split(',')[(stage1 // 2 + 1)]))
                    asking1 = asking.mo

                bot.send_message(message.chat.id, 'Следующий вопрос ты найдешь здесь:', parse_mode='html')
                bot.send_message(message.chat.id, asking1, parse_mode='html')
                PlayerTask.objects.filter(foreign_id=message.from_user.id).update(stage=stage1 + 1)
            else:
                bot.send_message(message.chat.id, 'На этом квест и заканчивается...\n'
                                                  'Спасибо, что прошла полностью квест!\n'
                                                  '\nВ ближайшее время, если ты станешь одной из победителей, мы тебе напишем!', parse_mode='html')
                bot.send_message(message.chat.id,
                                 'Не забывай следить за нашими мероприятиями!\n@hse_movement\nvk.com/movement_hse',
                                 parse_mode='html')
