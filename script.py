import uuid
import requests
import time
import os

def check_login_error(response_text: str) -> bool:
    return "login__body__hint" not in response_text

def check_login(response_text: str) -> bool:
    return "header-menu" in response_text

url = 'https://login.emaktab.uz/login'
logout_url = 'https://login.emaktab.uz/logout'
diary_url = 'https://emaktab.uz/marks'

def auto_post(user_login, user_pass, session):
    captcha = str(uuid.uuid4())
    data = {
        "exceededAttempts": "False",
        "ReturnUrl": "",
        "FingerprintId": "",
        "login": user_login,
        "password": user_pass,
        "Captcha.Input": captcha,
        "Captcha.Id": captcha
    }

    response = session.post(url, data=data)
    print(response.status_code)
    if response.status_code == 200:
        if not check_login_error(response.text):
            print(f"{user_login}: Неверный пароль!")
            return
        if check_login(response.text):
            print(f"{user_login}: Успешный вход!")
            diary_response = session.get(diary_url)
            if diary_response.status_code == 200:
                res = session.get(diary_url)
                with open(f"{user_login}.html", "w") as file:
                    file.write(res.text)
                print(f"{user_login}: Дневник загружен!")
                logout = session.post(logout_url)
                with open("user_logout.html", "w") as file:
                    file.write(logout.text)
                print(f"{user_login}: Выход")
        else:
            print(f"{user_login}: Вход не удался!")

logins = [
    {
        'login': "login",
        'password': "password"
    }
]

for person in logins:
    session = requests.Session()
    auto_post(person['login'], person['password'], session)
    print(f"Успех: {person['login']} | {person['password']}")
    try:
        file = rf"PATH\TO\YOUR\FILE\{person['login']}.html"
        os.remove(file)
        print("Успешно удален")
    except:
        print("Ошибка при удалении")
