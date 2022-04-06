#!/usr/bin/python
# Author: https://vk.com/id181265169
# https://github.com/fgRuslan/vk-spammer
import subprocess
import argparse
from socket import timeout
import vk_api
import urllib.request
import urllib.error
import urllib.parse
import json
import random
import time
from requests.utils import requote_uri
from python3_anticaptcha import ImageToTextTask, errors
import requests
import gspread
import threading
import sys
import os
import platform
import codecs
import wget
import random
import socks
import re


HOME_PATH = os.path.expanduser("~")
SPAMMER_PATH = os.path.join(HOME_PATH + "/" + ".vk-spammer/")

SPAMMING_ONLINE_USERS = False
SPAMMING_FRIENDS = False
SPAMMING_Groups = False
USE_TOKEN = False
SPAMMING_Groups_video = False

# Данные из Kate mobile
API_ID = "2685278"
tmp = "hHbJug59sKJie78wjrH8"

API_VERSION = 5.82

ANTICAPTCHA_KEY = ''

username = None
password = None

PO_version = 14
i_G = 0
ii = 0


def ensure_file_exists(path: str):
    if not os.path.exists(path):

        if path == "Count.txt":
            codecs.open(path, 'a').close()
            with open(path, 'w') as f:
                f.write("1")
                f.close()
        elif path == "token.json":
            ()
            wget.download('https://github.com/wolf1407/vk/raw/main/token.json')
        else:
            codecs.open(path, 'a').close()


ensure_file_exists("Accounts.txt")
ensure_file_exists("Groups.txt")
ensure_file_exists("Count.txt")
ensure_file_exists("token.json")


DELAY = 4  # Количество секунд задержки

auth_data = {}

# Проверяет наличие аккаунтов в файле


code_country = int(requests.get(
    'https://raw.githubusercontent.com/wolf1407/vk/main/version.py').text)


if code_country > PO_version:

    if not os.path.exists("update.bat"):
        wget.download(
            'https://raw.githubusercontent.com/wolf1407/vk/main/update.bat')
    # os.remove('vk.exe')
    input("Потрібно оновлення ПО, закрийте програму і запустіть файл 'update.bat'")
    sys.exit(1)


def check_accounts_count() -> bool:
    with open('Accounts.txt', 'r') as f:
        lines = f.readlines()
        return len(lines) > 0

# Проверяет наличие аккаунтов в файле


def check_groups_count() -> bool:
    with open('Groups.txt', 'r') as f:
        lines = f.readlines()
        return len(lines) > 0


def del_ac(ii):
    with open('Accounts.txt', 'r') as f:
        lines = f.readlines()
    with open('Accounts.txt', 'w') as f:
        f.writelines(lines[ii:])


def del_gr(i_G):
    with open('Groups.txt', 'r') as f:
        lines = f.readlines()
    with open('Groups.txt', 'w') as f:
        f.writelines(lines[i_G:])


def extract_group_id_or_name(group_link: str):
    """
    user_link: may be vk url or groupname
    method will extract id from text or groupname

    >>> extract_group_id_or_name("https://vk.com/club66")
    66
    >>> extract_group_id_or_name("https://vk.com/raby")
    'raby'
    """
    if isinstance(group_link, int):
        return group_link
    if not group_link.startswith('http'):
        try:
            return int(group_link)
        except ValueError as e:
            return group_link
    user_id_or_username = group_link.split('/')[-1]
    if user_id_or_username.startswith('club'):
        try:
            user_id_str = user_id_or_username[4:]
            return - int(user_id_str)
        except ValueError:
            logger.debug('It is probably a username starts with "club"')
            return user_id_str
    if user_id_or_username.startswith('public'):
        try:
            user_id_str = user_id_or_username[6:]
            return - int(user_id_str)
        except ValueError:
            logger.debug('It is probably a username starts with "public"')
            return user_id_str
    return user_id_or_username


# -------------------------------------------


def sendgr():

    user = None
    while user == None:
        try:
            user = vk.users.get(fields='sex', timeout=5)[0]
        except vk_api.exceptions.ApiError as e:
            print(e)
            user = 0
        except:
            print("Помилка звязку[3], спробуємо ще ...")
            time.sleep(3)

    user_sex = (user.get('sex'))

    gc = gspread.service_account(filename='token.json')
    sh = gc.open("ss")
    if user_sex == 1:
        worksheet = sh.worksheet("W_Coment")  # жінка > коменти
    else:
        worksheet = sh.worksheet("M_Coment")  # чоловік > коменти

    group_text1 = worksheet.col_values(1)
    group_text2 = worksheet.col_values(2)
    group_text3 = worksheet.col_values(3)
    group_text4 = worksheet.col_values(4)
    group_text5 = worksheet.col_values(5)

    # group_text.pop(0)

    acc_file = open("Groups.txt", "r", encoding='utf-8')
    lista = []

    for s in acc_file:
        s = s.rstrip()

        lista = lista + [s]
    global i_G
    i_G = 0
    i = 0

    while(True):
        for acca in lista:
            try:
                i_G = i_G+1

                acc = acca.split('|', 1)[0]
                tema = acca.split('|', 1)[1].split(";")

                tema3 = random.choices(tema, k=1)
                tema2 = tema3[0]
                group_text = None
                if tema2 == "1":
                    group_text = group_text1

                elif tema2 == "2":
                    group_text = group_text2

                elif tema2 == "3":
                    group_text = group_text3
                elif tema2 == "4":
                    group_text = group_text4
                elif tema2 == "5":
                    group_text = group_text5

                group_text.pop(0)

                print("Опрацювуємо групу "+acc+"\n")

                grid = extract_group_id_or_name(acc)

                if type(grid) == int:
                    acc = str(grid * -1)

                else:

                    grid2 = None
                    while grid2 == None:
                        try:
                            grid2 = vk.groups.getById(group_id=grid ,timeout=5)

                        except vk_api.exceptions.ApiError as e:
                            print(e)
                            grid2 = 1
                        except:
                            print("Помилка звязку[4], спробуємо ще ...")
                            time.sleep(3)

                    acc = str(grid2[0]['id'])

                man_id = "-"+acc  # id группа, с которой будем брать посты и комментарии
                # получаем последний пост со стены

                postidlist = None
                while postidlist == None:
                    try:
                        postidlist = vk.wall.get(
                            owner_id=man_id, count=6, sort='desc', timeout=5 ,offset=0)
                    except vk_api.exceptions.ApiError as e:
                        print(e)
                        postidlist = 1
                    except:
                        print("Помилка звязку, спробуємо ще ...")
                        time.sleep(3)
                listt_all = postidlist['items']
                listt = random.choices(listt_all, k=1)

                for post in listt:
                    messs = (random.choice(group_text))
                    mes = re.sub(
                        r"{(.+?)}", lambda x: random.choice(x.group(1).split("|")), messs)
                    a = str(post['id'])
                    try:
                        vk.wall.createComment(
                            owner_id=man_id, timeout=5, post_id=a, message=mes)
                        i = i+1
                        st_OK = i * "+"
                        st_NO = (20-i)*"_"

                        print("   Пост ✓  https://vk.com/public" +
                              acc + "?w=wall"+man_id + "_"+a + "\n   ["+st_OK+st_NO+f"] {i}/20\n")

                        pause = random.randrange(5, 15)
                        time.sleep(pause)
                    except vk_api.exceptions.ApiError as e:
                        if e.code == 5:
                            input("Аккаунт заблоковано, візьміть інший ")
                            break
                        print("Помилка відправлення!", e)
                        

                    except:
                        print("Помилка звязку[5], спробуємо ще ...")
                        time.sleep(3)

                if (i > 19):
                    break
            except:
                ()

        print("Всі групи оброблені")

        return


class MainThread(threading.Thread):
    def run(self):

        #print("-" * 4)
        #print("Задержка: ", args.delay)
        #print("-" * 4)
        print("Нажмите Ctrl+C чтобы остановить")

        DELAY = args.delay

        # Считываем текущее кол-во обработанных данных
        procResults = {
            "acc": 0,
            "group": 0
        }

        try:
            if(os.path.exists("Results.txt")):
                with open('Results.txt', 'r') as f:
                    procResults = json.load(f)
        except:
            ()
        # --------------------------------------------

        if SPAMMING_FRIENDS:
            user = vk.users.get(fields='sex')[0]
            user_sex = (user.get('sex'))
            gc = gspread.service_account(filename='token.json')
            sh = gc.open("ss")
            if user_sex == 1:
                worksheet = sh.worksheet("W_M")  # жінка > чоловіки
                worksheet2 = sh.worksheet("W_W")  # жінка > жінка
            else:
                worksheet = sh.worksheet("M_M")  # чоловік > чоловіки
                worksheet2 = sh.worksheet("M_W")  # чоловіки > жінка

            acc_file = open("Accounts.txt", "r", encoding='utf-8')
            lista = []

            for s in acc_file:
                s = s.rstrip()
                lista = lista + [s]

            with open('Count.txt', 'r') as f:
                lines = f.read()

                aaa = int(lines)

            # запишем файл построчно пропустив первую строку
            with open('Count.txt', 'w') as f:
                if aaa > 3:
                    aaa = 1
                else:
                    aaa = aaa+1
                f.write(str(aaa))
                f.close()

            count_sms = aaa
            text_m = worksheet.col_values(count_sms)
            text_m.pop(0)
            text_w = worksheet2.col_values(count_sms)
            text_w.pop(0)
            global ii
            ii = 0
            i = 0

            while(True):
                for acc in lista:

                    ii = ii+1

                    try:

                        # print(acc+"\n")
                        acc = acc.replace("https://vk.com/", "")

                    except:
                        print("Список аккаунтiв закiнчився, візьміть нову базу")
                        # sys.exit(1)
                        break

                    contact_info = None
                    while contact_info == None:
                        try:
                            contact_info = vk.users.get(
                                user_ids=acc, timeout=20, fields='sex')[0]
                        except vk_api.exceptions.ApiError as e:
                            print(e)
                            if e.code == 5:
                                return False
                        except:
                            print("Помилка звязку1, спробуємо ще ...")
                            time.sleep(3)

                    contact_sex = contact_info['sex']

                    if contact_sex == 1:
                        text = random.choice(text_w)
                    elif contact_sex == 2:
                        text = random.choice(text_m)
                    else:
                        text = random.choice(text_m)


#                         ch_n= random.randrange(1,10)
#                         if ch_n == 1:
#                         #text = random.choice(text_f)
#                             text2 = text.replace("а","a")
#                             text = text2.replace("о","o")
#                         elif ch_n == 2:
#                             text2 = text.replace("а","a")
#                             text = text2.replace("р","p")
#                         elif ch_n == 3:
#                             text2 = text.replace("р","p")
#                             text = text2.replace("о","o")
#                         elif ch_n == 4:
#                             text2 = text.replace("а","a")
#                             text = text2.replace("с","c")
#                         elif ch_n == 5:
#                             text2 = text.replace("с","c")
#                             text = text2.replace("о","o")
#                         elif ch_n == 6:
#                             text2 = text.replace("с","c")
#                             text = text2.replace("а","a")
#                         elif ch_n == 7:
#                             text2 = text.replace("у","y")
#                             text = text2.replace("о","o")
#                         elif ch_n == 8:
#                             text2 = text.replace("а","a")
#                             text = text2.replace("у","y")
#                         elif ch_n ==9:
#                             text2 = text.replace("у","y")
#                             text = text2.replace("с","c")
#                         elif ch_n == 10:
#                             text2 = text.replace("с","c")
#                             text = text2.replace("р","p")

                    text2 = re.sub(
                        r"{(.+?)}", lambda x: random.choice(x.group(1).split("|")), text)

                    r = None
                    while r == None:
                        try:
                            r = vk.messages.send(
                                domain=acc, timeout=20, message=text2, v=API_VERSION, random_id=random.randint(0, 10000))

                            i = i+1
                            st_OK = i * "+"
                            st_NO = (20-i)*"_"

                            print("Відправили користувачу", acc,
                                  "\n["+st_OK+st_NO+f"] {i}/20\n")

                            pause = random.randrange(5, 15)
                            time.sleep(pause)
                        except vk_api.exceptions.ApiError as e:

                            if e.code == 5:
                                input("Аккаунт заблоковано, візьміть інший ")
                                break
                            r = 1
                            print("Не вдалось відправити користувачу",
                                  acc, f"\n ({e})\n")
                        except:
                            print("Помилка звязку2, спробуємо ще ...")
                            time.sleep(3)

                    procResults["acc"] = procResults["acc"] + 1

                    if (i > 19):
                        break

                #print("Завдання 1 завершено")

                # Запишем результаты обработки
                with open('Results.txt', 'w') as f:
                    s = json.dump(procResults, f)

                setting = input(
                    "Завдання 1 завершено, введіть 2 натисніть Enter для переходу до розсилки по группам: ")

                if setting == "2":

                    sendgr()
                    setting = input(
                        "Всі завдання виконалили , візьміть нові бази посилань і груп і переходьте до роботи з іншим акаунтом")
                    return False

            return False

        elif SPAMMING_Groups:

            sendgr()
            #input("Завдання завершено, натисніть Enter для виходу")
            return False

        else:
            while(True):
                try:
                    msg = random.choice(messages)

                    print(victim)
                    r = vk.messages.send(
                        peer_id=victim, message=msg, timeout=5, v=API_VERSION, random_id=random.randint(0, 10000))
                    print("Sent ", msg)
                    time.sleep(DELAY)
                except vk_api.exceptions.ApiError as e:
                    print("ОШИБКА!")
                    print(e)
                except Exception as e:
                    print(e)

        remove_auth_data()

        input("Завдання завершено, натисніть Enter для виходу")


def main():
    try:
        thread = MainThread()
        thread.daemon = True
        thread.start()

        while thread.is_alive():
            thread.join(1)
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")

        input("Вихід")
        # sys.exit(1)


# -------------------------------------------
# Парсер аргументов
parser = argparse.ArgumentParser(description='Spam settings:')
parser.add_argument(
    '-d',
    '--delay',
    type=int,
    default=4,
    help='Delay (default: 4)'
)
parser.add_argument('-e', '--editmessages', action='store_true',
                    help='Use this argument to edit the message list')
parser.add_argument('-r', '--removedata', action='store_true',
                    help='Use this argument to delete auth data (login, password)')
parser.add_argument('-l', '--login', action='store', type=str,
                    help='Login to use for auth (you must also provide -p).\nOr you may provide an auth pair in format \'login:password\' (-p is not required)')
parser.add_argument('-p', '--password', action='store', type=str,
                    help='Password to use for auth (you must also provide -l).')
parser.add_argument('-t', '--target', action='store', type=int,
                    help='1 - direct messages, 2 - group posts')
args = parser.parse_args()
# -------------------------------------------

if(args.editmessages):
    if platform.system() == "Windows":
        os.system("notepad.exe " + SPAMMER_PATH + "messages.txt")
    if platform.system() == "Linux":
        os.system("nano " + SPAMMER_PATH + "messages.txt")
    print("Перезапустите спамер, чтобы обновить список сообщений")
    exit(0)

if(args.removedata):
    remove_auth_data()


# Пытаемся загрузить данные авторизации из файла
# Если не удалось, просим их ввести
load_result = False
#load_result = load_auth_data()

# Если креды переданы через cli, то используем их, иначе запрашиваем интерактивно
if(args.login):
    loginData = str(args.login)
    pair = loginData.split(':', 1)

    if(len(pair) == 1 and args.password):
        username = loginData

        if len(username) == 85:
            USE_TOKEN = True
            password = ''
        else:
            password = args.password
    elif(len(pair) == 2):
        username = pair[0]
        password = pair[1]
    else:
        print("Помилка. Невірний формат логіну/паролю.")
        exit(1)

    print("Данні авторизації отримані із командної строки\r\nЛогін: " +
          username + "\r\nПароль: " + password)

elif(load_result == False):
    username_ = input("Введіть дані від фейкового акканут (логін:пароль): ")
    auth_data = username_.split(":")
    username = auth_data[0]
    try:
        password = auth_data[1]
    except:
        password = input("Пароль: ")


#     if len(username) == 85:
#         USE_TOKEN = True
#     if not USE_TOKEN:
#         password = input("Пароль: ")
#     else:
#         password = ''
    #save_auth_data = input("Сохранить эти данные авторизации? (Y/n): ")

    save_auth_data = "n"
    if(save_auth_data == "Y" or save_auth_data == "y" or save_auth_data == ""):
        auth_data['username'] = username
        auth_data['password'] = password
        do_save_auth_data()
else:
    print("Данные авторизации получены из настроек")
    username = auth_data['username']
    password = auth_data['password']
    if len(username) == 85:
        USE_TOKEN = True


def captcha_handler(captcha):
    if ANTICAPTCHA_KEY == '':
        solution = input("Решите капчу ({0}): ".format(captcha.get_url()))
        return captcha.try_again(solution)
    key = ImageToTextTask.ImageToTextTask(
        anticaptcha_key=ANTICAPTCHA_KEY, save_format='const').captcha_handler(captcha_link=captcha.get_url())

    #s = captcha.try_again(key['solution']['text'])

    s = ""
    if('solution' in key):
        s = (key['solution']['text'])
        print("Каптча: "+s)
    else:
        print(
            "Помилка обробки каптчі: [" + key['errorCode'] + "] " + key['errorDescription'])

    return captcha.try_again(s)


def auth_handler():
    key = input("Введите код подтверждения: ")
    remember_device = True
    return key, remember_device


try:
    code_country = requests.get(
        'https://ipwhois.app/json/').json()["country_code"]
    print("Країна підключення:", code_country)
except:
    input("Будь-ласка, перевірте з'єднання VPN, не можливо підключитися")

if code_country == "UA":
    input("Будь-ласка, перевірте налаштування VPN, у вас показує країну UA")
    sys.exit(1)


# -------------------------------------------
# Логинимся и получаем токен

#session = requests.Session()
# session.proxies = {'https': 'socks5://buTUf2:UB7PeXTUjFyA@82.202.166.28:11467'}  # Замените на свой

#vk_session = VkApi()


#vk_session = vk_api.VkApi(session=session)


anticaptcha_api_key = '6b87e01434eed54edc689c47af0cd5f7'
#anticaptcha_api_key = input(     "API ключ от anti-captcha.com (оставьте пустым если он не нужен): ")
if anticaptcha_api_key == '':
    if USE_TOKEN:
        vk_session = vk_api.VkApi(
            token=username, auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)
    else:
        vk_session = vk_api.VkApi(
            username, password, auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)
else:
    ANTICAPTCHA_KEY = anticaptcha_api_key
    if USE_TOKEN:
        vk_session = vk_api.VkApi(token=username, captcha_handler=captcha_handler,
                                  auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)
    else:
        vk_session = vk_api.VkApi(username, password, captcha_handler=captcha_handler,
                                  auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)


ip = requests.get(
    'https://raw.githubusercontent.com/wolf1407/vk/main/proxy02.json').json()
ip_i = ip["proxy"]
ip2 = random.choice(ip_i)
ip = 'socks5://'+ip2


try:
    vk_session.auth(token_only=True)

    if ip2 != "0":

        vk_session.http.proxies = {'https': ip, 'http': ip}


except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_session.get_api()


try:
    user = vk.users.get(fields='sex' , timeout=20)[0]
    print("Авторизувалися в :", user.get('first_name'),
          "", user.get('last_name') + "\n")
except vk_api.exceptions.ApiError as e:
    print(e)
    if e.code == 5:
        input("Акаунт заблокований")
        sys.exit(1)


except:
    print("Помилка авторизації , перевірте дані, або візьміть інший аккаунт")
    input("Натисніть Ентер для виходу")
    # sys.exit(1)


# Если цель не задана через cli, то запрашиваем интерактивно
# victim="1"
# if(args.target):
#     victim = args.target
# else:
#     victim="1"
victim = input(
    "Введіть 1 для розсилання по особистим повідомленням, 2 для розсилання по групам: ")
#

if victim == "1":
    if(check_accounts_count() == False):
        print("Будь ласка замініть файл Accounts.txt на новий")
        input("Натисніть Enter для виходу")
        exit(1)
    if(check_groups_count() == False):
        print("Будь ласка замініть файл Groups.txt на новий")
        input("Натисніть Enter для виходу")
        exit(1)
    SPAMMING_FRIENDS = True
elif victim == "2":
    if(check_groups_count() == False):
        print("Будь ласка замініть файл Groups.txt на новий")
        input("Натисніть Enter для виходу")
        exit(1)
    SPAMMING_Groups = True
elif victim == "3":
    SPAMMING_Groups_video = True

# -------------------------------------------
# Запускатор главного потока

try:
    main()
except ValueError as e:
    input("Стоп", e)

del_ac(ii)
del_gr(i_G)

input("Завершити роботу")
