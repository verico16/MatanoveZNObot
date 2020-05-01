import telebot
import random
import time
import pymysql
from collections import deque

bot = telebot.TeleBot(TOKEN)


q = deque()
path = ""
isSolving = False
rightAnswer = 0
level = 0
tm = 0
isAdd = False
add_level = 0
add_ans = 0
add_lvls_list = [0, 0, 0, 0]
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
/task - розв'язуйте задачі, стань першим в рейтингу
/stat - статистика чату"""


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


@bot.message_handler(commands=['report'])
def report_message(message):
    bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeR @melkii_pumba')
    if message.chat.type == 'supergroup':
        bot.send_message(-1001418192939, 'Розбійник в @matan_help')


@bot.message_handler(commands=['question'])
def question_message(message):
    bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeR @melkii_pumba')
    if message.chat.type == 'supergroup':
        bot.send_message(-1001418192939, 'Є питання в @matan_help')


@bot.message_handler(commands=['task'])
def task_text(message):
    global isSolving
    global rightAnswer
    global path
    global level
    global tm
    tm1 = time.time()
    if int(tm1) - int(tm) > 1200:
        isSolving = False
    try:
        tester = message.text[6]
    except:
        bot.reply_to(message,
                     'Вказані невірні аргументи. Аргументом може слугувати лише число від 1 до 4 включно, де число позначає складність завдання')
        return 0
    if not isSolving and (
            message.text[6] == '1' or message.text[6] == '2' or message.text[6] == '3' or message.text[6] == '4'):
        listQ = open("Data/Tasks/q.txt", 'r')
        quantity = 0
        counter = 0
        for line in listQ:
            counter += 1
            if counter == int(message.text[6]):
                level = int(message.text[6])
                quantity = int(line)
        a = random.randint(1, quantity)
        path = r"Data/Tasks/Questions/" + message.text[6] + "/" + str(a) + ".png"
        file = open(path, 'rb')
        bot.send_photo(message.chat.id, file,
                       caption='Відповіддю є число в десятковому записі. Гарантується, що нескінченних десяткових періодичних дробів немає.\nРівень складності: ' + str(
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
    

@bot.message_handler(commands=['top'])
def top_10(message):
    top_table = []
    sort = message.text[5:]
    sort = sort.replace(" ", "")
    # print(sort)
    conn = pymysql.connect(host="localhost", user="andrii", password="password", database="Matanove")
    cur = conn.cursor()
    if sort == "msg":
        cur.execute(f"SELECT * FROM stat ORDER BY qty DESC")
        top_list = cur.fetchmany(size=10)
        # print(top_list)
        # вот отсюда
        for top_list_user in top_list:
            # print(top_list_user)
            top_id = int(top_list_user[1])
            # print(top_id)
            cur.execute(f"SELECT t1.name, t1.surname, t2.qty, t2.intel FROM identify=t1, stat=t2 WHERE t1.user_id = t2.user_id AND t1.user_id = '{top_id}'")
            top_name = cur.fetchall()
            # print(top_name)
            top_table.append(top_name[0])

        print(top_table)
        msg = ""
        for line in top_name[0]:
            print(line)
            msg = msg + str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[2]) + ' ' + str(line[3])
            # msg = msg + str(line)
        bot.reply_to(message, 'ім\'я, прізвище, кіл-сть повідомлень, інт. рейтинг \n'
                     + msg
                     )
    #     до сюда всё скопировать и вставить
    elif sort == "intel":
        cur.execute(f"SELECT * FROM stat ORDER BY intel DESC")
        top_list = cur.fetchmany(size=10)
    #     сюда
    else:
        bot.reply_to(message,
                     'Вказані невірні аргументи. Аргументом може слугувати лише msg або intel')
    conn.commit()
    cur.close()


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
    bot.reply_to(message, helloText)
    global PrevHelloMessageId
    global NewHelloMessageId
    PrevHelloMessageId = int(NewHelloMessageId)
    NewHelloMessageId = int(message.message_id) + 1
    bot.delete_message(message.chat.id, PrevHelloMessageId)


def send_text(message):
    global isSolving
    tm1 = time.time()
    txt = message.text
    txt = txt.replace(',', '.')
    if int(tm1) - int(tm) > 1200:
        isSolving = False
    try:
        float(txt)
        isVal = True
    except ValueError:
        isVal = False
    # print(message.text)
    if isVal:
        if isSolving and float(txt) == float(rightAnswer):
            bot.reply_to(message, '*Вітаємо!* _Ви першим розв\'язали задачу рівня ' + str(level) + ' за ' + str(
                int(tm1) - int(tm)) + ' с, і отримуєте _*+' + str(pts()) + '*_ до Вашого інтелектуального рейтингу_',
                         parse_mode="Markdown")
            isSolving = False
            intelligence(message, pts())


def handle_docs_photo(message):
    global isAdd
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
                cur.execute(f"INSERT INTO stat VALUES ('{user_false_list[0]}', '{user_false_list[1]}', '{user_false_list[2]}')")
                cur.execute(f"UPDATE stat SET qty = qty + 1 WHERE user_id = '{user_id}'")
                cur.execute(f"SELECT * FROM identify WHERE user_id = '{user_id}'")
                user_false_list1 = cur.fetchone()
                cur.execute(f"DELETE FROM identify WHERE user_id = '{user_id}'")
                cur.execute(f"INSERT INTO identify VALUES ('{user_false_list1[0]}', '{user_false_list1[1]}', '{user_false_list1[2]}')")
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

'''
bot.infinity_polling()
