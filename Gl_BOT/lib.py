# from numpy import random
# import telebot
# import time, re
# from database import *
# from mail import *
# from poll import *
# from scheduler import *
# from checker import *
# # from buttons import *
# exec(open('ua_len.py').read())

# TELEGRAM_BOT_ID = "5202517194:AAHkUwExe08QDb1coSmkm0auJpD5F8rsw3A"
# bot             = telebot.TeleBot(TELEGRAM_BOT_ID)
# group           = -725469696
# group_good      = -760065603
# admin_group     = -1001514147967
# groups          = [admin_group,group_good,group]

cursor = connection.cursor()

##############################################
#               FIRST REGISTRATION
##############################################

# def register(message):
#     mail=check_mail(message)
#     if mail:
#         code=gen_code()
#         send_code(mail,code)
#         bot.send_message(message.chat.id, ua_msg_verification_code)
#         bot.register_next_step_handler(message, ath, code, mail)

# def ath(message,code, mail):
#     code=code.replace(" ", "")
#     # if message.text == code:
#     update_by_param(message.chat.id, 'MAIL', mail)
#     update_by_param(message.chat.id, 'ISVERIFIED', True)
#     update_by_param(message.chat.id, 'NAME_SURNAME', get_name(mail))
#     finish_reg(message)
#     # else:
#     #     bot.send_message(message.chat.id, ua_msg_error_verification)
#
# def finish_reg(message):
#     bot.send_message(message.chat.id, ua_msg_finish_reg)
#     info=get_all_params(message.chat.id)
#     # print(info[0][3])
#     # print(get_hesh(info[0][3]))
#     msg="&#127381 <b>{}</b>\n<b>Емейл:</b> {}\n\n#{}".format(info[0][2],info[0][3],get_hesh(info[0][3]))
#     bot.send_message(group_good, msg, parse_mode='html')
#     # print(message,update,info[0][3])
#     poll(message,update,info[0][3])
#     insert_in_sheet(info[0][3])

##############################################
#         REGISTRATION YOU COLLEGUE
##############################################

# def register_behalf(message,mail):
#     if not is_param_exis('MAIL',mail):
#         name=get_name(mail)
#         date= int(time.time())
#         insert_query(0, 'username', name, mail, False, False, date, 'location_region', False, 'location_city', 'country', False, 'plan_relocate_info', False, 'ready_to_relocate_outside_info', 'mobilizate', 'mobilizate_date', False, 'can_work_reason', 'productivity', 'productivity_difficulties', False, 'need_equipment_info', False, 'need_resources_info', 'safe_mark', False, 'needmed_info', False, 'needeat_info', False, 'needwater_info', 'heedhelp_info')

# ##############################################
# #         CHECKERS
# ##############################################
#
# def check_group(chatid):
#     if chatid not in groups:
#         return True
#     else:
#         bot.send_message(chatid, "Action is not permitted")
#         return False
#
# def check_mail(message):
#     regex = r'\b[A-Za-z0-9._%+-]+@globallogic.com\b'
#     if(re.fullmatch(regex, message.text)):
#         return message.text
#     else:
#         bot.send_message(message.chat.id, ua_msg_error_email)
#         bot.register_next_step_handler(message, register)
#
# def check_user(chatid):
#     if is_param_exis('CHATID',chatid):
#         if get_by_params(chatid, 'ISVERIFIED'):
#             return True
#     else:
#         date= int(time.time())
#         insert_query(chatid, 'username', 'name_surname', 'mail', False, False, date, 'location_region', False, 'location_city', 'country', False, 'plan_relocate_info', False, 'ready_to_relocate_outside_info', 'mobilizate', 'mobilizate_date', False, 'can_work_reason', 'productivity', 'productivity_difficulties', False, 'need_equipment_info', False, 'need_resources_info', 'safe_mark', False, 'needmed_info', False, 'needeat_info', False, 'needwater_info', 'heedhelp_info')
#
# def is_updated(message,param):
#     if message.text == param:
#         update=True
#     else:
#         update=False
#     return update

# def get_name(mail):
#     name=mail.replace("@globallogic.com", "")
#     name=name.replace(".", " ")
#     name_surname=mail.title()
#     return name
#
# def get_hesh(mail):
#      name=mail.replace("@globallogic.com", "")
#      name=name.replace(".", "_")
#      return mail

##############################################
#               SOS
##############################################

# def sos1(message):
#     bot.send_message(message.chat.id, ua_msg_problem_description)
#     bot.register_next_step_handler(message, finish_sos)
#
# def finish_sos(message):
#     bot.send_message(message.chat.id, ua_msg_finish_sos)
#     info=get_all_params(message.chat.id)
#     msg="&#127384 {}\n\n{}\n#{}".format(info[0][10],message.text, get_hesh(info[0][3]))
#     bot.send_message(group, msg, parse_mode='html')

##############################################

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
#     update_by_mail(mail, 'SAFE_MARK',                      'safe_mark')
#     update_by_mail(mail, 'NEEDMED_INFO',                   'needmed_info')
#     update_by_mail(mail, 'NEEDEAT_INFO',                   'neadeat_info')
#     update_by_mail(mail, 'NEEDWATER_INFO',                 'needwater_info')
#     update_by_mail(mail, 'NEEDHELP_INFO',                  'needhelp_info')
