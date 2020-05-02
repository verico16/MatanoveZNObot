import telebot
import random
import time
import pymysql
from collections import deque
import math

bot = telebot.TeleBot(TOKEN)

q = deque()
path = ""
isSolving = False
rightAnswer = 0
level = 0
tm = 0
tmpar = 0
isPAdd = False
isAdd = False
add_level = 0
add_ans = 0
add_lvls_list = [0, 0, 0, 0, 0]
antirepeat = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
PrevHelloMessageId = 101437  # рандомні цифри, номер повідомлення
NewHelloMessageId = 101438  # message_id
helloText = """Вітаю в @matan_help ✋
Головні правила чату:
➡️Не ображати інших учасників
➡️Допомагати іншим учасникам, якщо маєте змогу
➡️Якщо вам потрібна допомога, то просто попросіть
➡️За рекламу інших сторінок - бан🚫
/help - доступні команди
Бажаємо вам 200 балів на ЗНО!"""
helpText = """ /report - повідомити про порушення
/question - якщо виникло питання
/task [складність]- розв'язуй задачі, стань першим в рейтингу(складність варіюється від 1 до 4, де 1-найлегший рівень)
/stat - статистика чату
/top [msg або intel]- топ 10 учасників чату(msg-сортування за кілкістю повідомлень, intel-за інтелектуальним рейтингом)"""


def rnd(x):
    if x == 0:
        return 0
    y = abs(x) * 10000.0
    if math.floor(y) % 10 >= 5:
        y += 10.0
    y /= 10.0
    y = math.floor(y)
    y = (x / abs(x)) * y / 1000.0
    return y


def pts():
    tm1 = int(time.time()) - int(tm)
    return round(
        pow(2, (level - 1) / 2.0) * pow(3, float(level) - float(tm1 / (120.0 * pow(10, float(level + 2) / 3.0)))))


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт! Я допомагаю в групі  @matan_help')


# команди
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, helpText)


def trueRandom(a, lvl):
    rndval = random.randint(1, a)
    for i in antirepeat[lvl - 1]:
        if i == rndval:
            return trueRandom(a, lvl)
    for i in range(1, 20):
        antirepeat[lvl - 1][i - 1] = antirepeat[lvl - 1][i]
    antirepeat[lvl - 1][i] = rndval
    return rndval


@bot.message_handler(commands=['report'])
def report_message(message):
    bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeP @melkii_pumba')
    if message.chat.type == 'supergroup':
        bot.send_message(-1001418192939, 'Розбійник в @matan_help')


@bot.message_handler(commands=['question'])
def question_message(message):
    bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeP @melkii_pumba')
    if message.chat.type == 'supergroup':
        bot.send_message(-1001418192939, 'Є питання в @matan_help')


# @bot.message_handler(commands=['parameters'])
# def parameters_text(message):
# 	global tmpar
# 	if time.time()-tmpar>600:
# 		tmpar=time.time()
# 		listQ = open("Data/Tasks/q.txt", 'r')
# 		counter=0
# 		quantity=0
# 		for line in listQ:
# 			counter+=1
# 			if counter==5:
# 				quantity=int(line)
# 		a = random.randint(1, quantity)
# 		pth = r"Data/Tasks/Questions/5/" + str(a) + ".png"
# 		file = open(pth, 'rb')
# 		bot.send_photo(message.chat.id, file, caption="Розв'язання цих задач на параметри не впливає на інтелектуальний рейтинг. Тут ви можете знайти лише вибрані задачі підвищеної складності. Викликати іншу задачу можна лише через 10 хвилин після виклику даної задачі. Відповідь автоматично не перевіряється.")


@bot.message_handler(commands=['task'])
def task_text(message):
    global isSolving
    global rightAnswer
    global path
    global level
    global tm
    tester = 0
    tm1 = time.time()
    if int(tm1) - int(tm) > 600 * level:
        isSolving = False
    try:
        tester = int(message.text[6:])
    except:
        bot.reply_to(message,
                     'Вказані невірні аргументи. Аргументом може слугувати лише число від 1 до 4 включно, де число позначає складність завдання')
        return 0
    if not isSolving and (tester == 1 or tester == 2 or tester == 3 or tester == 4):
        listQ = open("Data/Tasks/q.txt", 'r')
        quantity = 0
        counter = 0
        for line in listQ:
            counter += 1
            if counter == int(message.text[6]):
                level = int(message.text[6])
                quantity = int(line)
        a = trueRandom(quantity, level)
        path = r"Data/Tasks/Questions/" + message.text[6] + "/" + str(a) + ".png"
        file = open(path, 'rb')
        bot.send_photo(message.chat.id, file,
                       caption='Відповіддю є число в десятковому записі. Відповідь округлюється до трьох знаків після коми за правилами округлення.\nРівень складності: ' + str(
                           level) + '\nПриклад: 16; -38,8; 0; 44.268. \nТермін виконання - ' + str(
                           level * 10) + ' хвилин')
        isSolving = True
        path2 = "Data/Tasks/Solutions/" + str(level) + "/sol.txt"
        counter = 0
        sol = open(path2, 'r')
        for line in sol:
            counter += 1
            if counter == a:
                rightAnswer = line
        file.close()
        sol.close()
        listQ.close()
        tm = time.time()
    elif isSolving:
        file = open(path, 'rb')
        bot.send_photo(message.chat.id, file, caption=r"Спочатку розв'яжіть запропоновану задачу!")
    else:
        bot.reply_to(message,
                     'Вказані невірні аргументи. Аргументом може слугувати лише число від 1 до 4 включно, де число позначає складність завдання')
        return 0


@bot.message_handler(commands=['add'])
def add_command(message):
    global add_level
    global add_ans
    global isAdd
    if int(message.chat.id) != -1001382702607:
        bot.reply_to(message, 'На жаль, Ви не маєте прав додавати завдання до боту')
        return 0
    try:
        add_level = int(message.text[5])
        add_ans = message.text[7]
        add_ans = float(message.text[7:].replace(',', '.'))
        isAdd = True
    except:
        bot.reply_to(message, 'Невірні аргументи')
        return 0
    f = open('Data/Tasks/q.txt', 'r')
    counter = 0
    for line in f:
        add_lvls_list[counter] = int(line)
        counter += 1
    add_lvls_list[add_level - 1] += 1
    f.close()
    bot.reply_to(message, 'Ожидаю фото...')


# @bot.message_handler(commands=['stat'])
# def url_send(message):
#     url = ''
#     bot.reply_to(message, url)


@bot.message_handler(commands=['top'])
def top_10(message):
    # print(msg)
    sort = message.text[5:]
    sort = sort.replace(" ", "")
    # print(sort)
    conn = pymysql.connect(host="localhost", user="andrii", password="password", database="Matanove")
    cur = conn.cursor()
    if sort == "msg":
        msg = str('Рейтинг за кілкістю повідомлень\n')
        cur.execute(
        f"SELECT t1.name, t1.surname, t2.qty FROM identify=t1, stat=t2 WHERE t1.user_id = t2.user_id ORDER BY t2.qty DESC")
        top_name = cur.fetchmany(size=10)
        # print(top_name)
        counter = 1
        for person in top_name:
            msg += '<b><i>' + str(counter) + '. '
            msg += '</i></b>' + str(person[0]) + ' '
            msg += (str(person[1]) + ' - ', '- ')[person[1] == '']
            msg += '<b>' + str(person[2]) + '</b>\n'
            counter += 1
        # print(msg)
        bot.reply_to(message, msg, parse_mode="HTML")
    elif sort == "intel":
        msg = str('Інтелектуальний рейтинг\n')
        cur.execute(
        f"SELECT t1.name, t1.surname, t2.intel FROM identify=t1, stat=t2 WHERE t1.user_id = t2.user_id ORDER BY t2.intel DESC")
        top_name = cur.fetchmany(size=10)
        # print(top_name)
        counter = 1
        for person in top_name:
            msg += '<b><i>' + str(counter) + '. '
            msg += '</i></b>' + str(person[0]) + ' '
            msg += (str(person[1]) + ' - ', '- ')[person[1] == '']
            msg += '<b>' + str(person[2]) + '</b>\n'
            counter += 1
        # print(msg)
        bot.reply_to(message, msg, parse_mode="HTML")
    else:
        bot.reply_to(message,
                     'Вказані невірні аргументи. Аргументом може слугувати лише msg або intel')
    conn.commit()
    cur.close()


@bot.message_handler(commands=['paradd'])
def add_command(message):
    global isPAdd
    if int(message.chat.id) != -1001382702607:
        bot.reply_to(message, 'На жаль, Ви не маєте прав додавати завдання до боту')
        return 0
    f = open('Data/Tasks/q.txt', 'r')
    counter = 0
    for line in f:
        add_lvls_list[counter] = int(line)
        counter += 1
    add_lvls_list[4] += 1
    isPAdd = True
    bot.reply_to(message, 'Приму параметры только если Илона отсосёт...')


@bot.message_handler(content_types=[""'video_note', 'voice', 'sticker', 'audio', 'document', 'photo', 'text',
                                    'video', 'location', 'contact', 'new_chat_members', 'left_chat_member'""])
def sorting(message):
    queue(message)
    if message.content_type == 'new_chat_members':
        hello_message(message)
    elif message.content_type == 'text':
        send_text(message)
    elif message.content_type == 'photo':
        handle_docs_photo(message)
    else:
        pass


# Новий учасник групи зайшов в чат
def hello_message(message):
    if message.chat.id != -1001382702607 and message.chat.id != -1001415917929 and message.chat.id != -1001418192939:
        bot.leave_chat(message.chat.id)
    bot.reply_to(message, helloText)
    global PrevHelloMessageId
    global NewHelloMessageId
    PrevHelloMessageId = int(NewHelloMessageId)
    NewHelloMessageId = int(message.message_id) + 1
    bot.delete_message(message.chat.id, PrevHelloMessageId)


def send_text(message):
    if message.chat.id != -1001382702607 and message.chat.id != -1001415917929 and message.chat.id != -1001418192939:
        bot.leave_chat(message.chat.id)
        return 0
    global isSolving
    tm1 = time.time()
    txt = message.text
    temp = 0.0
    txt = txt.replace(',', '.')
    if int(tm1) - int(tm) > 600 * level:
        isSolving = False
    try:
        float(txt)
        isVal = True
    except ValueError:
        isVal = False
    if isVal:
        if isSolving and float(rnd(float(txt))) == float(rnd(float(rightAnswer))):
            bot.reply_to(message,
                         '<b>Вітаємо!</b> <i>Ви першим розв\'язали задачу рівня ' + str(level) + ' за <b>' + str(
                             int(tm1) - int(tm)) + ' с</b>, і отримуєте</i> <b>+' + str(
                             pts()) + '</b> <i>до Вашого інтелектуального рейтингу</i>', parse_mode="HTML")
            isSolving = False
            intelligence(message, pts())


def handle_docs_photo(message):
    global isAdd
    global isPAdd
    if isAdd and message.chat.id == -1001382702607:
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = "Data/Tasks/Questions/" + str(add_level) + "/" + str(add_lvls_list[add_level - 1]) + ".png"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
                bot.reply_to(message, "Ok!")
            f = open("Data/Tasks/q.txt", 'w')
            for i in add_lvls_list:
                f.write(str(i) + '\n')
            f.close()
            f = open("Data/Tasks/Solutions/" + str(add_level) + "/sol.txt", 'a')
            f.write('\n' + str(add_ans))
            isAdd = False
        except Exception as e:
            bot.reply_to(message, e)
    if isPAdd and message.chat.id == -1001382702607:
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = "Data/Tasks/Questions/5/" + str(add_lvls_list[add_level - 1]) + ".png"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
                bot.reply_to(message, "Илона отлично сосёт!")
            f = open("Data/Tasks/q.txt", 'w')
            for i in add_lvls_list:
                f.write(str(i) + '\n')
            f.close()
            isPAdd = False
        except Exception as e:
            bot.reply_to(message, e)


def queue(message):
    # if message.chat.id == -1001415917929:
    if message.chat.id == -1001418192939:
        q.append(message)
        while len(q) > 0:
            mssg = q.popleft()
            conn = pymysql.connect(host="localhost", user="andrii", password="password", database="Matanove")
            cur = conn.cursor()
            name = (str(mssg.from_user.first_name), "")[str(mssg.from_user.first_name) == "None"]
            surname = (str(mssg.from_user.last_name), "")[str(mssg.from_user.last_name) == "None"]
            user_id = mssg.from_user.id
            cur.execute(f"SELECT user_id FROM identify WHERE user_id = '{user_id}'")
            user_id_list = cur.fetchall()
            if len(user_id_list) == 1:
                # print(name + "1")
                cur.execute(f"UPDATE stat SET qty = qty + 1 WHERE user_id = '{user_id}'")
            elif len(user_id_list) == 0:
                # print(name + "2")
                cur.execute(f"INSERT INTO identify VALUES ('{name}', '{surname}', '{user_id}')")
                cur.execute(f"INSERT INTO stat (qty, user_id) VALUES (1, '{user_id}')")
            else:
                # print(name + "3")
                cur.execute(f"SELECT * FROM stat WHERE user_id = '{user_id}'")
                user_false_list = cur.fetchone()
                cur.execute(f"DELETE FROM stat WHERE user_id = '{user_id}'")
                cur.execute(
                    f"INSERT INTO stat VALUES ('{user_false_list[0]}', '{user_false_list[1]}', '{user_false_list[2]}')")
                cur.execute(f"UPDATE stat SET qty = qty + 1 WHERE user_id = '{user_id}'")
                cur.execute(f"SELECT * FROM identify WHERE user_id = '{user_id}'")
                user_false_list1 = cur.fetchone()
                cur.execute(f"DELETE FROM identify WHERE user_id = '{user_id}'")
                cur.execute(
                    f"INSERT INTO identify VALUES ('{user_false_list1[0]}', '{user_false_list1[1]}', '{user_false_list1[2]}')")
            conn.commit()
            cur.close()
    else:
        pass


def intelligence(message, intel):
    # print(intel)
    conn = pymysql.connect(host="localhost", user="andrii", password="password", database="Matanove")
    cur = conn.cursor()
    user_id = message.from_user.id
    query = "UPDATE `stat` SET `intel` = `intel` + {} WHERE `user_id` = '{}'".format(intel, user_id)
    # print(query)
    cur.execute(query)
    conn.commit()
    cur.close()


bot.infinity_polling()
