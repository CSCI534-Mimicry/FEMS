from flask import request, session
import requests
import os, csv
import urllib.request

base_vh_host_url = 'http://localhost:22500'

def au_delivery(mny, au_1, au_2, au_4, au_5, au_6, au_7, au_10, au_12, au_25, au_26, au_45):
    sex = session.get("sex")
    sex = "m" if sex == "male" else "f"
    username = str(session.get("dir"))
    action_dict = {
        'sex': sex,
        'user': username,
        'mny': mny,
        'au_1': au_1,
        'au_2': au_2,
        'au_4': au_4,
        'au_5': au_5,
        'au_6': au_6,
        'au_7': au_7 / 3,
        'au_10': au_10,
        'au_12': au_12,
        'au_25': au_25,
        'au_26': au_26,
        'au_45': au_45,
    }
    print(mny, sex, username, au_1, au_2, au_4, au_5, au_6, au_7, au_10, au_12, au_25, au_26, au_45)
    res = requests.post(base_vh_host_url + '/receive_au', json=action_dict)
    return res.status_code, res.text

def get_action_units(mny_idxs):
    # Openface Path Specific
    username = session.get("dir")
    filenames = ['./static/img/testers/' + str(username) + '/' + str(mny_idx) + '.jpg' for mny_idx in mny_idxs] # always exist
    out_dir = './static/img/testers/' + str(username) + '/au_out'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    os.system("E:/OpenFace_2.2.0_win_x64/FaceLandmarkImg.exe -f " + ' -f '.join(filenames) + " -out_dir " + out_dir)
    res = []
    for mny_idx in mny_idxs:
        aus = [0]*11
        with open(out_dir + '/' + str(mny_idx) + '.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                aus[0] = float(row[' AU01_r'])
                aus[1] = float(row[' AU02_r'])
                aus[2] = float(row[' AU04_r'])
                aus[3] = float(row[' AU05_r'])
                aus[4] = float(row[' AU06_r'])
                aus[5] = float(row[' AU07_r'])
                aus[6] = float(row[' AU10_r'])
                aus[7] = float(row[' AU12_r'])
                aus[8] = float(row[' AU25_r'])
                aus[9] = float(row[' AU26_r'])
                aus[10] = float(row[' AU45_r'])
        res.append(aus)
    return res

def purse_au_pic(mny_idx):
    action_unit = get_action_units([mny_idx])[0]

    usr_name = session.get("dir")
    dir_name = "./static/img/testers/" + str(usr_name)
    out_dir = dir_name + '/gnt'

    au_1, au_2, au_4, au_5, au_6, au_7, au_10, au_12, au_25, au_26, au_45 = \
        action_unit[0], action_unit[1], action_unit[2], action_unit[3], \
        action_unit[4], action_unit[5], action_unit[6], action_unit[7], \
        action_unit[8], action_unit[9], action_unit[10]
    
    status, vh_pic = au_delivery(mny_idx, au_1, au_2, au_4, au_5, au_6, au_7, au_10, au_12, au_25, au_26, au_45)
    if status != 200:
        return
    session["mny_" + str(mny_idx)] = True
    vh_pic_url = base_vh_host_url + vh_pic
    vh_pic_filedata = urllib.request.urlopen(vh_pic_url)
    datatowrite = vh_pic_filedata.read()
    with open(out_dir + '/' + str(mny_idx) + '.png', 'wb') as f:
        f.write(datatowrite)

def purse_au_pics():
    usr_name = session.get("dir")
    dir_name = "./static/img/testers/" + str(usr_name)

    file_list = os.listdir(dir_name)
    idx_list = list()
    if file_list is not None:
        for f_name in file_list:
            if f_name.split(".")[-1] == "jpg":
                idx = f_name.split(".")[0]
                idx_list.append(int(idx))
    idx_list.sort()
    action_unit_idx = []
    p = 0
    for i in range(11):
        if i in idx_list:
            p += 1
            action_unit_idx.append(i)
        else:
            if p < len(idx_list):
                action_unit_idx.append(idx_list[p])
            else:
                action_unit_idx.append(idx_list[-1])
    action_units = get_action_units(action_unit_idx)
    out_dir = dir_name + '/gnt'
    for i in range(len(action_units)):
        if os.path.exists(out_dir + '/' + str(i) + '.png') or "mny_" + str(i) in session:
            continue
        au_1, au_2, au_4, au_5, au_6, au_7, au_10, au_12, au_25, au_26, au_45 = \
            action_units[i][0], action_units[i][1], action_units[i][2], action_units[i][3], \
            action_units[i][4], action_units[i][5], action_units[i][6], action_units[i][7], \
            action_units[i][8], action_units[i][9], action_units[i][10]
        status, vh_pic = au_delivery(action_unit_idx[i], au_1, au_2, au_4, au_5, au_6, au_7, au_10, au_12, au_25, au_26, au_45)
        if status != 200:
            return
        vh_pic_url = base_vh_host_url + vh_pic
        vh_pic_filedata = urllib.request.urlopen(vh_pic_url)
        datatowrite = vh_pic_filedata.read()
        with open(out_dir + '/' + str(i) + '.png', 'wb') as f:
            f.write(datatowrite)