import re
import telebot
import time
from database import *
from numpy import random
from mail import *
from sheet import *
from poll import *
exec(open('en_len.py').read())

##############################################
#         CHECKERS
##############################################

def check_group(chatid):
    if chatid not in groups:
        return True
    else:
        bot.send_message(chatid, en_msg_not_permot)
        return False

def check_mail(message):
    regex = r'\b[A-Za-z0-9._%+-]+@globallogic.com\b'
    if(re.fullmatch(regex, message.text)):
        return message.text
    else:
        bot.send_message(message.chat.id, en_msg_error_email)
        bot.register_next_step_handler(message, register)

def check_user(chatid):
    if is_param_exis('CHATID',chatid):
        if get_by_params(chatid, 'ISVERIFIED'):
            return True
    else:
        date= int(time.time())
        insert_query(chatid, 'username', 'name_surname', 'mail', False, False, date, 'location_region', False, 'location_city', 'country', False, 'plan_relocate_info', False, 'ready_to_relocate_outside_info', 'mobilizate', 'mobilizate_date', False, 'can_work_reason', 'productivity', 'productivity_difficulties', False, 'need_equipment_info', False, 'needresources_info', 'safe_mark', False, 'needmed_info', False, 'neadsuplies_info', False, 'needwater_info', 'needhelp_info')

def register(message):
    mail=check_mail(message)
    if mail:
        code=gen_code()
        send_code(mail,code)
        bot.send_message(message.chat.id, en_msg_verification_code)
        bot.register_next_step_handler(message, ath, code, mail)

def ath(message,code, mail):
    code=code.replace(" ", "")
    if message.text == code:
        update_by_param(message.chat.id, 'MAIL', mail)
        update_by_param(message.chat.id, 'ISVERIFIED', True)
        update_by_param(message.chat.id, 'NAME_SURNAME', get_name(mail))
        finish_reg(message)
    else:
        bot.send_message(message.chat.id, en_msg_error_verification)

def finish_reg(message):
    bot.send_message(message.chat.id, en_msg_finish_reg)
    mail=get_by_params(message.chat.id, 'MAIL')
    get_project(mail)
    info=get_all_params(message.chat.id)
    msg="&#127381 <b>{}</b>\n<b>Емейл:</b> {}\n\n#{}".format(info[0][2],info[0][3],get_hesh(info[0][3]))
    supervisor=info[0][25].replace(" ", "_")
    msg+="\n#{}".format(get_hesh(supervisor))
    bot.send_message(group_good, msg, parse_mode='html')
    poll(message,update,info[0][3])
    insert_in_sheet(info[0][3])

def is_updated(message,param):
    if message.text == param:
        update=True
    else:
        update=False
    return update

def gen_code():
    x=random.randint(9, size=(2, 3))
    a=' '
    for i in x:
        for j in i:
            a+=str(j)
        a+=' '
    return a
