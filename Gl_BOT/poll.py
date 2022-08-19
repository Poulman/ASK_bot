import   telebot
# from lib import *
from mail import *
import re
from telebot import types
import sched, time
# from scheduler import *
from sheet import *
from buttons import *
from checker import *
exec(open('ua_len.py').read())

def poll(message,update,mail):

    def q_update_poll_param():
        bot.send_message(message.chat.id, "Please, chose section for update", reply_markup=topic)
        bot.register_next_step_handler(message, update_poll_param)

    def update_poll_param(message):
        if message.text == 'Location':
            location()
        if message.text == 'Mobilization status':
            mobil(message)
        if message.text == 'Possibility to work':
            q_can_work()
        if message.text == 'Productivity':
            q_productivity()
        if message.text == 'Relocation':
            q_plan_relocate()
        if message.text == 'Resources':
            q_need_some()
        if message.text == 'Nothing':
            bot.send_message(message.chat.id, "Thanks")
            return

    def location():
        # if
        # update=is_updated(message,'Location')
        bot.send_message(message.chat.id, 'Please, indicate your current regional center location. If your regional center is not on the list, write it down (ONLY regional center or the region).', reply_markup=Regions)
        bot.register_next_step_handler(message, location1)

    def q_is_regional_center():
        bot.send_message(message.chat.id, 'Please, specify do you locate in the regional center?', reply_markup=YesNo)
        bot.register_next_step_handler(message, location2)

    def q_country():
        bot.send_message(message.chat.id, 'Please, specify your country. Is not on the list, write it down', reply_markup=Countries)
        bot.register_next_step_handler(message, country)

    def q_citi():
        bot.send_message(message.chat.id, 'Please, specify your city/vilage location.')
        bot.register_next_step_handler(message, city)

    def q_mobil_ter():
        bot.send_message(message.chat.id, "Since when?")
        bot.register_next_step_handler(message, mobilized_data_t)

    def q_mobil_army():
        bot.send_message(message.chat.id, "Since when?")
        bot.register_next_step_handler(message, mobilized_data)

    def q_can_work():
        # update=is_updated(message,'Possibility to work')
        bot.send_message(message.chat.id, ua_q_can_work, reply_markup=YesNo)
        bot.register_next_step_handler(message, can_work)

    def q_productivity():
        # update=is_updated(message,'Productivity')
        bot.send_message(message.chat.id, ua_q_productivity, reply_markup=percent)
        bot.register_next_step_handler(message, productivity)

    def q_can_work_reason():
        bot.send_message(message.chat.id, ua_msg_reason)
        bot.register_next_step_handler(message, reason)

    def q_difficulties():
        bot.send_message(message.chat.id, 'Please, let us know what makes difficulties?')
        bot.register_next_step_handler(message, difficulties)

    def q_plan_relocate():
        # update=is_updated(message,'Relocation')
        bot.send_message(message.chat.id, ua_q_location, reply_markup=YesNo)
        bot.register_next_step_handler(message, plan_relocate)

    def q_plan_relocate_info():
        bot.send_message(message.chat.id, ua_msg_location)
        bot.register_next_step_handler(message, plan_relocate_info)

    def q_relocate_out():
        bot.send_message(message.chat.id, ua_q_relocate, reply_markup=YesNo)
        bot.register_next_step_handler(message, relocate_out)

    def q_relocate_out_info():
        bot.send_message(message.chat.id, ua_msg_relocate, reply_markup=relocate_info)
        bot.register_next_step_handler(message, relocate_out_info)

    def q_need_some():
        # update=is_updated(message,'Resources')
        bot.send_message(message.chat.id, "Please, specify if you need something from this list:", reply_markup=need_some_k)
        bot.register_next_step_handler(message, need_some)

    def q_resources(message):
        update_by_mail(mail, 'NEED_RESOURCES_INFO', message.text)
        q_need_some_more()

    def q_equipment(message):
        update_by_mail(mail, 'NEED_EQUIPMENT_INFO', message.text)
        q_need_some_more()

    def q_needeat(message):
        update_by_mail(mail, 'NEEDEAT_INFO', message.text)
        q_need_some_more()

    def q_need_some_more():
        bot.send_message(message.chat.id, "Please, indicate, do you need something more from this list?", reply_markup=need_some_k)
        bot.register_next_step_handler(message, need_some)

    def q_additional():
        bot.send_message(message.chat.id, ua_q_more_help, reply_markup=YesNo)
        bot.register_next_step_handler(message, additional)

    def q_additional_info():
        bot.send_message(message.chat.id, ua_msg_more_help)
        bot.register_next_step_handler(message, finish_q)

    def location1(message):
        update_by_mail(mail, 'LOCATION_REGION', message.text)
        if message.text != 'Out of Ukraine':
            update_by_mail(mail, 'COUNTRY', 'Ukraine')
            q_is_regional_center()
        else:
            q_country()

    def location2(message):
        if message.text != 'Back':
            if message.text == 'Yes':
                update_by_mail(mail, 'LOCATION_CITY', get_by_params_mail(mail, 'LOCATION_REGION'))
                update_by_mail(mail, 'IS_LOCATION_REGION_CENTER', True)
                if not update:
                    mobil(message)
                else:
                    bot.send_message(message.chat.id, "Information has been seccesfully updated")
                    output(mail)
                    return
            elif message.text == 'No':
                update_by_mail(mail, 'LOCATION_REGION', get_by_params_mail(mail,'LOCATION_REGION')+" region")
                update_by_mail(mail, 'IS_LOCATION_REGION_CENTER', False)
                q_citi()
            else:
                bot.send_message(message.chat.id, "Please, use buttons for this answer")
                q_is_regional_center()
        else:
            location()

    def city(message):
        update_by_mail(mail, 'LOCATION_CITY', message.text)
        if not update:
            mobil(message)
        else:
            bot.send_message(message.chat.id, "Information has been seccesfully updated")
            output(mail)
            return

    def country(message):
        update_by_mail(mail, 'COUNTRY', message.text)
        q_citi()

    def mobil(message):
        # update=is_updated(message,'Mobilization status')
        bot.send_message(message.chat.id, ua_msg_mobilizade, reply_markup=mobilizade)
        bot.register_next_step_handler(message, mobil1)

    def mobil1(message):
        if message.text != 'Back':
            update_by_mail(mail, 'MOBILIZATE', message.text)
            if  message.text == 'The Armed Forces of Ukraine':
                q_mobil_army()
            elif message.text == 'Territorial Defense':
                q_mobil_ter()
            elif message.text == 'No':
                if not update:
                    q_can_work()
                else:
                    bot.send_message(message.chat.id, "Information has been seccesfully updated")
                    output(mail)
                    return
            else:
                bot.send_message(message.chat.id, "Please, use buttons for this answer")
                mobil(message)
        else:
            location()

    def mobilized_data(message):
        update_by_mail(mail, 'MOBILIZATE_DATE', message.text)
        bot.send_message(message.chat.id, "Слава Україні!")
        output(mail)

    def mobilized_data_t(message):
        update_by_mail(mail, 'MOBILIZATE_DATE', message.text)
        if not update:
            q_can_work()
        else:
            bot.send_message(message.chat.id, "Information has been seccesfully updated")
            output(mail)
            return

    def can_work(message):
        if message.text != 'Back':
        #     mobil(message)
            if message.text == 'Yes':
                update_by_mail(mail, 'CAN_WORK', True)
                if not update:
                    q_productivity()
                else:
                    bot.send_message(message.chat.id, "Information has been seccesfully updated")
                    output(mail)
                    return
            elif message.text == 'No':
                update_by_mail(mail, 'CAN_WORK', False)
                update_by_mail(mail, 'PRODUCTIVITY', "0%")
                # update_by_mail(mail, 'NEED_RESOURCES', False)
                # update_by_mail(mail, 'NEED_EQUIPMENT', False)
                if get_by_params_mail(mail, "MOBILIZATE") == 'Territorial Defense':
                    bot.send_message(message.chat.id, "Слава Україні!")
                    output(mail)
                else:
                    q_can_work_reason()
            else:
                bot.send_message(message.chat.id, "Please, use buttons for this answer")
                q_can_work()
        else:
            mobil(message)
    # def productivity_update():
    #     update_by_mail(mail, 'PRODUCTIVITY', message.text)
    #     bot.send_message(message.chat.id, "Productivity updated seccesfully")

    def productivity(message):
        if message.text != 'Back':
            update_by_mail(mail, 'PRODUCTIVITY', message.text)
            if update:
                if not get_by_params_mail(mail, 'CAN_WORK'):
                    bot.send_message(message.chat.id, "You declared, that you can't work, is it actual?")
                    q_can_work()
                else:
                    bot.send_message(message.chat.id, "Information has been seccesfully updated")
                    output(mail)
                    return
            else:
                if message.text == '100%':
                    q_plan_relocate()
                elif message.text == '0%' or message.text == '25%' or message.text == '50%'  or message.text == '75%':
                    q_difficulties()
        else:
            q_can_work()

    def reason(message):
        update_by_mail(mail, 'CAN_WORK_REASON', message.text)
        if not update:
            q_plan_relocate()
        else:
            bot.send_message(message.chat.id, "Information has been seccesfully updated")
            output(mail)
            return

    def difficulties(message):
        update_by_mail(mail, 'PRODUCTIVITY_DIFFICULTIES', message.text)
        if not update:
            q_plan_relocate()
        else:
            bot.send_message(message.chat.id, "Information has been seccesfully updated")
            output(mail)
            return

    def plan_relocate(message):
        if message.text != 'Back':
            if message.text == 'Yes':
                update_by_mail(mail, 'PLAN_RELOCATE', True)
                q_plan_relocate_info()
            elif message.text == 'No':
                update_by_mail(mail, 'PLAN_RELOCATE', False)
                update_by_mail(mail, 'PLAN_RELOCATE_INFO', 'plan_relocate_info')
                q_relocate_out()
            else:
                bot.send_message(message.chat.id, "Please, use buttons for this answer")
                q_plan_relocate()
        else:
            q_can_work()

    def plan_relocate_info(message):
            update_by_mail(mail, 'PLAN_RELOCATE_INFO', message.text)
            q_relocate_out()

    def relocate_out(message):
        if message.text != 'Back':
            if message.text == 'Yes':
                update_by_mail(mail, 'READY_TO_RELOCATE_OUTSIDE', True)
                q_relocate_out_info()
            elif message.text == 'No':
                update_by_mail(mail, 'READY_TO_RELOCATE_OUTSIDE', False)
                update_by_mail(mail, 'READY_TO_RELOCATE_OUTSIDE_INFO', 'none')
                if not update:
                    q_need_some()
                else:
                    bot.send_message(message.chat.id, "Information has been seccesfully updated")
                    output(mail)
                    return
            else:
                bot.send_message(message.chat.id, "Please, use buttons for this answer")
                q_relocate_out()
        else:
            q_plan_relocate()

    def relocate_out_info(message):
        if message.text == 'Back':
            q_relocate_out()
        else:
            update_by_mail(mail, 'READY_TO_RELOCATE_OUTSIDE_INFO', message.text)
            if not update:
                q_need_some()
            else:
                bot.send_message(message.chat.id, "Information has been seccesfully updated")
                output(mail)
                return

    def need_some(message):
        if message.text == 'Software':
            update_by_mail(mail, 'NEED_RESOURCES', True)
            bot.send_message(message.chat.id, ua_msg_need_resources)
            bot.register_next_step_handler(message, q_resources)
        elif message.text == 'Hardware':
            update_by_mail(mail, 'NEED_EQUIPMENT', True)
            bot.send_message(message.chat.id, ua_msg_need_equipment)
            bot.register_next_step_handler(message, q_equipment)
        elif message.text == 'Supplies\n(Food, water, medical)':
            update_by_mail(mail, 'NEEDEAT', True)
            bot.send_message(message.chat.id, ua_msg_need_eat)
            bot.register_next_step_handler(message, q_needeat)
        elif message.text == 'Nothing':
            if not update:
                q_additional()
            else:
                bot.send_message(message.chat.id, "Information has been seccesfully updated")
                output(mail)
                return
        elif message.text == 'Back':
            q_relocate_out()
        else:
            bot.send_message(message.chat.id, "Please, use buttons for this answer")
            q_need_some()

    def additional(message):
        if message.text != 'Back':
            if message.text == 'Yes':
                q_additional_info()
            elif message.text == 'No':
                finish_q(message)
            else:
                bot.send_message(message.chat.id, "Please, use buttons for this answer")
                q_additional()
        else:
            q_need_some()

    def finish_q(message):
        if message.text != 'No':
            update_by_mail(mail, 'NEEDHELP_INFO', message.text)
        bot.send_message(message.chat.id, ua_msg_finish_q)
        update_by_mail(mail, 'LAST_DATE', int(time.time()))
        output(mail)

    if update:
        q_update_poll_param()
    else:
        location()

def output(mail):
    info=get_all_by_mail(mail)
    if info[0][10] != "Ukraine":
        msg="&#9989 {}\n<b>Місце розташування:</b> {}, {}\n".format(info[0][2],info[0][9],info[0][10])
    else:
        msg="&#9989 {}\n<b>Місце розташування:</b> {}\n".format(info[0][2],info[0][9])
    name=get_name(mail)
    all_good=True
    if info[0][15] != "No":
        all_good=False
        msg+="&#9888 <b>Мобілізація:</b> {}\n".format(info[0][15])
        if not info[0][17]:
            msg+="&#9888 <b>Не може працювати</b>\n"
    else:
        if not info[0][17]:
            all_good=False
            if info[0][18] != 'can_work_reason':
                msg+="&#9888 <b>Не може працювати:</b> {}\n".format(info[0][18])
            else:
                msg+="&#9888 <b>Не може працювати</b>\n"
    if info[0][22] != "need_equipment_info":
        all_good=False
        msg+="&#9888 <b>Потрібне обладнання:</b> {}\n".format(info[0][22])
    if info[0][24] != "needresources_info":
        all_good=False
        msg+="&#9888 <b>Потрібні ресурси:</b> {}\n".format(info[0][24])
    if info[0][29] != "neadsuplies_info":
        all_good=False
        msg+="&#9888 <b>Need Supplies:</b> {}\n".format(info[0][29])
    if info[0][11]:
        all_good=False
        msg+="&#9888 <b>Готовий/ва до релокації в безпечніше місце</b>\n"
    if info[0][13]:
        msg+="&#9888 <b>Може виїхати у зв'язку з </b> {}\n".format(relocate(mail))
    if info[0][19] == 'productivity':
        msg+="&#128187 <b>Продуктивність:</b> 0%\n"
    else:
        msg+="&#128187 <b>Продуктивність:</b> {}\n".format(info[0][19])
        if info[0][19] != '100%' and info[0][19] != '0%':
            all_good=False
            msg+="&#9888 <b>Труднощі:</b> {}\n".format(info[0][20])
    if info[0][32] != 'needhelp_info':
        all_good=False
        msg+="&#9888 <b>Додаткова інформація:</b> {}".format(info[0][32])
    msg+="\n#{}".format(get_hesh(mail))
    supervisor=info[0][25].replace(" ", "_")
    msg+="\n#{}".format(get_hesh(supervisor))
    if all_good:
        bot.send_message(group_good, msg, parse_mode='html')
    else:
        bot.send_message(group, msg, parse_mode='html')
    update_sheet(mail)

def relocate(mail):
    relocate_info = ""
    if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '1':
        relocate_info = "certificate of recruitment deferral and message on enrollment to"
    if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '2':
        relocate_info = "special military registration conclusion of military and medical commission on ineligibility"
    if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '3':
        relocate_info = "maintain three or more children aged to 18 y.o"
    if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '4':
        relocate_info = "raise alone a child (children) aged to 18 y.o."
    if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '5':
        relocate_info = "adopter/guardian"
    if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '6':
        relocate_info = "immediate family members perished or disappeared during the antiterrorist operation"
    if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == '7':
        relocate_info = "the reason is reported to manager"
    if get_by_params_mail(mail, "READY_TO_RELOCATE_OUTSIDE_INFO") == 'Female':
        relocate_info = "Female"
    return relocate_info

def refresh(mail):
    update_by_mail(mail, 'IS_LOCATION_REGION_CENTER',       False)
    update_by_mail(mail, 'PLAN_RELOCATE',                   False)
    update_by_mail(mail, 'READY_TO_RELOCATE_OUTSIDE',       False)
    update_by_mail(mail, 'CAN_WORK',                        False)
    update_by_mail(mail, 'NEED_EQUIPMENT',                  False)
    update_by_mail(mail, 'NEED_RESOURCES',                  False)
    update_by_mail(mail, 'NEEDMED',                         False)
    update_by_mail(mail, 'NEEDEAT',                         False)
    update_by_mail(mail, 'NEEDWATER',                       False)
    update_by_mail(mail, 'LOCATION_REGION',                'location_region')
    update_by_mail(mail, 'LOCATION_CITY',                  'location_city')
    update_by_mail(mail, 'COUNTRY',                        'country')
    update_by_mail(mail, 'PLAN_RELOCATE_INFO',             'plan_relocate_info')
    update_by_mail(mail, 'READY_TO_RELOCATE_OUTSIDE_INFO', 'ready_to_relocate_outside_info')
    update_by_mail(mail, 'mobilizate',                     'mobilizate')
    update_by_mail(mail, 'MOBILIZATE_DATE',                'mobilizate_date')
    update_by_mail(mail, 'CAN_WORK_REASON',                'can_work_reason')
    update_by_mail(mail, 'PRODUCTIVITY',                   'productivity')
    update_by_mail(mail, 'PRODUCTIVITY_DIFFICULTIES',      'productivity_difficulties')
    update_by_mail(mail, 'NEED_EQUIPMENT_INFO',            'need_equipment_info')
    update_by_mail(mail, 'NEED_RESOURCES_INFO',            'needresources_info')
    update_by_mail(mail, 'NEEDMED_INFO',                   'needmed_info')
    update_by_mail(mail, 'NEEDEAT_INFO',                   'neadsuplies_info')
    update_by_mail(mail, 'NEEDWATER_INFO',                 'needwater_info')
    update_by_mail(mail, 'NEEDHELP_INFO',                  'needhelp_info')
