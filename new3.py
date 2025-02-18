import uuid
import requests
import time


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
        "Captcha.Id": captcha  # ID sifatida ham captcha ishlatamiz
    }

    response = session.post(url, data=data)

    if response.status_code == 200:
        # write response.text to file
        if not check_login_error(response.text):
            print(f"{user_login}: Login yoki parol xato!")
            return
        if check_login(response.text):
            print(f"{user_login}: Login muvaffaqiyatli bajarildi!")
            diary_response = session.get(diary_url)
            if diary_response.status_code == 200:
                res = session.get(diary_url)
                with open(f"{user_login}.html", "w") as file:
                    file.write(res.text)
                print(f"{user_login}: Dnevnik yuklandi!")
                logout = session.post(logout_url)
                with open("user_logout.html", "w") as file:
                    file.write(logout.text)
                time.sleep(5)
        else:
            print(f"{user_login}: Login amalga oshmadi!")


logins = [
    {
        'login': "login",
        'password': "password"
    }
]

for person in logins:
    session = requests.Session()
    auto_post(person['login'], person['password'], session)
    print(f"Sinov tugadi: {person['login']} | {person['password']}")
