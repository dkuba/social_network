"""
Скрипт создаёт 1М записей пользователей в БД.
"""
import datetime
import os
import random
import string
import uuid

from dotenv import load_dotenv

from faker import Faker
import psycopg2.extras

from utils.passwd import hash_password

load_dotenv()

DEFAULT_USER_PASSWORD = 'password'

fake = Faker()

connection = psycopg2.connect(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME')
)


cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

cmd = """
INSERT INTO users.users 
(id, username, password, email, first_name, last_name, date_of_birth, user_gender, city, interests) 
VALUES %s;
"""

cursor.execute("""SELECT id FROM geo.cities;""")
citi_id = cursor.fetchone()['id']

counter = 0
items = []

user_names = set()
while len(user_names) < 1000000:
    name = fake.user_name()

    while name in user_names:
        name += random.choice(string.ascii_letters)

    user_names.add(name)
    counter += 1

    if not counter % 1000:
        print(counter)

date = datetime.datetime.now()
counter = 0

for idx in range(1000000):
    user_name = user_names.pop()

    items.append((
                       str(uuid.uuid4()),
                       user_name,
                       hash_password(DEFAULT_USER_PASSWORD),
                       f'{user_name}@{user_name}.com',
                       user_name + random.choice(string.ascii_letters),
                       user_name + random.choice(string.ascii_letters),
                       date,
                       random.choice(('муж', 'жен')),
                       citi_id,
                       'some hobbies'
                   ))

    counter += 1

    if not counter % 1000:
        print(counter)

    if not counter % 10000:
        print('Execute query...')
        psycopg2.extras.execute_values(cursor, cmd, items)
        print('Execute query FINISHED')

        connection.commit()

        items = []
