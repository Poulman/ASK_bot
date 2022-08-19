import psycopg2
exec(open('vars.py').read())

connection = psycopg2.connect(user="pavlo",
                              password="218591",
                              host="127.0.0.1",
                              port="5432",
                              database="accounts")

cursor = connection.cursor()

group           = -725469696
group_good      = -760065603
admin_group     = -1001514147967
groups          = [admin_group,group_good,group]


# cursor.execute("DROP TABLE employee")
# connection.commit()
# CHATID serial PRIMARY KEY
def create_table():
    create_table_query = '''CREATE TABLE IF NOT EXISTS employee
          (CHATID TEXT,
            PROJECT TEXT,
            NAME_SURNAME TEXT,
            MAIL TEXT,
            ISVERIFIED BOOLEAN,
            IS_TG_USER BOOLEAN,
            LAST_DATE TEXT DEFAULT now(),
            LOCATION_REGION TEXT,
            IS_LOCATION_REGION_CENTER BOOLEAN,
            LOCATION_CITY TEXT,
            COUNTRY TEXT,
            PLAN_RELOCATE BOOLEAN,
            PLAN_RELOCATE_INFO TEXT,
            READY_TO_RELOCATE_OUTSIDE BOOLEAN,
            READY_TO_RELOCATE_OUTSIDE_INFO TEXT,
            MOBILIZATE TEXT,
            MOBILIZATE_DATE TEXT,
            CAN_WORK BOOLEAN,
            CAN_WORK_REASON TEXT,
            PRODUCTIVITY TEXT,
            PRODUCTIVITY_DIFFICULTIES TEXT,
            NEED_EQUIPMENT BOOLEAN,
            NEED_EQUIPMENT_INFO TEXT,
            NEED_RESOURCES BOOLEAN,
            NEED_RESOURCES_INFO TEXT,
            SUPERVISOR TEXT,
            NEEDMED BOOLEAN,
            NEEDMED_INFO TEXT,
            NEEDEAT BOOLEAN,
            NEEDEAT_INFO TEXT,
            NEEDWATER BOOLEAN,
            NEEDWATER_INFO TEXT,
            NEEDHELP_INFO TEXT); '''
    cursor.execute(create_table_query)
    connection.commit()

def insert_query(chatid, project, name_surname, mail, isverified, is_tg_user, las_date, location_region, is_location_region_center, location_city, country, plan_relocate, plan_relocate_info, ready_to_relocate_outside, ready_to_relocate_outside_info, mobilizate, mobilizate_date, can_work, can_work_reason, productivity, productivity_difficulties, need_equipment, need_equipment_info, need_resources, need_resources_info, supervisor,needmed, needmed_info, needeat, needeat_info, needwater, needwater_info, heedhelp_info):
    insert_query = """ INSERT INTO employee (CHATID,
      PROJECT,
      NAME_SURNAME,
      MAIL,
      ISVERIFIED,
      IS_TG_USER,
      LAST_DATE,
      LOCATION_REGION,
      IS_LOCATION_REGION_CENTER,
      LOCATION_CITY,
      COUNTRY,
      PLAN_RELOCATE,
      PLAN_RELOCATE_INFO,
      READY_TO_RELOCATE_OUTSIDE,
      READY_TO_RELOCATE_OUTSIDE_INFO,
      MOBILIZATE,
      MOBILIZATE_DATE,
      CAN_WORK,
      CAN_WORK_REASON,
      PRODUCTIVITY,
      PRODUCTIVITY_DIFFICULTIES,
      NEED_EQUIPMENT,
      NEED_EQUIPMENT_INFO,
      NEED_RESOURCES,
      NEED_RESOURCES_INFO,
      SUPERVISOR,
      NEEDMED,
      NEEDMED_INFO,
      NEEDEAT,
      NEEDEAT_INFO,
      NEEDWATER,
      NEEDWATER_INFO,
      NEEDHELP_INFO) VALUES({}, '{}', '{}', '{}', {}, {}, '{}', '{}', {}, '{}', '{}', {}, '{}', {}, '{}', '{}', '{}', {}, '{}', '{}', '{}', {}, '{}', {}, '{}', '{}', {}, '{}', {}, '{}', {}, '{}', '{}')""".format(chatid, project, name_surname, mail, isverified, is_tg_user, las_date, location_region, is_location_region_center, location_city, country, plan_relocate, plan_relocate_info, ready_to_relocate_outside, ready_to_relocate_outside_info, mobilizate, mobilizate_date, can_work, can_work_reason, productivity, productivity_difficulties, need_equipment, need_equipment_info, need_resources, need_resources_info, supervisor,needmed, needmed_info, needeat, needeat_info, needwater, needwater_info, heedhelp_info)
    cursor.execute(insert_query)
    connection.commit()

def update_by_param(chatid, param, value):
    update_query = """Update employee set {} = '{}' where CHATID = '{}'""".format(param, value, str(chatid))
    cursor.execute(update_query)
    connection.commit()

def update_by_mail(mail, param, value):
    update_query = """Update employee set {} = '{}' where MAIL = '{}'""".format(param, value, mail)
    cursor.execute(update_query)
    connection.commit()

def get_by_params(chat_id, param):
    cursor.execute("SELECT {} from employee where CHATID = '{}'".format(param,chat_id))
    record =               cursor.fetchall()
    return                 record[0][0]

def get_by_params_mail(mail, param):
    cursor.execute("SELECT {} from employee where MAIL = '{}'".format(param,mail))
    record =               cursor.fetchall()
    return                 record[0][0]

def select_all():
    cursor.execute("SELECT * from employee")
    record =               cursor.fetchall()
    return                 record

def get_all_params(chat_id):
    if chat_id not in groups:
        cursor.execute("SELECT * from employee where CHATID = '{}'".format(chat_id))
        record =               cursor.fetchall()
        return record
    else:
        bot.send_message(chat_id, "Action is not permitted")

def get_all_by_mail(mail):
    cursor.execute("SELECT * from employee where MAIL = '{}'".format(mail))
    record =               cursor.fetchall()
    return record

def is_param_exis(param,value):
    cursor.execute("SELECT exists(SELECT * from employee where {} = '{}')".format(param,value))
    record = cursor.fetchall()
    return record[0][0]

def list_users_id():
    cursor.execute("SELECT CHATID from employee")
    column_names = [row[0] for row in cursor]
    return                 column_names
# print(select_all())
