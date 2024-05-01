import uuid

from database import get_db_connection, put_db_connection
from app.models import CreateUser, User
import psycopg2.extras

from utils import hash_password

psycopg2.extras.register_uuid()


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
             city_id)
        )
        user_id = cursor.fetchone()['id']
        connection.commit()
        return user_id
    finally:
        cursor.close()
        put_db_connection(connection)


async def get_user_by_id(user_id: uuid) -> User:
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
        cities.name as city, 
        interests
        
        FROM auth.users as usr
        
        INNER JOIN geo.cities as cities ON usr.city = cities.id 
        
        WHERE usr.id = %s;""",
                       (user_id,))

        user_data = cursor.fetchone()

        return User(**user_data)

    finally:
        cursor.close()
        put_db_connection(connection)


async def verify_user(username: str, password: str):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    print(f'hash_password(password): {hash_password(password)}')
    try:
        cursor.execute("""
        SELECT 
        
        usr.id, 
        username, 
        email, 
        first_name, 
        last_name, 
        date_of_birth, 
        cities.name as city, 
        interests
        
        FROM auth.users as usr
        
        INNER JOIN geo.cities as cities ON usr.city = cities.id 
        
        WHERE username = %s AND password = %s;""", (username, hash_password(password)))
        user = cursor.fetchone()
        return user
    finally:
        cursor.close()
        put_db_connection(connection)
