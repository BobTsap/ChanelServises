import os
from usd_today import usd_today
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


sheet_id = "1zF1XMM-RFPFwiIayKnUgYBhYJrFLVpQMMwCSYk5wZKs"

# Доступ к Google таблице через сервисный аккаунт
def get_service_sacc():
    creds_json = os.path.dirname(__file__) + "/creds/sacc1.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)

# Расчет данных для новой колонки в таблицу
def usd_to_rub(usd_today, values):
    for i in values:
        i.append(str(int(i[2])*usd_today))

# Получение данных из Google таблицы
def get_values():
    service = get_service_sacc()
    sheet = service.spreadsheets()

    resp = sheet.values().get(spreadsheetId=sheet_id, range="list1!A2:D").execute()
    values = resp.get('values', [])

    # Добавляем колонку с данными стоимости в рублях
    usd_to_rub(usd_today, values)
    print(values)

    if not values:
        print('No data found')
    
    return values

get_values()