import sys, os
import shutil
import csv

def check_complete_users(usr_name):   
    out_files_dir = "./static/img/testers/" + str(usr_name) + "/gnt/"
    for i in range(11):
        while not os.path.exists(out_files_dir + str(i) + '.png'):
            return False
    out_files_dir = "./static/img/testers/" + str(usr_name) + "/ran/"
    for i in range(11):
        while not os.path.exists(out_files_dir + str(i) + '.png'):
            return False
    return True

def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

testers_dir = "./static/img/testers/"
file_list = os.listdir(testers_dir)
acc_list = []
if file_list is not None:
    for f_name in file_list:
        if f_name == "test" or ".git" in f_name:
            continue
        res = check_complete_users(f_name)
        if res == True:
            print(f_name)
            acc_list.append(f_name)
            copyDirectory(testers_dir + f_name, "D:/Projs/FEMS_copy/FEMS/static/img/testers/" + f_name)

print("Success")