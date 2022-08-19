import re
import telebot
import time
from database import *
from numpy import random
from mail import *
from sheet import *
from poll import *
# exec(open('vars.py').read())
exec(open('ua_len.py').read())



# group           = -725469696
# group_good      = -760065603
# admin_group     = -1001514147967
# groups          = [admin_group,group_good,group]

##############################################
#         CHECKERS
##############################################

def check_group(chatid):
    if chatid not in groups:
        return True
    else:
        bot.send_message(chatid, "Action is not permitted")
        return False

def check_mail(message):
    regex = r'\b[A-Za-z0-9._%+-]+@globallogic.com\b'
    if(re.fullmatch(regex, message.text)):
        return message.text
    else:
        bot.send_message(message.chat.id, ua_msg_error_email)
        bot.register_next_step_handler(message, register)

def check_user(chatid):
    if is_param_exis('CHATID',chatid):
        if get_by_params(chatid, 'ISVERIFIED'):
            return True
    else:
        # bot.send_message(message.chat.id, ua_msg_start)
        # bot.register_next_step_handler(message, register)
        date= int(time.time())
        insert_query(chatid, 'username', 'name_surname', 'mail', False, False, date, 'location_region', False, 'location_city', 'country', False, 'plan_relocate_info', False, 'ready_to_relocate_outside_info', 'mobilizate', 'mobilizate_date', False, 'can_work_reason', 'productivity', 'productivity_difficulties', False, 'need_equipment_info', False, 'needresources_info', 'safe_mark', False, 'needmed_info', False, 'neadsuplies_info', False, 'needwater_info', 'needhelp_info')

def register(message):
    mail=check_mail(message)
    if mail:
        code=gen_code()
        send_code(mail,code)
        bot.send_message(message.chat.id, ua_msg_verification_code)
        bot.register_next_step_handler(message, ath, code, mail)

def ath(message,code, mail):
    code=code.replace(" ", "")
    if message.text == code:
        update_by_param(message.chat.id, 'MAIL', mail)
        update_by_param(message.chat.id, 'ISVERIFIED', True)
        update_by_param(message.chat.id, 'NAME_SURNAME', get_name(mail))
        finish_reg(message)
    else:
        bot.send_message(message.chat.id, ua_msg_error_verification)

def finish_reg(message):
    bot.send_message(message.chat.id, ua_msg_finish_reg)
    mail=get_by_params(message.chat.id, 'MAIL')
    get_project(mail)
    info=get_all_params(message.chat.id)
    msg="&#127381 <b>{}</b>\n<b>Емейл:</b> {}\n\n#{}".format(info[0][2],info[0][3],get_hesh(info[0][3]))
    bot.send_message(group_good, msg, parse_mode='html')
    poll(message,update,info[0][3])
    insert_in_sheet(info[0][3])

def is_updated(message,param):
    if message.text == param:
        update=True
    else:
        update=False
    return update

# def mess_to_all(message):
#     users=list_users_id()
#     for user in users:
#         if user > 0:
#             if check_user(user):
#                 message=bot.send_message(user, message.text)

# def get_name(mail):
#     name=mail.replace("@globallogic.com", "")
#     name=name.replace(".", " ")
#     name=name.title()
#     return name
#
# def get_hesh(mail):
#      name=mail.replace("@globallogic.com", "")
#      name=name.replace(".", "_")
#      return name

# def get_project_group(project):
#     for projects in DSO,Carelink,Mobile:
#         if project in projects:
#             if projects == "DSO":
#                 return 0
#             elif projects == "Carelink":
#                 return 1
#             else:
#                 return 2

def gen_code():
    x=random.randint(9, size=(2, 3))
    a=' '
    for i in x:
        for j in i:
            a+=str(j)
        a+=' '
    return a

# def list_users_id():
#     cursor.execute("SELECT CHATID from employee")
#     column_names = [row[0] for row in cursor]
#     return                 column_names

# def relocate(mail):
#     relocate_info = ""
#     if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '1':
#         relocate_info = "certificate of recruitment deferral and message on enrollment to"
#     if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '2':
#         relocate_info = "special military registration conclusion of military and medical commission on ineligibility"
#     if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '3':
#         relocate_info = "maintain three or more children aged to 18 y.o"
#     if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '4':
#         relocate_info = "raise alone a child (children) aged to 18 y.o."
#     if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '5':
#         relocate_info = "adopter/guardian"
#     if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '6':
#         relocate_info = "immediate family members perished or disappeared during the antiterrorist operation"
#     if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '7':
#         relocate_info = "the reason is reported to manager"
#     if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == 'Female':
#         relocate_info = "Female"
#     return relocate_info
#
# def refresh(mail):
#     update_by_mail(mail, 'IS_LOCATION_REGION_CENTER',       False)
#     update_by_mail(mail, 'PLAN_RELOCATE',                   False)
#     update_by_mail(mail, 'READY_TO_RELOCATE_OUTSIDE',       False)
#     update_by_mail(mail, 'CAN_WORK',                        False)
#     update_by_mail(mail, 'NEED_EQUIPMENT',                  False)
#     update_by_mail(mail, 'NEED_RESOURCES',                  False)
#     update_by_mail(mail, 'NEEDMED',                         False)
#     update_by_mail(mail, 'NEEDEAT',                         False)
#     update_by_mail(mail, 'NEEDWATER',                       False)
#     update_by_mail(mail, 'LOCATION_REGION',                'location_region')
#     update_by_mail(mail, 'LOCATION_CITY',                  'location_city')
#     update_by_mail(mail, 'COUNTRY',                        'country')
#     update_by_mail(mail, 'PLAN_RELOCATE_INFO',             'plan_relocate_info')
#     update_by_mail(mail, 'READY_TO_RELOCATE_OUTSIDE_INFO', 'ready_to_relocate_outside_info')
#     update_by_mail(mail, 'mobilizate',                     'mobilizate')
#     update_by_mail(mail, 'MOBILIZATE_DATE',                'mobilizate_date')
#     update_by_mail(mail, 'CAN_WORK_REASON',                'can_work_reason')
#     update_by_mail(mail, 'PRODUCTIVITY',                   'productivity')
#     update_by_mail(mail, 'PRODUCTIVITY_DIFFICULTIES',      'productivity_difficulties')
#     update_by_mail(mail, 'NEED_EQUIPMENT_INFO',            'need_equipment_info')
#     update_by_mail(mail, 'NEED_RESOURCES_INFO',            'needresources_info')
#     update_by_mail(mail, 'NEEDMED_INFO',                   'needmed_info')
#     update_by_mail(mail, 'NEEDEAT_INFO',                   'neadeat_info')
#     update_by_mail(mail, 'NEEDWATER_INFO',                 'needwater_info')
#     update_by_mail(mail, 'NEEDHELP_INFO',                  'needhelp_info')
