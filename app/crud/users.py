import uuid

from database import get_db_connection, get_db_connection_slave
from app.models import CreateUser, User
import psycopg2.extras

from utils import hash_password

psycopg2.extras.register_uuid()


# TODO: вынести CRUD пользователя в отдельный сервис, унаследованный от абстрактного класса
#  и, соответсвенно, во вьюхах сделать через Depends
async def create_user(user: CreateUser) -> uuid.UUID:
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute(
        """SELECT id FROM geo.cities WHERE name = %s""",
        (user.city,)
    )
    city_id = cursor.fetchone()['id']

    try:
        cursor.execute(
            """INSERT INTO auth.users (
            id, 
            username, 
            password, 
            email, 
            first_name, 
            last_name, 
            date_of_birth,
            user_gender, 
            city
            ) 
            VALUES (
            %s, 
            %s, 
            %s,
            %s, 
            %s, 
            %s,
            %s,
            %s,
            %s
            ) 
            RETURNING id;""",
            (uuid.uuid4(),
             user.username,
             hash_password(user.password),
             user.email,
             user.first_name,
             user.last_name,
             user.date_of_birth,
             user.user_gender,
             city_id)
        )
        user_id = cursor.fetchone()['id']
        connection.commit()
        return user_id
    finally:
        cursor.close()


async def search_user(username: str,
                      first_name: str,
                      last_name: str,
                      limit: int,
                      offset: int):

    connection = get_db_connection_slave()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cmd = """
        SELECT 

        usr.id, 
        username, 
        email, 
        first_name, 
        last_name, 
        date_of_birth,
        user_gender, 
        cities.name as city, 
        interests

        FROM auth.users as usr

        INNER JOIN geo.cities as cities ON usr.city = cities.id 
        
        WHERE true
        """

    if username:
        cmd += f""" AND username LIKE '{username}%'"""
    if first_name:
        cmd += f""" AND first_name LIKE '{first_name}%'"""
    if last_name:
        cmd += f""" AND last_name LIKE '{last_name}%'"""

    if limit and offset >= 0:
        cmd += f""" LIMIT {limit} OFFSET {offset}"""

    cmd += """ ORDER BY username"""

    try:
        cursor.execute(cmd)
        result = []

        for user_data in cursor.fetchall():
            result.append(User(**user_data))

        return result

    finally:
        cursor.close()


async def get_user_by_id(user_id: uuid) -> User | None:
    connection = get_db_connection_slave()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute("""
        SELECT 
        
        usr.id, 
        username, 
        email, 
        first_name, 
        last_name, 
        date_of_birth,
        user_gender, 
        cities.name as city, 
        interests
        
        FROM auth.users as usr
        
        INNER JOIN geo.cities as cities ON usr.city = cities.id 
        
        WHERE usr.id = %s;""",
                       (user_id,))

        user_data = cursor.fetchone()

        if not user_data:
            return

        return User(**user_data)

    finally:
        cursor.close()


async def verify_user(username: str, password: str):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute("""
        SELECT 
        
        usr.id, 
        username, 
        email, 
        first_name, 
        last_name, 
        date_of_birth,
        user_gender, 
        cities.name as city, 
        interests
        
        FROM auth.users as usr
        
        INNER JOIN geo.cities as cities ON usr.city = cities.id 
        
        WHERE username = %s AND password = %s;""", (username, hash_password(password)))
        user = cursor.fetchone()
        return user
    finally:
        cursor.close()
