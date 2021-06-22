import pymysql.cursors
from contextlib import closing
from config import DB_CONFIG


def get_connection():
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection


def insert_data(data, table_name):
    data_keys = tuple(data.keys())
    data_values = tuple(data.values())
    fields = ','.join(data_keys)
    mask = ','.join(['%s'] * len(data_values))

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = f'INSERT INTO {table_name} ({fields}) VALUES ({mask})'

            cursor.execute(sql, data_values)
            connection.commit()
    print(f'{table_name}: +{cursor.rowcount}(last_row_id = {cursor.lastrowid})')
    return cursor.lastrowid


def insert_order_items(data_values, fields_list, table_name):
    fields = ','.join(fields_list)
    mask = ','.join(['%s'] * len(fields_list))

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = f'INSERT INTO {table_name} ({fields}) VALUES ({mask})'
            cursor.executemany(sql, data_values)
            connection.commit()
    print(f'{table_name}: +{cursor.rowcount}')
    return cursor.rowcount


def get_service_tariffs():
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM service_tariffs')
    return cursor.fetchall()


def get_tariff_by_lifetime(lifetime):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM service_tariffs WHERE lifetime = %s', lifetime)
    return cursor.fetchone()


def get_user(_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE tg_id = %s', _id)
    return cursor.fetchone()


def get_user_question_and_offers(tg_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT A.answer, Q.* FROM answers as A RIGHT JOIN question_and_offers as Q'
                           ' ON A.question_id = Q.id where Q.questioner_tg_id = %s', tg_id)
    return cursor.fetchall()


def get_email(email):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE email = %s', email)
    return cursor.fetchone()


def get_sent_payment_request_by_money_lifetime(lifetime, user_tg_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM payment_requests where lifetime = %s AND status = %s AND from_user_tg_id = %s'
            cursor.execute(sql, (lifetime, 'sent', user_tg_id))
    return cursor.fetchone()


def get_user_payment_requests_by_status(status, user_tg_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM payment_requests where status = %s AND from_user_tg_id = %s',
                           (status, user_tg_id))
    return cursor.fetchall()


def get_payment_request_by_id(request_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM payment_requests WHERE id = %s', request_id)
    return cursor.fetchone()


def get_user_invite_link(user_tg_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM invite_links WHERE user_tg_id = %s', user_tg_id)
    return cursor.fetchone()


def get_all_users():
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users')
    return cursor.fetchall()


def get_question_offers_by_status(status):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT qo.*, u.fullname, u.username FROM question_and_offers as qo '
                           'INNER JOIN users as u ON qo.questioner_tg_id=u.tg_id WHERE qo.status = %s', status)
    return cursor.fetchall()


def get_all_premium_users():
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE status = "premium"')
    return cursor.fetchall()


def get_question_offer_by_id(_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT QO.*, U.fullname, U.username, U.lang FROM question_and_offers as QO '
                           'INNER JOIN users as U ON QO.questioner_tg_id=U.tg_id WHERE QO.id = %s', _id)
    return cursor.fetchone()


def get_all_payments():
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT P.id, P.payment_status,P.payer_tg_id, PR.price, PR.lifetime FROM payments as P '
                           'INNER JOIN payment_requests as PR ON P.payment_request_id = PR.id')
    return cursor.fetchall()


def get_sent_payment_requests():
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = 'SELECT U.fullname, U.username, PR.id, PR.from_user_tg_id, PR.price, PR.lifetime, PR.status ' \
                  'FROM users as U INNER JOIN payment_requests as PR ON U.tg_id = PR.from_user_tg_id WHERE ' \
                  'PR.status = "sent"'
            cursor.execute(sql)
    return cursor.fetchall()


def get_freebook_by_id(book_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM freebooks WHERE id = %s and is_available = TRUE', book_id)
    return cursor.fetchone()


def get_all_freebooks():
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM freebooks WHERE is_available = TRUE')
    return cursor.fetchall()


def update_quest_offer_status(status, quest_offer_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE question_and_offers SET status = %s WHERE id = %s', (status, quest_offer_id))
            connection.commit()
    return 'updated' if connection.affected_rows() != 0 else 'not updated'


def update_freebook(status, book_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE freebooks SET is_available = %s WHERE id = %s', (status, book_id))
            connection.commit()
    return 'updated' if connection.affected_rows() != 0 else 'not updated'


def update_payment_request_status(status, request_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE payment_requests SET status = %s WHERE id = %s', (status, request_id))
            connection.commit()
    return 'updated' if connection.affected_rows() != 0 else 'not updated'


def delete_service_tariff(lifetime):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM service_tariffs WHERE lifetime = %s', lifetime)
            connection.commit()
    return 'deleted' if connection.affected_rows() != 0 else 'not deleted'


def update_tarif_price(price, lifetime):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE service_tariffs SET price = %s WHERE lifetime = %s', (price, lifetime))
            connection.commit()
    return 'updated' if connection.affected_rows() != 0 else 'not updated'


def update_tarif_lifetime(new_lifetime, lifetime):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE service_tariffs SET lifetime = %s WHERE lifetime = %s', (new_lifetime, lifetime))
            connection.commit()
    return 'updated' if connection.affected_rows() != 0 else 'not updated'


def update_user_fullname(fullname, user_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE users SET fullname = %s WHERE id = %s', (fullname, user_id))
            connection.commit()
    return 'updated' if connection.affected_rows() != 0 else 'not updated'


def update_user_lang(lang, _id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE users SET lang = %s WHERE id = %s OR tg_id = %s', (lang, _id, _id))
            connection.commit()
    return 'updated' if connection.affected_rows() != 0 else 'not updated'


def update_user_status(status, user_tg_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE users SET status = %s WHERE tg_id = %s', (status, user_tg_id))
            connection.commit()
    return 'updated' if connection.affected_rows() != 0 else 'not updated'


def update_user_status_and_timestamps(status, timestamp, user_tg_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE users SET status = %s, premium_expire_timestamp = %s WHERE tg_id = %s',
                           (status, timestamp, user_tg_id))
            connection.commit()
    return 'updated' if connection.affected_rows() != 0 else 'not updated'


def update_post_status(status, post_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE posts SET status = %s WHERE id = %s', (status, post_id))
            connection.commit()
    return 'updated' if connection.affected_rows() != 0 else 'not updated'
