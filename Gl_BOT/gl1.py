import   telebot
from lib import *
from mail import *
import re
from telebot import types
import sched, time
from scheduler import *
from sheet import *

exec(open('ua_len.py').read())
print(".-------------------------------------------------.")
print("| GlobalLogicbot                                  |")
print("| Author: Pavlo Mikush                            |")
print("| Github                                          |")
print("._________________________________________________.")

TELEGRAMBOTID = "5202517194:AAHkUwExe08QDb1coSmkm0auJpD5F8rsw3A"
bot           = telebot.TeleBot(TELEGRAM_BOT_ID)
group         = -725469696
group_good    = -760065603
admins        = [391827007]
city=['Lviv', 'Kyiv', 'Kharkiv']

create_table()
print(select_all())

nums          = types.ReplyKeyboardMarkup(row_width=9, resize_keyboard=True, one_time_keyboard=True)
YesNo         = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
Regions       = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
Countries     = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True, one_time_keyboard=True)
percent       = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
mobilizade    = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True, one_time_keyboard=True)
relocate_info = types.ReplyKeyboardMarkup(row_width=7, resize_keyboard=True, one_time_keyboard=True)
need_some_k   = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
topic         = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)

One           = types.KeyboardButton(text='1')
Two           = types.KeyboardButton(text='2')
Three         = types.KeyboardButton(text='3')
Four          = types.KeyboardButton(text='4')
Five          = types.KeyboardButton(text='5')
Six           = types.KeyboardButton(text='6')
Seven         = types.KeyboardButton(text='7')
Eight         = types.KeyboardButton(text='8')
Nine          = types.KeyboardButton(text='9')
Back          = types.KeyboardButton(text='Back')

Yes           = types.KeyboardButton(text='Yes')
No            = types.KeyboardButton(text='No')
Back          = types.KeyboardButton(text='Back')

Kiyv_r        = types.KeyboardButton(text='Kyiv')
Kharkiv_r     = types.KeyboardButton(text='Kharkiv')
Lviv_r        = types.KeyboardButton(text='Lviv')
IF_r          = types.KeyboardButton(text='Ivano-Frankivsk')
Zakarpattia_r = types.KeyboardButton(text='Zakarpattia')
Ternopil_r    = types.KeyboardButton(text='Ternopil')
Poltava_r     = types.KeyboardButton(text='Poltava')
Dnipro_r      = types.KeyboardButton(text='Dnipro')
Rivne_r       = types.KeyboardButton(text='Rivne')

Out_of_Ukraine= types.KeyboardButton(text='Out of Ukraine')

Ukraine       = types.KeyboardButton(text='Ukraine')
Poland        = types.KeyboardButton(text='Poland')
Germany       = types.KeyboardButton(text='Germany')
Italy         = types.KeyboardButton(text='Italy')

quater        = types.KeyboardButton(text='25%')
half          = types.KeyboardButton(text='50%')
seventy_five  = types.KeyboardButton(text='75%')
full          = types.KeyboardButton(text='100%')
Back_         = types.KeyboardButton(text='Back')

yes_TrO       = types.KeyboardButton(text='Territorial Defense')
yes_army      = types.KeyboardButton(text='The Armed Forces of Ukraine')
no            = types.KeyboardButton(text='No')

Back          = types.KeyboardButton(text='Back')

One           = types.KeyboardButton(text='1')
Two           = types.KeyboardButton(text='2')
Three         = types.KeyboardButton(text='3')
Four          = types.KeyboardButton(text='4')
Five          = types.KeyboardButton(text='5')
Six           = types.KeyboardButton(text='6')
Seven         = types.KeyboardButton(text='7')
Female        = types.KeyboardButton(text='Female')
Back          = types.KeyboardButton(text='Back')

Resources     = types.KeyboardButton(text='Resources')
Equipment     = types.KeyboardButton(text='Equipment')
Supplies      = types.KeyboardButton(text='Supplies\n(Food, water, medical)')
# Medical       = types.KeyboardButton(text='Medical')
# Water         = types.KeyboardButton(text='Water')
Nothing       = types.KeyboardButton(text='Nothing')

Location      = types.KeyboardButton(text='Location')
Mobilizate    = types.KeyboardButton(text='Mobilization status')
Can_work      = types.KeyboardButton(text='Possibility to work')
Productivity  = types.KeyboardButton(text='Productivity')
# Safe_mark     = types.KeyboardButton(text='Safe mark')
Relocate      = types.KeyboardButton(text='Relocation')
Resources     = types.KeyboardButton(text='Resources')


nums.add(One, Two, Three, Four, Five, Six, Seven, Eight, Nine, Back)
YesNo.add(Yes,No, Back)
# Cities.add(Kiyv,Kharkiv,Lviv)
Regions.add(Kiyv_r,Kharkiv_r,Lviv_r,Zakarpattia_r,IF_r,Ternopil_r,Poltava_r,Dnipro_r,Rivne_r,Out_of_Ukraine)
percent.add(quater, half, seventy_five, full, Back_)
mobilizade.add(yes_TrO, yes_army, no, Back)
Countries.add(Poland,Germany,Italy)
relocate_info.add(One, Two, Three, Four, Five, Six, Seven,Female, Back)
need_some_k.add(Resources,Equipment,Supplies,Nothing)
topic.add(Location,Mobilizate,Can_work,Productivity,Relocate,Resources,Nothing)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if check_user(message.chat.id):
        bot.send_message(message.chat.id, ua_msg_welcome)
    else:
        bot.send_message(message.chat.id, ua_msg_start)
        bot.register_next_step_handler(message, register)

@bot.message_handler(commands=['behalf_colege'])
def behalf(message):
    bot.send_message(message.chat.id, "I answer on behalf of my collegue")
    bot.register_next_step_handler(message, behalf1)

def behalf1(message):
    update_by_param(message.chat.id, 'NAME_SURNAME', message.text)
    location(message)

@bot.message_handler(commands=['registration'])
def check_reg(message):
    if check_user(message.chat.id):
        bot.send_message(message.chat.id, ua_msg_already_registered)
    else:
        bot.send_message(message.chat.id, ua_msg_start)
        bot.register_next_step_handler(message, register)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, ua_msg_help)

@bot.message_handler(commands=['ping_all'])
def ping(message):
    if message.chat.id in admins:
        question_zero()
    else:
        bot.send_message(message.chat.id, "Command is not permissed")

@bot.message_handler(commands=['update_poll'])
def update_poll(message):
    bot.send_message(message.chat.id, "Please, chose section for update", reply_markup=topic)
    bot.register_next_step_handler(message, update_param)

# def update_param(message):
#     if message.text == 'Location':
#         location(message)
#     if message.text == 'Mobilization status':
#         mobil(message)
#     if message.text == 'Possibility to work':
#         q_can_work(message)
#     if message.text == 'Productivity':
#         q_productivity(message)
#     if message.text == 'Relocation':
#         q_plan_relocate(message)
#     if message.text == 'Resources':
#         q_need_some(message)
#     if message.text == 'Nothing':
#         bot.send_message(message.chat.id, "Thanks")
#         return

@bot.message_handler(commands=['poll'])
def send_poll(message):
    refresh(message.chat.id)
    location(message)


@bot.message_handler(commands=['sos'])
def send_help(message):
    if check_user(message.chat.id):
        bot.send_message(message.chat.id, 'Please, indicate your current city location. If your city is not on the list, write it down ', reply_markup=Regions)
        bot.register_next_step_handler(message, sos1)
    else:
        bot.send_message(message.chat.id, ua_msg_unregistered)

def sos1(message):
    bot.send_message(message.chat.id, ua_msg_problem_description)
    bot.register_next_step_handler(message, finish_sos)

@bot.message_handler(func=lambda m: True)
def text(message):
    info=get_all_params(message.chat.id)
    if check_user(message.chat.id):
        if message.text == 'r':
            reg_location(message)
        if message.text == 'Start poll':
            refresh(message.chat.id)
            location(message)
        if message.text == 'Update poll':
            update_poll(message)
        if message.text == 'Declared data is actual':
            bot.send_message(message.chat.id, "Thanks, data is actualized")
            # update_by_param(message.chat.id, 'ISACTUAL', True)
            output(message.chat.id)
    else:
        bot.send_message(message.chat.id, ua_msg_unregistered)

def register(message):
    regex = r'\b[A-Za-z0-9._%+-]+@globallogic.com\b'
    if(re.fullmatch(regex, message.text)):
        mail=message.text
        code=gen_code()
        send_code(mail,code)
        bot.send_message(message.chat.id, ua_msg_verification_code)
        bot.register_next_step_handler(message, ath, code, mail)
    else:
        bot.send_message(message.chat.id, ua_msg_error_email)
        bot.register_next_step_handler(message, register)

# def ath(message,code, email):
#     code=code.replace(" ", "")
#     if message.text == code:
#         update_by_param(message.chat.id, 'MAIL', email)
#         update_by_param(message.chat.id, 'ISVERIFIED', True)
#         name_surname(message)
#         finish_reg(message)
#     else:
#         bot.send_message(message.chat.id, ua_msg_error_verification)
#
# def name_surname(message):
#     info=get_all_params(message.chat.id)
#     mail=info[0][3].replace("@globallogic.com", "")
#     mail=mail.replace(".", " ")
#     name_surname=mail.title()
#     update_by_param(message.chat.id, 'NAME_SURNAME', name_surname)
#
# # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# # refresh(message.chat.id)
# # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# def location(message):
#     update=is_updated(message,'Location')
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
# def q_can_work(message):
#     update=is_updated(message,'Possibility to work')
#     bot.send_message(message.chat.id, ua_q_can_work, reply_markup=YesNo)
#     bot.register_next_step_handler(message, can_work,update)
#
# def q_productivity(message):
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
# def q_plan_relocate(message):
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
# def q_need_some(message):
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
#                 mobil(message)
#             else:
#                 bot.send_message(message.chat.id, "Information has been seccesfully updated")
#                 output(message.chat.id)
#                 return
#         if message.text == 'No':
#             update_by_param(message.chat.id, 'IS_LOCATION_REGION_CENTER', False)
#             q_citi(message,update)
#     else:
#         location1(message,update)
#
# def city(message,update):
#     update_by_param(message.chat.id, 'LOCATION_CITY', message.text)
#     if not update:
#         mobil(message)
#     else:
#         bot.send_message(message.chat.id, "Information has been seccesfully updated")
#         output(message.chat.id)
#         return
#
# def country(message,update):
#     update_by_param(message.chat.id, 'COUNTRY', message.text)
#     q_citi(message,update)
#
# def mobil(message):
#     update=is_updated(message,'Mobilization status')
#     bot.send_message(message.chat.id, ua_msg_mobilizade, reply_markup=mobilizade)
#     bot.register_next_step_handler(message, mobil1,update)
#
# def mobil1(message,update):
#     if message.text == 'Back':
#         location(message)
#     update_by_param(message.chat.id, 'MOBILIZATE', message.text)
#     if  message.text == 'The Armed Forces of Ukraine':
#         q_mobil_army(message,update)
#     if message.text == 'Territorial Defense':
#         q_mobil_ter(message,update)
#     if message.text == 'No':
#         if not update:
#             q_can_work(message)
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
#         q_can_work(message)
#     else:
#         bot.send_message(message.chat.id, "Information has been seccesfully updated")
#         output(message.chat.id)
#         return
#
# def can_work(message,update):
#     if message.text == 'Back':
#         mobil(message)
#     if message.text == 'Yes':
#         update_by_param(message.chat.id, 'CAN_WORK', True)
#         if not update:
#             q_productivity(message)
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
#         q_can_work(message)
#     update_by_param(message.chat.id, 'PRODUCTIVITY', message.text)
#     if message.text == '100%':
#         if not update:
#             q_plan_relocate(message)
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
#         q_plan_relocate(message)
#     else:
#         bot.send_message(message.chat.id, "Information has been seccesfully updated")
#         output(message.chat.id)
#         return
#
# def difficulties(message,update):
#     update_by_param(message.chat.id, 'PRODUCTIVITY_DIFFICULTIES', message.text)
#     if not update:
#         q_plan_relocate(message)
#     else:
#         bot.send_message(message.chat.id, "Information has been seccesfully updated")
#         output(message.chat.id)
#         return
#
# def plan_relocate(message,update):
#     if message.text == 'Back':
#         q_can_work(message)
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
#         plan_relocate(message)
#     if message.text == 'Yes':
#         update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE', True)
#         q_relocate_out_info(message,update)
#     elif message.text == 'No':
#         update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE', False)
#         update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE_INFO', 'none')
#         if not update:
#             q_need_some(message)
#         else:
#             bot.send_message(message.chat.id, "Information has been seccesfully updated")
#             output(message.chat.id)
#             return
#
# def relocate_out_info(message,update):
#     update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE_INFO', message.text)
#     if not update:
#         q_need_some(message)
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
#
# def additional(message):
#     if message.text == 'Back':
#         q_need_some(message)
#     if message.text == 'Yes':
#         q_additional_info(message)
#     elif message.text == 'No':
#         finish_q(message)
#
# def finish_q(message):
#     if message.text != 'No':
#         update_by_param(message.chat.id, 'NEEDHELP_INFO', message.text)
#     bot.send_message(message.chat.id, ua_msg_finish_q)
#     output(message.chat.id)
#
# def finish_reg(message):
#     update_by_param(message.chat.id, 'ISREGISTRED', True)
#     bot.send_message(message.chat.id, ua_msg_finish_reg)
#     info=get_all_params(message.chat.id)
#     mail=info[0][3].replace("@globallogic.com", "")
#     mail=mail.replace(".", "_")
#     msg="&#127381 <b>{}</b>\n<b>Емейл:</b> {}\n\n#{}".format(info[0][2],info[0][3],mail)
#     bot.send_message(group_good, msg, parse_mode='html')
#     location(message)
#     insert_in_sheet(message.chat.id)
#
# def finish_sos(message):
#     bot.send_message(message.chat.id, ua_msg_finish_sos)
#     info=get_all_params(message.chat.id)
#     mail=info[0][3].replace("@globallogic.com", "")
#     mail=mail.replace(".", "_")
#     msg="&#127384 {}\n\n{}\n#{}".format(info[0][10],message.text, mail)
#     bot.send_message(group, msg, parse_mode='html')
#
# def relocate(chatid):
#     # relocate_info =
#     # get_by_params(chat_id, param):
#     if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '1':
#         relocate_info = "certificate of recruitment deferral and message on enrollment to"
#     if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '2':
#         relocate_info = "special military registration conclusion of military and medical commission on ineligibility"
#     if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '3':
#         relocate_info = "maintain three or more children aged to 18 y.o"
#     if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '4':
#         relocate_info = "raise alone a child (children) aged to 18 y.o."
#     if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '5':
#         relocate_info = "adopter/guardian"
#     if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '6':
#         relocate_info = "immediate family members perished or disappeared during the antiterrorist operation"
#     if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '7':
#         relocate_info = "the reason is reported to manager"
#     if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == 'Female':
#         relocate_info = "Female"
#     return relocate_info
#
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
#     if info[0][26]:
#         all_good=False
#         msg+="&#9888 <b>Потрібні медикаменти:</b> {}\n".format(info[0][27])
#     if info[0][28]:
#         all_good=False
#         msg+="&#9888 <b>Потрібна їжа:</b> {}\n".format(info[0][29])
#     if info[0][30]:
#         all_good=False
#         msg+="&#9888 <b>Потрібна вода:</b> {}\n".format(info[0][31])
#     if info[0][11]:
#         all_good=False
#         msg+="&#9888 <b>Готовий/ва до релокації в безпечніше місце</b>\n"
#     if info[0][13]:
#         all_good=False
#         msg+="&#9888 <b>Може виїхати у зв'язку з </b> {}\n".format(relocate(chatid))
#     if not info[0][17]:
#         all_good=False
#         msg+="&#9888 <b>Не може працювати</b>\n"
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
#
# def is_updated(message,param):
#     if message.text == param:
#         update=True
#     else:
#         update=False
#     return update

bot.polling()
