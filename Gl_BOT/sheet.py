import pygsheets
import pandas as pd
# from lib import *
from datetime import datetime
from checker import *

gc = pygsheets.authorize(service_file='client_secret.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1tjSPeOvY8ueMnP7DlBfaeZHyprMZbpemXOgMTH12S2E/edit#gid=0')
# wks0 = sh[0]
# wks1 = sh[1]
# wks2 = sh[2]
wks4 = sh[4]
# df0  = pd.DataFrame(wks0.get_all_records())
# df1  = pd.DataFrame(wks1.get_all_records())
# df2  = pd.DataFrame(wks2.get_all_records())
df4  = pd.DataFrame(wks4.get_all_records())

def get_yes_no(param):
    if param:
        param='Yes'
    else:
        param='No'
    return param

def reverce(param):
    if param == 'Yes':
        param = 'No'
    else:
        param='Yes'
    return param


def get_project(mail):
    params=get_all_by_mail(mail)
    wks4 = sh[4]
    df4  = pd.DataFrame(wks4.get_all_records())
    if mail in df4.Email.values:
        index=df4.index[df4['Email']==mail].tolist()
        project=str(df4.iloc[index[0]]['Project Name'])
        update_by_mail(mail, 'PROJECT', project)
        project_index=get_project_group(project)
        get_manager(project_index,mail)
    else:
        insert_in_sheet(mail)

def get_project_group(project):
    counter=0
    for projects in DSO,Carelink,Mobile:
        if project in projects:
            return counter
        counter+=1
        if counter == 3:
            return 0

def get_manager(project_index,mail):
    wks = sh[project_index]
    df  = pd.DataFrame(wks.get_all_records())
    index=df.index[df['Email']==mail].tolist()
    supervisor=df.iloc[index[0]]['Supervisor Name']
    update_by_mail(mail, 'SUPERVISOR', supervisor)

def update_sheet(mail):
    params=get_all_by_mail(mail)
    project_index=get_project_group(params[0][1])
    wks = sh[project_index]
    df  = pd.DataFrame(wks.get_all_records())
    if mail in df.Email.values:
        index=df.index[df['Email']==params[0][3]].tolist()
        df.at[index, 'Current city location'] = params[0][7]
        if not params[0][8]:
            df.at[index, 'Current regional city/village (if not region capital)'] = params[0][9]
        else:
            df.at[index, 'Current regional city/village (if not region capital)'] = ""
        df.at[index, 'Current country location'] = params[0][10]
        df.at[index, 'Plans to change location? [Y/N]'] = get_yes_no(params[0][11])
        df.at[index, 'Can work? [Y/N]'] = get_yes_no(params[0][17])
        if not params[0][17]:
            df.at[index, 'Productivity, %'] = '0%'
        else:
            if params[0][19] == 'productivity':
                df.at[index, 'Productivity, %'] = '0%'
            else:
                df.at[index, 'Productivity, %'] = params[0][19]
        df.at[index, 'Since what date? (DD-MMM)'] = datetime.fromtimestamp(int(params[0][6])).strftime('%d/%m/%Y')
        df.at[index, 'Has needed equipment? [Y/N]'] = reverce(get_yes_no(params[0][21]))
        df.at[index, 'Has access to needed resources? [Y/N]'] = reverce(get_yes_no(params[0][23]))
        df.at[index, 'Can relocate outside of UA (exempt to martial law)? [Y/N]'] = get_yes_no(params[0][13])
        df.at[index, 'Is mobilized to army or ter oborona? [Y/N]'] = params[0][15]
        wks.set_dataframe(df, 'A1')
    else:
        return

def insert_in_sheet(mail):
    params=get_all_by_mail(mail)
    name=get_name(mail)
    project_index=get_project_group(params[0][1])
    wks = sh[project_index]
    df  = pd.DataFrame(wks.get_all_records())
    if mail not in df.Email.values:
        df.loc[df.shape[0]] = [name, mail, '','', '', '','', '', '','', '', '','', '', '','', '', '','', '', '','', '', '','', '', '','' ]
    wks.set_dataframe(df, 'A1')

def get_name(mail):
    name=mail.replace("@globallogic.com", "")
    name=name.replace(".", " ")
    name=name.title()
    return name
def get_hesh(mail):
     name=mail.replace("@globallogic.com", "")
     name=name.replace(".", "_")
     return name
