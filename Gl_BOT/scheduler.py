import schedule
import time
import   telebot
from telebot import types
# from lib import *
# from poll import *
from database import *
from checker import *


poll          = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
start_poll    = types.KeyboardButton(text='Start new poll')
update_poll   = types.KeyboardButton(text='Update existing data')
all_ok        = types.KeyboardButton(text='Declared data is actual')
poll.add(start_poll, update_poll, all_ok)

def mess_to_all(message):
    users=list_users_id()
    for user in users:
        if int(user) > 0:
            if check_user(user):
                message=bot.send_message(user, message.text)

def question_zero():
    users=list_users_id()
    for user in users:
        if int(user) > 0:
            if check_user(user):
                message=bot.send_message(user, "Please, fill the poll", reply_markup=poll)
                # update_by_param(user, 'ISACTUAL', True)

def list_users_id():
    cursor.execute("SELECT CHATID from employee")
    column_names = [row[0] for row in cursor]
    return                 column_names

# schedule.every().day.at("17:30").do(question_zero)

if __name__ == "__main__":
    question_zero()
