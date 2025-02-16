import requests
from time import sleep

logins = ["login1", "login2", "login3"]
password = "1234567a"

url = "https://login.emaktab.uz/login"
logout_url = "https://login.emaktab.uz/logout"
diary_url = "https://emaktab.uz/marks"

session = requests.Session()

for person in logins:
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    print(f"Вход в {person}")

    data = {
        'login': person,
        'password': password
    }

    response = session.post(url, data=data, headers=headers)

    if "captcha" in response.text.lower() or "Введите символы с картинки" in response.text:
        print(f"Обнаружена капча для {person}. Вход остановлен.")
        continue

    if response.status_code == 200 and "logout" in response.text:
        print(f"Успешный вход в {person}.")
    else:
        print(f"Вход провален для {person}. Код страницы: {response.status_code}")
        continue

    response = session.get(diary_url, headers=headers)
    print(f"Статус открытия Дневника: {response.status_code}")
    sleep(5)

    response = session.get(logout_url, headers=headers)
    print(f"Статус выхода из {person}: {response.status_code}\n\n")