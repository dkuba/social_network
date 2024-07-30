import uuid

import psycopg2.extras

from database import get_db_connection_slave, get_db_connection
from models.posts import Post, PostRead


async def create_post_in_db(user_id: uuid,
                      text: str):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute(
            """INSERT INTO users.posts (
            id, 
            user_id,
            post_text
            ) 
            VALUES (
            %s, 
            %s, 
            %s
            
            ) 
            RETURNING id;""",
            (uuid.uuid4(),
             user_id,
             text)
        )
        post_id = cursor.fetchone()['id']
        connection.commit()
        return post_id
    finally:
        cursor.close()


async def get_feeds_posts(user_id: uuid) -> list[PostRead] | None:
    """Возвращает посты друзей пользователя."""

    connection = get_db_connection_slave()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute("""
        SELECT 
        
        user_id,
        post_text
        
        FROM users.posts as posts
        
        INNER JOIN users.user_friends as friends ON friends.user_two_id = posts.user_id 
         
        WHERE friends.user_one_id = %s 
        
        ORDER BY date_inserted DESC 
        
        LIMIT 1000;
        """, (user_id,))

        posts = cursor.fetchall()

        if not posts:
            return

        return [PostRead(**post) for post in posts]

    finally:
        cursor.close()
