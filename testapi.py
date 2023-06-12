import requests as r
import base64

root = 'http://localhost:8080'


# Проверка создания пользователя:
answer = r.post(root + '/create_user', json={'user_name': 'ALLLEX'})
print(answer.status_code)
print(answer.json())

# Проверка загрузки файла:
with open('sample-9s.wav', 'rb') as f:
     wave_data = f.read()

answer = r.post(root + '/add_audio',
                 json={'user_id': 1, 'token': '',
                       'file': base64.b64encode(wave_data).decode()})


print(answer.status_code)
print(answer.text)