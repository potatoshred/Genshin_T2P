import PySimpleGUI as sg
import json
import os
import pickle
from pypinyin import lazy_pinyin


def read_data(folder_path):
    file_list = ['bk各层战斗数据.json',
                 'bk角色持有情况.json'
                 ]
    for file in file_list:
        if not os.path.exists(f'{folder_path}/{file}'):
            sg.PopupError(f'{folder_path}\n此目录下不存在目标文件: {file}\n'
                          f'\n请检查路径是否正确或从<url>https://youngmoe.com</url>下载json文件')
            return  False
    with open(folder_path + '/bk各层战斗数据.json', 'r', encoding='utf-8') as ji:
        raw_abyss = json.load(ji)['RECORDS']
    with open(folder_path + '/bk角色持有情况.json', 'r', encoding='utf-8') as ji:
        raw_playerbox = json.load(ji)['RECORDS']
    # 读取玩家角色
    data_0 = {}
    s5 = (
    '刻晴', '迪卢克', '七七', '琴', '莫娜', '温迪', '可莉', '达达利亚', '钟离', '阿贝多', '甘雨', '魈', '胡桃', '优菈', '万叶', '神里绫华', '宵宫', '雷电将军',
    '珊瑚宫心海', '埃洛伊', '', '')
    for seg in raw_playerbox:
        uid = seg['uid']
        fet = int(seg['Fetter'])
        lvl = int(seg['level'])
        con = int(seg['actived_constellation_num'])
        avt = seg['Avatar']
        rar = 4 + int(avt in s5)
        if not data_0.get(uid, 0):
            data_0[uid] = {'playerbox': {},
                           '091'      : [[], []],
                           '092'      : [[], []],
                           '093'      : [[], []],
                           '101'      : [[], []],
                           '102'      : [[], []],
                           '103'      : [[], []],
                           '111'      : [[], []],
                           '112'      : [[], []],
                           '113'      : [[], []],
                           '121'      : [[], []],
                           '122'      : [[], []],
                           '123'      : [[], []],
                           }
        #     idx = '%02d%d'%(flr,lvl)
        data_0[uid]['playerbox'][avt] = [lvl, con, fet, rar]

    # 读取深渊
    for seg in raw_abyss:
        uid = seg['uid']
        flr = seg['floor']
        lvl = seg['level']
        btl = seg['battle']
        avt = seg['avatar']

        idx = '%02d%s' % (int(flr), lvl)
        try:
            if avt not in data_0[uid][idx][int(btl) - 1]:
                data_0[uid][idx][int(btl) - 1].append(avt)
        except:
            pass
    return data_0


def read_config(file_config):
    if os.path.exists(file_config):
        with open(file_config, 'r', encoding='utf-8') as fi:
            param = json.load(fi)
        return param
    else:
        return {}


def write_config(param, file_config):
    with open(file_config, 'w', encoding='utf-8') as fo:
        json.dump(param, fo)

def get_parm(t1):
    tmp = {
        values[t1]:[range(values[t1+1],values[t1+2]+1),range(values[t1+3],values[t1+4]+1),range(values[t1+5],values[t1+6]+1)],
        values[t1+7]:[range(values[t1+8],values[t1+9]+1),range(values[t1+10],values[t1+11]+1),range(values[t1+12],values[t1+13]+1)],
        values[t1+14]:[range(values[t1+15],values[t1+16]+1),range(values[t1+17],values[t1+18]+1),range(values[t1+19],values[t1+20]+1)],
        values[t1+21]:[range(values[t1+22],values[t1+23]+1),range(values[t1+24],values[t1+25]+1),range(values[t1+26],values[t1+27]+1)],
    }
    for k,v in tmp.copy().items():
        if not k:
            tmp.pop(k)
    return tmp

def parse_teams(values:dict):
    t1=0
    t2=28
    for i in range(8):
        param[str(i*7)] = values[i*7]
    team1 = get_parm(t1)
    team2 = get_parm(t2)
    team1_names = set(team1.keys())
    team2_names = set(team2.keys())
    if team1_names.union(team2_names).__len__() < (len(team1_names)+len(team2_names)):
        return [team1,team2]
    else:
        return False
def parse_chamber(values:dict):
    floor_init = 56
    for i in range(4):
        if values[floor_init+i]:
            floor = 12-i
    chamber_init = 61
    for i in range(3):
        if values[chamber_init+i]:
            chamber = 3-i
    return '%02d%d'%(floor,chamber)

def teams_in_box(teams,playerbox:dict):
    team1,team2 = teams
    team_union = {}
    for k,v in team1.items():team_union[k]=v
    for k,v in team2.items():team_union[k]=v

    cnt = 0
    for mem,constrain in team_union.items():
        if mem in playerbox.keys():
            if playerbox[mem][0] in constrain[0]:
                if playerbox[mem][1] in constrain[1]:
                    if playerbox[mem][2] in constrain[2]:
                        cnt+=1
    print(mem,constrain)
    if cnt==team_union.__len__():
        return True
    else:
        return False

def team_similar(t1,t2):
    if not t1:
        return False
    cnt = 0
    for m in t1:
        if m in t2: cnt+=1
    if cnt == t1.__len__():
        return True
    else:
        return False

def calc(teams,data_0,chamber):
    cnter = [[0,0],[0,0]]
    both_have = 0
    for uid,detail in data_0.items():
        playerbox = detail['playerbox']

        if teams_in_box(teams,playerbox):
            both_have+=1
            team_chamber = detail[chamber]
            if team_similar(teams[0],team_chamber[0]):cnter[0][0]+=1
            if team_similar(teams[0],team_chamber[1]):cnter[0][1]+=1
            if team_similar(teams[1],team_chamber[0]):cnter[1][0]+=1
            if team_similar(teams[1],team_chamber[1]):cnter[1][1]+=1

    return [both_have,cnter]


with open('./pops.json', 'r', encoding='utf8') as fi:
    props = json.load(fi)
    character = props['character']
    weapon = props['weapon']
    artifact = props['artifact']
chara_names = list(character.keys())
chara_names.sort(key=lambda char: lazy_pinyin(char)[0][0])
data_0 = {}
data_out = []
param = read_config('./config.json')
folder_path = param.get('folder_path', '')
icon = "./favicon.ico"

# sg.theme('DarkBlack')  # Add a touch of color
  # Add a touch of color
# All the stuff inside your window.
theme = param.get("theme", "Default1")
if theme == "默认":
    theme = "Default1"
sg.theme(theme)
themes = ["默认", 'Black', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue',
          'Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue', 'DarkBlue1', 'DarkBlue10',
          'DarkBlue11', 'DarkBlue12', 'DarkBlue13', 'DarkBlue14', 'DarkBlue15', 'DarkBlue16', 'DarkBlue17',
          'DarkBlue2', 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7', 'DarkBlue8', 'DarkBlue9',
          'DarkBrown', 'DarkBrown1', 'DarkBrown2', 'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6',
          'DarkBrown7', 'DarkGreen', 'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5',
          'DarkGreen6', 'DarkGreen7', 'DarkGrey', 'DarkGrey1', 'DarkGrey10', 'DarkGrey11', 'DarkGrey12',
          'DarkGrey13', 'DarkGrey14', 'DarkGrey2', 'DarkGrey3', 'DarkGrey4', 'DarkGrey5', 'DarkGrey6', 'DarkGrey7',
          'DarkGrey8', 'DarkGrey9', 'DarkPurple', 'DarkPurple1', 'DarkPurple2', 'DarkPurple3', 'DarkPurple4', 'DarkPurple5',
          'DarkPurple6', 'DarkPurple7', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1', 'DarkTeal10',
          'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4', 'DarkTeal5', 'DarkTeal6', 'DarkTeal7', 'DarkTeal8',
          'DarkTeal9', 'Default', 'Default1', 'DefaultNoMoreNagging', 'GrayGrayGray', 'Green', 'GreenMono', 'GreenTan',
          'HotDogStand', 'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightBlue5',
          'LightBlue6', 'LightBlue7', 'LightBrown', 'LightBrown1', 'LightBrown10', 'LightBrown11', 'LightBrown12',
          'LightBrown13', 'LightBrown2', 'LightBrown3', 'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7',
          'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen', 'LightGreen1', 'LightGreen10', 'LightGreen2',
          'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6', 'LightGreen7', 'LightGreen8', 'LightGreen9',
          'LightGrey', 'LightGrey1', 'LightGrey2', 'LightGrey3', 'LightGrey4', 'LightGrey5', 'LightGrey6', 'LightPurple',
          'LightTeal', 'LightYellow', 'Material1', 'Material2', 'NeutralBlue', 'Purple', 'Python', 'Reddit', 'Reds',
          'SandyBeach', 'SystemDefault', 'SystemDefault1', 'SystemDefaultForReal', 'Tan', 'TanBlue', 'TealMono', 'Topanga']


column_floor = [  # [sg.Text('层',font=[6])],
    [sg.Radio("第12层", 'FLOOR', default=True), sg.Radio("第11层", 'FLOOR'), sg.Radio("第10层", 'FLOOR'),
     sg.Radio("第9层", 'FLOOR')]
]
column_chamber = [  # [sg.Text('间',font=[6])],
    [sg.Radio("第3间", "CHAMBER", default=True), sg.Radio("第2间", "CHAMBER"), sg.Radio("第1间", "CHAMBER")]
]
layout = [
    [sg.Text('队伍一', justification='center', size=(70, 1), background_color='darkred', text_color='white')],
    [sg.Text('选择角色'), sg.Combo(chara_names, size=(10, 1), default_value=param.get("0" ,'')),
     sg.Text('等级范围'), sg.Spin(list(range(1, 91)), initial_value=71), sg.Spin(list(range(1, 91)), initial_value=90),
     sg.Text('命座范围'), sg.Spin(list(range(0, 7)), initial_value=0), sg.Spin(list(range(0, 7)), initial_value=6),
     sg.Text('好感范围'), sg.Spin(list(range(0, 11)), initial_value=0), sg.Spin(list(range(0, 11)), initial_value=10),
     ],
    [sg.Text('选择角色'), sg.Combo(chara_names, size=(10, 1), default_value=param.get("7" ,'')),
     sg.Text('等级范围'), sg.Spin(list(range(1, 91)), initial_value=71), sg.Spin(list(range(1, 91)), initial_value=90),
     sg.Text('命座范围'), sg.Spin(list(range(0, 7)), initial_value=0), sg.Spin(list(range(0, 7)), initial_value=6),
     sg.Text('好感范围'), sg.Spin(list(range(0, 11)), initial_value=0), sg.Spin(list(range(0, 11)), initial_value=10),
     ],
    [sg.Text('选择角色'), sg.Combo(chara_names, size=(10, 1), default_value=param.get("14" ,'')),
     sg.Text('等级范围'), sg.Spin(list(range(1, 91)), initial_value=71),
     sg.Spin(list(range(1, 91)), initial_value=90),
     sg.Text('命座范围'), sg.Spin(list(range(0, 7)), initial_value=0), sg.Spin(list(range(0, 7)), initial_value=6),
     sg.Text('好感范围'), sg.Spin(list(range(0, 11)), initial_value=0),
     sg.Spin(list(range(0, 11)), initial_value=10),
     ],
    [sg.Text('选择角色'), sg.Combo(chara_names, size=(10, 1), default_value=param.get("21" ,'')),
     sg.Text('等级范围'), sg.Spin(list(range(1, 91)), initial_value=71),
     sg.Spin(list(range(1, 91)), initial_value=90),
     sg.Text('命座范围'), sg.Spin(list(range(0, 7)), initial_value=0), sg.Spin(list(range(0, 7)), initial_value=6),
     sg.Text('好感范围'), sg.Spin(list(range(0, 11)), initial_value=0),
     sg.Spin(list(range(0, 11)), initial_value=10),
     ],
    [sg.Text('队伍二', justification='center', size=(70, 1), background_color='darkcyan', text_color='white')],
    [sg.Text('选择角色'), sg.Combo(chara_names, size=(10, 1), default_value=param.get("28" ,'')),
     sg.Text('等级范围'), sg.Spin(list(range(1, 91)), initial_value=71),
     sg.Spin(list(range(1, 91)), initial_value=90),
     sg.Text('命座范围'), sg.Spin(list(range(0, 7)), initial_value=0), sg.Spin(list(range(0, 7)), initial_value=6),
     sg.Text('好感范围'), sg.Spin(list(range(0, 11)), initial_value=0),
     sg.Spin(list(range(0, 11)), initial_value=10),
     ],
    [sg.Text('选择角色'), sg.Combo(chara_names, size=(10, 1), default_value=param.get("35" ,'')),
     sg.Text('等级范围'), sg.Spin(list(range(1, 91)), initial_value=71),
     sg.Spin(list(range(1, 91)), initial_value=90),
     sg.Text('命座范围'), sg.Spin(list(range(0, 7)), initial_value=0), sg.Spin(list(range(0, 7)), initial_value=6),
     sg.Text('好感范围'), sg.Spin(list(range(0, 11)), initial_value=0),
     sg.Spin(list(range(0, 11)), initial_value=10),
     ],
    [sg.Text('选择角色'), sg.Combo(chara_names, size=(10, 1), default_value=param.get("42" ,'')),
     sg.Text('等级范围'), sg.Spin(list(range(1, 91)), initial_value=71),
     sg.Spin(list(range(1, 91)), initial_value=90),
     sg.Text('命座范围'), sg.Spin(list(range(0, 7)), initial_value=0), sg.Spin(list(range(0, 7)), initial_value=6),
     sg.Text('好感范围'), sg.Spin(list(range(0, 11)), initial_value=0),
     sg.Spin(list(range(0, 11)), initial_value=10),
     ],
    [sg.Text('选择角色'), sg.Combo(chara_names, size=(10, 1), default_value=param.get("49" ,'')),
     sg.Text('等级范围'), sg.Spin(list(range(1, 91)), initial_value=71),
     sg.Spin(list(range(1, 91)), initial_value=90),
     sg.Text('命座范围'), sg.Spin(list(range(0, 7)), initial_value=0), sg.Spin(list(range(0, 7)), initial_value=6),
     sg.Text('好感范围'), sg.Spin(list(range(0, 11)), initial_value=0),
     sg.Spin(list(range(0, 11)), initial_value=10),
     ],
    [sg.T("")],
    [sg.T("选择战斗数据", justification='center', size=[64, 1])],
    [sg.Column(column_floor), sg.VSeparator(), sg.Column(column_chamber)],
    [sg.T("")],
    [sg.In(folder_path, key='folder'),
     sg.FolderBrowse('选择数据路径', target='folder', key="-CHOOSEFOLDER-", enable_events=True,
                     initial_folder=folder_path or './'),
     sg.Button('读取数据', key='-READ-', tooltip="只需要读取一遍,第一遍会比较慢，请耐心等待十秒左右"),
     sg.Button('计算', key='-CALC-', enable_events=True, size=[6, 3])],
    [sg.T("")],
    [sg.Combo(themes,key="theme",default_value=param.get("theme", "Default1")), sg.Button('更改主题',key="-THEME-")],
    [sg.Graph((560, 160), (0, 160), (560, 0), background_color='grey', key="-GRAPH-", enable_events=True)],
    [sg.T('out:'),sg.StatusBar("",key="-CONSOLE-",size=[60,4],text_color='#777777')],


]

# Create the Window
window = sg.Window('T2P —— Tool for Team PVP   BY：k652@NGA', layout, icon=icon)
# Event Loop to process "events" and get the "values" of the inputs
graph = window["-GRAPH-"]
console = window["-CONSOLE-"]
# graph.draw_rectangle([0,0],[260,100],fill_color='darkred')


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        print(param)
        write_config(param, './config.json')
        break

    if event == "-THEME-" and values['theme']:
        theme = values['theme']
        param['theme'] = theme
        sg.PopupOK("更改的主题会在重启后生效",icon=icon)


    if event == "-READ-":
        if folder_path != values['folder']:
            data_flag = False
        else:
            data_flag = True
        folder_path = values['folder']
        param['folder_path'] = folder_path
        if not folder_path:
            sg.PopupError("请先选择数据路径", icon=icon)
            continue
        if data_0 and data_flag:
            sg.PopupOK("已读取数据", icon=icon)
        else:
            if os.path.exists(folder_path + '/cache'):
                if sg.PopupYesNo("发现缓存文件，是否读取？", icon=icon):
                    console.Update('读取缓存中')
                    with open(folder_path + '/cache', 'rb') as fi:
                        data_0 = pickle.load(fi, encoding='utf-8')
                    console.Update('读取缓存完毕')
                else:
                    console.Update('读取数据中')
                    tmp = read_data(folder_path)
                    if not tmp:
                        console.Update('读取失败')
                        continue
                    data_0 = tmp
                    console.Update('读取完毕')
            else:
                tmp = read_data(folder_path)
                if not tmp:
                    console.Update('读取失败')
                    continue
                data_0 = tmp
                console.Update('读取完毕')
                if not os.path.exists(folder_path + '/cache'):
                    if sg.PopupYesNo("是否在数据目录下建立缓存文件？（加快下一次启动时的计算速度）", icon=icon):
                        console.Update('写入缓存中')
                        with open(folder_path + '/cache', 'wb') as fo:
                            pickle.dump(data_0, fo)
                        console.Update('写入缓存完毕')
            sg.PopupOK("数据读取完毕", icon=icon)

    if event == "-CALC-":  # if user closes window or clicks cancel
        if data_0:
            teams = parse_teams(values)
            if teams:
                pass
            else:
                sg.PopupError("两队不存在竞争关系,请重新选择",icon=icon)
                continue
            chamber = parse_chamber(values)
            both_have, cnter = calc(teams, data_0,chamber)
            console.Update(f'深渊房间: {chamber[:2]}-{chamber[2]}\n'
                           f'两队队员: {list(teams[0].keys())}    {list(teams[1].keys())}\n'
                           f'计算结果: {cnter}, 共同持有人数: {both_have}')
            # sg.PopupOK(f'{cnter}')
            tot1 = sum(cnter[0]) or 0.00001
            tot2 = sum(cnter[1]) or 0.00001
            x_mid = 560 * tot1 / (tot1 + tot2)
            rect1 = [[0, 0], [x_mid, 160]]
            rect2 = [[x_mid, 0], [560, 160]]
            graph.draw_rectangle(*rect1, fill_color='darkred')
            graph.draw_rectangle(*rect2, fill_color='#009797')
            y1_mid = 160 * cnter[0][0] / tot1
            rect3 = [[0, 0], [x_mid, y1_mid]]
            graph.draw_rectangle(*rect3, fill_color='#A40000')
            y2_mid = 160 * cnter[1][0] / tot2
            rect4 = [[x_mid, 0], [560, y2_mid]]
            graph.draw_rectangle(*rect4, fill_color='darkcyan')

            graph.draw_text(f'上半: %d' % cnter[0][0], location=[x_mid / 2, y1_mid / 2], color='white')
            graph.draw_text(f'下半: %d' % cnter[0][1], location=[x_mid / 2, 80 + y1_mid / 2], color='white')
            graph.draw_text(f'上半: %d' % cnter[1][0], location=[280 + x_mid / 2, y2_mid / 2], color='white')
            graph.draw_text(f'下半: %d' % cnter[1][1], location=[280 + x_mid / 2, 80 + y2_mid / 2], color='white')

        else:
            sg.PopupError("请先读取数据", icon=icon)
    print(values)

window.close()
