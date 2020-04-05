import telebot;

TOKEN = 'token'
bot = telebot.TeleBot(TOKEN);

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт! Я допомагаю в групі  @matan_help')
    bot.send_message(message.chat.id, 'Бажаю усім 200 балів на ЗНО)')

#команди
helpText = """ /report - повідомити про порушення
/question - якщо виникло питання
/task - розв'язуйте задачі, стань першим в рейтингу
/stat - статистика чату
"""
@bot.message_handler(commands=['help'])
def help_message(message):
	bot.send_message(message.chat.id, helpText);
	

@bot.message_handler(commands=['report'])
def report_message(message):
	bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeR @melkii_pumba');
	if (message.chat.type == 'supergroup'):
		bot.send_message(-1001418192939, 'Розбійник в @matan_help');

@bot.message_handler(commands=['question'])
def question_message(message):
	bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeR @melkii_pumba');
	if (message.chat.type == 'supergroup'):
		bot.send_message(-1001418192939, 'Є питання в @matan_help');

# Новий учасник групи зайшов в чат
helloText = """Вітаю в @matan_help ✋

Головні правила чату:
➡️Не ображати інших учасників
➡️Допомагати іншим учасникам, якщо маєте змогу
➡️Якщо вам потрібна допомога, то просто попросіть
➡️За рекламу інших сторінок - бан🚫

/help - доступні команди

Бажаємо вам 200 балів на ЗНО!"""

PrevHelloMessageId = 51437 # рандомні цифри, номер повідомлення
NewHelloMessageId = 51438 # message_id

@bot.message_handler(content_types=['new_chat_members'])
def hello_message(message): 
	bot.reply_to(message, helloText)
	global PrevHelloMessageId 
	global NewHelloMessageId 
	PrevHelloMessageId = int(NewHelloMessageId)
	NewHelloMessageId = int(message.message_id) + 1 
	bot.delete_message(message.chat.id, PrevHelloMessageId) 


bot.polling()

