import requests
from time import sleep as sl
from user_agents import user_agent_list
from random import randint

loggins = [
    {
        'login': "login1",
        'password': "1234567a"
    },
    {
        'login': 'login2',
        'password': '1234567a'
    },
    {
        'login': 'login3',
        'password': '1234567a'
    }
]

url = 'https://login.emaktab.uz/login'
logout_url = 'https://login.emaktab.uz/logout'
diary_url = 'https://emaktab.uz/marks'

session = requests.Session()

for person in loggins:
    # Log in
    head = {'User-Agent': user_agent_list[randint(0, 11)]}
    sl(5)
    print(head)
    response = session.post(url, data=person, headers=head)
    print(f'Статус входа для {person["login"]}:', response.status_code)
    sl(5)
    # Open "Дневник"
    response = session.get(diary_url, headers=head)
    print(f'Открыть статус "Дневник" для {person["login"]}:', response.status_code)
    sl(5)
    # Log out
    response = session.get(logout_url, headers=head)
    print(f'Статус выхода для {person["login"]}:', response.status_code)
