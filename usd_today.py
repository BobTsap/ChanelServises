import requests

# запрос данных о курсе рубля к доллару через сервер ЦБ
data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
usd_today = float(data['Valute']['USD']['Value'])

print(usd_today)