import psycopg2
from get_table import get_values
import time

# Создание таблицы в БД PostgeSQL
def set_table():
    try:
        # Сonnect к БД
        # Т.к. для примера создана БД локально, то нужно прописать свои данные
        connection = psycopg2.connect(
            host="127.0.0.1",
            user="postgres",
            password="5544753",
            database="ChanelServises"
        )
        connection.autocommit = True

        # Создание таблицы
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS test_table(
                    id text NOT NULL,
                    order_numder text NOT NULL,
                    value_usd text NOT NULL,
                    delivery_date text NOT NULL,
                    value_rub text NOT NULL);"""
            )
        # Сохраняем копию данных для остслеживания изменений
        table1 = get_values()

        # Подготовка данных для импорта в таблицу [(), ()...]
        insert_data = []
        for row in table1:
            row = tuple(row)
            insert_data.append(row)
        print(insert_data)

        # Импорт данных в таблицу одним запросом
        with connection.cursor() as cursor:
            query = """INSERT INTO test_table VALUES (%s, %s, %s, %s, %s)"""
            cursor.executemany(query, insert_data)


        # Проверка изменений в Google таблице (1 раз в минуту)
        while True:
            table2 = get_values() # Берем текущее состояние Google таблицы
            # в случае изменения данных БД перезаписывается
            if table1 != table2:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """TRUNCATE TABLE test_table"""
                    )
                set_table()
            else:
                time.sleep(60)

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgeSQL connection closed")


if __name__ == "__main__":
    set_table()