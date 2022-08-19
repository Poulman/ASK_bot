import   telebot
from lib import *
from mail import *
import re
from telebot import types
import sched, time
from scheduler import *
from sheet import *
from buttons import *
from poll import *
# from checker import *
exec(open('ua_len.py').read())
# exec(open('vars.py').read())

print(".-------------------------------------------------.")
print("| GlobalLogicbot                                  |")
print("| Author: Pavlo Mikush                            |")
print("| Github                                          |")
print("._________________________________________________.")

create_table()
# update        = False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if check_user(message.chat.id):
        bot.send_message(message.chat.id, ua_msg_welcome)
    else:
        bot.send_message(message.chat.id, ua_msg_start)
        bot.register_next_step_handler(message, register)

@bot.message_handler(commands=['help'])
def send_help(message):
    if check_group(message.chat.id):
        bot.send_message(message.chat.id, ua_msg_help)

@bot.message_handler(commands=['answer_behalf'])
def behalf(message):
    if check_group(message.chat.id):
        bot.send_message(message.chat.id, "I answer on behalf of my collegue:\nIndicate the GlobalLogic mail of collegue")
        bot.register_next_step_handler(message, behalf_mail)

def behalf_mail(message):
    mail=check_mail(message)
    if mail:
        register_behalf(message,mail)
        insert_in_sheet(mail)
        poll(message,update,mail)

@bot.message_handler(commands=['registration'])
def check_reg(message):
    if check_group(message.chat.id):
        if check_user(message.chat.id):
            bot.send_message(message.chat.id, ua_msg_already_registered)
        else:
            bot.send_message(message.chat.id, ua_msg_start)
            bot.register_next_step_handler(message, register)

@bot.message_handler(commands=['update_poll'])
def update_poll(message):
    if check_group(message.chat.id):
        bot.send_message(message.chat.id, "Please, chose section for update", reply_markup=topic)
        bot.register_next_step_handler(message, update_param)

def update_param(message):
    update = True
    mail=get_by_params(message.chat.id, 'MAIL')
    poll(message,update,mail)

@bot.message_handler(commands=['send_message'])
def send_message(message):
    if message.chat.id == admin_group:
        bot.send_message(message.chat.id, "Please, type the message")
        bot.register_next_step_handler(message, mess_to_all)
    else:
        bot.send_message(message.chat.id, "Command is not permitted")

@bot.message_handler(commands=['ping_all'])
def ping(message):
    if message.chat.id == admin_group:
        question_zero()
    else:
        bot.send_message(message.chat.id, "Command is not permitted")

# def update_param(message):
#     update = True
#     mail=get_by_params(message.chat.id, 'MAIL')
#     poll(message,update,mail)
    # # poll.location(message)
    # p1 = poll(message, update)
    # p1.update_poll_param()
    # if message.text == 'Location':
    #     location(message,update)
    # if message.text == 'Mobilization status':
    #     mobil(message,update)
    # if message.text == 'Possibility to work':
    #     q_can_work(message,update)
    # if message.text == 'Productivity':
    #     q_productivity(message,update)
    # if message.text == 'Relocation':
    #     q_plan_relocate(message,update)
    # if message.text == 'Resources':
    #     q_need_some(message,update)
    # if message.text == 'Nothing':
    #     bot.send_message(message.chat.id, "Thanks")
    #     return

@bot.message_handler(commands=['poll'])
def send_poll(message):
    if check_group(message.chat.id):
        refresh(message.chat.id)
        # location(message,update)
        mail=get_by_params(message.chat.id, 'MAIL')
        poll(message,update,mail)

@bot.message_handler(commands=['sos'])
def send_help(message):
    if check_group(message.chat.id):
        if check_user(message.chat.id):
            bot.send_message(message.chat.id, 'Please, indicate your current city location. If your city is not on the list, write it down ', reply_markup=Regions)
            bot.register_next_step_handler(message, sos1)
        else:
            bot.send_message(message.chat.id, ua_msg_unregistered)

def sos1(message):
    bot.send_message(message.chat.id, ua_msg_problem_description)
    bot.register_next_step_handler(message, finish_sos)

##############################################
#               TEXT HANDLER
##############################################

@bot.message_handler(func=lambda m: True)
def text(message):
    if check_group(message.chat.id):
        if check_user(message.chat.id):
            info=get_all_params(message.chat.id)
            if message.text == 'r':
                reg_location(message)
            elif message.text == 'Start new poll':
                refresh(message.chat.id)
                location(message,update)
            elif message.text == 'Update existing data':
                update_poll(message)
            elif message.text == 'Declared data is actual':
                bot.send_message(message.chat.id, "Thanks, data is actualized")
                # update_by_param(message.chat.id, 'ISACTUAL', True)
                output(message.chat.id)
            else:
                bot.send_message(message.chat.id, "You can't type here. Please, follow the buttons.\nIn case of emergency, use /sos command")
        else:
            bot.send_message(message.chat.id, ua_msg_unregistered)

# def register(message):
#     # regex = r'\b[A-Za-z0-9._%+-]+@globallogic.com\b'
#     mail=check_mail(message)
#     if mail:
#         mail=message.text
#         code=gen_code()
#         send_code(mail,code)
#         bot.send_message(message.chat.id, ua_msg_verification_code)
#         bot.register_next_step_handler(message, ath, code, mail)
    # else:
    #     bot.send_message(message.chat.id, ua_msg_error_email)
    #     bot.register_next_step_handler(message, register)

def ath(message,code, mail):
    code=code.replace(" ", "")
    if message.text == code:
        update_by_param(message.chat.id, 'MAIL', mail)
        update_by_param(message.chat.id, 'ISVERIFIED', True)
        # name_surname(message)
        # name=get_name(mail)
        update_by_param(message.chat.id, 'NAME_SURNAME', get_name(mail))
        finish_reg(message)
    else:
        bot.send_message(message.chat.id, ua_msg_error_verification)

# def name_surname(message):
#     info=get_all_params(message.chat.id)
#     name=info[0][3].replace("@globallogic.com", "")
#     name=name.replace(".", " ")
#     name_surname=mail.title()
#     update_by_param(message.chat.id, 'NAME_SURNAME', name_surname)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# refresh(message.chat.id)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# def location(message,update):
#     # if
#     # update=is_updated(message,'Location')
#     bot.send_message(message.chat.id, 'Please, indicate your current regional center location. If your regional center is not on the list, write it down (ONLY regional center or the region).', reply_markup=Regions)
#     bot.register_next_step_handler(message, location1,update)
#
# def q_is_regional_center(message,update):
#     bot.send_message(message.chat.id, 'Please, specify do you locate in the regional center?', reply_markup=YesNo)
#     bot.register_next_step_handler(message, location2,update)
#
# def q_country(message,update):
#     bot.send_message(message.chat.id, 'Please, specify your country. Is not on the list, write it down', reply_markup=Countries)
#     bot.register_next_step_handler(message, country,update)
#
# def q_citi(message,update):
#     bot.send_message(message.chat.id, 'Please, specify your city/vilage location.')
#     bot.register_next_step_handler(message, city,update)
#
# def q_mobil_ter(message,update):
#     bot.send_message(message.chat.id, "Since when?")
#     bot.register_next_step_handler(message, mobilized_data_t,update)
#
# def q_mobil_army(message,update):
#     bot.send_message(message.chat.id, "Since when?")
#     bot.register_next_step_handler(message, mobilized_data,update)
#
# def q_can_work(message,update):
#     update=is_updated(message,'Possibility to work')
#     bot.send_message(message.chat.id, ua_q_can_work, reply_markup=YesNo)
#     bot.register_next_step_handler(message, can_work,update)
#
# def q_productivity(message,update):
#     update=is_updated(message,'Productivity')
#     bot.send_message(message.chat.id, ua_q_productivity, reply_markup=percent)
#     bot.register_next_step_handler(message, productivity,update)
#
# def q_can_work_reason(message,update):
#     bot.send_message(message.chat.id, ua_msg_reason)
#     bot.register_next_step_handler(message, reason,update)
#
# def q_difficulties(message,update):
#     bot.send_message(message.chat.id, 'Please, let us know what makes difficulties?')
#     bot.register_next_step_handler(message, difficulties,update)
#
# def q_plan_relocate(message,update):
#     update=is_updated(message,'Relocation')
#     bot.send_message(message.chat.id, ua_q_location, reply_markup=YesNo)
#     bot.register_next_step_handler(message, plan_relocate,update)
#
# def q_plan_relocate_info(message,update):
#     bot.send_message(message.chat.id, ua_msg_location)
#     bot.register_next_step_handler(message, plan_relocate_info,update)
#
# def q_relocate_out(message,update):
#     bot.send_message(message.chat.id, ua_q_relocate, reply_markup=YesNo)
#     bot.register_next_step_handler(message, relocate_out,update)
#
# def q_relocate_out_info(message,update):
#     bot.send_message(message.chat.id, ua_msg_relocate, reply_markup=relocate_info)
#     bot.register_next_step_handler(message, relocate_out_info,update)
#
# def q_need_some(message,update):
#     update=is_updated(message,'Resources')
#     bot.send_message(message.chat.id, "Please, specify if you need something from this list:", reply_markup=need_some_k)
#     bot.register_next_step_handler(message, need_some,update)
#
# def q_resources(message,update):
#     update_by_param(message.chat.id, 'NEED_RESOURCES_INFO', message.text)
#     q_need_some_more(message,update)
#
# def q_equipment(message,update):
#     update_by_param(message.chat.id, 'NEED_EQUIPMENT_INFO', message.text)
#     q_need_some_more(message,update)
#
# def q_needeat(message,update):
#     update_by_param(message.chat.id, 'NEEDEAT_INFO', message.text)
#     q_need_some_more(message,update)
#
# def q_needmed(message,update):
#     update_by_param(message.chat.id, 'NEEDMED_INFO', message.text)
#     q_need_some_more(message,update)
#
# def q_needwater(message,update):
#     update_by_param(message.chat.id, 'NEEDWATER_INFO', message.text)
#     q_need_some_more(message,update)
#
# def q_need_some_more(message,update):
#     bot.send_message(message.chat.id, "Please, indicate, do you need something more from this list?", reply_markup=need_some_k)
#     bot.register_next_step_handler(message, need_some,update)
#
# def q_additional(message):
#     bot.send_message(message.chat.id, ua_q_more_help, reply_markup=YesNo)
#     bot.register_next_step_handler(message, additional)
#
# def q_additional_info(message):
#     bot.send_message(message.chat.id, ua_msg_more_help)
#     bot.register_next_step_handler(message, finish_q)
#
# def location1(message,update):
#     update_by_param(message.chat.id, 'LOCATION_REGION', message.text)
#     if message.text != 'Out of Ukraine':
#         update_by_param(message.chat.id, 'COUNTRY', 'Ukraine')
#         q_is_regional_center(message,update)
#     else:
#         q_country(message,update)
#
# def location2(message,update):
#     if message.text != 'Back':
#         if message.text == 'Yes':
#             update_by_param(message.chat.id, 'LOCATION_CITY', get_by_params(message.chat.id, 'LOCATION_REGION'))
#             update_by_param(message.chat.id, 'IS_LOCATION_REGION_CENTER', True)
#             if not update:
#                 mobil(message,update)
#             else:
#                 bot.send_message(message.chat.id, "Information has been seccesfully updated")
#                 output(message.chat.id)
#                 return
#         if message.text == 'No':
#             update_by_param(message.chat.id, 'IS_LOCATION_REGION_CENTER', False)
#             q_citi(message,update)
#     else:
#         location(message,update)
#
# def city(message,update):
#     update_by_param(message.chat.id, 'LOCATION_CITY', message.text)
#     if not update:
#         mobil(message,update)
#     else:
#         bot.send_message(message.chat.id, "Information has been seccesfully updated")
#         output(message.chat.id)
#         return
#
# def country(message,update):
#     update_by_param(message.chat.id, 'COUNTRY', message.text)
#     q_citi(message,update)
#
# def mobil(message,update):
#     update=is_updated(message,'Mobilization status')
#     bot.send_message(message.chat.id, ua_msg_mobilizade, reply_markup=mobilizade)
#     bot.register_next_step_handler(message, mobil1,update)
#
# def mobil1(message,update):
#     if message.text == 'Back':
#         location(message,update)
#     update_by_param(message.chat.id, 'MOBILIZATE', message.text)
#     if  message.text == 'The Armed Forces of Ukraine':
#         q_mobil_army(message,update)
#     if message.text == 'Territorial Defense':
#         q_mobil_ter(message,update)
#     if message.text == 'No':
#         if not update:
#             q_can_work(message,update)
#         else:
#             bot.send_message(message.chat.id, "Information has been seccesfully updated")
#             output(message.chat.id)
#             return
#
# def mobilized_data(message,update):
#     update_by_param(message.chat.id, 'MOBILIZATE_DATE', message.text)
#     bot.send_message(message.chat.id, "Слава Україні!")
#
# def mobilized_data_t(message,update):
#     update_by_param(message.chat.id, 'MOBILIZATE_DATE', message.text)
#     if not update:
#         q_can_work(message,update)
#     else:
#         bot.send_message(message.chat.id, "Information has been seccesfully updated")
#         output(message.chat.id)
#         return
#
# def can_work(message,update):
#     if message.text == 'Back':
#         mobil(message,update)
#     if message.text == 'Yes':
#         update_by_param(message.chat.id, 'CAN_WORK', True)
#         if not update:
#             q_productivity(message,update)
#         else:
#             bot.send_message(message.chat.id, "Information has been seccesfully updated")
#             output(message.chat.id)
#             return
#     elif message.text == 'No':
#         update_by_param(message.chat.id, 'CAN_WORK', False)
#         update_by_param(message.chat.id, 'NEED_RESOURCES', False)
#         update_by_param(message.chat.id, 'NEED_EQUIPMENT', False)
#         if get_by_params(message.chat.id, "MOBILIZATE") == 'Territorial Defense':
#             bot.send_message(message.chat.id, "Слава Україні!")
#         else:
#             q_can_work_reason(message,update)
#
# # def productivity_update(message):
# #     update_by_param(message.chat.id, 'PRODUCTIVITY', message.text)
# #     bot.send_message(message.chat.id, "Productivity updated seccesfully")
#
# def productivity(message,update):
#     if message.text == 'Back':
#         q_can_work(message,update)
#     update_by_param(message.chat.id, 'PRODUCTIVITY', message.text)
#     if message.text == '100%':
#         if not update:
#             q_plan_relocate(message,update)
#         else:
#             bot.send_message(message.chat.id, "Information has been seccesfully updated")
#             output(message.chat.id)
#             return
#     elif message.text == '0%' or message.text == '25%' or message.text == '50%'  or message.text == '75%':
#         q_difficulties(message,update)
#
# def reason(message,update):
#     update_by_param(message.chat.id, 'CAN_WORK_REASON', message.text)
#     if not update:
#         q_plan_relocate(message,update)
#     else:
#         bot.send_message(message.chat.id, "Information has been seccesfully updated")
#         output(message.chat.id)
#         return
#
# def difficulties(message,update):
#     update_by_param(message.chat.id, 'PRODUCTIVITY_DIFFICULTIES', message.text)
#     if not update:
#         q_plan_relocate(message,update)
#     else:
#         bot.send_message(message.chat.id, "Information has been seccesfully updated")
#         output(message.chat.id)
#         return
#
# def plan_relocate(message,update):
#     if message.text == 'Back':
#         q_can_work(message,update)
#     if message.text == 'Yes':
#         update_by_param(message.chat.id, 'PLAN_RELOCATE', True)
#         q_plan_relocate_info(message,update)
#     elif message.text == 'No':
#         update_by_param(message.chat.id, 'PLAN_RELOCATE', False)
#         update_by_param(message.chat.id, 'PLAN_RELOCATE_INFO', 'plan_relocate_info')
#         q_relocate_out(message,update)
#
# def plan_relocate_info(message,update):
#     update_by_param(message.chat.id, 'PLAN_RELOCATE_INFO', message.text)
#     q_relocate_out(message,update)
#
# def relocate_out(message,update):
#     if message.text == 'Back':
#         q_plan_relocate(message,update)
#     if message.text == 'Yes':
#         update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE', True)
#         q_relocate_out_info(message,update)
#     elif message.text == 'No':
#         update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE', False)
#         update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE_INFO', 'none')
#         if not update:
#             q_need_some(message,update)
#         else:
#             bot.send_message(message.chat.id, "Information has been seccesfully updated")
#             output(message.chat.id)
#             return
#
# def relocate_out_info(message,update):
#     update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE_INFO', message.text)
#     if not update:
#         q_need_some(message,update)
#     else:
#         bot.send_message(message.chat.id, "Information has been seccesfully updated")
#         output(message.chat.id)
#         return
#
# def need_some(message,update):
#     if message.text == 'Resources':
#         update_by_param(message.chat.id, 'NEED_RESOURCES', True)
#         bot.send_message(message.chat.id, ua_msg_need_resources)
#         bot.register_next_step_handler(message, q_resources,update)
#     if message.text == 'Equipment':
#         update_by_param(message.chat.id, 'NEED_EQUIPMENT', True)
#         bot.send_message(message.chat.id, ua_msg_need_equipment)
#         bot.register_next_step_handler(message, q_equipment,update)
#     if message.text == 'Supplies\n(Food, water, medical)':
#         update_by_param(message.chat.id, 'NEEDEAT', True)
#         bot.send_message(message.chat.id, ua_msg_need_eat)
#         bot.register_next_step_handler(message, q_needeat,update)
#     # if message.text == 'Medical':
#     #     update_by_param(message.chat.id, 'NEEDMED', True)
#     #     bot.send_message(message.chat.id, ua_msg_need_med)
#     #     bot.register_next_step_handler(message, q_needmed,update)
#     # if message.text == 'Water':
#     #     update_by_param(message.chat.id, 'NEEDWATER', True)
#     #     bot.send_message(message.chat.id, ua_msg_need_water)
#     #     bot.register_next_step_handler(message, q_needwater,update)
#     if message.text == 'Nothing':
#         if not update:
#             q_additional(message)
#         else:
#             bot.send_message(message.chat.id, "Information has been seccesfully updated")
#             output(message.chat.id)
#             return
#     if message.text == 'Back':
#         q_relocate_out(message,update)
#
#
# def additional(message):
#     if message.text == 'Back':
#         q_need_some(message,update)
#     if message.text == 'Yes':
#         q_additional_info(message)
#     elif message.text == 'No':
#         finish_q(message)
#
# def finish_q(message):
#     if message.text != 'No':
#         update_by_param(message.chat.id, 'NEEDHELP_INFO', message.text)
#     bot.send_message(message.chat.id, ua_msg_finish_q)
#     update_by_param(message.chat.id, 'LAST_DATE', int(time.time()))
#     output(message.chat.id)

def finish_reg(message):
    update_by_param(message.chat.id, 'ISREGISTRED', True)
    bot.send_message(message.chat.id, ua_msg_finish_reg)
    info=get_all_params(message.chat.id)
    name=info[0][3].replace("@globallogic.com", "")
    name=name.replace(".", "_")
    # name=get_name(info[0][3])
    msg="&#127381 <b>{}</b>\n<b>Емейл:</b> {}\n\n#{}".format(info[0][2],info[0][3],name)
    bot.send_message(group_good, msg, parse_mode='html')
    poll(message,update,info[0][3])
    insert_in_sheet(info[0][3])

def finish_sos(message):
    bot.send_message(message.chat.id, ua_msg_finish_sos)
    info=get_all_params(message.chat.id)
    mail=info[0][3].replace("@globallogic.com", "")
    mail=mail.replace(".", "_")
    msg="&#127384 {}\n\n{}\n#{}".format(info[0][10],message.text, mail)
    bot.send_message(group, msg, parse_mode='html')

# def output(chatid):
#     info=get_all_params(chatid)
#     msg="&#9989 {}\n<b>Місце розташування:</b> {}\n".format(info[0][2],info[0][9])
#     mail=info[0][3].replace("@globallogic.com", "")
#     mail=mail.replace(".", "_")
#     all_good=True
#     if info[0][15] != "No":
#         all_good=False
#         msg+="&#9888 <b>Мобілізація:</b> {}\n".format(info[0][15])
#     if info[0][21]:
#         all_good=False
#         msg+="&#9888 <b>Потрібне обладнання:</b> {}\n".format(info[0][22])
#     if info[0][23]:
#         all_good=False
#         msg+="&#9888 <b>Потрібні ресурси:</b> {}\n".format(info[0][24])
#     if info[0][28]:
#         all_good=False
#         msg+="&#9888 <b>Need Supplies:</b> {}\n".format(info[0][29])
#     if info[0][11]:
#         all_good=False
#         msg+="&#9888 <b>Готовий/ва до релокації в безпечніше місце</b>\n"
#         if info[0][13]:
#             all_good=False
#             msg+="&#9888 <b>Може виїхати у зв'язку з </b> {}\n".format(relocate(chatid))
#     if not info[0][17]:
#         all_good=False
#         msg+="&#9888 <b>Не може працювати:{}</b>\n".format(info[0][18])
#     else:
#         if info[0][19] == 'productivity%':
#             msg+="&#128187 <b>Продуктивність:</b> 0%\n"
#         else:
#             msg+="&#128187 <b>Продуктивність:</b> {}\n".format(info[0][19])
#             if info[0][19] != '100%':
#                 all_good=False
#                 msg+="&#9888 <b>Труднощі:</b> {}\n".format(info[0][20])
#     if info[0][32] != 'needhelp_info':
#         all_good=False
#         msg+="&#9888 <b>Додаткова інформація:</b> {}".format(info[0][32])
#     msg+="\n#{}".format(mail)
#     if all_good:
#         bot.send_message(group_good, msg, parse_mode='html')
#     else:
#         bot.send_message(group, msg, parse_mode='html')
#     update_sheet(chatid)

bot.polling()
