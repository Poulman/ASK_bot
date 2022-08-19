import   telebot
import re
from telebot import types
import sched, time
from scheduler import *
from poll import *
from checker import *
exec(open('en_len.py').read())

print(".-------------------------------------------------.")
print("| GlobalLogicbot                                  |")
print("| Author: Pavlo Mikush                            |")
print("| Github                                          |")
print("._________________________________________________.")

create_table()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if check_user(message.chat.id):
        bot.send_message(message.chat.id, en_msg_welcome)
    else:
        bot.send_message(message.chat.id, en_msg_start)
        bot.register_next_step_handler(message, register)

@bot.message_handler(commands=['help'])
def send_help(message):
    if check_group(message.chat.id):
        bot.send_message(message.chat.id, en_msg_help)

@bot.message_handler(commands=['answer_behalf'])
def behalf(message):
    if check_group(message.chat.id):
        bot.send_message(message.chat.id, en_msg_behalf_collegue)
        bot.register_next_step_handler(message, behalf_mail)

def behalf_mail(message):
    mail=check_mail(message)
    if mail:
        register_behalf(message,mail)
        get_project(mail)
        poll(message,update,mail)

def register_behalf(message,mail):
    if not is_param_exis('MAIL',mail):
        name=get_name(mail)
        date= int(time.time())
        insert_query(0, 'username', name, mail, False, False, date, 'location_region', False, 'location_city', 'country', False, 'plan_relocate_info', False, 'ready_to_relocate_outside_info', 'mobilizate', 'mobilizate_date', False, 'can_work_reason', 'productivity', 'productivity_difficulties', False, 'need_equipment_info', False, 'needresources_info', 'manager', False, 'needmed_info', False, 'neadsuplies_info', False, 'needwater_info', 'needhelp_info')

@bot.message_handler(commands=['registration'])
def check_reg(message):
    if check_group(message.chat.id):
        if check_user(message.chat.id):
            bot.send_message(message.chat.id, en_msg_already_registered)
        else:
            bot.send_message(message.chat.id, en_msg_start)
            bot.register_next_step_handler(message, register)

@bot.message_handler(commands=['update_poll'])
def update_poll(message):
    if check_group(message.chat.id):
        update = True
        mail=get_by_params(message.chat.id, 'MAIL')
        poll(message,update,mail)

@bot.message_handler(commands=['send_message'])
def send_message(message):
    if message.chat.id == admin_group:
        bot.send_message(message.chat.id, en_msg_wait_msg)
        bot.register_next_step_handler(message, mess_to_all)
    else:
        bot.send_message(message.chat.id, en_msg_not_permot)

@bot.message_handler(commands=['ping_all'])
def ping(message):
    if message.chat.id == admin_group:
        question_zero()
    else:
        bot.send_message(message.chat.id, en_msg_not_permot)

@bot.message_handler(commands=['poll'])
def send_poll(message):
    if check_group(message.chat.id):
        if check_user(message.chat.id):
            mail=get_by_params(message.chat.id, 'MAIL')
            refresh(mail)
            mail=get_by_params(message.chat.id, 'MAIL')
            poll(message,update,mail)
        else:
            bot.send_message(message.chat.id, en_msg_unregistered)

##############################################
#               SOS
##############################################

@bot.message_handler(commands=['sos'])
def send_help(message):
    if check_group(message.chat.id):
        if check_user(message.chat.id):
            bot.send_message(message.chat.id, en_msg_сity_option, reply_markup=Regions)
            bot.register_next_step_handler(message, sos1)
        else:
            bot.send_message(message.chat.id, en_msg_unregistered)

def sos1(message):
    bot.send_message(message.chat.id, en_msg_problem_description)
    bot.register_next_step_handler(message, finish_sos)

def finish_sos(message):
    mail=get_by_params(message.chat.id, 'MAIL')
    bot.send_message(message.chat.id, en_msg_finish_sos)
    info=get_all_params(message.chat.id)
    msg="&#127384 {}\n\n{}".format(info[0][10],message.text)
    msg+="\n#{}".format(get_hesh(mail))
    supervisor=info[0][25].replace(" ", "_")
    msg+="\n#{}".format(get_hesh(supervisor))
    bot.send_message(group, msg, parse_mode='html')

##############################################
#               TEXT HANDLER
##############################################

@bot.message_handler(func=lambda m: True)
def text(message):
    if check_group(message.chat.id):
        if check_user(message.chat.id):
            info=get_all_params(message.chat.id)
            mail=info[0][3]
            if message.text == 'r':
                reg_location(message)
            elif message.text == 'Start new poll':
                refresh(mail)
                poll(message,update,mail)
            elif message.text == 'Update existing data':
                poll(message,True,mail)
            elif message.text == 'Declared data is actual':
                bot.send_message(message.chat.id, en_msg_data_actualized)
                output(mail)
            else:
                bot.send_message(message.chat.id, en_msg_error_type)
        else:
            bot.send_message(message.chat.id, en_msg_unregistered)

bot.polling()
