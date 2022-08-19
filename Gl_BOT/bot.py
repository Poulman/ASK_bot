import   telebot
from lib import *
from mail import *
import re
from telebot import types
import sched, time

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
city=['Lviv', 'Kyiv', 'Kharkiv']

create_table()
# print(select_all())

nums          = types.ReplyKeyboardMarkup(row_width=9, resize_keyboard=True, one_time_keyboard=True)
YesNo         = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
Regions       = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
Countries     = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True, one_time_keyboard=True)
percent       = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
mobilizade    = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True, one_time_keyboard=True)
relocate_info = types.ReplyKeyboardMarkup(row_width=7, resize_keyboard=True, one_time_keyboard=True)

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

nums.add(One, Two, Three, Four, Five, Six, Seven, Eight, Nine, Back)
YesNo.add(Yes,No, Back)
# Cities.add(Kiyv,Kharkiv,Lviv)
Regions.add(Kiyv_r,Kharkiv_r,Lviv_r,Zakarpattia_r,IF_r,Ternopil_r,Poltava_r,Dnipro_r,Rivne_r,Out_of_Ukraine)
percent.add(quater, half, seventy_five, full, Back_)
mobilizade.add(yes_TrO, yes_army, no, Back)
Countries.add(Poland,Germany,Italy)
relocate_info.add(One, Two, Three, Four, Five, Six, Seven,Female, Back)

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

def ath(message,code, email):
    code=code.replace(" ", "")
    if message.text == code:
        update_by_param(message.chat.id, 'MAIL', email)
        update_by_param(message.chat.id, 'ISVERIFIED', True)
        name_surname(message)
        finish_reg(message)
    else:
        bot.send_message(message.chat.id, ua_msg_error_verification)

def name_surname(message):
    info=get_all_params(message.chat.id)
    mail=info[0][3].replace("@globallogic.com", "")
    mail=mail.replace(".", " ")
    name_surname=mail.title()
    update_by_param(message.chat.id, 'NAME_SURNAME', name_surname)

# def sub_location(message):
#     update_by_param(message.chat.id, 'LOCATION_REGION', message.text)

def location(message):
    refresh(message.chat.id)
    bot.send_message(message.chat.id, 'Please, indicate your current regional center location. If your regional center is not on the list, write it down (ONLY regional center or the region).', reply_markup=Regions)
    bot.register_next_step_handler(message, sub_location)
    # specify_loc(message)

# def sub_location(message):
#     update_by_param(message.chat.id, 'LOCATION_REGION', message.text)

def location1(message):
    update_by_param(message.chat.id, 'LOCATION_REGION', message.text)
    if message.text != 'Out of Ukraine':
        update_by_param(message.chat.id, 'COUNTRY', 'Ukraine')
        bot.send_message(message.chat.id, 'Please, specify do you locate in the regional center?', reply_markup=YesNo)
        bot.register_next_step_handler(message, question1)
    else:
        bot.send_message(message.chat.id, 'Please, specify your country. Is not on the list, write it down', reply_markup=Countries)
        bot.register_next_step_handler(message, country)

def question1(message):
    if message.text != 'Back':
        if message.text == 'Yes':
            update_by_param(message.chat.id, 'LOCATION_CITY', get_by_params(message.chat.id, 'LOCATION_REGION'))
            update_by_param(message.chat.id, 'IS_LOCATION_REGION_CENTER', True)
            question_mobil(message)
            # bot.send_message(message.chat.id, ua_msg_mobilizade, reply_markup=mobilizade)
            # bot.register_next_step_handler(message, question2)
        if message.text == 'No':
            update_by_param(message.chat.id, 'IS_LOCATION_REGION_CENTER', False)
            bot.send_message(message.chat.id, 'Please, specify your location.')
            bot.register_next_step_handler(message, city)
    else:
        bot.send_message(message.chat.id, 'Please, indicate your current regional center location. If your regional center is not on the list, write it down (ONLY regional center or the region).', reply_markup=Regions)
        bot.register_next_step_handler(message, location)

def city(message):
    update_by_param(message.chat.id, 'LOCATION_CITY', message.text)
    # bot.send_message(message.chat.id, ua_msg_mobilizade, reply_markup=mobilizade)
    # bot.register_next_step_handler(message, question2)
    question_mobil(message)

def country(message):
    update_by_param(message.chat.id, 'COUNTRY', message.text)
    bot.send_message(message.chat.id, 'Please, specify your location.')
    bot.register_next_step_handler(message, city)

def question_mobil(message):
    bot.send_message(message.chat.id, ua_msg_mobilizade, reply_markup=mobilizade)
    bot.register_next_step_handler(message, question2)

def question2(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, 'Please, indicate your current regional center location. If your regional center is not on the list, write it down (ONLY regional center or the region).', reply_markup=Regions)
        bot.register_next_step_handler(message, specify_loc)
    update_by_param(message.chat.id, 'MOBILIZATE', message.text)
    if  message.text == 'The Armed Forces of Ukraine':
        bot.send_message(message.chat.id, "Since when?")
        bot.register_next_step_handler(message, mobilized_data)
    if message.text == 'Territorial Defense':
        bot.send_message(message.chat.id, "Since when?")
        bot.register_next_step_handler(message, mobilized_data_t)
    if message.text == 'No':
        bot.send_message(message.chat.id, ua_q_can_work, reply_markup=YesNo)
        bot.register_next_step_handler(message, question3)

def mobilized_data(message):
    update_by_param(message.chat.id, 'MOBILIZATE_DATE', message.text)
    bot.send_message(message.chat.id, "Перемога за нами!")

def mobilized_data_t(message):
    update_by_param(message.chat.id, 'MOBILIZATE_DATE', message.text)
    bot.send_message(message.chat.id, ua_q_can_work, reply_markup=YesNo)
    bot.register_next_step_handler(message, question3)


def question3(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_msg_mobilizade, reply_markup=mobilizade)
        bot.register_next_step_handler(message, question2)
    if message.text == 'Yes':
        update_by_param(message.chat.id, 'CAN_WORK', True)
        bot.send_message(message.chat.id, ua_q_productivity, reply_markup=percent)
        bot.register_next_step_handler(message, question4)
    elif message.text == 'No':
        update_by_param(message.chat.id, 'CAN_WORK', False)
        update_by_param(message.chat.id, 'NEED_RESOURCES', False)
        update_by_param(message.chat.id, 'NEED_EQUIPMENT', False)
        if get_by_params(message.chat.id, "MOBILIZATE") == 'Territorial Defense':
            bot.send_message(message.chat.id, "Перемога за нами!")
        else:
            bot.send_message(message.chat.id, ua_msg_reason)
            bot.register_next_step_handler(message, reason)

def question4(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_q_can_work, reply_markup=YesNo)
        bot.register_next_step_handler(message, question3)
    update_by_param(message.chat.id, 'PRODUCTIVITY', message.text)
    if message.text == '100%':
        bot.send_message(message.chat.id, ua_q_all_need, reply_markup=YesNo)
        bot.register_next_step_handler(message, question5)
    elif message.text == '0%' or message.text == '25%' or message.text == '50%'  or message.text == '75%':
        bot.send_message(message.chat.id, 'Please, let us know what makes difficulties?')
        bot.register_next_step_handler(message, difficulties)

def reason(message):
    update_by_param(message.chat.id, 'CAN_WORK_REASON', message.text)
    bot.send_message(message.chat.id, ua_q_location, reply_markup=YesNo)
    bot.register_next_step_handler(message, question9)

def difficulties(message):
    update_by_param(message.chat.id, 'PRODUCTIVITY_DIFFICULTIES', message.text)
    bot.send_message(message.chat.id, ua_q_all_need, reply_markup=YesNo)
    bot.register_next_step_handler(message, question5)

def question5(message):
        if message.text == 'Back':
            bot.send_message(message.chat.id, ua_q_productivity, reply_markup=percent)
            bot.register_next_step_handler(message, question4)
        if message.text == 'No':
            update_by_param(message.chat.id, 'NEED_EQUIPMENT', True)
            bot.send_message(message.chat.id, ua_msg_need_all)
            bot.register_next_step_handler(message, question6)
        elif message.text == 'Yes':
            update_by_param(message.chat.id, 'NEED_EQUIPMENT', False)
            question6(message)

def question6(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_q_all_need, reply_markup=YesNo)
        bot.register_next_step_handler(message, question5)
    else:
        update_by_param(message.chat.id, 'NEED_EQUIPMENT_INFO', message.text)
        bot.send_message(message.chat.id, ua_q_need_resources, reply_markup=YesNo)
        bot.register_next_step_handler(message, question7)

def question7(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_q_all_need, reply_markup=YesNo)
        bot.register_next_step_handler(message, question5)
        # question4(message)
    if message.text == 'No':
        update_by_param(message.chat.id, 'NEED_RESOURCES', True)
        bot.send_message(message.chat.id, ua_msg_need_resources)
        bot.register_next_step_handler(message, question8)
    elif message.text == 'Yes':
        update_by_param(message.chat.id, 'NEED_RESOURCES', False)
        update_by_param(message.chat.id, 'NEED_RESOURCES_INFO', 'none')
        question8(message)

def question8(message):
    if message.text != 'Yes':
        update_by_param(message.chat.id, 'NEED_RESOURCES_INFO', message.text)
    bot.send_message(message.chat.id, ua_q_location, reply_markup=YesNo)
    bot.register_next_step_handler(message, question9)

def question9(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_q_need_resources, reply_markup=YesNo)
        bot.register_next_step_handler(message, question7)
    if message.text == 'Yes':
        update_by_param(message.chat.id, 'PLAN_RELOCATE', True)
        bot.send_message(message.chat.id, ua_msg_location)
        bot.register_next_step_handler(message, question10)
    elif message.text == 'No':
        update_by_param(message.chat.id, 'PLAN_RELOCATE', False)
        update_by_param(message.chat.id, 'PLAN_RELOCATE_INFO', 'plan_relocate_info')
        question10(message)

def question10(message):
    if message.text != 'No':
        update_by_param(message.chat.id, 'PLAN_RELOCATE_INFO', message.text)
        # if get_by_params(message.chat.id, 'COUNTRY') == 'Ukraine':
            # print(YesNo)
        bot.send_message(message.chat.id, ua_q_relocate, reply_markup=YesNo)
        bot.register_next_step_handler(message, question11)
    else:
        bot.send_message(message.chat.id, ua_msg_safe, reply_markup=nums)
        bot.register_next_step_handler(message, question13)

def question11(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_q_location, reply_markup=YesNo)
        bot.register_next_step_handler(message, question9)
    if message.text == 'Yes':
        update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE', True)
        # print(relocate)
        bot.send_message(message.chat.id, ua_msg_relocate, reply_markup=relocate_info)
        bot.register_next_step_handler(message, question12)
    elif message.text == 'No':
        update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE', False)
        update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE_INFO', 'none')
        question12(message)

def question12(message):
    if message.text != 'Yes':
        update_by_param(message.chat.id, 'READY_TO_RELOCATE_OUTSIDE_INFO', message.text)
    bot.send_message(message.chat.id, ua_msg_safe, reply_markup=nums)
    bot.register_next_step_handler(message, question13)

def question13(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_q_relocate, reply_markup=YesNo)
        bot.register_next_step_handler(message, question11)
    else:
        update_by_param(message.chat.id, 'SAFE_MARK', message.text)
        bot.send_message(message.chat.id, ua_q_need_med, reply_markup=YesNo)
        bot.register_next_step_handler(message, question14)

def question14(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_msg_safe, reply_markup=nums)
        bot.register_next_step_handler(message, question13)
    if message.text == 'No':
        update_by_param(message.chat.id, 'NEEDMED', True)
        bot.send_message(message.chat.id, ua_msg_need_med)
        bot.register_next_step_handler(message, question15)
    elif message.text == 'Yes':
        update_by_param(message.chat.id, 'NEEDMED', False)
        update_by_param(message.chat.id, 'NEEDMED_INFO', 'none')
        question15(message)

def question15(message):
    if message.text != 'Yes':
        update_by_param(message.chat.id, 'NEEDMED_INFO', message.text)
    bot.send_message(message.chat.id, ua_q_need_eat, reply_markup=YesNo)
    bot.register_next_step_handler(message, question16)

def question16(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_q_need_med, reply_markup=YesNo)
        bot.register_next_step_handler(message, question14)
    if message.text == 'No':
        update_by_param(message.chat.id, 'NEEDEAT', True)
        bot.send_message(message.chat.id, ua_msg_need_eat)
        bot.register_next_step_handler(message, question17)
    elif message.text == 'Yes':
        update_by_param(message.chat.id, 'NEEDEAT', False)
        update_by_param(message.chat.id, 'NEEDEAT_INFO', 'none')
        question17(message)

def question17(message):
    if message.text != 'Yes':
        update_by_param(message.chat.id, 'NEEDEAT_INFO', message.text)
    bot.send_message(message.chat.id, ua_q_need_water, reply_markup=YesNo)
    bot.register_next_step_handler(message, question18)

def question18(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_q_need_eat, reply_markup=YesNo)
        bot.register_next_step_handler(message, question16)
    if message.text == 'No':
        update_by_param(message.chat.id, 'NEEDWATER', True)
        bot.send_message(message.chat.id, ua_msg_need_water)
        bot.register_next_step_handler(message, question19)
    elif message.text == 'Yes':
        update_by_param(message.chat.id, 'NEEDWATER', False)
        update_by_param(message.chat.id, 'NEEDWATER_INFO', 'none')
        question19(message)

def question19(message):
    if message.text != 'Yes':
        update_by_param(message.chat.id, 'NEEDWATER_INFO', message.text)
    bot.send_message(message.chat.id, ua_q_more_help, reply_markup=YesNo)
    bot.register_next_step_handler(message, question20)

def question20(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, ua_q_need_water, reply_markup=YesNo)
        bot.register_next_step_handler(message, question18)
    if message.text == 'Yes':
        bot.send_message(message.chat.id, ua_msg_more_help)
        bot.register_next_step_handler(message, finish_q)
    elif message.text == 'No':
        finish_q(message)

def finish_q(message):
    if message.text != 'No':
        update_by_param(message.chat.id, 'NEEDHELP_INFO', message.text)
        # update_by_param(message.chat.id, 'ISACTUAL', True)
    bot.send_message(message.chat.id, ua_msg_finish_q)
    output(message.chat.id)

def finish_reg(message):
    update_by_param(message.chat.id, 'ISREGISTRED', True)
    bot.send_message(message.chat.id, ua_msg_finish_reg)
    info=get_all_params(message.chat.id)
    mail=info[0][3].replace("@globallogic.com", "")
    mail=mail.replace(".", "_")
    msg="&#127381 <b>{}</b>\n<b>Емейл:</b> {}\n\n#{}".format(info[0][2],info[0][3],mail)
    bot.send_message(group_good, msg, parse_mode='html')
    location(message)

def finish_sos(message):
    bot.send_message(message.chat.id, ua_msg_finish_sos)
    info=get_all_params(message.chat.id)
    mail=info[0][3].replace("@globallogic.com", "")
    mail=mail.replace(".", "_")
    msg="&#127384 {}\n\n{}\n#{}".format(info[0][10],message.text, mail)
    bot.send_message(group, msg, parse_mode='html')


def output(chatid):
    info=get_all_params(chatid)
    msg="&#9989 {}\n<b>Місце розташування:</b> {}\n".format(info[0][2],info[0][9])
    mail=info[0][3].replace("@globallogic.com", "")
    mail=mail.replace(".", "_")
    all_good=True
    if info[0][15] != "No":
        all_good=False
        msg+="&#9888 <b>Мобілізація:</b> {}\n".format(info[0][15])
    if info[0][21]:
        all_good=False
        msg+="&#9888 <b>Потрібне обладнання:</b> {}\n".format(info[0][22])
    if info[0][23]:
        all_good=False
        msg+="&#9888 <b>Потрібні ресурси:</b> {}\n".format(info[0][24])
    if info[0][26]:
        all_good=False
        msg+="&#9888 <b>Потрібні медикаменти:</b> {}\n".format(info[0][27])
    if info[0][28]:
        all_good=False
        msg+="&#9888 <b>Потрібна їжа:</b> {}\n".format(info[0][29])
    if info[0][30]:
        all_good=False
        msg+="&#9888 <b>Потрібна вода:</b> {}\n".format(info[0][31])
    if info[0][11]:
        all_good=False
        msg+="&#9888 <b>Готовий/ва до релокації в безпечніше місце</b>\n"
    if info[0][13]:
        all_good=False
        msg+="&#9888 <b>Може виїхати у зв'язку з </b> {}\n".format(relocate(chatid))
    if not info[0][17]:
        all_good=False
        msg+="&#9888 <b>Не може працювати</b>\n"
    else:
        msg+="&#128187 <b>Продуктивність:</b> {}\n".format(info[0][19])
        if info[0][19] != '100%':
            all_good=False
            msg+="&#9888 <b>Труднощі:</b> {}\n".format(info[0][20])
    if info[0][32] != 'needhelp_info':
        all_good=False
        msg+="&#9888 <b>Додаткова інформація:</b> {}".format(info[0][32])
    msg+="\n#{}".format(mail)
    if all_good:
        bot.send_message(group_good, msg, parse_mode='html')
    else:
        bot.send_message(group, msg, parse_mode='html')

def relocate(chatid):
    # relocate_info =
    # get_by_params(chat_id, param):
    if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '1':
        relocate_info = "certificate of recruitment deferral and message on enrollment to"
    if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '2':
        relocate_info = "special military registration conclusion of military and medical commission on ineligibility"
    if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '3':
        relocate_info = "maintain three or more children aged to 18 y.o"
    if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '4':
        relocate_info = "raise alone a child (children) aged to 18 y.o."
    if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '5':
        relocate_info = "adopter/guardian"
    if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '6':
        relocate_info = "immediate family members perished or disappeared during the antiterrorist operation"
    if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == '7':
        relocate_info = "the reason is reported to manager"
    if get_by_params(chatid, "READY_TO_RELOCATE_OUTSIDE_INFO") == 'Female':
        relocate_info = "Female"
    return relocate_info

bot.polling()
