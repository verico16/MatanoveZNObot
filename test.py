import telebot
import sqlite3
from bs4 import BeautifulSoup
import threading

lock = threading.Lock()
# python test.py
# python d:\\test\matanbot\bot.py
TOKEN = '1184413942:AAFUBjVItCCweXDXbMEBp8thmlqS8RM3_vw'
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('test.db', check_same_thread = False)
cur = conn.cursor()
def create_table():
	cur.execute("""CREATE TABLE IF NOT EXISTS  statistics
										( user_id integer, name text, surname text, number_of_messages integer,
										activity real DEFAULT 0 , intelligence integer DEFAULT 0 )
								""")
	conn.commit()

create_table()

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привіт! Я допомагаю в групі  @matan_help')


@bot.message_handler(content_types=[""'video_note', 'voice', 'sticker', 'audio', 'document', 'photo', 'text',
																			'video', 'location', 'contact', 'new_chat_members', 'left_chat_member'""])
def count_msg(message):
	if (message.chat.id == -1001418192939): #айді троленка
		name = (message.from_user.first_name, "")[str(message.from_user.first_name) == "None"]
		surname = (message.from_user.last_name, "")[str(message.from_user.last_name) == "None"]
		usr_id = message.from_user.id
		mssg_id = message.message_id
		cur.execute("SELECT user_id FROM statistics WHERE user_id IN ({})".format(usr_id))
		user_id_list = cur.fetchall()	
		if (len(user_id_list) == 1):
			cur.execute("UPDATE statistics SET number_of_messages =+ 1 WHERE user_id = {}".format(usr_id))
			conn.commit()
		elif (len(user_id_list) == 0):
			cur.execute("INSERT INTO statistics (number_of_messages, name, surname, user_id) VALUES ( 1, '{}', '{}', {})".format(name, surname, usr_id))
			conn.commit()
		else: #якщо є дублікат
			cur.execute("SELECT * FROM statistics WHERE user_id IN ({})".format(usr_id))
			user_list_item = cur.fetchone()
			cur.execute("DELETE FROM statistics WHERE user_id IN ({})".format(usr_id))
			cur.execute("INSERT INTO statistics (user_id, name, surname, number_of_messages, activity, intelligence) VALUES ( {}, '{}', '{}', {}, {}, {})".format(user_list_item[0], user_list_item[1], user_list_item[2], user_list_item[3], user_list_item[4], user_list_item[5]))
			conn.commit()
			#кожні 5 повідомлень рахую активність
		if ((message.message_id % 5) == 0):
			cur.execute("SELECT  user_id, number_of_messages FROM statistics")
			activ_list = cur.fetchall()
			a_lenght = len(activ_list)
			for i in range(0, a_lenght):
				tupl = activ_list[i]
				ur_id = int(tupl[0])
				ur_mssg = int(tupl[1])
				all_mssg = message.message_id - 80129 #номер поточного повідомлення - номер першого повідомлення - 1
				proportion = (100*ur_mssg) / all_mssg #пропорція
				activ =  round(proportion, 3) 
				cur.execute("UPDATE statistics SET activity = {} WHERE user_id = '{}'".format(activ, ur_id))
				conn.commit()
			#потім добавляю нові данні на сайт
			cur.execute('SELECT name, surname, number_of_messages, activity, intelligence FROM statistics')
			list_of_users = cur.fetchall()
			html = open("index.html", "r")
			soup = BeautifulSoup(html, "lxml")
			u_lenght = len(list_of_users)
			for i in range(0, u_lenght):
				tag = soup.find('tr', id=i)
				list_item = list_of_users[i]
				usermame = str(list_item[0]) + ' ' + str(list_item[1])
				num_of_mssg = str(list_item[2])
				activ = str(list_item[3])
				intel = str(list_item[4])
				content = "<td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td>".format(i+1, usermame, num_of_mssg, activ, intel)
			new_text = soup.prettify()
			html.close()
			html = open("index.html", "w")
			html.write(str(new_text))
			html.close()
	else:
		pass



def intelligence(message, intel):
	cur = conn.cursor()
	user_id = message.from_user.id
	cur.execute("UPDATE statistics SET intelligence = (intelligence + {}) WHERE user_id = '{}'".format(intel, user_id))
	conn.commit()
	cur.close()



#refresh_html()

#cur.close()
#conn.close()

bot.infinity_polling()






