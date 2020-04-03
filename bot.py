import telebot;
#import random;

TOKEN = '1184413942:AAFUBjVItCCweXDXbMEBp8thmlqS8RM3_vw'
bot = telebot.TeleBot(TOKEN);

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт! Я допомагаю в групі  @matan_help. Поки що у мене зовсім малий функціонал. Прошу не спамити команди в групу без поважної причини)')
    bot.send_message(message.chat.id, 'Бажаю усім 200 балів на ЗНО)')
@bot.message_handler(commands=['help'])
def send_help_message(message):
	bot.send_message(message.chat.id, 'Командою "/questiоn" ви можете попросиди допомоги з якоюсь задачею');
	bot.send_message(message.chat.id, 'Командою "/repоrt" ви можете повідомити про порушення, один з адмінів прийде на допомогу');

@bot.message_handler(commands=['report'])
def report_message(message):
	bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeR @melkii_pumba');
	if (message.chat.type == 'supergroup'):
		bot.send_message(message.chat.id, 'Розбійник в @matan_help');

@bot.message_handler(commands=['question'])
def question_message(message):
	bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeR @melkii_pumba');
	if (message.chat.type == 'supergroup'):
		bot.send_message(message.chat.id, 'Є питання в @matan_help');

@bot.message_handler(content_types=['new_chat_members'])
def hello_message(message): 
	bot.reply_to(message, '*Вітаю в Матановому і так інше*')


#перша версія команди /tast	
#isSolving = False;
#@bot.message_handler(command=['task'])
#def task_text(message):
#    if not isSolving:
#        a = random.randint(1, 10)
#        path = "Data/Tasks/2/Questions/".replace('/', '\\')+str(a)+".png"
#         with open(path, "r") as file:
#            ph = file.read()
#        bot.send_photo(message.chat.id, photo=ph)
#    	print(path)



bot.polling()










